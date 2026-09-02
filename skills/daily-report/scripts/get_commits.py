#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取 Git 提交记录"""

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_commits(
    repo_path: str,
    since: str,
    until: str,
    author: Optional[str] = None,
    branches: Optional[list[str]] = None,
    repo_name: Optional[str] = None,
) -> list[dict]:
    """
    获取指定日期范围的 Git 提交记录

    Args:
        repo_path: Git 仓库路径
        since: 开始日期 (YYYY-MM-DD)
        until: 结束日期 (YYYY-MM-DD)
        author: 作者名称（可选）
        branches: 分支列表（可选，指定后只查这些分支；默认查询所有分支）
        repo_name: 仓库名称（可选，用于日志和输出的 repo 字段）

    Returns:
        提交记录列表
    """
    repo = Path(repo_path)
    if not repo.exists():
        raise FileNotFoundError(f"仓库路径不存在: {repo_path}")

    if not (repo / ".git").exists():
        raise ValueError(f"不是有效的 Git 仓库: {repo_path}")

    name = repo_name or repo.name

    cmd = [
        "git",
        "-C",
        str(repo),
        "log",
        f"--since={since} 00:00:00",
        f"--until={until} 23:59:59",
        "--pretty=format:%H|%s|%ad|%an",
        "--date=short",
    ]

    if branches:
        # 指定分支：先校验存在性，不存在的分支跳过并警告
        valid_branches = []
        for branch in branches:
            check = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", branch],
                capture_output=True, text=True, encoding="utf-8",
            )
            if check.returncode == 0:
                valid_branches.append(branch)
            else:
                print(f"警告: 仓库 {name} 中分支不存在，已跳过: {branch}")

        if not valid_branches:
            print(f"警告: 仓库 {name} 的指定分支均不存在，本次不获取该仓库提交")
            return []

        cmd.extend(valid_branches)
    else:
        # 默认：查询所有分支（含远程和未合并分支）
        cmd.append("--all")

    if author:
        cmd.extend(["--author", author])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, encoding="utf-8"
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git 命令执行失败: {e.stderr}")

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue

        parts = line.split("|", 3)
        if len(parts) == 4:
            hash_val, subject, date, author_name = parts
            commits.append(
                {
                    "hash": hash_val,
                    "subject": subject,
                    "date": date,
                    "author": author_name,
                    "repo": name,
                }
            )

    return commits


def main():
    parser = argparse.ArgumentParser(description="获取 Git 提交记录")
    parser.add_argument("--since", required=True, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--until", required=True, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--repo", required=True, help="Git 仓库路径")
    parser.add_argument("--author", help="作者名称（可选）")
    parser.add_argument(
        "--branch",
        action="append",
        dest="branches",
        help="指定分支（可多次传入，只查这些分支；不传则查询所有分支）",
    )
    parser.add_argument("--output", help="输出文件路径（可选，默认输出到标准输出）")

    args = parser.parse_args()

    commits = get_commits(
        args.repo, args.since, args.until, args.author, args.branches
    )

    output = json.dumps(commits, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
