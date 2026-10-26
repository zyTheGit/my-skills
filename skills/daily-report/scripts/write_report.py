#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接写入日报到工作内容文件（解决编码问题，按年份自动归档）"""

import argparse
import re
import sys
from pathlib import Path

from archive_report import archive_file
from common import (
    ensure_utf8_stdio,
    match_date_line,
    read_text_utf8_or_gbk,
    resolve_report_file,
    safe_write,
)

ensure_utf8_stdio()


def check_date_exists(date_str: str, output_path: str) -> bool:
    """
    检查文件中是否已存在指定日期的日报

    Args:
        date_str: 日期字符串（如 2026年04月20日）
        output_path: 输出文件路径

    Returns:
        bool: 是否已存在
    """
    output_file = Path(output_path)
    if not output_file.exists():
        return False

    try:
        content = read_text_utf8_or_gbk(output_file)
        return date_str in content
    except Exception:
        return False


def remove_existing_date_report(date_str: str, output_path: str) -> str:
    """
    移除文件中已存在的指定日期的日报

    Args:
        date_str: 日期字符串（如 2026年04月20日）
        output_path: 输出文件路径

    Returns:
        str: 移除后的内容
    """
    output_file = Path(output_path)
    try:
        content = read_text_utf8_or_gbk(output_file)

        # 使用正则表达式匹配该日期下的所有内容
        # 匹配格式：日期行 + 后续的编号行（直到下一个日期或文件结尾）
        pattern = rf'{re.escape(date_str)}.*?(?=\n\d{{4}}年\d{{2}}月\d{{2}}日|$)'
        new_content = re.sub(pattern, '', content, flags=re.DOTALL)

        # 清理多余的空行
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)

        return new_content.strip()
    except Exception:
        return ""


def normalize_newlines(content: str) -> str:
    """
    统一换行符处理，兼容不同 agent 传入方式

    不同 agent 传入 \n 的方式不同：有的通过参数传，字面量 \n 不会被转义；
    有的通过 stdin 传，\n 是真正的换行符。

    策略：把字面量 \\n 统一替换为真正的换行符，再清理多余空行
    """
    # 如果内容中包含字面量 \\n（两个字符），替换为真正的换行符
    if r"\n" in content:
        content = content.replace(r"\n", "\n")

    # 清理多余空行（3个以上连续换行压缩为2个）
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content


def _detect_content_date(content: str) -> tuple[int, int, int] | None:
    """从日报内容中提取日期 (年, 月, 日)；无日期行返回 None"""
    for line in content.split("\n"):
        m = match_date_line(line)
        if m is not None:
            return m
    return None


def _has_date(target: Path, date: tuple[int, int, int]) -> bool:
    """目标文件是否已包含该日期（两种格式都检查）"""
    if not target.exists():
        return False
    y, m, d = date
    candidates = [f"{y}年{m:02d}月{d:02d}日", f"{y}/{m:02d}/{d:02d}"]
    content = read_text_utf8_or_gbk(target)
    return any(c in content for c in candidates)


def write_report(content: str, output_path: str, mode: str = "append", overwrite_date: str = None) -> None:
    """
    写入日报到输出文件

    Args:
        content: 日报内容
        output_path: 输出文件路径
        mode: 写入模式 (append/overwrite)
        overwrite_date: 要覆盖的日期（如果 mode 是 overwrite）
    """
    output_file = Path(output_path)

    # 统一换行符处理
    content = normalize_newlines(content)

    # 确保目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 按年份归档：写入前先把主文件里的历史年份拆到 工作内容_YYYY.txt，
    # 确保主文件只保留当前年份。归档失败不阻塞写入（仅警告）。
    if mode == "append" and output_file.exists():
        try:
            archive_file(str(output_file))
        except Exception as e:
            print(f"警告: 年度归档失败（不影响本次写入）: {e}")

    if mode == "append":
        # 确定目标文件：内容属往年则写入对应年份归档文件，否则写入主文件
        content_date = _detect_content_date(content)
        target = resolve_report_file(output_file, content_date) if content_date else output_file

        # 去重检查：目标文件已有该日期则跳过，防止重复写入
        if content_date and _has_date(target, content_date):
            y, m, d = content_date
            print(f"提示: {y}年{m:02d}月{d:02d}日的日报已存在于 {target.name}，跳过写入")
            print(f"如需覆盖请使用 --mode overwrite --overwrite-date \"{y}年{m:02d}月{d:02d}日\"")
            return

        # 追加内容（文件不存在则直接写入）
        if target.exists():
            existing_content = read_text_utf8_or_gbk(target)
            new_content = existing_content.rstrip() + "\n\n" + content
        else:
            new_content = content
    elif mode == "overwrite":
        if not overwrite_date:
            # 禁止不带日期参数的全文覆写，保护历史内容
            print("错误: --mode overwrite 需要同时指定 --overwrite-date，防止误删历史日报")
            sys.exit(1)
        # 覆盖指定日期的日报
        target = output_file
        existing_content = remove_existing_date_report(overwrite_date, output_path)
        if existing_content:
            new_content = existing_content + "\n\n" + content
        else:
            new_content = content
    else:
        print(f"错误: 未知写入模式 {mode}")
        sys.exit(1)

    # 安全写入：先编码验证，再写临时文件，最后原子替换。
    # 避免 write_text 先截断文件、编码失败时历史内容被清空的严重事故。
    try:
        safe_write(target, new_content)
    except RuntimeError as e:
        print(f"错误: {e}")
        print("原始文件未做任何修改，请检查传入内容后重试。")
        sys.exit(1)

    print(f"日报已写入: {target}")


def main():
    parser = argparse.ArgumentParser(description="写入日报到工作内容文件")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--content", required=False, help="日报内容（直接传入）")
    parser.add_argument("--file", required=False, help="日报文件路径")
    parser.add_argument("--mode", default="append", choices=["append", "overwrite"], help="写入模式")
    parser.add_argument("--overwrite-date", required=False, help="要覆盖的日期（如 2026年04月20日）")
    parser.add_argument("--check-date", required=False, help="检查指定日期是否已存在（只检查不写入）")

    args = parser.parse_args()

    # 只检查日期是否存在
    if args.check_date:
        exists = check_date_exists(args.check_date, args.output)
        print(f"日期 {args.check_date} 已存在: {exists}")
        sys.exit(0 if exists else 1)

    if args.content:
        # 换行符由 normalize_newlines 统一处理，此处直接传入
        content = args.content
    elif args.file:
        content = Path(args.file).read_text(encoding="utf-8")
    else:
        # 从标准输入读取
        content = sys.stdin.read()

    write_report(content, args.output, args.mode, args.overwrite_date)


if __name__ == "__main__":
    main()
