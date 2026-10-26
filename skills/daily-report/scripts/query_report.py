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


def norm_date(d: str) -> str:
    """2026-04-10 / 2026/04/10 -> 2026年04月10日"""
    m = re.match(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$", d.strip())
    if not m:
        return d
    y, mo, da = m.groups()
    return f"{y}年{int(mo):02d}月{int(da):02d}日"


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

    # 按日期降序排序（最近的在前），用于关键词搜索
    def entry_date(e):
        m = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})", e[0].strip())
        return m.groups() if m else ("0", "0", "0")

    entries_sorted = sorted(entries, key=entry_date, reverse=True)

    # ---- 按月统计日报 ----------------
    if args.month:
        m = re.match(r"^(\d{4})-(\d{1,2})$", args.month.strip())
        if not m:
            print(f"月份格式错误: {args.month}，请使用 YYYY-MM")
            sys.exit(1)
        y, mo = m.groups()
        days = []
        for e in entries:
            dm = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})日?", e[0].strip())
            if dm and dm.group(1) == y and int(dm.group(2)) == int(mo):
                days.append(e[0].strip())
        if not days:
            print(f"{y}年{int(mo):02d}月 没有日报记录")
            sys.exit(0)
        # 按日排序去重（保留原样去重，含加班标记）
        def day_of(s):
            m = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})", s)
            return int(m.group(3)) if m else 0

        seen = set()
        uniq = []
        for d in sorted(days, key=day_of):
            key = re.sub(r"\s*（加班）", "", d)
            if key in seen:
                continue
            seen.add(key)
            uniq.append(d)
        print(f"=== {y}年{int(mo):02d}月 日报：{len(uniq)} 天 ===")
        for d in uniq:
            dm = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})", d)
            dt = datetime(int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
            wd = WEEKDAYS[dt.weekday()]
            tag = "  （加班）" if "加班" in d else ""
            print(f"  {dt.month:02d}-{dt.day:02d} {wd}{tag}")
        return

    # ---- 按日期查询 ----
    if args.date:
        target = norm_date(args.date)
        found = False
        for e in entries_sorted:
            if e[0].strip().startswith(target):
                print("\n".join(e))
                found = True
                break
        if not found:
            print(f"未找到 {args.date} 的日报")
            sys.exit(1)
        return

    # ---- 范围查询 ----
    if args.since or args.until:
        since = norm_date(args.since) if args.since else "0000年01月01日"
        until = norm_date(args.until) if args.until else "9999年12月31日"
        count = 0
        # 范围查询按正序输出
        for e in sorted(entries, key=entry_date):
            d = e[0].strip()
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
