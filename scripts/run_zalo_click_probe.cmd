@echo off
setlocal
echo =======================================================
echo ASTUR / ZALO READ-ONLY MOUSE BLOCKER DIAGNOSTIC
echo =======================================================
echo This does NOT click, move, close or change windows.
echo Open it in the SAME Windows desktop session as Zalo.
echo Trigger a notification, then point at a blocked area.
echo The test records for 45 seconds and writes a JSONL log
echo to Desktop\Astur_Zalo_Mouse_Diagnostics.
echo.
where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%~dp0capture_zalo_click_blocker.py" --seconds 45
) else (
    python "%~dp0capture_zalo_click_blocker.py" --seconds 45
)
if errorlevel 1 echo Diagnostic did not complete. Check Python installation.
echo.
echo Diagnostic ended. Log path is printed above.
pause
