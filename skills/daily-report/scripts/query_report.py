# -*- coding: utf-8 -*-
"""日报查询脚本（脚本化查询，避免 cat 全文占用上下文）

输出文件路径来自配置 config.json 的 output_file；--all-files 时同时搜索
同目录下按年份归档的文件（<主文件名>_*.txt）。

用法:
  uv run python scripts/query_report.py --date 2026-04-10           # 查询某天
  uv run python scripts/query_report.py --keyword 关键词 --limit 5   # 按关键词搜最近5条
  uv run python scripts/query_report.py --since 2026-07-01 --until 2026-07-15  # 范围查询
  uv run python scripts/query_report.py --month 2026-07             # 列出某月日报日期（含星期）
  uv run python scripts/query_report.py --date 2026-04-10 --all-files          # 主文件+归档文件
"""
import argparse
import os
import pathlib
import re
import sys
from datetime import datetime

from common import (
    ensure_utf8_stdio,
    load_config,
    match_date_line,
    read_text_utf8_or_gbk,
    resolve_config_dir,
)

ensure_utf8_stdio()

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def split_entries(lines):
    entries = []
    cur = []
    for line in lines:
        if match_date_line(line) is not None:
            if cur:
                entries.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        entries.append(cur)
    return entries


def parse_arg_date(value: str) -> tuple[int, int, int]:
    """解析命令行日期参数 YYYY-MM-DD / YYYY/MM/DD，非法时退出"""
    m = re.match(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$", value.strip())
    if not m:
        print(f"日期格式错误: {value}，请使用 YYYY-MM-DD")
        sys.exit(1)
    return tuple(int(x) for x in m.groups())


def resolve_files(all_files: bool, config_dir: str | None) -> list[pathlib.Path]:
    config_path, _ = resolve_config_dir(config_dir)
    config = load_config(config_path)
    main = pathlib.Path(
        os.path.expandvars(os.path.expanduser(config["output_file"]))
    )
    files = [main]
    if all_files:
        files.extend(sorted(main.parent.glob(f"{main.stem}_*{main.suffix}")))
    return [f for f in files if f.exists()]


def load_entries(files: list[pathlib.Path]):
    result = []
    for f in files:
        result.extend(split_entries(read_text_utf8_or_gbk(f).split("\n")))
    return result


def main():
    parser = argparse.ArgumentParser(description="查询日报内容（不读取整个文件）")
    parser.add_argument("--date", help="查询某天，格式 YYYY-MM-DD")
    parser.add_argument("--keyword", help="按关键词搜索")
    parser.add_argument("--since", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--until", help="结束日期 YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=5, help="关键词搜索最多返回条数（默认5）")
    parser.add_argument("--month", help="列出某月日报日期（格式 YYYY-MM）")
    parser.add_argument("--all-files", action="store_true", help="同时搜索归档文件")
    parser.add_argument("--config-dir", help="配置目录路径（默认读取环境变量/.env/用户目录）")
    args = parser.parse_args()

    if not (args.date or args.keyword or args.since or args.until or args.month):
        parser.print_help()
        sys.exit(1)

    try:
        files = resolve_files(args.all_files, args.config_dir)
    except (FileNotFoundError, KeyError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)

    if not files:
        print("日报输出文件不存在，请先生成日报")
        sys.exit(1)

    entries = load_entries(files)

    # 条目日期元组 (年, 月, 日)；文件里三种日期行格式（中文/斜杠/ISO）都能识别
    def entry_key(e):
        d = match_date_line(e[0].strip()) if e else None
        return d or (0, 0, 0)

    # 按日期降序排序（最近的在前），用于关键词搜索
    entries_sorted = sorted(entries, key=entry_key, reverse=True)

    # ---- 按月统计日报 ----
    if args.month:
        m = re.match(r"^(\d{4})-(\d{1,2})$", args.month.strip())
        if not m:
            print(f"月份格式错误: {args.month}，请使用 YYYY-MM")
            sys.exit(1)
        y, mo = int(m.group(1)), int(m.group(2))
        by_day: dict[int, str] = {}
        for e in entries:
            d = entry_key(e)
            if d[0] == y and d[1] == mo and d[2] and d[2] not in by_day:
                by_day[d[2]] = e[0].strip()
        if not by_day:
            print(f"{y}年{mo:02d}月 没有日报记录")
            sys.exit(0)
        print(f"=== {y}年{mo:02d}月 日报：{len(by_day)} 天 ===")
        for day in sorted(by_day):
            dt = datetime(y, mo, day)
            wd = WEEKDAYS[dt.weekday()]
            tag = "  （加班）" if "加班" in by_day[day] else ""
            print(f"  {mo:02d}-{day:02d} {wd}{tag}")
        return

    # ---- 按日期查询 ----
    if args.date:
        target = parse_arg_date(args.date)
        found = False
        for e in entries_sorted:
            if entry_key(e) == target:
                print("\n".join(e))
                found = True
                break
        if not found:
            print(f"未找到 {args.date} 的日报")
            sys.exit(1)
        return

    # ---- 范围查询 ----
    if args.since or args.until:
        since = parse_arg_date(args.since) if args.since else (0, 1, 1)
        until = parse_arg_date(args.until) if args.until else (9999, 12, 31)
        count = 0
        # 范围查询按正序输出；无日期行的散落内容不参与
        for e in sorted(entries, key=entry_key):
            d = entry_key(e)
            if d == (0, 0, 0):
                continue
            if since <= d <= until:
                print("\n".join(e))
                print()
                count += 1
        if count == 0:
            print("该范围内无日报")
        else:
            print(f"共 {count} 天")
        return

    # ---- 关键词搜索 ----
    if args.keyword:
        hits = [e for e in entries_sorted if any(args.keyword in l for l in e)]
        if not hits:
            print(f"未找到包含「{args.keyword}」的日报")
            sys.exit(1)
        for e in hits[: args.limit]:
            print(f"----- {e[0].strip()} -----")
            print("\n".join(e))
            print()
        total = len(hits)
        shown = min(total, args.limit)
        print(f"命中 {total} 天，显示 {shown} 天（可用 --limit 调整）")
        return


if __name__ == "__main__":
    main()
