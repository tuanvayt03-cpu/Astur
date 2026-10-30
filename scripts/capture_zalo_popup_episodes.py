#!/usr/bin/env python3
"""Bounded read-only HWND probe for native Zalo/Telegram-style toast windows.

No message contents, screenshots, window titles or clipboard contents.
The script never changes window position, focus, size, visibility or app state.
"""
import argparse
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime
from ctypes import wintypes

CANDIDATE_WIDTH = (230, 700)
CANDIDATE_HEIGHT = (45, 180)
ENDED_GAP = 0.35
CHANGE_COOLDOWN = 2.0

def is_toast_shape(rect, monitor):
    x, y, right, bottom = rect
    mx, my, mr, mb = monitor
    width, height = right - x, bottom - y
    return (CANDIDATE_WIDTH[0] <= width <= CANDIDATE_WIDTH[1]
            and CANDIDATE_HEIGHT[0] <= height <= CANDIDATE_HEIGHT[1]
            and width >= 2 * height
            and x >= mx - 35 and right <= mr + 35
            and ((my - 35 <= y <= my + 55)
                 or (mb - 55 <= bottom <= mb + 35)))

def episode_transition(previous, current, age, title_length_changed):
    """One occurrence per SHOW episode; a distinct metadata change is tentative."""
    if previous is None:
        return "new-window"
    if age >= CHANGE_COOLDOWN and title_length_changed:
        return "metadata-change"
    return None

def self_test():
    screen = (0, 0, 1920, 1080)
    assert is_toast_shape((115, 0, 465, 80), screen)
    assert is_toast_shape((400, 1000, 800, 1080), screen)
    assert not is_toast_shape((0, 0, 1920, 1080), screen)
    assert not is_toast_shape((0, 0, 640, 480), screen)
    assert not is_toast_shape((10, 250, 360, 330), screen)
    assert is_toast_shape((-1800, -10, -1450, 70), (-1920, 0, 0, 1080))
    assert episode_transition(None, {}, 0, False) == "new-window"
    assert episode_transition({}, {}, 1, False) is None
    assert episode_transition({}, {}, 3, True) == "metadata-change"
    print("PASS: 9 independent toast detection and episode assertions")

def desktop_dir():
    # Resolve the Windows Desktop known folder (including redirected desktops).
    buf = ctypes.create_unicode_buffer(260)
    if ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, buf) == 0:
        p = Path(buf.value)
        if p.is_dir():
            return p
    return Path.home() / "Desktop"

class Win32:
    def __init__(self):
        self.u = ctypes.WinDLL("user32", use_last_error=True)
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        self.enum_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        self.cache = {}
        class RECT(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                        ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
        class MONITORINFO(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", RECT),
                        ("rcWork", RECT), ("dwFlags", wintypes.DWORD)]
        self.RECT, self.MONITORINFO = RECT, MONITORINFO
        self.u.EnumWindows.argtypes = [self.enum_type, wintypes.LPARAM]
        self.u.EnumWindows.restype = wintypes.BOOL
        self.u.IsWindowVisible.argtypes = [wintypes.HWND]
        self.u.IsWindowVisible.restype = wintypes.BOOL
        self.u.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]
        self.u.GetWindowRect.restype = wintypes.BOOL
        self.u.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
        self.u.GetWindowLongPtrW.restype = ctypes.c_ssize_t
        self.u.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        self.u.GetClassNameW.restype = ctypes.c_int
        self.u.GetWindowTextLengthW.argtypes = [wintypes.HWND]
        self.u.GetWindowTextLengthW.restype = ctypes.c_int
        self.u.GetWindow.argtypes = [wintypes.HWND, wintypes.UINT]
        self.u.GetWindow.restype = wintypes.HWND
        self.u.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        self.u.GetWindowThreadProcessId.restype = wintypes.DWORD
        self.u.GetForegroundWindow.restype = wintypes.HWND
        self.u.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
        self.u.MonitorFromWindow.restype = wintypes.HANDLE
        self.u.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MONITORINFO)]
        self.u.GetMonitorInfoW.restype = wintypes.BOOL
        self.k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.k.OpenProcess.restype = wintypes.HANDLE
        self.k.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        self.k.QueryFullProcessImageNameW.restype = wintypes.BOOL
        self.k.CloseHandle.argtypes = [wintypes.HANDLE]

    def process_name(self, pid):
        if pid in self.cache:
            return self.cache[pid]
        handle = self.k.OpenProcess(0x1000, False, pid)
        name = ""
        if handle:
            try:
                b = ctypes.create_unicode_buffer(2048)
                length = wintypes.DWORD(len(b))
                if self.k.QueryFullProcessImageNameW(handle, 0, b, ctypes.byref(length)):
                    name = os.path.basename(b.value).lower()
            finally:
                self.k.CloseHandle(handle)
        self.cache[pid] = name
        return name

    def snapshot(self):
        out = {}
        @self.enum_type
        def each(hwnd, _):
            if not self.u.IsWindowVisible(hwnd):
                return True
            rc = self.RECT()
            if not self.u.GetWindowRect(hwnd, ctypes.byref(rc)):
                return True
            rect = [rc.left, rc.top, rc.right, rc.bottom]
            if rect[2] <= rect[0] or rect[3] <= rect[1]:
                return True
            pid = wintypes.DWORD()
            self.u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            monitor_handle = self.u.MonitorFromWindow(hwnd, 2)
            mi = self.MONITORINFO()
            mi.cbSize = ctypes.sizeof(mi)
            if not monitor_handle or not self.u.GetMonitorInfoW(monitor_handle, ctypes.byref(mi)):
                return True
            mon = mi.rcMonitor
            monitor = [mon.left, mon.top, mon.right, mon.bottom]
            cls = ctypes.create_unicode_buffer(160)
            self.u.GetClassNameW(hwnd, cls, len(cls))
            raw_owner = self.u.GetWindow(hwnd, 4)
            h = int(hwnd)
            out[h] = {
                "hwnd": h, "pid": pid.value, "exe": self.process_name(pid.value),
                "class": cls.value, "owner": int(raw_owner or 0),
                "style": f"0x{int(self.u.GetWindowLongPtrW(hwnd, -16)) & 0xffffffff:08x}",
                "exstyle": f"0x{int(self.u.GetWindowLongPtrW(hwnd, -20)) & 0xffffffff:08x}",
                "title_length_only": self.u.GetWindowTextLengthW(hwnd),
                "rect": rect, "monitor": monitor,
                "toast_shape": is_toast_shape(rect, monitor),
            }
            return True
        self.u.EnumWindows(each, 0)
        fg = int(self.u.GetForegroundWindow() or 0)
        return out, fg

def app_layout(frame):
    # Lightweight geometry comparison, excluding tiny popups, hidden/offscreen apps.
    return {str(k): {"exe": v["exe"], "class": v["class"], "rect": v["rect"]}
            for k, v in frame.items()
            if not v["toast_shape"]
            and v["rect"][0] > -10000 and v["rect"][1] > -10000
            and v["rect"][2] - v["rect"][0] >= 250
            and v["rect"][3] - v["rect"][1] >= 180
            and not v["class"].lower().startswith(("progman", "workerw", "shell_traywnd"))}

def changes(before, after):
    diff = []
    for key in before.keys() & after.keys():
        a, b = before[key]["rect"], after[key]["rect"]
        if any(abs(x - y) > 5 for x, y in zip(a, b)):
            diff.append({"hwnd": int(key), "exe": after[key]["exe"],
                         "before": a, "after": b})
    return diff[:30]

def notify_finish(summary):
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except Exception:
        pass
    # Transient tray balloon, launched ONLY after capture has stopped.
    if os.name != "nt":
        return
    msg = "Astur Zalo: FINISH - %s/%s popup, log saved on Desktop" % (
        summary["detected"], summary["target"])
    script = (
        "Add-Type -AssemblyName System.Windows.Forms;"
        "$n=New-Object System.Windows.Forms.NotifyIcon;"
        "$n.Icon=[System.Drawing.SystemIcons]::Information;"
        "$n.Visible=$true;"
        "$n.BalloonTipTitle='Astur Zalo - FINISH';"
        "$n.BalloonTipText='" + msg + "';"
        "$n.ShowBalloonTip(5000);"
        "Start-Sleep -Seconds 6;"
        "$n.Dispose()"
    )
    try:
        subprocess.Popen(["powershell.exe", "-NoProfile", "-WindowStyle", "Hidden",
                          "-Command", script],
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def run(args):
    if os.name != "nt":
        raise RuntimeError("Windows only")
    outdir = Path(args.output) if args.output else desktop_dir() / "Astur_Zalo_Popup_Diagnostics"
    outdir.mkdir(parents=True, exist_ok=True)
    tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = outdir / ("zalo_popup_%s.jsonl" % tag)
    summary_path = outdir / ("zalo_popup_%s_summary.json" % tag)
    win = Win32()
    previous, fg_previous = win.snapshot()
    previous_ids = {h for h, v in previous.items() if v["toast_shape"]}
    last_seen = {h: time.monotonic() for h in previous_ids}
    episode_at = {}
    counted = 0
    pending = []
    started = time.monotonic()
    until = started + args.minutes * 60
    stats = {"sample_cycles": 0, "candidates_seen": 0}
    print("ASTUR ZALO PROBE ACTIVE | target=%d | maximum=%.1f minutes" %
          (args.target, args.minutes), flush=True)
    print("No texts, screenshots, clipboard or window titles captured.", flush=True)
    print("Log: %s" % log_path, flush=True)
    reason = "TIME_LIMIT"
    with log_path.open("w", encoding="utf-8", buffering=1) as out:
        try:
            while time.monotonic() < until:
                frame, fg = win.snapshot()
                stats["sample_cycles"] += 1
                now = time.monotonic()
                current = {h: v for h, v in frame.items() if v["toast_shape"]}
                stats["candidates_seen"] = max(stats["candidates_seen"], len(current))
                for h, info in current.items():
                    was = previous.get(h)
                    reappeared = (h not in previous_ids
                                  and now - last_seen.get(h, -1000) >= ENDED_GAP)
                    metadata_changed = (was is not None
                                        and info["title_length_only"] != was["title_length_only"])
                    kind = episode_transition(None if reappeared else was,
                                              info, now - episode_at.get(h, -1000),
                                              metadata_changed)
                    if h in previous_ids and h not in episode_at:
                        # A pre-existing toast at startup is not a new episode.
                        kind = None
                    if kind:
                        counted += 1
                        episode_at[h] = now
                        record = {
                            "event": "CANDIDATE", "number": counted,
                            "event_kind": kind, "confidence": (
                                "shape-only; unconfirmed Zalo" if kind == "new-window"
                                else "tentative metadata-change; unconfirmed Zalo"),
                            "time_local": datetime.now().astimezone().isoformat(),
                            "window": info,
                            "foreground_hwnd": fg,
                            "foreground_exe": frame.get(fg, {}).get("exe", ""),
                            "layout_before": app_layout(previous),
                            "layout_during": app_layout(frame),
                            "geometry_changes_immediate": changes(app_layout(previous), app_layout(frame)),
                        }
                        out.write(json.dumps(record, ensure_ascii=False) + "\n")
                        pending.append((now + 1.2, record["number"], app_layout(previous)))
                        print("Detected candidate %d/%d | %s | exe=%s class=%s" %
                              (counted, args.target, kind, info["exe"], info["class"]), flush=True)
                    last_seen[h] = now
                for due, number, baseline in pending[:]:
                    if now >= due:
                        out.write(json.dumps({
                            "event": "AFTER_1.2S", "number": number,
                            "time_local": datetime.now().astimezone().isoformat(),
                            "foreground_hwnd": fg,
                            "foreground_exe": frame.get(fg, {}).get("exe", ""),
                            "layout_after": app_layout(frame),
                            "geometry_changes": changes(baseline, app_layout(frame)),
                        }, ensure_ascii=False) + "\n")
                        pending.remove((due, number, baseline))
                previous, fg_previous = frame, fg
                previous_ids = set(current)
                if counted >= args.target:
                    reason = "TARGET_REACHED"
                    # Record after-change for final candidate without waiting indefinitely.
                    ending = time.monotonic() + 1.3
                    while pending and time.monotonic() < ending:
                        time.sleep(0.1)
                        f, fg = win.snapshot()
                        for due, number, baseline in pending[:]:
                            if time.monotonic() >= due:
                                out.write(json.dumps({
                                    "event": "AFTER_1.2S", "number": number,
                                    "layout_after": app_layout(f),
                                    "geometry_changes": changes(baseline, app_layout(f)),
                                }, ensure_ascii=False) + "\n")
                                pending.remove((due, number, baseline))
                    break
                time.sleep(args.interval)
        except KeyboardInterrupt:
            reason = "MANUAL_STOP"
        except Exception as err:
            reason = "ERROR"
            out.write(json.dumps({"event": "ERROR", "type": type(err).__name__,
                                  "detail": str(err)[:200]}) + "\n")
        summary = {
            "status": "FINISH", "reason": reason,
            "detected": counted, "target": args.target,
            "duration_seconds": round(time.monotonic() - started, 2),
            "capture": "Win32 HWND metadata only; candidates are shape-based, not proven Zalo",
            "limitations": ("Native top-level HWND changes only; re-used renderer HWND "
                            "without metadata changes or in-page/browser UI will not count."),
            "raw_log": str(log_path), "stats": stats,
        }
        out.write(json.dumps({"event": "FINISH", **summary}, ensure_ascii=False) + "\n")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FINISH | reason=%s | %d/%d | %s" %
          (reason, counted, args.target, summary_path), flush=True)
    if not args.no_notify:
        notify_finish(summary)
    return 0 if reason != "ERROR" else 1

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", type=int, default=3)
    p.add_argument("--minutes", type=float, default=30.0)
    p.add_argument("--interval", type=float, default=0.10)
    p.add_argument("--output", type=str, default="")
    p.add_argument("--no-notify", action="store_true")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--smoke", action="store_true",
                   help="3-second native Win32/JSON smoke test in disposable temp folder")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.smoke:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="astur_zalo_probe_") as root:
            args.target, args.minutes, args.interval = 3, 0.05, 0.1
            args.output, args.no_notify = root, True
            code = run(args)
            logs = list(Path(root).glob("*_summary.json"))
            assert code == 0 and len(logs) == 1
            result = json.loads(logs[0].read_text(encoding="utf-8"))
            assert result["status"] == "FINISH" and result["reason"] == "TIME_LIMIT"
            assert result["stats"]["sample_cycles"] > 0
            assert Path(result["raw_log"]).exists()
        print("PASS: Win32 live read-only scan and disposable JSON logs")
        return 0
    if not (1 <= args.target <= 5 and 0.05 <= args.minutes <= 60
            and 0.08 <= args.interval <= 1.0):
        p.error("target=1..5, minutes=0.05..60, interval=0.08..1.0")
    return run(args)

if __name__ == "__main__":
    sys.exit(main())
