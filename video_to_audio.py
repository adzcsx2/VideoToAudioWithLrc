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

# Pre-compile regex pattern for better performance
TIMESTAMP_PATTERN = re.compile(r'\[(\d{2}):(\d{2})(?:\.(\d{2}))?\]')

# Constants
MAX_LYRICS_LENGTH = 2000
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


def parse_lrc_file(lrc_path: Path) -> Tuple[Dict[str, str], str, str]:
    """解析LRC文件，保留时间戳的歌词"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']
    lrc_content = None

    # 尝试不同编码读取
    for encoding in encodings:
        try:
            with open(lrc_path, 'r', encoding=encoding) as f:
                lrc_content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if lrc_content is None:
        return {}, "", ""

    metadata = {}
    lyrics_with_timestamp = []
    pure_lyrics_lines = []

    for line in lrc_content.split('\n'):
        line = line.strip()
        if not line:
            continue

        # 解析元数据
        if line.startswith('[ar:'):
            metadata['ARTIST'] = line[4:-1]
        elif line.startswith('[ti:'):
            metadata['TITLE'] = line[4:-1]
        elif line.startswith('[al:'):
            metadata['ALBUM'] = line[4:-1]
        elif line.startswith('[au:'):
            metadata['COMPOSER'] = line[4:-1]
        elif line.startswith('[offset:'):
            try:
                metadata['OFFSET'] = str(int(line[8:-1]))
            except:
                pass

        # 如果行包含时间戳
        if TIMESTAMP_PATTERN.search(line):
            # 保留整行（包括时间戳）
            lyrics_with_timestamp.append(line)

            # 同时提取纯歌词（去除时间戳）
            pure_lyric = TIMESTAMP_PATTERN.sub('', line).strip()
            if pure_lyric and not pure_lyric.startswith('['):
                pure_lyrics_lines.append(pure_lyric)

    # 带时间戳的歌词（用于FLAC）
    timed_lyrics = '\n'.join(lyrics_with_timestamp)
    # 纯歌词（用于M4A）
    pure_lyrics = '\n'.join(pure_lyrics_lines)

    return metadata, timed_lyrics, pure_lyrics




def embed_lyrics_to_flac(flac_path: Path, lrc_path: Path, output_path: Path) -> bool:
    """嵌入歌词到FLAC（保留时间戳）"""
    try:
        metadata, timed_lyrics, pure_lyrics = parse_lrc_file(lrc_path)

        # 如果没有歌词，直接复制文件
        if not timed_lyrics:
            print("警告: 没有找到有效的歌词内容")
            shutil.copy2(flac_path, output_path)
            return True

        # 限制歌词长度，避免过长导致失败
        original_length = len(timed_lyrics)
        if len(timed_lyrics) > MAX_LYRICS_LENGTH:
            timed_lyrics = timed_lyrics[:MAX_LYRICS_LENGTH] + f"\n...(歌词过长，已截断到{MAX_LYRICS_LENGTH}字符)"
            print(f"注意: 歌词过长({original_length}字符)，已截断到{MAX_LYRICS_LENGTH}字符")

        # 等待一下，确保文件不被锁定
        time.sleep(0.5)

        # 使用最简单直接的方法：创建带歌词的新文件
        # 首先确保输入输出文件不同
        if flac_path.resolve() == output_path.resolve():
            # 如果相同，使用临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.flac')
            temp_file.close()
            actual_output = Path(temp_file.name)
        else:
            actual_output = output_path

        # 构建元数据参数
        metadata_args = []
        for key, value in metadata.items():
            if key and value and len(str(value)) < 100:
                metadata_args.extend(['-metadata', f"{key}={value}"])

        # 使用FFmpeg一次性创建带歌词的文件
        cmd = [
            'ffmpeg', '-i', str(flac_path),
            '-c', 'copy',
            '-metadata', f"LYRICS={timed_lyrics}",
            *metadata_args,
            '-y', str(actual_output)
        ]

        # 执行命令
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              encoding='utf-8',
                              creationflags=subprocess.CREATE_NO_WINDOW)

        if result.returncode == 0:
            print(f"成功嵌入歌词({len(timed_lyrics)}字符)")

            # 如果使用了临时文件，移动到最终位置
            if actual_output != output_path:
                time.sleep(0.2)  # 再次等待确保文件释放
                if output_path.exists():
                    output_path.unlink()
                shutil.move(str(actual_output), str(output_path))

            return True
        else:
            # 打印错误信息
            print(f"FFmpeg错误: {result.stderr[:300]}...")
            return False

    except Exception as e:
        print(f"嵌入FLAC歌词时发生异常: {e}")
        # 如果发生错误，至少确保输出文件存在
        if not output_path.exists() and flac_path.exists():
            try:
                shutil.copy2(flac_path, output_path)
            except:
                pass
        return False


def process_media(input_path: str, output_path: Optional[str] = None, start_time: Optional[float] = None,
                 duration: Optional[float] = None, lrc_path: Optional[str] = None,
                 flac_compression: int = DEFAULT_FLAC_COMPRESSION) -> bool:
    """
    处理媒体文件，转换为FLAC格式
    支持歌词嵌入（保留时间戳）
    """
    input_path = Path(input_path)

    # 生成输出文件名
    if output_path is None:
        suffix = ".flac"
        if lrc_path:
            # 如果输入文件已经包含_with_lyrics，添加_new_lyrics
            if "_with_lyrics" in input_path.stem:
                suffix = f"_new_lyrics{suffix}"
            else:
                suffix = f"_with_lyrics{suffix}"
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

    print("\n正在处理...")

    try:
        # 检查是否只是添加歌词（不进行音频处理）
        just_add_lyrics = (input_path.suffix.lower() == '.flac' and
                          start_time is None and
                          duration is None and
                          lrc_path is not None)

        if just_add_lyrics:
            # 直接复制FLAC文件并添加歌词
            shutil.copy2(input_path, output_path)
            print(f"复制FLAC文件完成")

            # 嵌入歌词
            print("\n正在嵌入歌词...")
            success = embed_lyrics_to_flac(output_path, lrc_path, output_path)

            if success:
                print("歌词嵌入成功!")
                return True
            else:
                print("歌词嵌入失败，但音频文件已生成")
                return False

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
    -c <级别>            FLAC压缩级别 (0-8，默认5)
    -h, --help           显示帮助信息

格式说明:
    FLAC: 无损压缩，音质最佳，支持内嵌歌词（保留时间戳）

歌词支持:
    FLAC格式支持带时间戳的歌词，格式为 [mm:ss.xx]歌词内容
    生成的FLAC文件中的歌词可以被支持的音乐播放器显示为同步歌词

示例:
    # 从MP4提取音频，删除前7秒，转为FLAC并嵌入歌词
    python video_to_audio.py input.mp4 -ss 7 -l 歌词.lrc

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
    python video_to_audio.py video.mp4 -ss 01:00 -t 03:00 -l lyrics.lrc -c 8
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
                           lrc_path, flac_compression)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()