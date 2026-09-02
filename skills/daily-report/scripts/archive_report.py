#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按年份归档日报

策略：主文件只保留当年内容，历史年份自动拆到 工作内容_YYYY.txt。
支持两种日期格式：2026年04月02日（中文）和 2026/04/02（斜杠）。

用法:
    uv run python scripts/archive_report.py --output <主文件路径> [--year 2026] [--dry-run]
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from common import match_date_line, read_text_utf8_or_gbk, safe_write

# 确保 Windows 上的 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


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


def _block_date(block: list[str]) -> tuple[int, int, int] | None:
    """提取块的日期 (年, 月, 日)，无日期行返回 None"""
    for line in block:
        m = match_date_line(line)
        if m is not None:
            return m
    return None


def _date_key(block: list[str]) -> str:
    """从块日期提取排序键 YYYY-MM-DD，无日期行的排最后"""
    d = _block_date(block)
    if d is None:
        return "9999-99-99"
    return f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}"


def _block_text(block: list[str]) -> str:
    """块转文本（去末尾空白）"""
    return "\n".join(block).rstrip()


def _has_body(block: list[str]) -> bool:
    """块内除日期行外是否有实质内容行（过滤空块）"""
    for line in block:
        s = line.strip()
        if s and match_date_line(line) is None:
            return True
    return False


def archive_file(output_path: str, current_year: int | None = None, dry_run: bool = False) -> dict:
    """拆分主文件：历史年份归档到 工作内容_YYYY.txt，当年保留在主文件

    Args:
        output_path: 主文件路径
        current_year: 当前年份（默认取今年）
        dry_run: 仅预览，不实际写入

    Returns:
        dict: {"archived": {年份: 块数}, "kept": 当年块数, "current_year": 年}
    """
    if current_year is None:
        current_year = datetime.now().year

    output_file = Path(output_path)
    if not output_file.exists():
        print(f"警告: 主文件不存在: {output_file}")
        return {"archived": {}, "kept": 0, "current_year": current_year}

    content = read_text_utf8_or_gbk(output_file)
    # 过滤空块：只有日期行、无正文的块不归档
    blocks = [(y, b) for y, b in parse_blocks(content) if _has_body(b)]

    # 按年份分组；无日期行的散落内容归入当年
    by_year: dict[int, list[list[str]]] = {}
    for year, block in blocks:
        y = year if year is not None else current_year
        by_year.setdefault(y, []).append(block)

    # 各年份块按日期排序
    for y in by_year:
        by_year[y].sort(key=_date_key)

    # 归档历史年份（合并已存在的归档文件，去重后重写）
    archived: dict[int, int] = {}
    for year, year_blocks in by_year.items():
        if year == current_year:
            continue
        archive_path = output_file.with_name(f"{output_file.stem}_{year}{output_file.suffix}")

        # 收集归档文件已有块（可能是上次归档留下的），只保留属于该年份的
        existing_blocks: list[list[str]] = []
        if archive_path.exists():
            existing_blocks = [b for b in parse_blocks(read_text_utf8_or_gbk(archive_path))
                               if (d := _block_date(b)) is not None and d[0] == year]

        # 合并去重（按整块内容，同日期不同内容不合并）
        seen: set[str] = set()
        merged: list[list[str]] = []
        for b in existing_blocks + year_blocks:
            key = _block_text(b)
            if key in seen:
                continue
            seen.add(key)
            merged.append(b)

        merged.sort(key=_date_key)

        if dry_run:
            archived[year] = len(merged)
            continue

        new_content = "\n\n".join(_block_text(b) for b in merged) + "\n" if merged else ""
        safe_write(archive_path, new_content)
        archived[year] = len(merged)

    # 主文件只留当年
    current_blocks = by_year.get(current_year, [])
    current_blocks.sort(key=_date_key)
    kept = len(current_blocks)

    if not dry_run:
        new_content = "\n\n".join(_block_text(b) for b in current_blocks) + "\n" if current_blocks else ""
        safe_write(output_file, new_content)

        # 归档后校验：主文件不应残留非当年日期
        stray = sorted({y for y, _ in parse_blocks(read_text_utf8_or_gbk(output_file))
                        if y is not None and y != current_year})
        if stray:
            print(f"警告: 主文件仍包含非 {current_year} 年日期: {stray}")

    return {"archived": archived, "kept": kept, "current_year": current_year}


def main():
    parser = argparse.ArgumentParser(description="按年份归档日报")
    parser.add_argument("--output", required=True, help="主文件路径（如 工作内容.txt）")
    parser.add_argument("--year", type=int, help="当前年份（默认取今年）")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际拆分")
    args = parser.parse_args()

    try:
        result = archive_file(args.output, args.year, args.dry_run)
    except RuntimeError as e:
        print(f"错误: {e}")
        sys.exit(1)

    print(f"当前年份: {result['current_year']}")
    print(f"主文件保留当年块数: {result['kept']}")
    if result["archived"]:
        print("归档的年份:")
        for year in sorted(result["archived"]):
            print(f"  工作内容_{year}.txt: {result['archived'][year]} 个日报块")
    else:
        print("无需归档的历史年份。")


if __name__ == "__main__":
    main()
