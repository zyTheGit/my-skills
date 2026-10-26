#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化与更新日报配置"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from common import (
    DOTENV_PATH,
    ENV_CONFIG_DIR,
    ensure_utf8_stdio,
    load_config as load_shared_config,
    read_dotenv,
    resolve_config_dir,
    safe_write,
)

ensure_utf8_stdio()


def get_default_config_dir() -> Path:
    """获取默认配置目录（优先级：环境变量 > .env > ~/.config/daily-report/）"""
    return resolve_config_dir(None)[0]


def get_default_config(config_dir: Path | None = None) -> dict:
    """获取默认配置"""
    config_dir = config_dir or get_default_config_dir()
    output_file = Path.home() / "Desktop" / "工作内容.txt"

    return {
        "repos": [],
        "output_file": str(output_file),
        "author": None,
        "holiday_api": "https://timor.tech/api/holiday/info/",
        "default_content": "日常工作",
        "web": {
            "enabled": False,
            "url": "",
            "copy_include_date": False,
            "workflow_entry_text": "工作日报",
            "project_name": "",
            "reviewer": "",
            "allow_date_mismatch": False,
            "browser": {
                "channel": "msedge",
                "executable": "",
                "profile_dir": str(config_dir / "browser-profile"),
                "remote_debugging_port": 9333,
            },
            "login": {
                "username": "",
                "password": "",
                "username_selector": "",
                "password_selector": "",
                "submit_selector": "",
                "timeout_ms": 20000,
            },
            "form_ready_selector": "",
        },
    }


SECRET_KEY_PARTS = ("password", "passwd", "secret", "token")


def mask_secrets(value):
    """递归脱敏配置中的密码、密钥字段"""
    if isinstance(value, dict):
        masked = {}
        for key, item in value.items():
            if any(part in key.lower() for part in SECRET_KEY_PARTS):
                masked[key] = "***" if item else ""
            else:
                masked[key] = mask_secrets(item)
        return masked
    if isinstance(value, list):
        return [mask_secrets(item) for item in value]
    return value


SKIP_DIR_NAMES = {
    ".git", ".svn", ".hg", ".idea", ".vscode", ".venv", "venv",
    "node_modules", "__pycache__", "dist", "build", "target",
    "vendor", "coverage",
}


def _git_remote(repo_path: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def scan_git_repos(root: str | Path, depth: int = 3) -> tuple[Path, list[dict]]:
    """扫描目录下的 Git 仓库（找到仓库后不再向下钻取）"""
    root_path = Path(os.path.expandvars(os.path.expanduser(str(root)))).resolve()
    if not root_path.is_dir():
        raise FileNotFoundError(f"扫描目录不存在: {root_path}")

    repos: list[dict] = []

    def visit(current: Path, level: int) -> None:
        if (current / ".git").exists():
            repos.append({
                "path": str(current),
                "name": current.name,
                "remote": _git_remote(current),
            })
            return
        if level >= depth:
            return
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            return
        for entry in entries:
            if not entry.is_dir():
                continue
            if entry.name in SKIP_DIR_NAMES or entry.name.startswith("."):
                continue
            visit(entry, level + 1)

    visit(root_path, 0)
    return root_path, repos


def _parse_repo_arg(value: str) -> dict:
    """解析 --repo 参数：PATH 或 PATH=显示名称"""
    raw, sep, name = value.partition("=")
    raw = raw.strip()
    path = Path(os.path.expandvars(os.path.expanduser(raw))).resolve()
    display = name.strip() if sep else ""
    return {"path": str(path), "name": display or path.name}


def _normalize_repos(values: list[str]) -> list[dict]:
    repos = []
    for value in values:
        repo = _parse_repo_arg(value)
        repo_path = Path(repo["path"])
        if not repo_path.is_dir():
            print(f"警告: 仓库路径不存在: {repo['path']}", file=sys.stderr)
        elif not (repo_path / ".git").exists():
            print(f"警告: 目录不是 Git 仓库: {repo['path']}", file=sys.stderr)
        repos.append(repo)
    return repos


def _merge_web_defaults(config: dict, config_dir: Path) -> dict:
    defaults = get_default_config(config_dir)["web"]
    web = config.setdefault("web", {})
    for key, value in defaults.items():
        if isinstance(value, dict):
            section = web.setdefault(key, {})
            for child_key, child_value in value.items():
                section.setdefault(child_key, child_value)
        else:
            web.setdefault(key, value)
    return web


def _apply_updates(config: dict, updates: dict, config_dir: Path) -> None:
    if "repos" in updates:
        config["repos"] = updates["repos"]
    for key in ("author", "output_file", "default_content", "holiday_api"):
        if key in updates:
            config[key] = updates[key]

    web_update = updates.get("web")
    if web_update:
        web = _merge_web_defaults(config, config_dir)
        if "enabled" in web_update:
            web["enabled"] = web_update["enabled"]
        if "url" in web_update:
            web["url"] = web_update["url"]
            if "enabled" not in web_update:
                web["enabled"] = True
        if "username" in web_update:
            web.setdefault("login", {})["username"] = web_update["username"]
        for key in (
            "workflow_entry_text",
            "project_name",
            "reviewer",
            "allow_date_mismatch",
        ):
            if key in web_update:
                web[key] = web_update[key]
        if web.get("enabled") and not web.get("url"):
            raise ValueError("启用网页日报需要 web.url，请同时传入 --web-url")


def _build_updates(args) -> dict:
    updates: dict = {}
    if args.repos is not None:
        updates["repos"] = _normalize_repos(args.repos)
    if args.author is not None:
        updates["author"] = args.author
    if args.output is not None:
        updates["output_file"] = str(
            Path(os.path.expandvars(os.path.expanduser(args.output))).resolve()
        )
    if args.default_content is not None:
        updates["default_content"] = args.default_content
    if args.holiday_api is not None:
        updates["holiday_api"] = args.holiday_api

    web_update: dict = {}
    if args.web_enabled is not None:
        web_update["enabled"] = args.web_enabled
    if args.web_url is not None:
        web_update["url"] = args.web_url
    if args.web_username is not None:
        web_update["username"] = args.web_username
    if args.project is not None:
        web_update["project_name"] = args.project
    if args.reviewer is not None:
        web_update["reviewer"] = args.reviewer
    if args.workflow_entry is not None:
        web_update["workflow_entry_text"] = args.workflow_entry
    if args.allow_date_mismatch is not None:
        web_update["allow_date_mismatch"] = args.allow_date_mismatch
    if web_update:
        updates["web"] = web_update
    return updates


def save_config_dir_to_env(
    config_dir: Path, env_path: Path | None = None
) -> Path:
    """把配置目录写入技能目录的 .env，供后续运行自动读取"""
    env_path = env_path or DOTENV_PATH
    env_path.parent.mkdir(parents=True, exist_ok=True)

    value = str(config_dir).replace("\\", "/")
    new_line = f'{ENV_CONFIG_DIR}="{value}"'

    lines: list[str] = []
    if env_path.is_file():
        lines = env_path.read_text(encoding="utf-8-sig").splitlines()

    output = []
    replaced = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"{ENV_CONFIG_DIR}=") or stripped.startswith(
            f"export {ENV_CONFIG_DIR}="
        ):
            if not replaced:
                output.append(new_line)
                replaced = True
            continue
        output.append(line)

    if not replaced:
        output.append(new_line)

    env_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    return env_path


def _print_summary(config: dict, config_dir: Path) -> None:
    repos = config.get("repos") or []
    print(f"配置目录: {config_dir}")
    print(f"Git 仓库: {len(repos)} 个")
    for repo in repos[:10]:
        print(f"  - {repo.get('name')}: {repo.get('path')}")
    if len(repos) > 10:
        print(f"  ... 还有 {len(repos) - 10} 个")
    print(f"作者: {config.get('author') or '未配置'}")
    print(f"输出文件: {config.get('output_file') or '未配置'}")

    web = config.get("web") or {}
    if web.get("enabled"):
        login = web.get("login") or {}
        password_state = "已配置" if login.get("password") else (
            "未配置（编辑 config.json，或使用 DAILY_REPORT_WEB_PASSWORD）"
        )
        print(f"网页日报: 已启用 {web.get('url')}")
        print(f"  账号: {login.get('username') or '未配置'}")
        print(f"  密码: {password_state}")
        print(f"  上报项目: {web.get('project_name') or '未配置'}")
        print(f"  审核人: {web.get('reviewer') or '未配置'}")
    else:
        print("网页日报: 未启用")


def init_config(
    config_dir: Path | None = None,
    updates: dict | None = None,
    save_env: bool = False,
) -> Path:
    """创建或增量更新配置文件"""
    config_dir = Path(config_dir) if config_dir else get_default_config_dir()
    config_path = config_dir / "config.json"

    exists = config_path.exists()
    if exists:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        config = get_default_config(config_dir)

    if updates:
        _apply_updates(config, updates, config_dir)

    config_dir.mkdir(parents=True, exist_ok=True)
    safe_write(config_path, json.dumps(config, ensure_ascii=False, indent=2) + "\n")
    print(("已更新配置文件: " if exists else "已创建配置文件: ") + str(config_path))
    _print_summary(config, config_dir)

    if save_env:
        env_path = save_config_dir_to_env(config_dir)
        print(f"已写入环境变量文件: {env_path}")
        print(f"  {ENV_CONFIG_DIR}={config_dir}")

    return config_path


def load_config(config_dir: Path | None = None) -> dict:
    """加载配置文件；不存在时抛出 FileNotFoundError"""
    return load_shared_config(config_dir)


def build_status(config_dir: Path, source: str) -> dict:
    config_path = config_dir / "config.json"
    dotenv_value = read_dotenv().get(ENV_CONFIG_DIR, "").strip()
    status = {
        "config_dir": str(config_dir),
        "default_config_dir": str(Path.home() / ".config" / "daily-report"),
        "source": source,
        "config_path": str(config_path),
        "dotenv_path": str(DOTENV_PATH),
        "dotenv_configured": bool(dotenv_value),
        "exists": config_path.exists(),
        "valid": False,
        "repo_count": 0,
        "web_enabled": False,
        "needs_setup": True,
    }
    if not config_path.exists():
        return status

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        status["error"] = f"{type(exc).__name__}: {exc}"
        return status

    repos = config.get("repos") or []
    status.update({
        "valid": True,
        "repo_count": len(repos),
        "web_enabled": bool((config.get("web") or {}).get("enabled")),
        "needs_setup": len(repos) == 0,
    })
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化日报生成配置")
    parser.add_argument(
        "--config-dir",
        help="配置目录路径（优先级最高；默认读取环境变量/.env/用户目录）",
    )
    parser.add_argument("--show", action="store_true", help="显示当前配置（脱敏）")
    parser.add_argument("--status", action="store_true", help="以 JSON 输出配置状态")
    parser.add_argument("--scan", metavar="DIR", help="扫描目录下的 Git 仓库并输出 JSON")
    parser.add_argument("--scan-depth", type=int, default=3, help="仓库扫描深度，默认 3")
    parser.add_argument(
        "--repo",
        dest="repos",
        action="append",
        help="仓库，格式 PATH 或 PATH=显示名称，可重复传入（覆盖现有 repos）",
    )
    parser.add_argument("--author", help="Git 作者名称")
    parser.add_argument("--output", help="日报输出文件路径")
    parser.add_argument("--default-content", help="无提交时的默认日报内容")
    parser.add_argument("--holiday-api", help="节假日 API 地址")
    web_group = parser.add_mutually_exclusive_group()
    web_group.add_argument(
        "--enable-web", dest="web_enabled", action="store_true", default=None,
        help="启用网页日报",
    )
    web_group.add_argument(
        "--disable-web", dest="web_enabled", action="store_false", default=None,
        help="停用网页日报",
    )
    parser.add_argument("--web-url", help="网页日报表单地址（传入时自动启用）")
    parser.add_argument("--web-username", help="网页日报登录账号（密码请写入配置或环境变量）")
    parser.add_argument(
        "--workflow-entry",
        help="登录后点击的流程入口文字，默认“工作日报”",
    )
    parser.add_argument(
        "--project",
        help="填报时选择的项目名称或项目编码（web.project_name）",
    )
    parser.add_argument(
        "--reviewer",
        help="提交审核时选择的审核人姓名（web.reviewer）",
    )
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--allow-date-mismatch",
        dest="allow_date_mismatch",
        action="store_true",
        default=None,
        help="允许表单日期与日报日期不一致",
    )
    date_group.add_argument(
        "--disallow-date-mismatch",
        dest="allow_date_mismatch",
        action="store_false",
        default=None,
        help="表单日期与日报日期不一致时停止填写（默认）",
    )
    parser.add_argument(
        "--save-env",
        action="store_true",
        help=f"把配置目录写入技能目录 .env（{ENV_CONFIG_DIR}）",
    )

    args = parser.parse_args()
    config_dir, source = resolve_config_dir(args.config_dir)

    try:
        if args.scan:
            root, repos = scan_git_repos(args.scan, args.scan_depth)
            print(json.dumps(
                {"root": str(root), "repos": repos}, ensure_ascii=False, indent=2
            ))
            return 0

        if args.status:
            print(json.dumps(
                build_status(config_dir, source), ensure_ascii=False, indent=2
            ))
            return 0

        if args.show:
            config = load_config(config_dir)
            print(json.dumps(mask_secrets(config), ensure_ascii=False, indent=2))
            return 0

        init_config(
            config_dir,
            updates=_build_updates(args),
            save_env=args.save_env,
        )
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
