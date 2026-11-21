# 首次配置与故障排查参考

## 首次配置（仅当配置缺失时）

运行 `uv run python scripts/init_config.py --status` 查看状态；`needs_setup=true` 或配置不存在时按以下两轮流程交互：

1. **第一轮**：确认配置目录（默认 `~/.config/daily-report`）、项目扫描根目录、Git 作者名（可先查 `git config --global user.name`）及输出文件路径（默认 `~/Desktop/工作内容.txt`）。
2. **扫描仓库**：
   ```bash
   uv run python scripts/init_config.py --scan "<扫描根目录>"
   ```
   自动跳过 `node_modules`、`dist`、虚拟环境等，默认深度 3（`--scan-depth` 可调）；扫描不到时由用户直接指定仓库路径。
3. **第二轮**：选择纳入日报的仓库及显示名；确认是否启用网页日报（启用时仅询问表单地址与登录账号，密码由用户自行编辑配置或设置环境变量）。
4. **写入配置**（首次始终加 `--save-env`，把配置目录写入技能目录 `.env`）：
   ```bash
   uv run python scripts/init_config.py \
     --repo "<仓库路径>=<显示名>" \
     --author "<作者>" \
     --output "<输出文件>" \
     [--enable-web --web-url "<表单地址>" --web-username "<账号>"] \
     --save-env
   ```
   配置为增量合并；`--repo` 整体替换仓库列表。

**配置目录解析优先级**：`--config-dir` > 环境变量 `DAILY_REPORT_CONFIG_DIR` > 技能目录 `.env` > 默认 `~/.config/daily-report`。

**`config.json` 关键字段**：`repos`（path/name，可选 branches）、`output_file`、`author`、`holiday_api`（默认中国节假日 API，可换可留空）、`default_content`、`web`（网页日报配置）。完整参数见 [scripts.md](scripts.md)。

---

## 网页日报手动/变体用法

配置齐全时标准流程第 3 步会自动执行 `--fill`；以下为按需使用的手动模式：

```bash
# 填写项目与正文并保存草稿（--project 缺省读 web.project_name）
uv run --with playwright python scripts/publish_report.py --fill

# 只复制正文 + 登录 + 打开表单，不填表（web.project_name 未配置时的退化行为）
uv run --with playwright python scripts/publish_report.py --date 2026-05-28

# 只复制不打开浏览器
uv run --with playwright python scripts/publish_report.py --copy-only

# 提交审核（仅用户明确要求，先确认项目/日期/正文/审核人，再带 --yes）
uv run --with playwright python scripts/publish_report.py --submit --yes --project "<项目>" --reviewer "<审核人>"
```

- **剪贴板跨平台**：Windows/macOS 原生支持；Linux 需已安装 `wl-copy`（Wayland）或 `xclip`/`xsel`（X11）。
- **浏览器**：复用系统已安装的 Edge/Chrome（专用 Profile 保持登录态），不额外下载 Chromium；找不到时通过 `web.browser.executable` 指定。
- **退出码**：`0` 成功；`1` 配置/剪贴板/浏览器失败；`2` 已复制已打开但自动登录失败（需人工登录，**禁止重试**避免锁号，出现验证码同样停止）；`3` 填写/提交中途停止（浏览器保持打开，由用户手动完成）。
- 表单日期与日报日期不一致时默认停止，禁止主动加 `--allow-date-mismatch` 绕过。

---

## 故障排除（速查）

| 现象 | 处理 |
| :--- | :--- |
| 提示配置文件不存在 | 执行上述「首次配置」流程 |
| 配置目录和预期不一致 | 核对脚本首行输出的实际来源与 4 级解析优先级 |
| 获取不到提交 | 核对仓库路径（`git -C <path> status`）、日期格式、`author` 是否与实际提交者一致 |
| 写入乱码 | 确认正文经 `--summary-file` / stdin 传入而非 argv；脚本统一 UTF-8 写入（读旧 GBK 文件自动回退） |
| 节假日判断不准 | 删除配置目录下的 `holiday_cache.json` 后重试 |
| 网页登录/填写失败 | 查看配置目录 `logs/` 下截图与 DOM 快照；详查见 [scripts.md](scripts.md) |

---

## 脚本一览

| 脚本 | 用途 |
| :--- | :--- |
| `generate_report.py` | 统一入口：`--raw` 取数 / `--summary-file` 写入 / 无参数规则格式化 |
| `query_report.py` | 查询历史日报（按日期/关键词/月份/范围） |
| `publish_report.py` | 网页日报联动：复制、登录、打开表单、填写、提交 |
| `init_config.py` | 配置状态检查、仓库扫描、创建或增量更新配置 |
| `get_commits.py` / `check_holiday.py` / `format_report.py` / `write_report.py` / `archive_report.py` | 单步底层工具，通常由统一入口调度 |
