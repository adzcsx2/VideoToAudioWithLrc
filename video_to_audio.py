#!/usr/bin/env python3
"""
视频转音频工具
支持：视频转FLAC格式转换及LRC歌词嵌入（保留时间戳）
"""

import sys
import os
import subprocess
import re
import tempfile
import time
import shutil
from pathlib import Path
from typing import Optional, Dict, Tuple

# 导入元数据处理模块
from flac_metadata_utils import (
    embed_lyrics_to_flac,
    write_metadata_to_flac,
    write_metadata_from_file,
    parse_metadata_file
)

# Constants
DEFAULT_FLAC_COMPRESSION = 5


def check_ffmpeg():
    """检查FFmpeg是否安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True,
                              text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW)
        return result.returncode == 0
    except FileNotFoundError:
        return False




def parse_time(time_str):
    """解析时间字符串"""
    try:
        return float(time_str)
    except ValueError:
        pass

    pattern = r'^(?:(\d+):)?(?:(\d+):)?(\d+)(?:\.(\d+))?$'
    match = re.match(pattern, time_str.strip())

    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3))
        milliseconds = int(match.group(4) if match.group(4) else 0)

        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return total_seconds

    return None


def format_time(seconds):
    """格式化时间显示"""
    hours = int(seconds // 3600)
    seconds = seconds % 3600
    minutes = int(seconds // 60)
    seconds = seconds % 60
    secs = int(seconds)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"








def process_media(input_path: str, output_path: Optional[str] = None, start_time: Optional[float] = None,
                 duration: Optional[float] = None, lrc_path: Optional[str] = None,
                 flac_compression: int = DEFAULT_FLAC_COMPRESSION, metadata_file: Optional[str] = None) -> bool:
    """
    处理媒体文件，转换为FLAC格式
    支持歌词嵌入（保留时间戳）
    支持元数据文件添加元数据（包括封面图片）
    """
    input_path = Path(input_path)

    # 生成输出文件名
    if output_path is None:
        suffix = ".flac"
        if lrc_path or metadata_file:
            # 如果输入文件已经包含_with_metadata，添加_new_metadata
            if "_with_metadata" in input_path.stem:
                suffix = f"_new_metadata{suffix}"
            else:
                suffix = f"_with_metadata{suffix}"
        output_path = input_path.parent / f"{input_path.stem}_trimmed{suffix}"
    else:
        output_path = Path(output_path)
        if not output_path.suffix.lower().endswith('flac'):
            output_path = output_path.with_suffix('.flac')

    # 检查文件
    if not input_path.exists():
        print(f"错误: 文件 '{input_path}' 不存在")
        return False

    if lrc_path:
        lrc_path = Path(lrc_path)
        if not lrc_path.exists():
            print(f"错误: LRC文件 '{lrc_path}' 不存在")
            return False

    if metadata_file:
        metadata_file = Path(metadata_file)
        if not metadata_file.exists():
            print(f"错误: 元数据文件 '{metadata_file}' 不存在")
            return False

    # 显示信息
    print(f"\n输入文件: {input_path}")
    print(f"输出文件: {output_path}")
    if start_time is not None:
        print(f"开始时间: {format_time(start_time)}")
    if duration is not None:
        print(f"持续时间: {format_time(duration)}")
    print(f"输出格式: FLAC")
    if lrc_path:
        print(f"歌词文件: {lrc_path}")
    if metadata_file:
        print(f"元数据文件: {metadata_file}")

    print("\n正在处理...")

    try:
        # 检查是否只是添加歌词/元数据（不进行音频处理）
        just_add_metadata = (input_path.suffix.lower() == '.flac' and
                           start_time is None and
                           duration is None and
                           (lrc_path is not None or metadata_file is not None))

        if just_add_metadata:
            # 直接复制FLAC文件
            shutil.copy2(input_path, output_path)
            print(f"复制FLAC文件完成")

            # 嵌入歌词
            if lrc_path:
                print("\n正在嵌入歌词...")
                success = embed_lyrics_to_flac(output_path, lrc_path, output_path)

                if success:
                    print("歌词嵌入成功!")
                else:
                    print("歌词嵌入失败，但音频文件已生成")

            # 添加元数据
            if metadata_file:
                if lrc_path:
                    print("\n正在添加元数据...")
                else:
                    print("\n正在添加元数据...")

                # 创建临时文件名来避免原地编辑
                temp_metadata_output = output_path.with_name(f"{output_path.stem}_temp_metadata{output_path.suffix}")

                success = write_metadata_from_file(output_path, metadata_file, temp_metadata_output)

                if success:
                    # 成功后替换原文件
                    time.sleep(0.2)  # 等待文件释放
                    if output_path.exists():
                        output_path.unlink()
                    shutil.move(str(temp_metadata_output), str(output_path))
                    print("元数据添加成功!")
                else:
                    print("元数据添加失败，但音频文件已生成")
                    # 清理临时文件
                    if temp_metadata_output.exists():
                        temp_metadata_output.unlink()

            return True

        # 需要进行音频处理的情况
        # 构建FFmpeg命令
        cmd = ['ffmpeg', '-i', str(input_path)]

        if start_time is not None:
            cmd.extend(['-ss', str(start_time)])
        if duration is not None:
            cmd.extend(['-t', str(duration)])

        # FLAC格式编码
        cmd.extend([
            '-vn', '-acodec', 'flac',
            '-compression_level', str(flac_compression),
            '-ar', '44100', '-ac', '2', '-sample_fmt', 's16',
            '-avoid_negative_ts', '1', '-y', str(output_path)
        ])

        result = subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW)

        if result.returncode == 0:
            print("处理成功!")

            output_size = output_path.stat().st_size / (1024 * 1024)
            print(f"文件大小: {output_size:.2f} MB")

            # 嵌入歌词
            if lrc_path:
                print("\n正在嵌入歌词...")
                # 等待FFmpeg完全释放文件
                time.sleep(1.0)

                # 直接使用生成的文件作为输出，避免额外的复制
                success = embed_lyrics_to_flac(output_path, lrc_path, output_path)

                if success:
                    print("歌词嵌入成功!")
                else:
                    print("歌词嵌入失败，但音频文件已生成")

            # 添加元数据
            if metadata_file:
                if lrc_path:
                    print("\n正在添加元数据...")
                else:
                    print("\n正在添加元数据...")

                # 等待前面的处理完成
                time.sleep(0.5)

                # 创建临时文件名来避免原地编辑
                temp_metadata_output = output_path.with_name(f"{output_path.stem}_temp_metadata{output_path.suffix}")

                success = write_metadata_from_file(output_path, metadata_file, temp_metadata_output)

                if success:
                    # 成功后替换原文件
                    import shutil
                    time.sleep(0.2)  # 等待文件释放
                    if output_path.exists():
                        output_path.unlink()
                    shutil.move(str(temp_metadata_output), str(output_path))
                    print("元数据添加成功!")
                else:
                    print("元数据添加失败，但音频文件已生成")
                    # 清理临时文件
                    if temp_metadata_output.exists():
                        temp_metadata_output.unlink()

            return True
        else:
            print(f"处理失败，返回码: {result.returncode}")
            return False

    except Exception as e:
        print(f"错误: {e}")
        return False


def print_help():
    """打印帮助信息"""
    print("""
视频转音频转换工具

========================================
使用说明（无参数时显示）
========================================

你需要提供一个输入文件。基本用法格式：

    python video_to_audio.py <输入文件.mp4> [选项]

常用命令示例：

1. 从MP4提取音频，删除前7秒，转为FLAC并嵌入歌词：
   python video_to_audio.py input.mp4 -ss 7 -l 歌词.lrc

2. 从MP4提取音频，删除前30秒，转为FLAC并嵌入歌词：
   python video_to_audio.py input.mp4 -ss 00:30 -l 歌词.lrc

3. 从MP4提取音频（不删除前部）：
   python video_to_audio.py input.mp4

4. 从第30秒开始转换，并嵌入歌词：
   python video_to_audio.py video.mp4 -ss 30 -l 歌词.lrc

========================================
工具清单
========================================

1. lrc_time_adjuster.py - LRC歌词时间调整工具
   # 将歌词往前移动7秒
   python lrc_time_adjuster.py song.lrc -7

2. video_to_audio.py - 视频转FLAC格式转换工具
   专门处理视频转FLAC格式转换和歌词嵌入

========================================
常见问题
========================================

1. 需要安装FFmpeg：https://ffmpeg.org/download.html
2. FLAC歌词无需额外软件，直接使用FFmpeg嵌入

========================================
详细参数说明
========================================

用法:
    python video_to_audio.py <输入文件> [选项]

基本选项:
    -ss <时间>           从指定时间开始裁剪
    -t <时长>            裁剪指定时长
    -o <输出文件>        指定输出文件路径
    -l <LRC文件>         嵌入LRC歌词文件（保留时间戳）
    -metadata <文件>    从元数据文件添加元数据（标题、艺术家、封面等）
    -c <级别>            FLAC压缩级别 (0-8，默认5)
    -h, --help           显示帮助信息

格式说明:
    FLAC: 无损压缩，音质最佳，支持内嵌歌词（保留时间戳）

歌词支持:
    FLAC格式支持带时间戳的歌词，格式为 [mm:ss.xx]歌词内容
    生成的FLAC文件中的歌词可以被支持的音乐播放器显示为同步歌词

元数据支持:
    支持从元数据文件读取并添加各种元数据，包括：
    - 基本信息：标题、艺术家、专辑、日期、流派等
    - 封面图片：支持本地路径、网络URL、Base64编码
    - 支持B站特殊格式的图片URL

    元数据文件格式：
    标题(TITLE)：歌曲名称
    艺术家(ARTIST)：歌手名
    专辑(ALBUM)：专辑名
    封面图片(COVER_IMAGE): /path/to/image.jpg

示例:
    # 从MP4提取音频，删除前7秒，转为FLAC并嵌入歌词
    python video_to_audio.py input.mp4 -ss 7 -l 歌词.lrc

    # 从MP4提取音频，添加元数据（包括封面）
    python video_to_audio.py input.mp4 -metadata metadata.txt

    # 从MP4提取音频，同时嵌入歌词和添加元数据
    python video_to_audio.py input.mp4 -l lyrics.lrc -metadata metadata.txt

    # 从MP4提取音频，删除前30秒，转为FLAC并嵌入歌词
    python video_to_audio.py input.mp4 -ss 00:30 -l 歌词.lrc

    # 从MP4提取音频（不删除前部）
    python video_to_audio.py input.mp4

    # 从第30秒开始转换
    python video_to_audio.py video.mp4 -ss 30

    # FLAC最高压缩级别
    python video_to_audio.py audio.wav -c 8

    # 指定输出文件
    python video_to_audio.py audio.wav -o output.flac -l lyrics.lrc

    # 所有功能组合
    python video_to_audio.py video.mp4 -ss 01:00 -t 03:00 -l lyrics.lrc -metadata metadata.txt -c 8
    """)


def main():
    if not check_ffmpeg():
        print("错误: 未找到FFmpeg")
        print("下载地址: https://ffmpeg.org/download.html")
        sys.exit(1)

    args = sys.argv[1:]

    if '-h' in args or '--help' in args or len(args) == 0:
        print_help()
        sys.exit(0)

    input_file = args[0]

    # 默认参数
    output_path = None
    start_time = None
    duration = None
    lrc_path = None
    metadata_file = None
    flac_compression = DEFAULT_FLAC_COMPRESSION

    # 解析参数
    i = 1
    while i < len(args):
        if args[i] == '-ss' and i + 1 < len(args):
            start_time = parse_time(args[i + 1])
            if start_time is None:
                print(f"错误: 无法解析时间 '{args[i + 1]}'")
                sys.exit(1)
            i += 2
        elif args[i] == '-t' and i + 1 < len(args):
            duration = parse_time(args[i + 1])
            if duration is None:
                print(f"错误: 无法解析时长 '{args[i + 1]}'")
                sys.exit(1)
            i += 2
        elif args[i] == '-o' and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif args[i] == '-l' and i + 1 < len(args):
            lrc_path = args[i + 1]
            i += 2
        elif args[i] == '-metadata' and i + 1 < len(args):
            metadata_file = args[i + 1]
            i += 2
        elif args[i] == '-c' and i + 1 < len(args):
            try:
                flac_compression = int(args[i + 1])
                if flac_compression < 0 or flac_compression > 8:
                    raise ValueError
            except ValueError:
                print("错误: FLAC压缩级别必须是0-8")
                sys.exit(1)
            i += 2
        else:
            print(f"警告: 未知选项 {args[i]}")
            i += 1

    # 处理文件
    success = process_media(input_file, output_path, start_time, duration,
                           lrc_path, flac_compression, metadata_file)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()