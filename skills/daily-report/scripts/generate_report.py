#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动化生成日报 - 统一入口脚本"""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from common import (
    ensure_utf8_stdio,
    format_report,
    load_config,
    resolve_config_dir,
    resolve_report_file,
)
from get_commits import get_commits
from write_report import write_report

ensure_utf8_stdio()


def get_all_commits(
    config: dict, since: str, until: str, branches: list[str] | None = None
) -> list[dict]:
    """并行获取所有仓库的提交记录

    Args:
        config: 配置字典
        since: 开始日期 (YYYY-MM-DD)
        until: 结束日期 (YYYY-MM-DD)
        branches: 命令行指定的分支（可选，优先于每个仓库配置的 branches）
    """
    author = config.get("author")
    repo_configs = config["repos"]

    def fetch(repo_config: dict) -> list[dict]:
        repo_path = repo_config["path"]
        repo_name = repo_config["name"]
        repo_branches = branches or repo_config.get("branches")
        try:
            return get_commits(
                repo_path, since, until,
                author=author, branches=repo_branches, repo_name=repo_name,
            )
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"警告: 无法获取仓库 {repo_name} ({repo_path}) 的提交记录: {e}")
            return []

    if len(repo_configs) <= 1:
        results = [fetch(rc) for rc in repo_configs]
    else:
        with ThreadPoolExecutor(max_workers=min(8, len(repo_configs))) as pool:
            results = list(pool.map(fetch, repo_configs))

    all_commits = []
    seen_hashes: set[str] = set()
    for result in results:
        for commit in result:
            # 主仓库与其 worktree 同时配置时会采到同一提交，按 hash 去重
            if commit["hash"] in seen_hashes:
                continue
            seen_hashes.add(commit["hash"])
            all_commits.append(commit)
    return all_commits


def check_holiday(date: str, api_url: str = "", cache_dir: Path | None = None) -> bool:
    """检查是否为节假日（缓存 + API + 周末回退）"""
    if api_url:
        try:
            from check_holiday import check_holiday as check_holiday_api
            result = check_holiday_api(date, api_url, cache_dir)
            return not result["is_workday"]
        except Exception as e:
            print(f"节假日 API 不可用 ({e})，回退到周末判断")

    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt.weekday() >= 5  # 周六=5, 周日=6


def check_date_exists(date: str, output_path: str) -> bool:
    """检查指定日期的日报是否已存在（往年自动查对应归档文件）"""
    from write_report import check_date_exists as _check
    dt = datetime.strptime(date, "%Y-%m-%d")
    date_str = f"{dt.year}年{dt.month:02d}月{dt.day:02d}日"
    target = resolve_report_file(Path(output_path), (dt.year, dt.month, dt.day))
    return _check(date_str, str(target))


def _read_summary_file(path: str) -> str:
    summary_path = Path(path)
    if not summary_path.is_file():
        print(f"错误: --summary-file 文件不存在: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        return summary_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return summary_path.read_text(encoding="gbk")


def main():
    parser = argparse.ArgumentParser(description="自动化生成日报")
    parser.add_argument(
        "--config-dir",
        help="配置目录路径（优先级最高；默认读取环境变量/.env/用户目录）"
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
    parser.add_argument(
        "--summary-file",
        help="AI 汇总内容所在的 UTF-8 文件路径（推荐：避免中文经命令行参数传递出现编码问题）",
    )

    args = parser.parse_args()

    # 配置目录发现：命令行 > 环境变量 > .env > 默认路径
    config_dir, config_source = resolve_config_dir(args.config_dir)

    print(f"使用配置目录: {config_dir}（来源: {config_source}）")
    sys.stdout.flush()

    try:
        config = load_config(config_dir)
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)

    # 快速写入路径：--summary/--summary-file 只负责把已汇总好的内容写入文件，
    # 不再获取提交、不调用节假日 API（推荐配合上一步 --raw 使用）
    if args.summary_file or (args.summary and not args.raw):
        content = (
            _read_summary_file(args.summary_file) if args.summary_file else args.summary
        )
        write_report(content, config["output_file"], mode="append", force=args.force)
        return

    if not config.get("repos"):
        print("警告: 配置中没有仓库（repos），本次日报不会包含提交记录")

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

    # 节假日判断（结果按日期缓存在配置目录，重复运行不再发网络请求）
    is_holiday = check_holiday(since, config.get("holiday_api", ""), config_dir)
    is_overtime = is_holiday and bool(commits)
    if is_overtime:
        print("检测到节假日/周末加班")

    default_content = config.get("default_content", "日常工作")

    # --raw 模式：输出结构化 JSON 供 AI 自行汇总
    if args.raw:
        import json
        web = config.get("web") or {}
        raw_data = {
            "date": since,
            "since": since,
            "until": until,
            "is_holiday": is_holiday,
            "is_overtime": is_overtime,
            "has_commits": len(commits) > 0,
            "default_content": default_content,
            "output_file": config["output_file"],
            "web_enabled": bool(web.get("enabled")),
            "web_project_configured": bool(str(web.get("project_name") or "").strip()),
            "commits": commits,
        }
        print(json.dumps(raw_data, ensure_ascii=False, indent=2))
        return

    # 格式化日报（规则式，传统模式）
    report = format_report(since, commits, is_holiday, default_content)

    print("\n生成的日报内容:")
    print(report)
    print()

    # 写入文件（--force 时替换同日旧块）
    write_report(report, config["output_file"], mode="append", force=args.force)


if __name__ == "__main__":
    main()
