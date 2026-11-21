---
name: daily-report
description: 根据当天 Git 提交记录自动生成工作日报。当用户提到"生成日报"、"日报"、"工作日报"、"git日报"、"提交日报"、"每日汇报"等关键词时使用此技能。支持指定日期、多仓库汇总、节假日判断、历史日报查询，自动追加到工作日志文件；已配置网页日报系统时自动登录、填写表单并保存草稿（提交审核仍需用户明确要求）。跨平台（Windows/macOS/Linux）、跨 agent 工具通用。
allowed-tools: Read Write Bash(uv:*) Bash(python:*) Bash(python3:*) Bash(git:*)
---

# 工作日报生成技能

根据 Git 提交记录自动生成工作日报：并行采集多仓库提交，AI 汇总润色，判断加班，安全追加到日志文件。

## 核心原则

- **快速路径**：配置已存在时直接执行「标准流程」，不先跑 `--status`；仅报「配置文件不存在」或首次使用时进入配置流程。
- **编码安全**：日报正文一律写入 UTF-8 临时文件后用 `--summary-file` 传入（或经 stdin 管道），**严禁把多行中文正文内联在命令行参数里**（规避 Windows GBK 乱码）。
- **解释器**：优先 `uv run python`；无 uv 时回退 `python3` / `python`（除 `publish_report.py` 需 playwright 外均为纯标准库）。
- **防重与覆盖**：脚本自带同日去重；覆盖需用户明确同意后追加 `--force`，禁止静默覆盖。
- **网页自动填报**：`web.enabled=true` 时写入后直接执行 `--fill` 保存草稿；`web.project_name` 缺失时退化为登录+打开表单+复制正文；`--submit --yes` 仅在用户明确要求且核对项目/日期/正文/审核人后执行。
- **敏感信息**：账号密码仅从配置文件或环境变量读取，不打印、不写入对话和示例。

## 标准流程（三步）

### 第 1 步：获取结构化原始数据

```bash
uv run python scripts/generate_report.py --raw
```

指定日期加 `--date YYYY-MM-DD`；范围用 `--since` / `--until`；指定分支用 `--branch`。检查输出 JSON：
- `has_commits=false` → 正文使用 `default_content`
- `is_overtime=true` → 日期行后加 `（加班）`
- 退出码 1 且提示「日报已存在」→ 询问用户确认后再带 `--force` 覆盖写入

### 第 2 步：AI 汇总并写入

1. 按下方「AI 汇总规则」整理 commits 为日报正文，写入 UTF-8 临时文件 `<系统临时目录>/daily-report-YYYY-MM-DD.txt`
2. 执行写入（不重复跑 git 与节假日 API）：
   ```bash
   uv run python scripts/generate_report.py --summary-file <临时文件>
   ```
3. 删除临时文件，向用户展示最终日报内容与输出文件路径。

### 第 3 步：网页日报自动填报（按 `--raw` 输出判断，无需询问）

| 条件 | 动作 |
| :--- | :--- |
| `web_enabled=true` 且 `web_project_configured=true` 且日期为今天 | 直接执行 `uv run --with playwright python scripts/publish_report.py --fill` 保存草稿并汇报 |
| `web_enabled=true` 但 `web_project_configured=false` | 执行 `publish_report.py`（登录+打开表单+复制正文），仅提醒一次补配 `web.project_name` |
| `web_enabled=false` | 不执行网页步骤；可在汇报中提一句支持启用网页自动填报（仅提醒一次） |
| 日报日期不是今天 | 不自动执行网页步骤；用户明确要求时再加 `--date` 执行 |

> 退出码 2（登录失败）或 3（填写中断）时禁止重试，向用户说明原因并保留打开的浏览器以便手动完成。

## AI 汇总规则与输出格式

1. **语义归类**：按项目与功能模块自然分组，合并同功能多次提交；BUG 编号自然融入对应功能描述。
2. **功能前置 & 弱 AI 化**：句首带功能/模块名，语气平实简短，不写「完成了……开发工作」等空泛套话。
3. **输出格式**（日期行顶格，与首行不留空行；多项目用中文序号分节，项目间空一行；单项目直接编号）：

```text
2026年05月28日
一、项目A
1. 列表页：查询改为分页加载，减少首屏等待
2. 数据编辑：修复回显异常（#1024），调整表单加载逻辑

二、项目B
1. 报表导出：新增批量导出，支持 Excel 格式
```

加班日：`2026年05月30日 （加班）`；无提交：`日期行` + `1. 日常工作`。

## 查询历史日报

禁止 `cat` 整份日志文件，使用查询脚本：

```bash
uv run python scripts/query_report.py --date 2026-05-28
uv run python scripts/query_report.py --keyword 关键词 --month 2026-05
uv run python scripts/query_report.py --date 2026-01-05 --all-files
```

## 详细参考

- 首次配置引导、配置优先级、网页日报手动参数与故障排除：[references/setup-and-troubleshoot.md](references/setup-and-troubleshoot.md)
- 全部脚本完整参数与示例：[references/scripts.md](references/scripts.md)
