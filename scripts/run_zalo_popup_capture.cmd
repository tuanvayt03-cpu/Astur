@echo off
setlocal
title Astur - Thu thap popup Zalo (3 lan)
cd /d "%~dp0.."
echo.
echo ===========================================
echo  ASTUR ZALO POPUP CAPTURE - READ ONLY
echo  3 popups hoac toi da 30 phut
echo  Khong doc noi dung tin nhan, khong doi UI.
echo ===========================================
echo.
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3 scripts\capture_zalo_popup_episodes.py --target 3 --minutes 30 --interval 0.10
) else (
    python scripts\capture_zalo_popup_episodes.py --target 3 --minutes 30 --interval 0.10
)
set "CODE=%ERRORLEVEL%"
if not "%CODE%"=="0" (
    echo.
    echo [ERROR] Code=%CODE% - kiem tra Python/terminal.
    echo Neu loi, CMD se dung de anh xem thong bao.
    pause
)
endlocal
exit /b %CODE%
