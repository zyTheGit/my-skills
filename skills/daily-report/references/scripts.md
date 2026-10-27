# 脚本参考

所有脚本优先用 `uv run python` 运行；环境没有 uv 时可直接用 `python3`/`python`（除 publish_report.py 需要 playwright 外均为纯标准库）。脚本内部已统一 UTF-8 stdio，中文输出不受 Windows 控制台 GBK 影响。

## 配置目录解析

`generate_report.py`、`publish_report.py`、`query_report.py`、`init_config.py` 共用同一套解析逻辑，优先级从高到低：

1. 命令行 `--config-dir <目录>`
2. 环境变量 `DAILY_REPORT_CONFIG_DIR`
3. 技能目录 `.env` 中的 `DAILY_REPORT_CONFIG_DIR`
4. 默认 `~/.config/daily-report/`

`.env` 只在环境变量未设置时生效。脚本会打印实际目录和来源：

```
使用配置目录: /home/user/.config/daily-report（来源: 默认路径）
```

`write_report.py`、`archive_report.py`、`format_report.py` 不使用配置目录，直接通过 `--output` 指定文件。

---

## generate_report.py（推荐 - 统一入口）

整合获取提交、节假日检查、格式化、写入全流程。

```bash
uv run python scripts/generate_report.py [--date YYYY-MM-DD] [--force]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--config-dir` | 否 | 配置目录（默认见"配置目录解析"） |
| `--date` | 否 | 指定日期，默认今天 |
| `--since` / `--until` | 否 | 日期范围（与 --date 二选一） |
| `--force` | 否 | 强制覆盖已存在的日报（替换同日旧块，往年自动定位归档文件） |
| `--branch` | 否 | 指定分支，可多次传入；不传则用仓库配置或所有分支 |
| `--raw` | 否 | 输出原始提交数据 (JSON)，由 AI 进行汇总 |
| `--summary` | 否 | AI 汇总后的日报内容（短内容适用；长中文正文建议用 --summary-file） |
| `--summary-file` | 否 | AI 汇总内容所在的 UTF-8 文件路径（**推荐**：避免中文经 argv 传递出现编码问题） |

**行为**：
- 多仓库并行执行 `git log`（最多 8 并发）
- 节假日结果按日期缓存在配置目录 `holiday_cache.json`，命中缓存不发网络请求；API 超时 5 秒，失败回退周末判断
- `--summary-file` / `--summary` 走快速写入路径：只加载配置并写文件，不再获取提交、不再查节假日
- 同日日报已存在时跳过写入并提示；`--force` 或 overwrite 模式覆盖

---

## query_report.py

查询历史日报，避免 cat 整个日志文件占用上下文。输出文件路径自动读取配置的 `output_file`。文件里三种日期行格式（`2026年04月10日` / `2026/04/10` / `2026-04-10`）都能识别；命令行日期参数用 `YYYY-MM-DD`。

```bash
uv run python scripts/query_report.py --date 2026-04-10
uv run python scripts/query_report.py --keyword 关键词 --limit 5
uv run python scripts/query_report.py --since 2026-07-01 --until 2026-07-15
uv run python scripts/query_report.py --month 2026-07
uv run python scripts/query_report.py --date 2026-01-05 --all-files
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--date` | 否 | 查询某天 (YYYY-MM-DD) |
| `--keyword` | 否 | 按关键词搜索，配合 `--limit`（默认 5） |
| `--since` / `--until` | 否 | 范围查询 |
| `--month` | 否 | 列出某月日报日期（含星期、加班标记），格式 YYYY-MM |
| `--all-files` | 否 | 同时搜索同目录归档文件（`<主文件名>_*.txt`） |
| `--config-dir` | 否 | 配置目录 |

以上查询参数至少提供一个。

---

## get_commits.py

获取单个仓库的 Git 提交记录。

```bash
uv run python scripts/get_commits.py --since 2026-04-10 --until 2026-04-10 --repo /path/to/repo [--author name]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--since` / `--until` | 是 | 日期范围 (YYYY-MM-DD) |
| `--repo` | 是 | Git 仓库路径 |
| `--author` | 否 | 按作者过滤 |
| `--branch` | 否 | 指定分支，可多次；不传则查询所有分支（--all） |
| `--output` | 否 | 输出文件路径，默认输出到 stdout |

**输出**：JSON 提交列表。git 输出解析使用 `\x1f` 字段分隔符并关闭 `core.quotepath`，提交信息含 `|`、中文路径均不会破坏解析。

---

## check_holiday.py

检查节假日状态（中国节假日 API + 周末回退，API 地址可配置替换）。

```bash
uv run python scripts/check_holiday.py --date 2026-04-10 [--api-url https://...] [--cache-dir <配置目录>]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--date` | 是 | 日期 (YYYY-MM-DD) |
| `--api-url` | 否 | 节假日 API 地址（默认 timor.tech） |
| `--cache-dir` | 否 | 缓存目录；传入后命中缓存直接返回，不再发请求 |
| `--output` | 否 | 输出文件路径 |

**输出**：JSON，含 `is_workday` 字段；`cached=true` 表示来自缓存，`fallback=true` 表示 API 失败回退周末判断（回退结果不缓存）。调休安排变更时删除缓存目录下的 `holiday_cache.json` 即可。

---

## format_report.py

规则式格式化日报内容（不经 AI，独立 CLI）。

```bash
uv run python scripts/format_report.py --date 2026-04-10 --commits commits.json --is-holiday false
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--date` | 是 | 日期 (YYYY-MM-DD) |
| `--commits` | 是 | 提交记录 JSON 文件路径 |
| `--is-holiday` | 是 | 是否为节假日 (true/false) |
| `--default-content` | 否 | 无提交时的默认内容（默认"日常工作"） |
| `--output` | 否 | 输出文件路径 |

---

## write_report.py

写入日报到文件，处理编码和换行兼容。

**安全写入**：先编码验证 UTF-8，再写临时文件，最后原子替换。编码失败时不会破坏原文件。

**自动年度归档**：append 模式写入前，自动把主文件中的历史年份内容拆到 `<主文件名>_YYYY.txt`，主文件只保留当前年份。归档失败仅告警，不影响本次写入。

```bash
# 推荐：正文经文件或 stdin 传入，避免 shell 编码问题
uv run python scripts/write_report.py --output /path/to/output.txt --file /path/to/content.txt
cat /path/to/content.txt | uv run python scripts/write_report.py --output /path/to/output.txt
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--output` | 是 | 输出文件路径 |
| `--content` | 否 | 日报内容（短内容适用；与 --file/stdin 三选一） |
| `--file` | 否 | 日报内容文件路径（UTF-8） |
| `--mode` | 否 | 写入模式：append（默认）/ overwrite |
| `--overwrite-date` | 否 | 覆盖指定日期的日报（overwrite 模式必填，防止误删历史；支持 `2026年04月20日` / `2026/04/20` / `2026-04-20`，往年自动定位归档文件） |
| `--force` | 否 | append 时同日日报已存在则替换旧块后写入（不加则跳过并提示） |
| `--check-date` | 否 | 仅检查日期是否已存在，不写入 |

不传 `--content`/`--file` 时从 stdin 读取。换行符自动统一（字面量 `\n` → 真正换行符），多余空行压缩。

---

## publish_report.py

自动登录网页日报系统，复制正文、打开表单，可选填写项目/完成工作并保存或提交审核。

```bash
uv run --with playwright python scripts/publish_report.py [--date YYYY-MM-DD] [--copy-only] [--no-copy] [--fill] [--submit --yes] [--project NAME] [--reviewer NAME] [--allow-date-mismatch] [--print] [--include-date] [--config-dir <path>]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--date` | 否 | 日期，默认今天 |
| `--copy-only` | 否 | 只复制内容，不打开浏览器 |
| `--no-copy` | 否 | 不写剪贴板，可与 `--fill` 一起用 |
| `--fill` | 否 | 填写项目名称、完成工作并保存草稿 |
| `--submit` | 否 | 填写后选择审核人并提交审核，必须同时加 `--yes` |
| `--yes` | 否 | 确认提交审核 |
| `--project` | 否 | 项目名称或编码，覆盖 `web.project_name` |
| `--reviewer` | 否 | 审核人姓名，覆盖 `web.reviewer` |
| `--allow-date-mismatch` | 否 | 允许表单日期与日报日期不一致 |
| `--print` | 否 | 同时把正文打印到 stdout |
| `--include-date` | 否 | 复制内容包含日期行（默认不含） |
| `--config-dir` | 否 | 配置目录 |

**默认行为**（不带 `--fill` 时）：
- 从 `output_file` 对应文件（往年自动取归档文件）提取当天日报块
- 默认去掉日期行，只复制正文
- 剪贴板跨平台：Windows（CF_UNICODETEXT）、macOS（pbcopy）、Linux（wl-copy / xclip / xsel，需自行安装）；系统剪贴板被占用时，打开浏览器后会自动经页面上下文重试一次
- 浏览器发现跨平台：Windows/macOS/Linux 常见安装路径 + PATH 查找，优先 `web.browser.channel` 指定的渠道，找不到时回退另一渠道；专用 Profile 启动，通过 CDP 连接
- 自动填写 `web.login.username/password` 登录；已有登录态则跳过
- 打开 `web.url`，浏览器保持打开，脚本退出
- 不填表、不点击保存、不选择审核人

> **技能标准流程**在 `web.enabled=true` 且 `web.project_name` 已配置、日报日期为今天时，会自动带 `--fill` 执行（登录、填写项目与完成工作、保存草稿），无需用户确认；提交审核（`--submit --yes`）永远只在用户明确要求时执行。

**填写流程（`--fill`）**：
1. 点击 `web.workflow_entry_text`（默认"工作日报"）打开表单
2. 等待日期加载，校验表单日期与 `--date` 一致；不一致默认停止
3. 在"项目名称"选择器中搜索项目名称或编码，选中并点"确定"，回填"项目编码"
4. 将正文填入"完成工作"
5. 点击"保存"保存草稿；等待页面出现提交审核入口

> 填写/提交流程中的字段标签、按钮文案和弹层选择器针对常见的 uni-app 工作流表单调优；其他系统页面结构不同时，需通过 `web.form_ready_selector`、`web.login.*_selector` 等配置覆盖，或只使用复制+手动粘贴模式。

**提交流程（`--submit --yes`）**：
1. 完成 `--fill` 的全部步骤
2. 点击提交审核入口
3. 在"选择人员"中按审核人姓名选中，点"确定"
4. 再次点击提交审核
5. 等待提交响应和弹层关闭

**退出码**：

| 退出码 | 含义 |
|--------|------|
| 0 | 复制/打开成功；带 `--submit` 时提交成功 |
| 1 | 配置、日报内容、剪贴板或浏览器启动失败；`--submit` 未加 `--yes` |
| 2 | 内容已复制、浏览器已打开，但自动登录失败（需人工登录） |
| 3 | 填写或提交中途停止（日期不一致、项目/审核人未找到等），浏览器保持打开 |

**登录相关配置**：见 [SKILL.md](../SKILL.md) 的网页日报说明。页面结构特殊时可覆盖：

```json
{
  "web": {
    "login": {
      "username_selector": "input[type~=\"text\"]",
      "password_selector": "input[type=password]",
      "submit_selector": "button.login-btn"
    }
  }
}
```

**环境变量**（优先级高于配置文件）：

```bash
DAILY_REPORT_WEB_USERNAME=your-account
DAILY_REPORT_WEB_PASSWORD=your-password
```

**失败排查**：
- 自动登录失败会在配置目录 `logs/` 下保存 `login-failed-*.png` 和 `.html`；填写失败保存 `fill-failed-*`
- 提示"未找到账号输入框"时检查输入框 `type`：部分 uni-app 页面写成 `type=" text"`（带前导空格），应使用 `input[type~="text"]` 匹配
- 浏览器调试端口未就绪时，关闭日报系统专用浏览器窗口后重试；端口被占用时改 `web.browser.remote_debugging_port`
- 脚本不会自动重试登录，避免账号锁定；出现验证码时停止自动登录等待人工
- 项目/审核人匹配到多个时停止并列出候选，用更完整的名称重试
- 保存/提交接口的成败判定是宽松的：HTTP < 400 且未显式 `success: false` 时，未知 `code` 会再看 `msg` 是否含"成功/success"，最终以页面 UI 状态兜底（出现提交入口/审核弹层关闭即按成功处理，仅打印警告）。如出现"未识别的成功标识"警告，说明系统 code 惯例特殊，可把该 code 补进脚本的 `SUCCESS_CODES`
- Linux 下剪贴板失败：安装 `xclip`/`xsel`（X11）或 `wl-clipboard`（Wayland）；确认运行在桌面会话而非无头服务进程

---

## archive_report.py

按年份归档日报，主文件只保留当年，历史年份拆到 `<主文件名>_YYYY.txt`。

```bash
uv run python scripts/archive_report.py --output /path/to/工作内容.txt [--year 2026] [--dry-run]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--output` | 是 | 主文件路径 |
| `--year` | 否 | 当前年份（默认取今年） |
| `--dry-run` | 否 | 仅预览拆分结果，不实际写入 |

**归档规则**：
- 支持两种日期格式：`2026年04月02日`（中文）和 `2026/04/02`（斜杠）
- 主文件只保留 `--year` 指定年份的日报块
- 历史年份按年拆分；归档文件已存在时合并去重（按整块内容），不会重复追加
- 无日期行的散落内容归入当前年份

**自动触发**：`write_report.py` 在 append 模式写入前会自动调用归档，无需手动运行。

---

## init_config.py

查看配置状态、扫描 Git 仓库、创建或增量更新配置。

```bash
uv run python scripts/init_config.py --status
uv run python scripts/init_config.py --scan "/path/to/projects"
uv run python scripts/init_config.py --repo "/path/to/repo-a=项目A" --author "name" --output "~/Desktop/工作内容.txt"
uv run python scripts/init_config.py --enable-web --web-url "https://..." --save-env
uv run python scripts/init_config.py --project "项目A" --reviewer "审核人姓名"
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--config-dir` | 否 | 配置目录路径（优先级最高） |
| `--status` | 否 | 以 JSON 输出配置目录、来源、是否存在、仓库数量、网页日报状态、`needs_setup` |
| `--scan DIR` | 否 | 扫描目录下的 Git 仓库，输出 JSON；找到仓库后不再向下钻取 |
| `--scan-depth N` | 否 | 扫描深度，默认 3；跳过 `node_modules`、`dist`、虚拟环境等 |
| `--repo PATH[=NAME]` | 否 | 仓库，可重复；会整体替换现有 `repos`。不写名称时用目录名 |
| `--author` | 否 | Git 作者名称 |
| `--output` | 否 | 日报输出文件路径，转为绝对路径保存 |
| `--default-content` | 否 | 无提交时的默认内容 |
| `--holiday-api` | 否 | 节假日 API 地址 |
| `--enable-web` / `--disable-web` | 否 | 启用/停用网页日报；启用需要已有或同时传入 `--web-url` |
| `--web-url` | 否 | 日报表单地址；传入时自动启用网页日报 |
| `--web-username` | 否 | 网页登录账号；密码不要通过命令行传入 |
| `--workflow-entry` | 否 | 登录后点击的流程入口文字，默认"工作日报" |
| `--project` | 否 | 填报时选择的项目名称或项目编码（写入 `web.project_name`） |
| `--reviewer` | 否 | 提交审核时选择的审核人姓名（写入 `web.reviewer`） |
| `--allow-date-mismatch` / `--disallow-date-mismatch` | 否 | 表单日期与日报日期不一致时是否继续（默认停止） |
| `--show` | 否 | 显示当前配置，密码字段脱敏 |
| `--save-env` | 否 | 把配置目录写入技能目录 `.env`；首次配置时建议始终传入 |

**行为**：
- 配置文件不存在时创建，存在时增量合并；只覆盖显式传入的字段
- 新配置会补齐 `web` 段默认值
- `--show` / `--status` 不创建配置文件
- 配置成功后打印摘要（密码只显示是否已配置）

**输出示例（`--status`）**：

```json
{
  "config_dir": "/home/user/.config/daily-report",
  "default_config_dir": "/home/user/.config/daily-report",
  "source": "默认路径",
  "config_path": "/home/user/.config/daily-report/config.json",
  "dotenv_path": "/path/to/skill/.env",
  "dotenv_configured": false,
  "exists": true,
  "valid": true,
  "repo_count": 3,
  "web_enabled": false,
  "needs_setup": false
}
```
