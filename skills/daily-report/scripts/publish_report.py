#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打开网页日报表单，把当天日报正文复制到剪贴板，可选自动填写并提交。

默认只复制内容并打开表单。使用 --fill 会填写项目名称、完成工作并保存草稿；
再加 --submit --yes 会选择审核人并提交审核。

用法:
    uv run --with playwright python scripts/publish_report.py [--date YYYY-MM-DD]
    uv run --with playwright python scripts/publish_report.py --fill --project 项目名称
    uv run --with playwright python scripts/publish_report.py --submit --yes
"""

import argparse
import ctypes
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from common import (
    ensure_utf8_stdio,
    find_report_block,
    load_config,
    match_date_line,
    read_text_utf8_or_gbk,
    resolve_config_dir,
    resolve_report_file,
)

ensure_utf8_stdio()

DEFAULT_PORT = 9333

BROWSER_CANDIDATES = {
    "win32": {
        "msedge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ],
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
    },
    "darwin": {
        "msedge": [
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ],
        "chrome": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ],
    },
    "linux": {
        "msedge": [
            "/usr/bin/microsoft-edge",
            "/usr/bin/microsoft-edge-stable",
        ],
        "chrome": [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ],
    },
}
WHICH_NAMES = {
    "msedge": ["msedge", "microsoft-edge", "microsoft-edge-stable"],
    "chrome": ["chrome", "google-chrome", "google-chrome-stable", "chromium-browser", "chromium"],
}

USERNAME_SELECTORS = [
    'input[autocomplete="username"]',
    'input[name*="user" i]',
    'input[id*="user" i]',
    'input[name*="account" i]',
    'input[id*="account" i]',
    'input[placeholder*="账号"]',
    'input[placeholder*="用户名"]',
    'input[placeholder*="工号"]',
    'input[placeholder*="手机号"]',
    'input[placeholder*="邮箱"]',
    'input[type~="text"]',
    'input.uni-input-input[type~="text"]',
    'input[type="text"]',
    'input:not([type])',
    'input.uni-input-input:not([type="password"]):not([type="number"])',
]
PASSWORD_SELECTORS = ['input[type~="password"]', 'input[type="password"]']
SUBMIT_SELECTORS = [
    'button:has-text("登录")',
    'button:has-text("登 录")',
    'button:has-text("立即登录")',
    'input[type="submit"]',
    '[role="button"]:has-text("登录")',
    'uni-button:has-text("登录")',
    '.el-button:has-text("登录")',
]
CAPTCHA_SELECTORS = [
    'input[placeholder*="验证码"]',
    'input[name*="captcha" i]',
    'input[id*="captcha" i]',
    'img[src*="captcha" i]',
    'img[alt*="验证码"]',
]


def _expand_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(str(value))))


def _copy_windows(text: str) -> None:
    """写入 Windows 剪贴板（CF_UNICODETEXT），失败时抛 RuntimeError"""
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    cf_unicodetext = 13
    gmem_moveable = 0x0002

    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL
    user32.EmptyClipboard.restype = wintypes.BOOL
    user32.CloseClipboard.restype = wintypes.BOOL
    user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
    user32.SetClipboardData.restype = wintypes.HANDLE
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = wintypes.LPVOID
    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalUnlock.restype = wintypes.BOOL
    kernel32.GlobalFree.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalFree.restype = wintypes.HGLOBAL

    opened = False
    for _ in range(60):
        if user32.OpenClipboard(None):
            opened = True
            break
        time.sleep(0.05)
    if not opened:
        raise RuntimeError(
            "剪贴板被其他程序占用或系统拒绝访问。"
            "排查：关闭剪贴板管理/历史工具和安全软件后重试，或重启资源管理器"
        )

    try:
        if not user32.EmptyClipboard():
            raise RuntimeError("清空剪贴板失败")

        data = text.replace("\n", "\r\n").encode("utf-16-le") + b"\x00\x00"
        handle = kernel32.GlobalAlloc(gmem_moveable, len(data))
        if not handle:
            raise RuntimeError("分配剪贴板内存失败")

        pointer = kernel32.GlobalLock(handle)
        if not pointer:
            kernel32.GlobalFree(handle)
            raise RuntimeError("锁定剪贴板内存失败")

        ctypes.memmove(pointer, data, len(data))
        kernel32.GlobalUnlock(handle)

        if not user32.SetClipboardData(cf_unicodetext, handle):
            kernel32.GlobalFree(handle)
            raise RuntimeError("写入剪贴板失败")
    finally:
        user32.CloseClipboard()


def _copy_via_command(text: str, commands: list[list[str]]) -> None:
    """通过系统剪贴板命令写入（macOS/Linux），失败时抛 RuntimeError"""
    last_error = ""
    for cmd in commands:
        tool = shutil.which(cmd[0])
        if not tool:
            continue
        try:
            result = subprocess.run(
                [tool] + cmd[1:],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=10,
            )
            if result.returncode == 0:
                return
            last_error = result.stderr.decode("utf-8", errors="replace").strip()
        except (OSError, subprocess.SubprocessError) as exc:
            last_error = str(exc)
    raise RuntimeError(
        "未找到可用的剪贴板命令"
        + (f"（最后错误: {last_error}）" if last_error else "")
        + "；Linux 请安装 xclip/xsel（X11）或 wl-clipboard（Wayland）"
    )


def copy_to_clipboard(text: str) -> None:
    """跨平台写入系统剪贴板，失败时抛 RuntimeError"""
    if sys.platform == "win32":
        _copy_windows(text)
    elif sys.platform == "darwin":
        _copy_via_command(text, [["pbcopy"]])
    else:
        _copy_via_command(
            text, [["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]
        )


def _copy_via_browser(page, text: str) -> bool:
    """系统剪贴板被占用时，借助浏览器页面上下文重试写入"""
    try:
        return bool(page.evaluate(
            """async (text) => {
                try {
                    await navigator.clipboard.writeText(text);
                    return true;
                } catch (e) {
                    const ta = document.createElement('textarea');
                    ta.value = text;
                    ta.style.position = 'fixed';
                    ta.style.opacity = '0';
                    document.body.appendChild(ta);
                    ta.select();
                    const ok = document.execCommand('copy');
                    ta.remove();
                    return ok;
                }
            }""",
            text,
        ))
    except Exception:
        return False


def _load_report_body(
    output_path: str, date: tuple[int, int, int], include_date: bool
) -> tuple[str, Path, int]:
    output_file = _expand_path(output_path)
    target = resolve_report_file(output_file, date)
    if not target.exists():
        raise FileNotFoundError(
            f"未找到 {target}，请先生成 {date[0]}-{date[1]:02d}-{date[2]:02d} 的日报"
        )

    content = read_text_utf8_or_gbk(target)
    block, matches = find_report_block(content, date)
    if block is None:
        raise ValueError(
            f"{target.name} 中没有 {date[0]}年{date[1]:02d}月{date[2]:02d}日 的日报"
        )
    if matches > 1:
        print(f"警告: 找到 {matches} 个同日日报块，使用最后一个", file=sys.stderr)

    lines = block if include_date else [
        line for line in block if match_date_line(line) != date
    ]
    body = "\n".join(lines).strip()
    if not body:
        raise ValueError("当天日报正文为空")
    return body, target, matches


def _find_browser(web: dict) -> str:
    browser_cfg = web.get("browser") or {}
    configured = browser_cfg.get("executable")
    if configured:
        path = _expand_path(configured)
        if path.is_file():
            return str(path)
        raise FileNotFoundError(f"配置的浏览器不存在: {path}")

    channel = str(browser_cfg.get("channel") or "msedge").lower()
    platform_key = "darwin" if sys.platform == "darwin" else (
        "win32" if sys.platform == "win32" else "linux"
    )
    candidates = BROWSER_CANDIDATES[platform_key].get(channel, [])
    # 指定渠道找不到时，回退尝试另一渠道
    other = "chrome" if channel == "msedge" else "msedge"
    candidates = candidates + BROWSER_CANDIDATES[platform_key].get(other, [])
    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate

    for name in WHICH_NAMES[channel] + WHICH_NAMES[other]:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError(
        "未找到 Edge/Chrome，请在 web.browser.executable 中指定浏览器路径"
    )


def _cdp_alive(port: int) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/json/version", timeout=1
        ) as response:
            return response.status == 200
    except Exception:
        return False


def _ensure_browser(web: dict, config_dir: Path) -> int:
    browser_cfg = web.get("browser") or {}
    port = int(browser_cfg.get("remote_debugging_port") or DEFAULT_PORT)
    if _cdp_alive(port):
        return port

    executable = _find_browser(web)
    profile_dir = _expand_path(
        browser_cfg.get("profile_dir") or (config_dir / "browser-profile")
    )
    profile_dir.mkdir(parents=True, exist_ok=True)

    args = [
        executable,
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-sync",
        "--disable-extensions",
        "--disable-session-crashed-bubble",
        "--disable-features=msEdgeFirstRunExperience",
        "--start-maximized",
        "about:blank",
    ]
    if browser_cfg.get("headless"):
        args.insert(1, "--headless=new")

    creationflags = 0
    if sys.platform == "win32":
        creationflags = (
            subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        )

    subprocess.Popen(
        args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
        close_fds=True,
    )

    deadline = time.time() + 30
    while time.time() < deadline:
        if _cdp_alive(port):
            return port
        time.sleep(0.3)

    raise RuntimeError(
        f"浏览器调试端口 {port} 未就绪。\n"
        "请关闭已打开的日报系统专用浏览器窗口后重试，"
        "或修改 web.browser.remote_debugging_port 换一个端口。"
    )


def _frames(page):
    return page.frames or [page.main_frame]


def _first_visible(page, selectors: list[str], timeout_ms: int = 0):
    """在页面及 iframe 中查找第一个可见元素，返回 (frame, locator)"""
    selectors = [selector for selector in selectors if selector]
    deadline = time.time() + timeout_ms / 1000

    while True:
        for frame in _frames(page):
            for selector in selectors:
                try:
                    locator = frame.locator(selector)
                    if locator.count() > 0 and locator.first.is_visible():
                        return frame, locator.first
                except Exception:
                    continue
        if time.time() >= deadline:
            return None
        time.sleep(0.2)


def _has_password_field(page, timeout_ms: int = 0) -> bool:
    return _first_visible(page, PASSWORD_SELECTORS, timeout_ms) is not None


def _save_debug(page, label: str, config_dir: Path) -> list[Path]:
    log_dir = config_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    saved: list[Path] = []

    screenshot = log_dir / f"{label}-{stamp}.png"
    try:
        page.screenshot(path=str(screenshot), full_page=True)
        saved.append(screenshot)
    except Exception:
        pass

    snapshot = log_dir / f"{label}-{stamp}.html"
    try:
        snapshot.write_text(page.content(), encoding="utf-8")
        saved.append(snapshot)
    except Exception:
        pass

    return saved


def _auto_login(page, web: dict, target_url: str, username: str, password: str) -> bool:
    if _find_form_frame(page, timeout_ms=1500) is not None:
        return True

    login_cfg = web.get("login") or {}
    timeout_ms = int(login_cfg.get("timeout_ms") or 20000)

    page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
    if not _has_password_field(page, timeout_ms=6000):
        return True

    if _first_visible(page, CAPTCHA_SELECTORS):
        print("自动登录失败：登录页需要验证码，请在浏览器中手动登录", file=sys.stderr)
        return False

    username_el = _first_visible(
        page, [login_cfg.get("username_selector") or ""] + USERNAME_SELECTORS, 3000
    )
    password_el = _first_visible(
        page, [login_cfg.get("password_selector") or ""] + PASSWORD_SELECTORS, 3000
    )
    submit_el = _first_visible(
        page, [login_cfg.get("submit_selector") or ""] + SUBMIT_SELECTORS, 3000
    )

    missing = []
    if username_el is None:
        missing.append("账号输入框")
    if password_el is None:
        missing.append("密码输入框")
    if submit_el is None:
        missing.append("登录按钮")
    if missing:
        print(
            "自动登录失败：未找到 " + "、".join(missing)
            + "，请检查 web.login.*_selector 配置",
            file=sys.stderr,
        )
        return False

    try:
        username_el[1].click()
        username_el[1].fill(username)
        password_el[1].click()
        password_el[1].fill(password)
        submit_el[1].click()
    except Exception as exc:
        print(f"自动登录失败：填写登录表单时出错: {exc}", file=sys.stderr)
        return False

    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        if not _has_password_field(page):
            break
        page.wait_for_timeout(300)
    else:
        print("自动登录失败：登录后仍停留在登录页", file=sys.stderr)
        return False

    page.wait_for_timeout(1200)
    page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
    if _has_password_field(page, timeout_ms=4000):
        print("自动登录后仍未进入日报表单，请在浏览器中手动登录", file=sys.stderr)
        return False
    return True


def _pick_page(context, target_url: str):
    from urllib.parse import urlparse

    host = urlparse(target_url).netloc
    for page in context.pages:
        try:
            if host and urlparse(page.url).netloc == host:
                return page
        except Exception:
            continue
    for page in context.pages:
        if page.url == "about:blank":
            return page
    return context.new_page()


def _is_visible(locator) -> bool:
    try:
        return locator.count() > 0 and locator.first.is_visible()
    except Exception:
        return False


def _first_visible_locator(locator):
    try:
        for index in range(locator.count()):
            element = locator.nth(index)
            if element.is_visible():
                return element
    except Exception:
        pass
    return None


def _wait_until(check, timeout_s: float, interval: float = 0.3):
    deadline = time.time() + timeout_s
    while True:
        try:
            result = check()
        except Exception:
            result = None
        if result:
            return result
        if time.time() >= deadline:
            return None
        time.sleep(interval)


def _click_visible(locator, timeout_s: float = 0) -> bool:
    deadline = time.time() + timeout_s
    while True:
        try:
            for index in range(locator.count()):
                element = locator.nth(index)
                if element.is_visible():
                    element.click()
                    return True
        except Exception:
            pass
        if time.time() >= deadline:
            return False
        time.sleep(0.2)


def _form_item(frame, label: str):
    pattern = re.compile(rf"^\s*{re.escape(label)}\s*$")
    return (
        frame.locator(".uni-forms-item")
        .filter(has=frame.locator(".item-label-text", has_text=pattern))
        .first
    )


def _field_value(frame, label: str) -> str:
    item = _form_item(frame, label)
    return item.locator("input, textarea").first.input_value(timeout=5000).strip()


def _find_form_frame(page, timeout_ms: int = 0):
    def find():
        for frame in _frames(page):
            try:
                if _form_item(frame, "完成工作").count():
                    return frame
            except Exception:
                continue
        return None

    return _wait_until(find, timeout_ms / 1000)


def _open_work_report_form(page, web: dict):
    frame = _find_form_frame(page)
    if frame is not None:
        return frame

    entry_text = str(web.get("workflow_entry_text") or "工作日报").strip()
    clicked = False
    for frame in _frames(page):
        try:
            candidates = frame.get_by_text(entry_text, exact=True)
            if candidates.count() and _click_visible(candidates, 3000):
                clicked = True
                break
        except Exception:
            continue
    if not clicked:
        for frame in _frames(page):
            try:
                if _click_visible(frame.locator(f"text={entry_text}"), 2000):
                    clicked = True
                    break
            except Exception:
                continue
    if not clicked:
        raise RuntimeError(
            f"未找到流程入口“{entry_text}”，请检查 web.workflow_entry_text"
        )

    frame = _find_form_frame(page, timeout_ms=30000)
    if frame is None:
        raise RuntimeError(
            f"点击“{entry_text}”后未加载出日报表单，请检查网络或 web.workflow_entry_text"
        )
    return frame


def _check_form_date(frame, expected: str, allow_mismatch: bool) -> None:
    try:
        form_date = _wait_until(lambda: _field_value(frame, "日期") or None, 15)
    except Exception as exc:
        raise RuntimeError(f"无法读取表单日期: {exc}") from exc

    if not form_date:
        raise RuntimeError("表单日期为空，已停止填写")
    if form_date == expected:
        return
    if allow_mismatch:
        print(
            f"警告: 表单日期 {form_date} 与日报日期 {expected} 不一致，"
            "已按 --allow-date-mismatch 继续",
            file=sys.stderr,
        )
        return
    raise RuntimeError(
        f"表单日期 {form_date} 与日报日期 {expected} 不一致，已停止填写。"
        "请确认表单日期后重试；如确实要填到当前表单，请加 --allow-date-mismatch"
    )


def _parse_project_text(text: str) -> tuple[str, str]:
    name = code = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("项目名称："):
            name = line.split("：", 1)[1].strip()
        elif line.startswith("项目编码："):
            code = line.split("：", 1)[1].strip()
    return name, code


def _close_grid_picker(frame) -> None:
    _click_visible(frame.locator(".je-modal-window__buttons .button-default"), 2000)


def _current_grid(frame):
    return _first_visible_locator(frame.locator(".je-func-select-grid"))


def _fill_project(frame, project: str) -> None:
    item = _form_item(frame, "项目名称")
    picker = item.locator(".je-input-picker").first
    if not _is_visible(picker):
        raise RuntimeError("项目名称不是可点击的选择器，页面结构可能已变化")
    picker.click()

    grid = _wait_until(lambda: _current_grid(frame), 15)
    if grid is None:
        raise RuntimeError("项目名称选择器未打开")

    chosen = None
    last_texts: list[str] = []
    deadline = time.time() + 20
    while time.time() < deadline:
        grid = _current_grid(frame)
        if grid is None:
            raise RuntimeError("项目名称选择器已关闭")

        search = grid.locator("input.uni-input-input").first
        search_active = False
        try:
            if search.count():
                if search.input_value().strip() != project:
                    search.fill(project)
                search_active = search.input_value().strip() == project
        except Exception:
            pass

        try:
            texts = [
                text.strip()
                for text in grid.locator(".je-list-item-wrapper").all_inner_texts()
            ]
        except Exception:
            texts = []
        if texts and search_active:
            last_texts = texts

        exact: list[tuple[str, str]] = []
        fuzzy: list[tuple[str, str]] = []
        for text in texts:
            name, code = _parse_project_text(text)
            if not name:
                continue
            if name == project or code == project:
                exact.append((name, code))
            elif project in name or (code and project in code):
                fuzzy.append((name, code))

        exact = list(dict.fromkeys(exact))
        fuzzy = list(dict.fromkeys(fuzzy))
        if exact:
            if len(exact) > 1:
                names = "、".join(f"{n}（{c}）" for n, c in exact[:5])
                _close_grid_picker(frame)
                raise RuntimeError(
                    f"项目“{project}”匹配到多个：{names}，请填写更完整的名称"
                )
            chosen = exact[0]
            break
        if fuzzy:
            if len(fuzzy) > 1:
                names = "、".join(f"{n}（{c}）" for n, c in fuzzy[:5])
                _close_grid_picker(frame)
                raise RuntimeError(
                    f"项目“{project}”匹配到多个：{names}，请填写更完整的名称"
                )
            chosen = fuzzy[0]
            break
        time.sleep(0.4)

    if chosen is None:
        suggestions = [
            name
            for name, _ in (_parse_project_text(text) for text in last_texts[:5])
            if name
        ]
        _close_grid_picker(frame)
        hint = "；候选：" + "、".join(suggestions) if suggestions else ""
        raise RuntimeError(f"未找到项目“{project}”{hint}")

    grid = _current_grid(frame)
    if grid is None:
        raise RuntimeError("项目名称选择器已关闭")
    grid.locator(".je-list-item-wrapper").filter(has_text=chosen[0]).first.click()
    time.sleep(0.5)
    if not _click_visible(frame.locator(".je-modal-window__buttons .button-primary"), 5000):
        raise RuntimeError("项目选择器未找到“确定”按钮")

    _wait_until(lambda: _current_grid(frame) is None, 10)
    value = _field_value(frame, "项目名称")
    if chosen[0] not in value:
        raise RuntimeError(
            f"项目选择后回显异常：期望包含“{chosen[0]}”，实际“{value}”"
        )
    if not _field_value(frame, "项目编码"):
        raise RuntimeError("项目选择后项目编码为空")


def _fill_work_content(frame, body: str) -> None:
    textarea = _form_item(frame, "完成工作").locator("textarea").first
    if not _is_visible(textarea):
        raise RuntimeError("未找到“完成工作”输入框")
    textarea.click()
    textarea.fill(body)
    if textarea.input_value().strip() != body.strip():
        raise RuntimeError("完成工作内容写入后校验失败")


def _click_form_button(frame, text: str, timeout_s: float = 5) -> bool:
    return _click_visible(
        frame.locator(".footer-buttons uni-view.button").filter(has_text=text),
        timeout_s,
    )


def _response_message(response) -> tuple[int, str, dict]:
    status = getattr(response, "status", 0)
    payload: dict = {}
    try:
        payload = response.json()
    except Exception:
        pass
    message = str(payload.get("msg") or payload.get("message") or "")
    return status, message, payload


# 常见"成功"code 惯例；不在名单内的 code 再看 msg，最终以页面 UI 状态兜底
SUCCESS_CODES = {0, "0", 200, "200", "0000", "000000", True, "true", "success", "ok"}


def _response_ok(status: int, message: str, payload: dict) -> bool:
    """宽松判定接口是否成功：显式失败才算失败，未知 code 交给 msg 和 UI 兜底"""
    if status >= 400:
        return False
    if payload.get("success") is False:
        return False

    code = payload.get("code")
    if code is None:
        return True
    if isinstance(code, bool):
        return code
    normalized = code.strip().lower() if isinstance(code, str) else code
    if normalized in SUCCESS_CODES:
        return True

    msg = str(message or "").strip().lower()
    return bool(msg) and ("成功" in msg or "success" in msg or msg == "ok")


def _save_draft(page, frame) -> None:
    try:
        with page.expect_response(
            lambda response: "dailySubmit/doSave" in response.url, timeout=20000
        ) as response_info:
            if not _click_form_button(frame, "保存", 5000):
                if not _click_form_button(frame, "操作", 3000):
                    raise RuntimeError("未找到“保存”按钮")
                sheet_save = frame.locator(".uni-actionsheet__cell").filter(
                    has_text="保存"
                )
                if not _click_visible(sheet_save, 3000):
                    raise RuntimeError("操作菜单中未找到“保存”")
        response = response_info.value
    except Exception as exc:
        details = ""
        try:
            errors = [
                text.strip()
                for text in frame.locator(".uni-forms-item__error").all_inner_texts()
                if text.strip()
            ]
            if errors:
                details = "；表单提示：" + "；".join(errors)
        except Exception:
            pass
        raise RuntimeError(f"保存草稿失败: {exc}{details}") from exc

    status, message, payload = _response_message(response)
    response_ok = _response_ok(status, message, payload)

    submit_button = frame.locator(".footer-buttons uni-view.button").filter(
        has_text="发起->日报审核"
    )
    button_shown = _wait_until(lambda: _is_visible(submit_button), 20)

    if button_shown:
        # 页面已出现提交入口 = 草稿实际保存成功；code 惯例不认识时只告警不报错
        if not response_ok:
            print(
                f"警告: 保存接口返回未识别的成功标识（HTTP {status}, "
                f"code={payload.get('code')!r}, msg={message}），"
                "但页面已出现“发起->日报审核”，按保存成功处理",
                file=sys.stderr,
            )
        print("已保存草稿" + (f"：{message}" if message else ""))
        return

    if not response_ok:
        raise RuntimeError(f"保存草稿失败: HTTP {status} {message or payload}")
    raise RuntimeError(
        f"保存接口已返回成功（msg={message}），但页面未出现“发起->日报审核”，请检查浏览器"
    )


def _select_reviewer(picker, reviewer: str) -> None:
    def scan() -> tuple[list[str], list[str], list[str]]:
        titles = [
            text.strip()
            for text in picker.locator(".user-item-title").all_inner_texts()
            if text.strip()
        ]
        exact: list[str] = []
        fuzzy: list[str] = []
        for title in titles:
            name = title.split("(", 1)[0].strip()
            if title == reviewer or name == reviewer:
                exact.append(title)
            elif reviewer and reviewer in title:
                fuzzy.append(title)
        return exact, fuzzy, titles

    exact, fuzzy, titles = scan()
    if not exact and not fuzzy:
        search_bar = picker.locator(".je-tree-search-bar .je-search-bar").first
        if _is_visible(search_bar):
            search_bar.click()
            time.sleep(0.5)
            search_input = picker.locator("input.uni-input-input").first
            if _is_visible(search_input):
                search_input.fill(reviewer)
                time.sleep(1.5)
                exact, fuzzy, titles = scan()

    if not exact and not fuzzy:
        sample = "、".join(titles[:8]) if titles else "（列表为空）"
        raise RuntimeError(f"未找到审核人“{reviewer}”，当前可选：{sample}")

    matches = list(dict.fromkeys(exact or fuzzy))
    if len(matches) > 1:
        raise RuntimeError(
            f"审核人“{reviewer}”匹配到多个：" + "、".join(matches[:5])
        )
    title = matches[0]
    person = picker.locator(".je-tree-item").filter(
        has=picker.locator(
            ".user-item-title", has_text=re.compile(rf"^{re.escape(title)}$")
        )
    ).first
    if not _is_visible(person):
        raise RuntimeError(f"未找到审核人“{title}”的可点击节点")
    person.click()
    time.sleep(0.8)

    def selected_count() -> int:
        match = re.search(r"已选数据（(\d+)）", picker.inner_text())
        return int(match.group(1)) if match else 0

    if not _wait_until(lambda: selected_count() > 0, 5):
        raise RuntimeError(f"点击审核人“{title}”后未选中，请检查浏览器")


def _submit_for_review(page, frame, reviewer: str) -> None:
    if not _click_form_button(frame, "发起->日报审核", 5000):
        raise RuntimeError("未找到“发起->日报审核”按钮")

    operation = _wait_until(
        lambda: _first_visible_locator(frame.locator(".je-func-workflow-operation")),
        15,
    )
    if operation is None:
        raise RuntimeError("发起审核弹层未打开")

    add_user = operation.locator(".user-add").first
    if not _is_visible(add_user):
        raise RuntimeError("审核弹层中未找到“选择人员”")
    add_user.click()

    picker = _wait_until(
        lambda: _first_visible_locator(frame.locator(".je-func-workflow-user")), 15
    )
    if picker is None:
        raise RuntimeError("人员选择器未打开")

    try:
        _select_reviewer(picker, reviewer)
        if not _click_visible(
            picker.locator(".footer-buttons uni-view.button").filter(has_text="确定"),
            5000,
        ):
            raise RuntimeError("人员选择器未找到“确定”按钮")
    except Exception:
        _click_visible(
            picker.locator(".footer-buttons uni-view.button").filter(has_text="取消"),
            2000,
        )
        raise

    def reviewer_shown() -> bool:
        try:
            return reviewer in "".join(operation.locator(".user-title").all_inner_texts())
        except Exception:
            return False

    if not _wait_until(reviewer_shown, 10):
        raise RuntimeError("审核人已选择，但弹层中未回显，请检查浏览器")

    final = operation.locator(".footer-buttons uni-view.button").filter(
        has_text="发起->日报审核"
    )
    response = None
    try:
        with page.expect_response(
            lambda response: response.request.method == "POST"
            and ("workflow" in response.url or "dailySubmit" in response.url),
            timeout=15000,
        ) as response_info:
            if not _click_visible(final, 5000):
                raise RuntimeError("审核弹层中未找到“发起->日报审核”按钮")
        response = response_info.value
    except Exception as exc:
        if _wait_until(lambda: not _is_visible(operation), 8):
            print("已提交审核（未捕获到响应，但审核弹层已关闭）。")
            return
        raise RuntimeError(f"提交审核失败或未收到响应: {exc}") from exc

    status, message, payload = _response_message(response)
    response_ok = _response_ok(status, message, payload)

    closed = _wait_until(lambda: not _is_visible(operation), 15)
    if closed:
        # 审核弹层已关闭 = 提交实际成功；code 惯例不认识时只告警不报错
        if not response_ok:
            print(
                f"警告: 提交接口返回未识别的成功标识（HTTP {status}, "
                f"code={payload.get('code')!r}, msg={message}），"
                "但审核弹层已关闭，按提交成功处理",
                file=sys.stderr,
            )
        print("已提交审核" + (f"：{message}" if message else ""))
        return

    if not response_ok:
        raise RuntimeError(f"提交审核失败: HTTP {status} {message or payload}")
    raise RuntimeError(
        f"提交接口已返回成功（msg={message}），但审核弹层未关闭，请检查浏览器"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="复制日报正文并打开网页日报表单，可选自动填写和提交审核"
    )
    parser.add_argument("--date", help="日期 YYYY-MM-DD，默认今天")
    parser.add_argument(
        "--config-dir",
        help="配置目录路径（优先级最高；默认读取环境变量/.env/用户目录）",
    )
    parser.add_argument("--copy-only", action="store_true", help="只复制内容，不打开浏览器")
    parser.add_argument("--no-copy", action="store_true", help="不写入剪贴板")
    parser.add_argument("--print", dest="print_content", action="store_true", help="同时打印正文")
    parser.add_argument("--include-date", action="store_true", help="复制内容包含日期行")
    parser.add_argument(
        "--fill", action="store_true", help="填写项目名称和完成工作，并保存草稿"
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="填写后选择审核人并提交审核（需同时加 --yes）",
    )
    parser.add_argument("--yes", action="store_true", help="确认提交审核")
    parser.add_argument("--project", help="项目名称或项目编码（覆盖 web.project_name）")
    parser.add_argument("--reviewer", help="审核人姓名（覆盖 web.reviewer）")
    parser.add_argument(
        "--allow-date-mismatch",
        action="store_true",
        help="允许表单日期与日报日期不一致",
    )
    args = parser.parse_args()

    config_dir, config_source = resolve_config_dir(args.config_dir)
    print(f"使用配置目录: {config_dir}（来源: {config_source}）")
    try:
        config = load_config(config_dir)
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"错误: 日期格式应为 YYYY-MM-DD，收到 {date_str}", file=sys.stderr)
        return 1
    date = (parsed.year, parsed.month, parsed.day)

    web = config.get("web") or {}
    if not web.get("enabled") and not args.copy_only:
        print(
            "错误: 未启用网页日报配置。请先在 config.json 中添加 web 配置，"
            "并将 web.enabled 设为 true。",
            file=sys.stderr,
        )
        return 1

    fill = args.fill or args.submit
    if args.copy_only and fill:
        print("错误: --copy-only 不能与 --fill/--submit 同时使用", file=sys.stderr)
        return 1
    if args.copy_only and args.no_copy:
        print("错误: --copy-only 与 --no-copy 不能同时使用", file=sys.stderr)
        return 1
    if args.submit and not args.yes:
        print(
            "错误: --submit 会提交审核，请同时加 --yes 确认", file=sys.stderr
        )
        return 1

    project = (args.project or web.get("project_name") or "").strip()
    reviewer = (args.reviewer or web.get("reviewer") or "").strip()
    if fill and not project:
        print(
            "错误: 填写表单需要项目名称，请加 --project 或配置 web.project_name",
            file=sys.stderr,
        )
        return 1
    if args.submit and not reviewer:
        print(
            "错误: 提交审核需要审核人，请加 --reviewer 或配置 web.reviewer",
            file=sys.stderr,
        )
        return 1

    expected_form_date = f"{date[0]}-{date[1]:02d}-{date[2]:02d}"
    include_date = args.include_date or bool(web.get("copy_include_date"))
    try:
        body, target, _ = _load_report_body(
            config["output_file"], date, include_date
        )
    except (KeyError, FileNotFoundError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    clipboard_done = args.no_copy
    if args.no_copy:
        print(f"已跳过剪贴板，正文 {len(body)} 字")
    else:
        try:
            copy_to_clipboard(body)
            clipboard_done = True
            print(
                f"已复制日报正文: {len(body)} 字"
                f"（{'含' if include_date else '不含'}日期行）"
            )
        except RuntimeError as exc:
            if args.copy_only:
                print(f"错误: 写入剪贴板失败: {exc}", file=sys.stderr)
                return 1
            print(
                f"警告: 系统剪贴板写入失败（{exc}），将在浏览器打开后重试",
                file=sys.stderr,
            )
    print(f"来源: {target}")
    if args.print_content:
        print("\n" + body + "\n")
    sys.stdout.flush()

    if args.copy_only:
        return 0

    target_url = str(web.get("url") or "").strip()
    if not target_url:
        print("错误: 未配置 web.url", file=sys.stderr)
        return 1

    login_cfg = web.get("login") or {}
    username = os.environ.get("DAILY_REPORT_WEB_USERNAME") or login_cfg.get("username")
    password = os.environ.get("DAILY_REPORT_WEB_PASSWORD") or login_cfg.get("password")
    if not username or not password:
        print(
            "错误: 未配置网页账号密码。请设置 web.login.username / web.login.password，"
            "或使用环境变量 DAILY_REPORT_WEB_USERNAME / DAILY_REPORT_WEB_PASSWORD。",
            file=sys.stderr,
        )
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "错误: 缺少 playwright 依赖，请使用以下命令运行：\n"
            "  uv run --with playwright python scripts/publish_report.py",
            file=sys.stderr,
        )
        return 1

    try:
        port = _ensure_browser(web, config_dir)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    playwright = sync_playwright().start()
    page = None
    try:
        browser = playwright.chromium.connect_over_cdp(
            f"http://127.0.0.1:{port}"
        )
        if not browser.contexts:
            print("错误: 浏览器没有可用窗口，请关闭专用浏览器后重试", file=sys.stderr)
            return 1

        page = _pick_page(browser.contexts[0], target_url)
        page.bring_to_front()

        if not _auto_login(page, web, target_url, str(username), str(password)):
            saved = _save_debug(page, "login-failed", config_dir)
            for path in saved:
                print(f"调试文件: {path}", file=sys.stderr)
            print(
                "浏览器已保持打开，请手动完成登录并进入日报表单。",
                file=sys.stderr,
            )
            return 2

        if not clipboard_done:
            if _copy_via_browser(page, body):
                clipboard_done = True
                print(f"已通过浏览器复制日报正文: {len(body)} 字")
            else:
                print(
                    f"警告: 剪贴板写入失败，正文仍在来源文件 {target} 中，可手动复制",
                    file=sys.stderr,
                )

        if fill:
            try:
                form = _open_work_report_form(page, web)
                _check_form_date(
                    form, expected_form_date, args.allow_date_mismatch
                )
                _fill_project(form, project)
                _fill_work_content(form, body)
                _save_draft(page, form)
                if args.submit:
                    _submit_for_review(page, form, reviewer)
            except Exception as exc:
                for path in _save_debug(page, "fill-failed", config_dir):
                    print(f"调试文件: {path}", file=sys.stderr)
                print(f"错误: {exc}", file=sys.stderr)
                print("浏览器已保持打开，可手动完成剩余操作。", file=sys.stderr)
                return 3

            page.bring_to_front()
            print(f"已填写项目: {project}")
            print(f"完成工作: {len(body)} 字")
            if args.submit:
                print(f"已提交审核，审核人: {reviewer}")
            else:
                print("已保存草稿。确认无误后可加 --submit --yes 提交审核。")
            print("浏览器保持打开。")
            return 0

        ready_selector = web.get("form_ready_selector")
        if ready_selector:
            try:
                page.wait_for_selector(ready_selector, timeout=15000)
            except Exception:
                print(
                    f"警告: 未等到表单就绪元素 {ready_selector}，页面可能仍在加载",
                    file=sys.stderr,
                )
        else:
            page.wait_for_timeout(1500)

        page.bring_to_front()
        print("已登录并打开日报表单，浏览器保持打开。")
        print(f"访问地址: {target_url}")
        print("请将剪贴板内容粘贴到【完成工作】。本脚本不会填表或提交。")
        return 0
    except Exception as exc:
        print(f"错误: 打开日报表单失败: {exc}", file=sys.stderr)
        if page is not None:
            for path in _save_debug(page, "publish-failed", config_dir):
                print(f"调试文件: {path}", file=sys.stderr)
        return 1
    finally:
        # 只断开 CDP 连接，不调用 browser.close()，浏览器窗口保持打开
        playwright.stop()


if __name__ == "__main__":
    sys.exit(main())
