---
name: daily-report
description: 根据当天 Git 提交记录自动生成工作日报。当用户提到"生成日报"、"日报"、"工作日报"、"git日报"、"提交日报"、"每日汇报"等关键词时使用此技能。支持指定日期、多仓库汇总、节假日判断、历史日报查询，自动追加到工作日志文件；已配置网页日报系统时自动登录、填写表单并保存草稿（提交审核仍需用户明确要求）。跨平台（Windows/macOS/Linux）、跨 agent 工具通用。
allowed-tools: Read Write Bash(uv:*) Bash(python:*) Bash(python3:*) Bash(git:*)
---

# 工作日报生成技能

根据 Git 提交记录自动生成工作日报：并行采集多仓库提交，AI 汇总润色，判断加班，安全追加到日志文件。

## 核心原则

- **快速路径**：配置已存在时直接执行"标准流程"两条命令，不要先跑 `--status` 等前置检查；只有报"配置文件不存在"或用户首次使用时才进入配置流程
- **编码规则**：日报正文一律写入 UTF-8 临时文件后用 `--summary-file` 传入（或经 stdin 管道），**不要把多行中文正文内联在命令行参数里**——Windows 控制台默认 GBK，argv 传中文易乱码；脚本内部已统一 UTF-8 stdio
- **解释器**：优先 `uv run python`；环境没有 uv 时用 `python3` 或 `python`（除 publish_report.py 需要 playwright 外，其余脚本均为纯标准库）
- **不重复写入**：脚本自带同日去重，重复运行会跳过并提示；覆盖需用户明确要求（`--force` 或 overwrite 模式）
- **网页自动填报**：配置了 `web.enabled=true` 时，日报写入后**直接执行自动填表**（`--fill`，保存草稿），不要询问或提醒用户；`web.project_name` 未配置时退化为登录+打开表单+复制正文，并提示一次补配项目。`--submit` 提交审核不自动执行，仅在用户明确要求时、经确认项目/日期/正文/审核人后加 `--submit --yes`
- **敏感信息**：账号密码只从配置文件或环境变量读取，不打印、不写入对话和日志；不要把用户的内网地址、真实姓名等写进任何输出示例

## 标准流程（两步）

### 第 1 步：获取结构化原始数据

```bash
uv run python scripts/generate_report.py --raw
```

指定日期加 `--date YYYY-MM-DD`；范围用 `--since` / `--until`；指定分支用 `--branch`（可多次）。

一次调用内完成：并行读取所有仓库 `git log` → 节假日判断（结果按日期缓存在配置目录，重复运行不发网络请求；API 不可用回退周末判断）→ 输出 JSON：

```json
{
  "date": "2026-05-28",
  "is_holiday": false,
  "is_overtime": false,
  "has_commits": true,
  "default_content": "日常工作",
  "output_file": "~/Desktop/工作内容.txt",
  "web_enabled": true,
  "web_project_configured": true,
  "commits": [
    { "hash": "abc123", "subject": "feat: 列表查询改为分页加载", "date": "2026-05-28", "author": "dev", "repo": "项目A" }
  ]
}
```

**检查点**：
- `has_commits=false` → 正文用 `default_content`
- `is_overtime=true` → 日期行后加"（加班）"
- 退出码 1 且提示"日报已存在" → 询问用户是否覆盖，确认后第 2 步写入时用 `--force` 语义（overwrite 模式），不要静默覆盖

### 第 2 步：AI 汇总并写入

1. 按下方"AI 汇总规则"把 commits 汇总成日报正文
2. 用 Write 工具把正文写入临时文件（UTF-8），如 `<系统临时目录>/daily-report-2026-05-28.txt`
3. 执行写入（不重复跑 git 和节假日 API，秒级完成）：

```bash
uv run python scripts/generate_report.py --summary-file <临时文件>
```

4. 写入成功后删除临时文件，向用户展示最终日报内容和输出文件路径

写入脚本自动处理：目录创建、UTF-8 原子写入（失败不破坏原文件）、字面量 `\n` 转换、历史年份归档（`工作内容_YYYY.txt`）、同日去重。

### 第 3 步：网页日报自动填报（按 --raw 输出判断，无需询问）

| 条件 | 动作 |
|------|------|
| `web_enabled=true` 且 `web_project_configured=true` 且日报日期为今天 | 直接执行 `uv run --with playwright python scripts/publish_report.py --fill`（自动登录、填项目与完成工作、保存草稿），把结果随日报一起汇报 |
| `web_enabled=true` 但 `web_project_configured=false` | 执行 `publish_report.py`（默认模式：登录+打开表单+复制正文），并在汇报里提醒一次：补配 `web.project_name` 即可全自动填报 |
| `web_enabled=false` | 不执行网页步骤；可在汇报里提一句支持"网页日报自动填报"（启用 `web` 并配置 `project_name`），仅提醒一次，不反复打扰 |
| 日报日期不是今天 | 不自动执行网页步骤（历史日期与表单当天日期不一致，自动填写会停止）；用户明确要求时再加 `--date` 执行 |

未配置时的提醒只在对话汇报里给出一次（说明"配置后可自动填报/提交"），不要弹窗打断、不要反复追问。退出码 2（登录失败）/ 3（填写中断）时不要重试，把原因和"浏览器已保持打开可手动完成"告知用户。提交审核（`--submit --yes`）永远不自动执行。

## AI 汇总规则

1. **语义理解**：理解每条提交的真实含义，不机械罗列
2. **智能归类**：按项目和功能模块自然分组，而非简单按 commit 类型（feat/fix）分类
3. **合并同类项**：同个功能的多次提交合并为一条连贯描述（如"导出支持 Excel"+"导出支持 PDF" → "导出：支持 Excel、PDF 两种格式"）
4. **BUG 融入上下文**：BUG 编号不单独罗列，自然融入对应功能描述（如"修复数据回显异常（#1024）"）
5. **功能名称前置**：句首带功能/模块名，再接具体改动（如"批量导入：启用按钮并补充提交参数"）
6. **语言弱 AI 化**：像人手写日报，具体细节落实：
   - 不用"完成了……的开发/优化工作"这类空泛句式，直接写做了什么
   - 少用"提升用户体验"等主观概括词，写具体行为（如"列表查询改为分页加载"）
   - 不堆砌形容词，语气平实简短，一条一事

**输出格式**（日期行顶格；多项目用中文序号分节，项目间空一行；单项目直接编号列条目）：

```
2026年05月28日
一、项目A
1. 列表页：查询改为分页加载，减少首屏等待
2. 数据编辑：修复回显异常（#1024），调整表单加载逻辑

二、项目B
1. 报表导出：新增批量导出，支持 Excel 格式
```

加班日示例：`2026年05月30日 （加班）`；无提交示例：日期行 + `1. 日常工作`。

## 查询历史日报

不要 cat 整个日志文件（占用上下文），用查询脚本：

```bash
uv run python scripts/query_report.py --date 2026-05-28      # 某天
uv run python scripts/query_report.py --keyword 关键词        # 搜索
uv run python scripts/query_report.py --month 2026-05        # 某月清单
uv run python scripts/query_report.py --date 2026-01-05 --all-files  # 含往年归档
```

输出文件路径自动读取配置，无需传参。

## 首次配置（仅当配置缺失时）

运行 `uv run python scripts/init_config.py --status` 查看状态；`needs_setup=true` 或配置不存在时按以下流程交互（用宿主工具的交互提问能力，如 AskUserQuestion；一次最多 4 问）：

**第一轮**：是否使用默认配置目录（`~/.config/daily-report`）；项目扫描根目录；Git 作者名（先跑 `git config --global user.name` 作默认值）；输出文件路径（默认 `~/Desktop/工作内容.txt`）。

**扫描仓库**：

```bash
uv run python scripts/init_config.py --scan "<扫描根目录>"
```

自动跳过 `node_modules`、`dist`、虚拟环境等，默认深度 3（`--scan-depth` 可调）。扫描不到时请用户直接给仓库路径。

**第二轮**：选择纳入日报的仓库及显示名；是否启用网页日报（启用则问表单地址和登录账号——密码不要问，让用户自行编辑配置文件或设置环境变量）。

**写入配置**（首次始终加 `--save-env`，把配置目录记入技能目录 `.env`，后续不再询问）：

```bash
uv run python scripts/init_config.py \
  --repo "<仓库路径>=<显示名>" \
  --author "<作者>" \
  --output "<输出文件>" \
  [--enable-web --web-url "<表单地址>" --web-username "<账号>"] \
  --save-env
```

配置为增量合并；`--repo` 整体替换仓库列表。完成后展示配置摘要，继续标准流程。

**配置目录解析优先级**：`--config-dir` > 环境变量 `DAILY_REPORT_CONFIG_DIR` > 技能目录 `.env` > 默认 `~/.config/daily-report`。脚本启动时打印实际目录和来源。

**config.json 关键字段**：`repos`（path/name，可选 branches）、`output_file`、`author`、`holiday_api`（默认中国节假日 API，可换可留空）、`default_content`、`web`（可选，网页日报联动）。完整说明见 [references/scripts.md](references/scripts.md)。

## 网页日报联动（需 web.enabled=true）

配置齐全时标准流程第 3 步会自动执行 `--fill`。以下为手动/变体用法：

```bash
# 填写项目与正文并保存草稿（标准流程自动执行的就是这条，--project 缺省读 web.project_name）
uv run --with playwright python scripts/publish_report.py --fill

# 只复制正文 + 登录 + 打开表单，不填表（web.project_name 未配置时的退化行为）
uv run --with playwright python scripts/publish_report.py --date 2026-05-28

# 只复制不打开浏览器
uv run --with playwright python scripts/publish_report.py --copy-only

# 提交审核（仅用户明确要求，先确认项目/日期/正文/审核人，再带 --yes）
uv run --with playwright python scripts/publish_report.py --submit --yes --project "<项目>" --reviewer "<审核人>"
```

- 剪贴板跨平台：Windows/macOS 原生支持；Linux 需已安装 `wl-copy`（Wayland）或 `xclip`/`xsel`（X11）
- 浏览器使用系统已安装的 Edge/Chrome（专用 Profile 保持登录态），不额外下载 Chromium；找不到时在 `web.browser.executable` 指定路径
- 退出码：0 成功；1 配置/剪贴板/浏览器失败；2 已复制已打开但自动登录失败（人工登录，**不要自动重试**，避免账号锁定；出现验证码同样停止）；3 填写/提交中途停止（日期不一致、项目/审核人未找到等，浏览器保持打开可手动完成）
- 表单日期与日报日期不一致时默认停止，不要主动加 `--allow-date-mismatch` 绕过
- 失败排查（截图/DOM 快照位置、选择器配置）见 [references/scripts.md](references/scripts.md)

## 故障排除（速查）

| 现象 | 处理 |
|------|------|
| 提示配置文件不存在 | 进入"首次配置"流程 |
| 配置目录和预期不一致 | 看脚本首行输出的来源；优先级见上文 |
| 获取不到提交 | 核对仓库路径（`git -C <path> status`）、日期格式、`author` 是否与实际提交者一致 |
| 写入乱码 | 确认正文经 `--summary-file`/stdin 传入而非 argv；输出文件由脚本统一 UTF-8 写入，读取旧 GBK 文件会自动回退 |
| 节假日判断不准 | API 结果按日期缓存在配置目录 `holiday_cache.json`，当年调休安排变更时可删除该缓存 |
| 网页登录/填写失败 | 看配置目录 `logs/` 下截图；详细排查见 references/scripts.md |

## 脚本一览

| 脚本 | 用途 |
|------|------|
| `generate_report.py` | 统一入口：`--raw` 取数 / `--summary-file` 写入 / 不带参数走规则式格式化 |
| `query_report.py` | 查询历史日报（按日期/关键词/月份/范围） |
| `publish_report.py` | 网页日报：复制、登录、打开表单、填写、提交 |
| `init_config.py` | 配置状态、仓库扫描、创建/增量更新配置 |
| `get_commits.py` / `check_holiday.py` / `format_report.py` / `write_report.py` / `archive_report.py` | 单步工具，一般由统一入口调用 |

详细参数见 [references/scripts.md](references/scripts.md)。
