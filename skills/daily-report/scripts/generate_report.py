#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动化生成日报 - 统一入口脚本"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from common import format_report, summarize_commits
from get_commits import get_commits
from write_report import write_report

# 确保 Windows 上的 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def discover_config_dir() -> Path:
    """获取配置目录（固定路径：~/.config/daily-report/）"""
    return Path.home() / ".config" / "daily-report"


def load_config(config_dir: Path) -> dict:
    """加载配置文件"""
    import json
    config_path = config_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"请先运行: uv run python scripts/init_config.py"
        )
    return json.loads(config_path.read_text(encoding="utf-8"))


def get_all_commits(
    config: dict, since: str, until: str, branches: list[str] | None = None
) -> list[dict]:
    """获取所有仓库的提交记录

    Args:
        config: 配置字典
        since: 开始日期 (YYYY-MM-DD)
        until: 结束日期 (YYYY-MM-DD)
        branches: 命令行指定的分支（可选，优先于每个仓库配置的 branches）
    """
    all_commits = []

    for repo_config in config["repos"]:
        repo_path = repo_config["path"]
        repo_name = repo_config["name"]
        author = config.get("author")

        # 分支优先级：命令行 --branch > 仓库配置 branches > 默认所有分支
        repo_branches = branches or repo_config.get("branches")

        try:
            all_commits.extend(
                get_commits(
                    repo_path, since, until,
                    author=author, branches=repo_branches, repo_name=repo_name,
                )
            )
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"警告: 无法获取仓库 {repo_name} ({repo_path}) 的提交记录: {e}")

    return all_commits


def check_holiday(date: str, api_url: str = "") -> bool:
    """检查是否为节假日（API + 周末回退）"""
    # 优先尝试 API
    if api_url:
        try:
            from check_holiday import check_holiday as check_holiday_api
            result = check_holiday_api(date, api_url)
            return not result["is_workday"]
        except Exception as e:
            print(f"节假日 API 不可用 ({e})，回退到周末判断")

    # 回退：周末判断
    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt.weekday() >= 5  # 周六=5, 周日=6


def check_date_exists(date: str, output_path: str) -> bool:
    """检查指定日期的日报是否已存在"""
    from write_report import check_date_exists as _check
    dt = datetime.strptime(date, "%Y-%m-%d")
    date_str = f"{dt.year}年{dt.month:02d}月{dt.day:02d}日"
    return _check(date_str, output_path)


def main():
    parser = argparse.ArgumentParser(description="自动化生成日报")
    parser.add_argument(
        "--config-dir",
        help="配置目录路径（可选，默认自动发现）"
    )
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认今天")
    parser.add_argument("--since", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--until", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--force", action="store_true", help="强制覆盖已存在的日报")
    parser.add_argument(
        "--branch",
        action="append",
        dest="branches",
        help="指定分支（可多次传入，作用于所有仓库；不传则使用仓库配置或默认所有分支）",
    )
    parser.add_argument("--raw", action="store_true", help="输出原始提交数据 (JSON)，交给 AI 进行汇总")
    parser.add_argument("--summary", help="AI 汇总后的日报内容（跳过规则式格式化）")

    args = parser.parse_args()

    # 配置目录发现
    if args.config_dir:
        config_dir = Path(args.config_dir)
    else:
        config_dir = discover_config_dir()

    print(f"使用配置目录: {config_dir}")

    config = load_config(config_dir)

    # 日期处理
    if args.date:
        since = args.date
        until = args.date
    elif args.since and args.until:
        since = args.since
        until = args.until
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        since = today
        until = today

    # 检查是否已存在
    if args.date or (since == until):
        if not args.force and check_date_exists(since, config["output_file"]):
            print(f"警告: {since} 的日报已存在，使用 --force 参数强制覆盖")
            sys.exit(1)

    # 获取提交记录
    commits = get_all_commits(config, since, until, args.branches)
    print(f"获取到 {len(commits)} 条提交记录")

    if commits:
        for commit in commits[:5]:
            print(f"  [{commit['repo']}] {commit['subject']}")
        if len(commits) > 5:
            print(f"  ... 还有 {len(commits) - 5} 条")

    # 节假日判断
    is_holiday = check_holiday(since, config.get("holiday_api", ""))
    is_overtime = is_holiday and bool(commits)
    if is_overtime:
        print("检测到节假日/周末加班")

    default_content = config.get("default_content", "日常工作")

    # --raw 模式：输出结构化 JSON 供 AI 自行汇总
    if args.raw:
        import json
        raw_data = {
            "date": since,
            "since": since,
            "until": until,
            "is_holiday": is_holiday,
            "is_overtime": is_overtime,
            "has_commits": len(commits) > 0,
            "default_content": default_content,
            "commits": commits,
        }
        print(json.dumps(raw_data, ensure_ascii=False, indent=2))
        return

    # 格式化日报（规则式，传统模式）
    if args.summary:
        report = args.summary
    else:
        report = format_report(since, commits, is_holiday, default_content)

    print("\n生成的日报内容:")
    print(report)
    print()

    # 写入文件
    write_report(report, config["output_file"], mode="append")


if __name__ == "__main__":
    main()
