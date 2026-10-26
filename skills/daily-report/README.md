# 日报生成技能使用指南

跨平台（Windows/macOS/Linux）、跨 agent 工具通用。脚本优先用 `uv run python` 运行；环境没有 uv 时可用 `python3`/`python`（除 publish_report.py 需要 playwright 外均为纯标准库）。

## 快速开始

### 1. 初始化配置

先查看当前配置状态（不会创建文件）：

```bash
uv run python scripts/init_config.py --status
```

首次使用时，直接对 skill 说“生成日报”，它会先询问**是否使用默认配置路径 `~/.config/daily-report`**；不使用则让你输入自定义目录。随后再询问项目扫描根目录、Git 作者、输出文件，以及是否启用网页日报系统。首次配置完成后，配置目录会自动写入技能目录 `.env`，后续不再询问。

也可以手动配置。先扫描 Git 仓库：

```bash
uv run python scripts/init_config.py --scan "/path/to/projects"
```

再写入配置（首次建议加 `--save-env`）：

```bash
uv run python scripts/init_config.py \
  --repo "/path/to/projects/project-a=项目A" \
  --repo "/path/to/projects/project-b=项目B" \
  --author "your-name" \
  --output "~/Desktop/工作内容.txt" \
  --save-env
```

**配置目录解析顺序**：

1. `--config-dir <目录>`
2. 环境变量 `DAILY_REPORT_CONFIG_DIR`
3. 技能目录 `.env` 中的 `DAILY_REPORT_CONFIG_DIR`
4. 默认 `~/.config/daily-report/`

更换配置目录并持久化：

```bash
uv run python scripts/init_config.py --config-dir "D:/configs/daily-report" --save-env
```

### 2. 修改配置

配置保存在 `<配置目录>/config.json`。也可以继续用 `init_config.py` 增量修改，只覆盖传入的字段：

```bash
uv run python scripts/init_config.py --author "new-name"
```

配置文件格式：

```json
{
  "repos": [
    { "path": "/path/to/your/project-a", "name": "项目A" },
    { "path": "/path/to/your/project-b", "name": "项目B" }
  ],
  "output_file": "~/Desktop/工作内容.txt",
  "author": "your-name",
  "holiday_api": "https://timor.tech/api/holiday/info/",
  "default_content": "日常工作"
}
```

**配置项说明**：
- `repos`: 仓库列表，每项为 `{"path": 仓库路径, "name": 显示名称}`（可选 `branches` 指定分支）；直接写字符串会报 KeyError
- `output_file`: 日报输出文件路径，目录不存在时会自动创建
- `author`: Git 作者名称（可选，用于过滤提交）
- `holiday_api`: 节假日 API 地址
- `default_content`: 当天无提交记录时的默认日报内容

### 3. 生成日报

**生成今天的日报**：
```
生成日报
```

**生成指定日期的日报**：
```
生成 2026-04-09 的日报
```

**生成本周的日报**：
```
生成本周的日报
```

### 4. 查询历史日报

不要直接打开整个日志文件，用查询脚本（输出文件路径自动读配置）：

```bash
uv run python scripts/query_report.py --date 2026-04-10      # 某天
uv run python scripts/query_report.py --keyword 关键词        # 搜索
uv run python scripts/query_report.py --month 2026-04        # 某月清单（含星期、加班标记）
uv run python scripts/query_report.py --date 2026-01-05 --all-files  # 含往年归档文件
```

### 5. 网页日报联动（可选）

配置了网页日报后，对 skill 说"生成日报"会在写入本地后**自动**登录、填写项目与完成工作并保存草稿，无需再确认。也可单独执行：

```bash
# 自动填写并保存草稿（项目读 web.project_name）
uv run --with playwright python scripts/publish_report.py --fill

# 不带 --fill 时只复制正文（不含日期行）+ 登录 + 打开表单
uv run --with playwright python scripts/publish_report.py
```

首次使用可以交互式配置，也可以命令行开启：

```bash
uv run python scripts/init_config.py \
  --enable-web \
  --web-url "http://your-daily-system/app#/pages/tabbar/cooperation/workflow-initiate" \
  --web-username "your-account" \
  --project "项目名称或项目编码"
```

密码请直接编辑 `config.json` 的 `web.login.password`，或使用环境变量，不要写在命令历史里：

```json
{
  "web": {
    "enabled": true,
    "url": "http://your-daily-system/app#/pages/tabbar/cooperation/workflow-initiate",
    "project_name": "项目名称或项目编码",
    "browser": {
      "channel": "msedge",
      "profile_dir": "~/.config/daily-report/browser-profile"
    },
    "login": {
      "username": "your-account",
      "password": "your-password"
    }
  }
}
```

说明：
- 首次运行会下载 Playwright Python 包；浏览器使用系统已安装的 Edge/Chrome，不额外下载 Chromium
- 登录态保存在专用 Profile 中，后续运行会复用
- `web.project_name` 已配置时 skill 流程自动 `--fill` 保存草稿；未配置时退化为只复制正文、打开表单，不会填表
- 需要账号密码时也可以用 `DAILY_REPORT_WEB_USERNAME` / `DAILY_REPORT_WEB_PASSWORD` 环境变量
- 自动登录失败时浏览器会保持打开，截图和 DOM 快照保存在 `~/.config/daily-report/logs/`

### 6. 提交审核（需明确要求）

自动填报只保存草稿，不会提交审核。配置审核人：

```bash
uv run python scripts/init_config.py --reviewer "审核人姓名"
```

用户明确要求提交、并确认项目/日期/正文/审核人后执行：

```bash
uv run --with playwright python scripts/publish_report.py --submit --yes
```

说明：
- “项目名称”是选择器，脚本会用配置值搜索项目名称或编码，选中后自动回填“项目编码”
- 默认会校验表单日期与日报日期，不一致时停止；`--allow-date-mismatch` 可绕过（慎用）
- `--fill` 只保存草稿；`--submit` 才会打开审核人选择并提交，必须加 `--yes`
- 剪贴板被占用时可加 `--no-copy`
- 填写/提交中途停止时退出码为 3，浏览器保持打开，可手动完成剩余步骤
- 一个表单只能选一个项目；日报覆盖多个项目时用主项目填报，或分多次运行

## 示例输出

### 工作日示例

```
2026年4月10日
1. 完成用户认证模块开发
2. 修复登录页面样式问题
3. 优化数据库查询性能
```

### 周末加班示例

```
2026年4月12日 （加班）
1. 紧急修复生产环境bug
2. 完成数据迁移脚本
```

## 常见问题

### Q: 如何查看当前配置？

```bash
# 配置目录、来源、仓库数量、网页日报状态
uv run python scripts/init_config.py --status

# 完整配置（密码已脱敏）
uv run python scripts/init_config.py --show
```

### Q: 如何添加新的仓库？

先扫描，再用 `--repo` 覆盖仓库列表（每个 `--repo` 一项）：

```bash
uv run python scripts/init_config.py --scan "C:/projects"
uv run python scripts/init_config.py \
  --repo "C:/projects/a=项目A" \
  --repo "C:/projects/b=项目B"
```

也可以直接编辑配置文件的 `repos` 数组。

### Q: 如何过滤特定作者的提交？

在配置文件中设置 `author` 字段。

### Q: 节假日判断不准确怎么办？

skill 会自动调用节假日 API，如果 API 不可用会回退到周末判断。

## 注意事项

1. 确保 Git 仓库路径正确
2. 确保有权限访问仓库
3. 输出文件目录不存在时会自动创建
4. 节假日 API 需要网络连接，不可用时自动回退到周末判断

## 高级用法

### 多仓库汇总

配置多个仓库时，skill 会自动合并所有提交记录并统一汇总。

### 自定义日期范围

```
生成 2026-04-01 到 2026-04-10 的日报
```

### 查看脚本帮助

```bash
uv run python scripts/get_commits.py --help
uv run python scripts/check_holiday.py --help
uv run python scripts/format_report.py --help
```