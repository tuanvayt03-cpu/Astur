#!/usr/bin/env python3
"""Read-only Win32 HWND metadata sampler for transient notification diagnosis.

No window titles, message text, screenshots, or secrets are collected. This
does not modify the desktop. Run while reproducing a Zalo/Telegram toast.
"""
import argparse
import ctypes
import json
import os
import time
from ctypes import wintypes

if os.name != "nt":
    raise SystemExit("Windows only")

u32 = ctypes.WinDLL("user32", use_last_error=True)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
WINFUNCTYPE = ctypes.WINFUNCTYPE
LONG_PTR = ctypes.c_ssize_t
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
u32.EnumWindows.argtypes = [WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
u32.EnumWindows.restype = wintypes.BOOL
u32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
u32.GetClassNameW.restype = ctypes.c_int
u32.IsWindowVisible.argtypes = [wintypes.HWND]
u32.IsWindowVisible.restype = wintypes.BOOL
u32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]
u32.GetWindowRect.restype = wintypes.BOOL
u32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
u32.GetWindowLongPtrW.restype = LONG_PTR
u32.GetWindow.argtypes = [wintypes.HWND, wintypes.UINT]
u32.GetWindow.restype = wintypes.HWND
u32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
u32.GetWindowTextLengthW.restype = ctypes.c_int
u32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
u32.GetWindowThreadProcessId.restype = wintypes.DWORD
k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
k32.OpenProcess.restype = wintypes.HANDLE
k32.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
k32.QueryFullProcessImageNameW.restype = wintypes.BOOL
k32.CloseHandle.argtypes = [wintypes.HANDLE]
k32.CloseHandle.restype = wintypes.BOOL

def process_name(pid):
    handle = k32.OpenProcess(0x1000, False, pid)
    if not handle:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(2048)
        size = wintypes.DWORD(len(buf))
        if k32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
            return os.path.basename(buf.value).lower()
    finally:
        k32.CloseHandle(handle)
    return ""

def snapshot():
    found = []
    cb_type = WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    @cb_type
    def each(hwnd, _):
        if not u32.IsWindowVisible(hwnd):
            return True
        rect = RECT()
        if not u32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return True
        width, height = rect.right - rect.left, rect.bottom - rect.top
        if width <= 0 or height <= 0:
            return True
        b = ctypes.create_unicode_buffer(256)
        u32.GetClassNameW(hwnd, b, 256)
        pid = wintypes.DWORD()
        u32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        # No title text, only length to show if it qualifies for Astur adoption.
        owner = u32.GetWindow(hwnd, 4)  # GW_OWNER
        style = int(u32.GetWindowLongPtrW(hwnd, -16)) & 0xFFFFFFFF
        ex = int(u32.GetWindowLongPtrW(hwnd, -20)) & 0xFFFFFFFF
        found.append({
            "hwnd": int(hwnd), "pid": pid.value, "class": b.value,
            "owner": int(owner or 0), "style_hex": f"0x{style:08x}",
            "exstyle_hex": f"0x{ex:08x}",
            "title_length": u32.GetWindowTextLengthW(hwnd),
            "size": [width, height], "position": [rect.left, rect.top],
            "has_toolwindow": bool(ex & 0x80), "has_noactivate": bool(ex & 0x08000000),
        })
        return True
    u32.EnumWindows(each, 0)
    name_cache = {}
    for window in found:
        pid = window["pid"]
        if pid not in name_cache:
            name_cache[pid] = process_name(pid)
        window["exe"] = name_cache[pid]
    return found

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=int, default=0, help="bounded sampling duration, <=60")
    parser.add_argument("--interval", type=float, default=0.25)
    args = parser.parse_args()
    if not (0 <= args.seconds <= 60) or not (0.1 <= args.interval <= 5):
        parser.error("duration or interval outside safe bounds")
    observed = {}
    end = time.monotonic() + args.seconds
    while True:
        for w in snapshot():
            key = w["hwnd"]
            if key not in observed:
                observed[key] = w
        if time.monotonic() >= end:
            break
        time.sleep(args.interval)
    candidates = [w for w in observed.values()
                  if (w["size"][0] < 1000 and w["size"][1] < 550)
                  or any(s in (w["class"] + w["exe"]).lower()
                         for s in ("telegram", "zalo", "snip", "notification", "toast", "screenclipping"))]
    print(json.dumps({
        "note": "Diagnostic only: small size alone does NOT mean a notification.",
        "sampled_windows": len(observed),
        "candidates": sorted(candidates, key=lambda a: (a["exe"], a["class"], a["hwnd"])),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
