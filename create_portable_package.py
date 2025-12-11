#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建便携版包 - 包含所有必要的文件和依赖
"""

import os
import shutil
import sys
from pathlib import Path
import subprocess
import urllib.request
import zipfile

def create_portable_package():
    """创建便携版程序包"""
    print("=" * 60)
    print("创建便携版程序包")
    print("=" * 60)

    # 创建输出目录
    output_dir = Path("视频转FLAC音频工具_便携版")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    print("\n1. 复制主程序...")
    # 复制必要的Python文件
    files_to_copy = [
        "video_to_audio_gui.py",
        "video_to_audio.py",
        "flac_metadata_utils.py",
        "lrc_time_adjuster.py",
        "view_lyrics.py"
    ]

    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, output_dir)
            print(f"   ✓ {file}")

    # 复制测试文件（可选）
    test_dir = output_dir / "test"
    if Path("test").exists():
        shutil.copytree("test", test_dir)
        print(f"   ✓ test目录")

    print("\n2. 下载FFmpeg...")
    # 下载FFmpeg
    ffmpeg_zip = output_dir / "ffmpeg.zip"
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    try:
        print(f"   正在下载 {ffmpeg_url}...")
        urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
        print(f"   ✓ FFmpeg下载完成")

        # 解压并提取ffmpeg.exe
        temp_dir = output_dir / "ffmpeg_temp"
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 查找ffmpeg.exe
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower() == 'ffmpeg.exe':
                    src = Path(root) / file
                    dst = output_dir / 'ffmpeg.exe'
                    shutil.copy2(src, dst)
                    print(f"   ✓ ffmpeg.exe提取成功")
                    break

        # 清理
        ffmpeg_zip.unlink()
        shutil.rmtree(temp_dir)

    except Exception as e:
        print(f"   ✗ FFmpeg下载失败: {e}")
        print("   请手动下载FFmpeg并放置到程序目录")

    print("\n3. 创建运行脚本...")
    # 创建Windows批处理文件
    run_bat = output_dir / "运行程序.bat"
    with open(run_bat, "w", encoding="utf-8") as f:
        f.write("""@echo off
title 视频转FLAC音频工具
cd /d "%~dp0"

python video_to_audio_gui.py

if errorlevel 1 (
    echo.
    echo [错误] 启动失败
    echo 请确保已安装Python和必要的依赖包
    echo 依赖安装命令：
    echo   pip install Pillow requests
    echo.
)

pause
""")
    print("   ✓ 运行程序.bat")

    # 创建下载FFmpeg的脚本
    download_ffmpeg_bat = output_dir / "下载FFmpeg.bat"
    with open(download_ffmpeg_bat, "w", encoding="utf-8") as f:
        f.write("""@echo off
title 下载FFmpeg
cd /d "%~dp0"

echo 正在下载FFmpeg...
python download_ffmpeg.py

pause
""")
    print("   ✓ 下载FFmpeg.bat")

    print("\n4. 创建说明文档...")
    # 创建README
    readme_path = output_dir / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""视频转FLAC音频工具 - 便携版

功能说明：
1. 将视频/音频文件转换为FLAC格式
2. 支持嵌入LRC歌词文件
3. 支持从元数据文件添加标题、艺术家、专辑等信息
4. 支持添加封面图片（本地或网络）
5. 支持音频裁剪（设置开始时间和持续时间）

使用前准备：
1. 确保系统已安装Python 3.7或更高版本
   下载地址：https://www.python.org/downloads/

2. 安装Python依赖包：
   pip install Pillow requests

运行方法：
- 双击"运行程序.bat"启动GUI界面

文件说明：
- video_to_audio_gui.py - GUI主程序
- video_to_audio.py - 核心转换功能
- flac_metadata_utils.py - 元数据处理模块
- ffmpeg.exe - FFmpeg程序（音频/视频处理）
- test/ - 测试文件目录
- README.txt - 本说明文件

元数据文件格式：
标题(TITLE)：歌曲名称
艺术家(ARTIST)：歌手名
专辑(ALBUM)：专辑名称
日期(DATE)：2024-12-11
流派(GENRE)：流行
封面图片(COVER_IMAGE): /path/to/cover.jpg
封面图片(COVER_IMAGE): https://example.com/image.jpg

注意事项：
1. 首次运行前请确保已安装Python和依赖包
2. 如遇到FFmpeg相关错误，请双击"下载FFmpeg.bat"
3. 程序会自动创建测试用的metadata.txt文件

更多信息请访问项目主页。
""")
    print("   ✓ README.txt")

    print("\n5. 创建安装依赖的脚本...")
    # 安装依赖脚本
    install_deps_bat = output_dir / "安装依赖.bat"
    with open(install_deps_bat, "w", encoding="utf-8") as f:
        f.write("""@echo off
title 安装Python依赖
cd /d "%~dp0"

echo 正在安装Python依赖包...
echo.

echo 安装 Pillow (图像处理)...
pip install Pillow

echo.
echo 安装 requests (网络请求)...
pip install requests

echo.
echo 依赖安装完成！
pause
""")
    print("   ✓ 安装依赖.bat")

    print("\n" + "=" * 60)
    print(f"便携版创建完成！")
    print(f"输出目录：{output_dir.absolute()}")
    print("\n使用说明：")
    print("1. 将整个文件夹复制到目标电脑")
    print("2. 运行'安装依赖.bat'安装Python包")
    print("3. 双击'运行程序.bat'启动程序")
    print("=" * 60)

if __name__ == "__main__":
    create_portable_package()