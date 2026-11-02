#!/usr/bin/env python3
"""Bounded read-only Windows mouse-hit diagnostics for Astur / Zalo overlays.

Collects process executable names, HWND/class/style/rect, cursor coordinates and
WindowFromPoint targets. NEVER captures titles, messages, screenshots, keystrokes,
clipboard content, or mouse clicks. Run in the SAME interactive desktop session
as the popup, then reproduce it while the sampler is active.
"""
import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime
import json
import tempfile
import time
from pathlib import Path

from capture_zalo_popup_episodes import Win32, desktop_dir, is_toast_shape


def points_for_monitor(monitor):
    left, top, right, bottom = monitor
    w, h = right - left, bottom - top
    if w <= 0 or h <= 0:
        return []
    return [
        (left + w * pct // 100, top + min(h - 1, y))
        for y in (60, max(0, h - 180), max(0, h - 40))
        for pct in (20, 50, 80)
    ]


def suspicious_windows(frame):
    results = []
    for obj in frame.values():
        exe = obj.get("exe", "")
        name = exe.lower()
        if (name in ("zalo.exe", "zalopc.exe", "astur.exe")
                or is_toast_shape(obj.get("rect", [0, 0, 0, 0]),
                                  obj.get("monitor", [0, 0, 0, 0]))):
            results.append({
                key: obj.get(key) for key in (
                    "hwnd", "pid", "exe", "class", "owner", "style", "exstyle",
                    "rect", "monitor"
                )
            })
    return results[:80]


def setup_user32(win):
    win.u.GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
    win.u.GetCursorPos.restype = wintypes.BOOL
    win.u.MonitorFromPoint.argtypes = [wintypes.POINT, wintypes.DWORD]
    win.u.MonitorFromPoint.restype = wintypes.HANDLE
    win.u.GetClipCursor.argtypes = [ctypes.POINTER(win.RECT)]
    win.u.GetClipCursor.restype = wintypes.BOOL
    class GUITHREADINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD), ("flags", wintypes.DWORD),
            ("hwndActive", wintypes.HWND), ("hwndFocus", wintypes.HWND),
            ("hwndCapture", wintypes.HWND), ("hwndMenuOwner", wintypes.HWND),
            ("hwndMoveSize", wintypes.HWND), ("hwndCaret", wintypes.HWND),
            ("rcCaret", win.RECT),
        ]
    win.GUITHREADINFO = GUITHREADINFO
    win.u.GetGUIThreadInfo.argtypes = [wintypes.DWORD, ctypes.POINTER(GUITHREADINFO)]
    win.u.GetGUIThreadInfo.restype = wintypes.BOOL
    return win


def cursor_position(win):
    point = wintypes.POINT()
    if not win.u.GetCursorPos(ctypes.byref(point)):
        return None
    return point.x, point.y


def monitor_for_cursor(win, cursor):
    if cursor is None:
        return None
    m = win.u.MonitorFromPoint(wintypes.POINT(*cursor), 2)
    info = win.MONITORINFO()
    info.cbSize = ctypes.sizeof(info)
    if not m or not win.u.GetMonitorInfoW(m, ctypes.byref(info)):
        return None
    r = info.rcMonitor
    return (r.left, r.top, r.right, r.bottom)


def hit(win, frame, x, y):
    hwnd = win.u.WindowFromPoint(wintypes.POINT(x, y))
    root = win.u.GetAncestor(hwnd, 2) if hwnd else None
    rid = int(root or hwnd or 0)
    metadata = frame.get(rid, {})
    if not metadata and rid:
        b = ctypes.create_unicode_buffer(160)
        win.u.GetClassNameW(rid, b, len(b))
        pid = wintypes.DWORD()
        win.u.GetWindowThreadProcessId(rid, ctypes.byref(pid))
        metadata = {"class": b.value, "exe": win.process_name(pid.value)}
    return {
        "at": [x, y], "hit_hwnd": int(hwnd or 0), "root_hwnd": rid,
        "root_exe": metadata.get("exe", ""), "root_class": metadata.get("class", ""),
        "root_rect": metadata.get("rect"),
    }


def capture_state(win, suspects):
    """Read-only UI thread capture owner and system cursor confinement."""
    clipped = win.RECT()
    clip = None
    if win.u.GetClipCursor(ctypes.byref(clipped)):
        clip = [clipped.left, clipped.top, clipped.right, clipped.bottom]
    capture = []
    queried = set()
    for item in suspects:
        if item.get("exe", "").lower() not in ("zalo.exe", "zalopc.exe", "astur.exe"):
            continue
        thread_id = int(win.u.GetWindowThreadProcessId(item["hwnd"], None))
        if not thread_id or thread_id in queried:
            continue
        queried.add(thread_id)
        info = win.GUITHREADINFO()
        info.cbSize = ctypes.sizeof(info)
        if win.u.GetGUIThreadInfo(thread_id, ctypes.byref(info)):
            capture.append({"thread_id": thread_id, "hwnd_capture": int(info.hwndCapture or 0),
                            "hwnd_move_size": int(info.hwndMoveSize or 0)})
    return {"clip_rect": clip, "ui_thread_capture": capture}


def observe(win):
    frame, _ = win.snapshot()
    cursor = cursor_position(win)
    monitor = monitor_for_cursor(win, cursor)
    suspects = suspicious_windows(frame)
    if not monitor:
        return {"cursor": cursor, "monitor": None, "hits": [],
                "suspects": suspects, "capture_state": capture_state(win, suspects)}
    pts = points_for_monitor(monitor)
    if cursor is not None:
        pts = [cursor] + pts
    return {
        "cursor": cursor, "monitor": monitor,
        "hits": [hit(win, frame, x, y) for x, y in pts],
        "suspects": suspects, "capture_state": capture_state(win, suspects),
    }


def run(seconds, interval, output):
    win = setup_user32(Win32())
    output.mkdir(parents=True, exist_ok=True)
    path = output / ("astur_zalo_mouse_%s.jsonl" % datetime.now().strftime("%Y%m%d_%H%M%S"))
    print("READ-ONLY Zalo/Astur mouse probe | %.1f seconds" % seconds, flush=True)
    print("Move your pointer into a blocked area while the popup is visible.", flush=True)
    print("No clicks, texts, titles, screenshots or app changes recorded.", flush=True)
    print("Log: %s" % path, flush=True)
    start = time.monotonic()
    samples = 0
    with path.open("w", encoding="utf-8") as f:
        while time.monotonic() - start < seconds:
            sample = observe(win)
            sample["elapsed_s"] = round(time.monotonic() - start, 2)
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            samples += 1
            time.sleep(interval)
    print("FINISH | %s snapshots | %s" % (samples, path), flush=True)
    return path, samples


def self_test():
    screen = (0, 0, 1920, 1080)
    pts = points_for_monitor(screen)
    assert len(pts) == 9
    assert len(set(pts)) == 9
    assert all(0 <= x < 1920 and 0 <= y < 1080 for x, y in pts)
    assert points_for_monitor((0, 0, 0, 0)) == []
    assert suspicious_windows({
        1: {"exe": "Zalo.exe", "hwnd": 1, "rect": [0, 0, 900, 900],
            "monitor": list(screen)},
        2: {"exe": "Astur.exe", "hwnd": 2, "rect": [0, 0, 900, 900],
            "monitor": list(screen)},
        3: {"exe": "Notepad.exe", "hwnd": 3, "rect": [0, 0, 900, 900],
            "monitor": list(screen)},
    }) == [
        {"hwnd": 1, "pid": None, "exe": "Zalo.exe", "class": None,
         "owner": None, "style": None, "exstyle": None,
         "rect": [0, 0, 900, 900], "monitor": list(screen)},
        {"hwnd": 2, "pid": None, "exe": "Astur.exe", "class": None,
         "owner": None, "style": None, "exstyle": None,
         "rect": [0, 0, 900, 900], "monitor": list(screen)},
    ]
    print("PASS: coordinate sampling, input metadata scope, suspect filtering")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seconds", type=float, default=30.0)
    p.add_argument("--interval", type=float, default=0.25)
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if args.smoke:
        with tempfile.TemporaryDirectory(prefix="astur_mouse_") as root:
            path, n = run(0.5, 0.20, Path(root))
            assert n > 0 and path.exists()
            for line in path.read_text(encoding="utf-8").splitlines():
                record = json.loads(line)
                assert "hits" in record and "suspects" in record
        print("PASS: read-only Win32 smoke")
        return
    if not (5 <= args.seconds <= 90 and 0.1 <= args.interval <= 1):
        p.error("seconds must be 5..90 and interval 0.1..1")
    run(args.seconds, args.interval, args.output or
        desktop_dir() / "Astur_Zalo_Mouse_Diagnostics")


if __name__ == "__main__":
    main()
