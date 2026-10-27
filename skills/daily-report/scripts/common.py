#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日报生成技能 - 共享工具函数"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ENV_CONFIG_DIR = "DAILY_REPORT_CONFIG_DIR"


def ensure_utf8_stdio() -> None:
    """把 stdin/stdout/stderr 统一为 UTF-8（幂等）

    Windows 控制台/管道默认可能是 GBK，中文正文经 argv 或 stdin 传递时
    会乱码或抛 UnicodeEncodeError。所有脚本入口先调用本函数。
    """
    for stream_name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None or not hasattr(stream, "reconfigure"):
            continue
        if getattr(stream, "encoding", "").lower().replace("-", "") != "utf8":
            stream.reconfigure(encoding="utf-8", errors="replace")


DOTENV_PATH = Path(__file__).resolve().parent.parent / ".env"

_dotenv_loaded = False
_dotenv_keys: set[str] = set()


def read_dotenv(path: Path | None = None) -> dict[str, str]:
    """读取 .env 文件，返回键值对（不修改环境变量）"""
    env_path = path or DOTENV_PATH
    values: dict[str, str] = {}
    if not env_path.is_file():
        return values

    try:
        lines = env_path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return values

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        if key:
            values[key] = value.strip().strip('"').strip("'")
    return values


def load_dotenv(path: Path | None = None) -> set[str]:
    """加载技能目录下的 .env，仅填充尚未设置的环境变量"""
    global _dotenv_loaded
    if _dotenv_loaded:
        return _dotenv_keys
    _dotenv_loaded = True

    for key, value in read_dotenv(path).items():
        if key not in os.environ:
            os.environ[key] = value
            _dotenv_keys.add(key)

    return _dotenv_keys


def discover_config_dir_with_source() -> tuple[Path, str]:
    """解析配置目录，返回 (目录, 来源)

    优先级：环境变量 > 技能目录 .env > 默认 ~/.config/daily-report
    命令行 --config-dir 由调用方自行处理，优先级最高。
    """
    load_dotenv()
    raw = os.environ.get(ENV_CONFIG_DIR, "").strip()
    if raw:
        source = ".env" if ENV_CONFIG_DIR in _dotenv_keys else "环境变量"
        return Path(os.path.expandvars(raw)).expanduser(), source
    return Path.home() / ".config" / "daily-report", "默认路径"


def discover_config_dir() -> Path:
    return discover_config_dir_with_source()[0]


def resolve_config_dir(cli_value: str | None) -> tuple[Path, str]:
    """统一入口：命令行 > 环境变量 > .env > 默认"""
    if cli_value:
        return Path(os.path.expandvars(os.path.expanduser(cli_value))), "命令行"
    return discover_config_dir_with_source()


def load_config(config_dir: Path | None = None) -> dict:
    """加载配置文件；不存在时抛出 FileNotFoundError

    注意：调用方打印配置时需要自行脱敏密码字段。
    """
    config_dir = config_dir or discover_config_dir()
    config_path = config_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"请先运行: uv run python scripts/init_config.py\n"
            f"或用 --config-dir / 环境变量 {ENV_CONFIG_DIR} 指定配置目录"
        )
    return json.loads(config_path.read_text(encoding="utf-8"))


def match_date_line(line: str) -> tuple[int, int, int] | None:
    """匹配日报日期行，返回 (年, 月, 日)；不匹配返回 None

    支持三种格式：
    - 中文：2026年04月02日
    - 斜杠：2026/04/02
    - ISO：2026-04-02
    日期后可带任意注释（如 （加班）、（周会））。

    识别策略：先按日期结构匹配（行首锚定），再验证月日合法
    （1-12月、1-31日），避免正文行以年份开头时的误判。
    """
    for pattern in (
        r"^(\d{4})年(\d{1,2})月(\d{1,2})日",
        r"^(\d{4})/(\d{1,2})/(\d{1,2})",
        r"^(\d{4})-(\d{1,2})-(\d{1,2})",
    ):
        m = re.match(pattern, line)
        if m:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if 1 <= mo <= 12 and 1 <= d <= 31:
                return y, mo, d
    return None


def read_text_utf8_or_gbk(path: Path) -> str:
    """读取文本文件，UTF-8 失败时回退 GBK"""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="gbk")


def parse_blocks(content: str) -> list[tuple[int | None, list[str]]]:
    """按日期行切分日报块，返回 [(year, block_lines), ...]

    每个块以日期行开头，到下一个日期行或文件末尾结束。
    无日期行的散落内容归属为 None（调用方归入当年）。
    """
    blocks: list[tuple[int | None, list[str]]] = []
    current_year: int | None = None
    current_block: list[str] = []

    for line in content.split("\n"):
        m = match_date_line(line)
        if m is not None:
            if current_block:
                blocks.append((current_year, current_block))
            current_year = m[0]
            current_block = [line]
        else:
            current_block.append(line)

    if current_block:
        blocks.append((current_year, current_block))

    return blocks


def find_report_block(
    content: str, date: tuple[int, int, int]
) -> tuple[list[str] | None, int]:
    """查找指定日期的日报块，返回 (块内容, 匹配数量)

    同一天存在多个块时返回最后一个（通常是后追加的）。
    """
    matches = [
        block
        for _, block in parse_blocks(content)
        if any(match_date_line(line) == date for line in block)
    ]
    if not matches:
        return None, 0
    return matches[-1], len(matches)


def resolve_report_file(output_file: Path, date: tuple[int, int, int]) -> Path:
    """当天日报所在文件：当年→主文件，往年→工作内容_YYYY.txt"""
    if date[0] == datetime.now().year:
        return output_file
    return output_file.with_name(f"{output_file.stem}_{date[0]}{output_file.suffix}")


def safe_write(path: Path, content: str) -> None:
    """安全写入：先编码验证；已存在的文件原地覆写，新文件走临时+原子替换。

    原地覆写保留同一文件对象——Windows 桌面上"临时文件+替换"会被
    Explorer 视为删除重建，导致图标位置重排。
    失败时抛 RuntimeError。
    """
    try:
        data = content.encode("utf-8")
    except UnicodeEncodeError as e:
        raise RuntimeError(f"内容包含无法编码为 UTF-8 的字符: {e}") from e

    if path.exists():
        try:
            with open(path, "wb") as f:
                f.write(data)
        except OSError as e:
            raise RuntimeError(f"写入文件失败: {e}") from e
        return

    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_bytes(data)
    try:
        os.replace(tmp_path, path)
    except Exception as e:
        if tmp_path.exists():
            tmp_path.unlink()
        raise RuntimeError(f"替换文件失败: {e}") from e


def _longest_common_substring(a: str, b: str) -> str:
    """返回两个字符串的最长公共子串"""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    end_pos = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
    return a[end_pos - max_len:end_pos]


def _merge_similar_items(items: list[str]) -> list[str]:
    """
    合并同类项：检测共享公共子串的条目，合并为一条
    如 "导出模块支持 Excel 格式" 和 "导出模块支持 PDF 格式"
    → "Excel 格式、PDF 格式等导出模块支持"
    """
    if len(items) <= 1:
        return items

    n = len(items)
    used = set()
    result = []

    for i in range(n):
        if i in used:
            continue

        group = [i]
        for j in range(i + 1, n):
            if j in used:
                continue
            common = _longest_common_substring(items[i], items[j])
            # 公共子串需 >= 6 且包含中文，避免 "等loading" 这种不通顺合并
            if len(common) >= 6 and re.search(r'[一-龥]', common):
                group.append(j)
                used.add(j)

        if len(group) == 1:
            result.append(items[group[0]])
        else:
            group_items = [items[idx] for idx in group]
            # 找组内所有条目的最长公共子串
            common = group_items[0]
            for gi in range(1, len(group_items)):
                common = _longest_common_substring(common, group_items[gi])

            if common and len(common) >= 4:
                parts = []
                for s in group_items:
                    idx = s.index(common)
                    prefix = s[:idx].strip()
                    # 如果公共部分在开头，取后缀作为区分
                    suffix = s[idx + len(common):].strip()
                    if prefix:
                        parts.append(prefix)
                    elif suffix:
                        parts.append(suffix)
                    else:
                        parts.append(s)
                unique = "、".join(p for p in parts if p)
                if unique:
                    result.append(f"{unique}等{common}")
                else:
                    result.append(common)
            else:
                result.extend(group_items)

    return result


def categorize_commit(subject: str) -> str:
    """根据提交信息前缀分类（支持中英文冒号）"""
    match = re.match(r"^(\w+)(\(.+\))?[：:]\s*", subject)
    if match:
        prefix = match.group(1).lower()
        type_mapping = {
            "feat": "功能开发", "feature": "功能开发",
            "fix": "问题修复", "bugfix": "问题修复",
            "refactor": "代码重构",
            "docs": "文档更新",
            "test": "测试相关",
            "chore": "构建/工具",
            "style": "样式调整",
            "perf": "性能优化",
        }
        return type_mapping.get(prefix, "其他工作")

    keywords = {
        "添加": "功能开发", "完成": "功能开发", "实现": "功能开发", "新增": "功能开发",
        "修复": "问题修复", "解决": "问题修复",
        "优化": "性能优化",
        "重构": "代码重构",
    }
    for keyword, category in keywords.items():
        if keyword in subject:
            return category
    return "其他工作"


def clean_subject(subject: str) -> str:
    """清洗提交信息：移除前缀和技术细节，保留核心描述"""
    # 移除英文前缀 (feat:, fix: 等)
    cleaned = re.sub(
        r"^(feat|feature|fix|bugfix|refactor|docs|test|chore|style|perf)(\(.+?\))?:\s*",
        "", subject, flags=re.IGNORECASE
    )
    # 移除中文冒号前缀
    cleaned = re.sub(
        r"^(feat|feature|fix|bugfix|refactor|docs|test|chore|style|perf)(\(.+?\))?：\s*",
        "", cleaned, flags=re.IGNORECASE
    )
    # 移除 BUG 编号引用（会单独汇总）
    cleaned = re.sub(
        r'\s*(?:BUG|bug|禅道)[#\-\s]*\d+\s*', ' ', cleaned, flags=re.IGNORECASE
    )
    # 先移除 [type](scope)[：:] 整体前缀（如 [fix](planner): xxx），避免拆散
    cleaned = re.sub(r"^\[\w+\]\([\w\s\-]+\)\s*[：:]?\s*", "", cleaned)
    # 移除 ticket/issue 编号
    cleaned = re.sub(r"\s*#\d+\s*", " ", cleaned)
    cleaned = re.sub(r"\s*\[[\w-]+\]\s*", " ", cleaned)
    # 移除行首残留的 (scope) 标记
    cleaned = re.sub(r"^\s*\([\w\s\-]+\)\s*", "", cleaned)
    # 移除 (#pr) 等标记
    cleaned = re.sub(r"\s*\(#\w+\)\s*", " ", cleaned)
    # 清理残留的分隔符
    cleaned = re.sub(r'\s*[-:：]\s*', ' ', cleaned)
    # 压缩多余空格
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # 跳过无意义提交
    stripped = cleaned.strip()
    if stripped.lower() in ("tongbu", "1", "同步", ".", "..", ""):
        return ""
    # 过滤 "Update xxx" 等纯文件更新提交
    if re.match(r'^Update\s+\S', stripped, re.IGNORECASE):
        return ""
    return stripped


def extract_bug_numbers(subject: str) -> list[str]:
    """从提交信息中提取 BUG 编号列表"""
    numbers = []

    # 原有模式：BUG123, bug123, 禅道123, #123
    for match in re.finditer(
        r'(?:BUG|bug|禅道)[#\-\s]*(\d+)|#(\d+)',
        subject
    ):
        num = match.group(1) or match.group(2)
        if num not in numbers:
            numbers.append(num)

    # 新增：识别 fix: 后跟纯数字的 BUG 编号（如 fix: 3337、3480、3477）
    # 同时支持中英文冒号，排除单数字的无效提交
    fix_match = re.match(
        r'^fix(?:\(.+?\))?[：:]\s*([\d、，,\s\-]+)$',
        subject, re.IGNORECASE
    )
    if fix_match:
        for num in re.findall(r'\d+', fix_match.group(1)):
            if num not in numbers and len(num) >= 2:
                numbers.append(num)

    return numbers


def summarize_commits_grouped(commits: list[dict]) -> tuple[dict[str, dict[str, list[str]]], list[str]]:
    """
    分组汇总提交记录 - 按项目分组，再按类型分组，BUG编号统一收集

    返回: (grouped, bug_numbers)
    grouped = {
        "项目A": {"功能开发": [...], "问题修复": [...]},
        "项目B": {"功能开发": [...]},
    }
    bug_numbers = ["1001", "1002"]
    """
    filtered = [c for c in commits if not c["subject"].lower().startswith("merge")]

    all_bug_numbers = []
    grouped: dict[str, dict[str, list[str]]] = {}

    for commit in filtered:
        repo = commit["repo"]
        subject = commit["subject"]

        # 提取 BUG 编号
        bug_nums = extract_bug_numbers(subject)
        all_bug_numbers.extend(bug_nums)

        # 清洗提交信息
        cleaned = clean_subject(subject)
        if not cleaned:
            continue

        # 清洗后只剩纯数字，归类为 BUG 编号
        if re.match(r'^[\d、，,\s\-]+$', cleaned):
            for num in re.findall(r'\d+', cleaned):
                if num not in all_bug_numbers and len(num) >= 2:
                    all_bug_numbers.append(num)
            continue

        # 判断类型
        category = categorize_commit(subject)

        if repo not in grouped:
            grouped[repo] = {}
        if category not in grouped[repo]:
            grouped[repo][category] = []

        if cleaned not in grouped[repo][category]:
            grouped[repo][category].append(cleaned)

    # 合并同类项：每个项目每个类别内相似的条目合并
    for repo in grouped:
        for cat in grouped[repo]:
            grouped[repo][cat] = _merge_similar_items(grouped[repo][cat])

    # BUG编号去重，保持发现顺序
    bug_seen = set()
    unique_bugs = []
    for num in all_bug_numbers:
        if num not in bug_seen:
            bug_seen.add(num)
            unique_bugs.append(num)

    return grouped, unique_bugs


def format_report(
    date: str,
    commits: list[dict],
    is_holiday: bool,
    default_content: str = "日常工作",
) -> str:
    """
    格式化日报内容
    按项目分类 → 相同类型合并 → BUG修复统一汇总
    """
    dt = datetime.strptime(date, "%Y-%m-%d")
    date_str = f"{dt.year}年{dt.month:02d}月{dt.day:02d}日"

    if is_holiday and commits:
        date_str += " （加班）"

    # 检查是否有非 Merge 的有效提交
    filtered = [c for c in commits if not c["subject"].lower().startswith("merge")]
    if not filtered:
        return f"{date_str}\n1. {default_content}"

    grouped, bug_numbers = summarize_commits_grouped(commits)

    lines = [date_str]

    # 类别显示顺序
    category_order = [
        "功能开发", "样式调整", "性能优化", "代码重构",
        "问题修复", "文档更新", "测试相关", "构建/工具", "其他工作",
    ]

    cn_numerals = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

    for idx, (repo_name, categories) in enumerate(grouped.items()):
        numeral = cn_numerals[idx] if idx < len(cn_numerals) else str(idx + 1)
        # 项目之间保留空行，日期行后无空行
        if idx > 0:
            lines.append("")
        lines.append(f"{numeral}、{repo_name}")

        sorted_cats = sorted(
            categories.keys(),
            key=lambda c: category_order.index(c) if c in category_order else 99,
        )

        for cat in sorted_cats:
            items = categories[cat]
            # 合并同类项为一行，用；分隔
            merged = f"{cat}：{'；'.join(items)}"
            lines.append(f"  - {merged}")

    # 统一 BUG 修复汇总
    if bug_numbers:
        lines.append(f"\nBUG修复：{'、'.join(bug_numbers)}")

    return "\n".join(lines).strip()
