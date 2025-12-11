@echo off
chcp 65001 > nul
title 视频转FLAC音频工具 - 一键打包

echo ========================================
echo 视频转FLAC音频工具 - 一键打包
echo ========================================
echo.

echo 正在检查Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo 开始打包...
python build_exe.py

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 打包文件位于：dist\视频转FLAC音频工具.exe
echo.

pause