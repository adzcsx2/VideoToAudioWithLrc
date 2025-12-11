#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 使用PyInstaller将GUI程序打包成exe
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller安装成功！")
        return True
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败，请手动安装: pip install pyinstaller")
        return False

def create_icon():
    """创建简单的图标文件（可选）"""
    # 如果有icon.png，可以转换为icon.ico
    # 这里只是占位，实际使用时需要提供图标文件
    pass

def build_exe():
    """构建exe文件"""
    print("开始构建exe文件...")

    # 构建命令
    cmd = [
        "pyinstaller",
        "--name=视频转FLAC音频工具",
        "--onefile",  # 打包成单个exe
        "--windowed",  # 不显示控制台窗口
        "--clean",  # 清理临时文件
        "--noconfirm",  # 覆盖输出目录不询问
        # 添加数据文件
        "--add-data=*.py;.",  # 包含所有py文件
        # 隐藏导入
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        # 排除不需要的模块（减小文件大小）
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        # 图标（如果有）
        # "--icon=icon.ico",
        "video_to_audio_gui.py"
    ]

    # 执行构建
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("构建成功！")
        print(result.stdout)

        # 输出文件路径
        exe_path = Path("dist/视频转FLAC音频工具.exe")
        if exe_path.exists():
            print(f"\nexe文件已生成: {exe_path.absolute()}")
            print(f"文件大小: {exe_path.stat().st_size / (1024*1024):.2f} MB")

            # 创建说明文件
            readme_path = Path("dist/使用说明.txt")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("""视频转FLAC音频工具 - 使用说明

功能特点：
1. 将视频/音频文件转换为FLAC格式
2. 支持嵌入LRC歌词文件
3. 支持从元数据文件添加标题、艺术家、专辑等信息
4. 支持添加封面图片（本地或网络）
5. 支持音频裁剪（设置开始时间和持续时间）

使用方法：
1. 点击"浏览..."选择要转换的视频或音频文件
2. 可选择LRC歌词文件（可选）
3. 可选择元数据文件（可选）
4. 设置输出文件路径（可选，默认会自动生成）
5. 设置转换参数：
   - 开始时间：裁剪开始位置（如 30 或 01:30）
   - 持续时间：裁剪时长（如 60 或 02:00）
   - FLAC压缩级别：0-8（5为默认值，越大压缩率越高但速度越慢）
6. 点击"执行转换"开始处理

元数据文件格式示例：
标题(TITLE)：歌曲名称
艺术家(ARTIST)：歌手名
专辑(ALBUM)：专辑名称
日期(DATE)：2024-12-11
流派(GENRE)：流行
封面图片(COVER_IMAGE): /path/to/cover.jpg
封面图片(COVER_IMAGE): https://example.com/image.jpg
封面图片(COVER_IMAGE): data:image/jpeg;base64,/9j/4AAQ...

注意事项：
1. 需要系统已安装FFmpeg程序
2. 建议将ffmpeg.exe放在与exe文件同一目录下
3. 转换大文件时请耐心等待
4. 输出文件为FLAC格式，无损压缩

FFmpeg下载地址：https://ffmpeg.org/download.html
""")
            print(f"\n使用说明已保存到: {readme_path.absolute()}")

        return True

    except subprocess.CalledProcessError as e:
        print("构建失败！")
        print(e.stderr)
        return False

def main():
    print("=" * 60)
    print("视频转FLAC音频工具 - 打包脚本")
    print("=" * 60)

    # 检查当前目录
    if not Path("video_to_audio_gui.py").exists():
        print("错误: 未找到video_to_audio_gui.py文件")
        print("请在项目根目录运行此脚本")
        return

    # 检查PyInstaller
    if not check_pyinstaller():
        print("未检测到PyInstaller")
        if not install_pyinstaller():
            return

    # 清理之前的构建
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            print(f"清理 {dir_name} 目录...")
            shutil.rmtree(dir_name)

    # 构建exe
    if build_exe():
        print("\n打包完成！")
        print("exe文件位于 dist 目录中")
        print("\n提示：")
        print("1. 请确保目标电脑已安装FFmpeg")
        print("2. 可以将ffmpeg.exe与打包的exe放在同一目录下")
    else:
        print("\n打包失败，请检查错误信息")

if __name__ == "__main__":
    main()