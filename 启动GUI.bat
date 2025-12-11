@echo off
chcp 65001 > nul
title 视频转FLAC音频工具

echo ========================================
echo 视频转FLAC音频工具
echo ========================================
echo.

echo 检查FFmpeg...
ffmpeg -version > nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到FFmpeg，程序可能无法正常工作
    echo 请运行 download_ffmpeg.py 下载安装FFmpeg
    echo.
)

echo 启动GUI界面...
python video_to_audio_gui.py

if errorlevel 1 (
    echo.
    echo [错误] 启动失败，请检查：
    echo 1. 是否已安装Python
    echo 2. 是否已安装依赖包：pip install Pillow requests
    echo.
)

pause