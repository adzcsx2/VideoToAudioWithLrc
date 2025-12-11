#!/usr/bin/env python3
"""
快速查看FLAC文件歌词
"""

import sys
import os
import subprocess
import re
from pathlib import Path
from typing import List, Dict

def view_lyrics(flac_file: str) -> None:
    """查看FLAC文件的歌词"""
    flac_path = Path(flac_file)

    cmd = ['ffmpeg', '-i', str(flac_path), '-hide_banner']
    result = subprocess.run(cmd, capture_output=True, text=True,
                          encoding='utf-8', errors='ignore',
                          creationflags=subprocess.CREATE_NO_WINDOW)

    output = result.stderr

    print(f"\n文件: {flac_path.name}")
    print("=" * 50)

    # 使用正则表达式更高效地提取歌词
    lyrics_pattern = re.compile(r'^\s*LYRICS\s*:\s*(.*)$')
    continuation_pattern = re.compile(r'^\s*:\s*(.*)$')

    lyrics_content = []
    in_lyrics = False

    for line in output.split('\n'):
        lyrics_match = lyrics_pattern.match(line)
        if lyrics_match:
            in_lyrics = True
            lyrics = lyrics_match.group(1).strip()
            if lyrics:
                lyrics_content.append(lyrics)
        elif in_lyrics:
            continuation_match = continuation_pattern.match(line)
            if continuation_match:
                lyrics_content.append(continuation_match.group(1).strip())
            elif ':' in line:
                # 遇到新的标签，停止收集
                break

    if lyrics_content:
        print("\n[包含歌词]\n")
        # 合并所有歌词行
        full_lyrics = '\n'.join(lyrics_content)
        print(full_lyrics)

        # 检查时间戳
        if '[00:' in full_lyrics:
            print("\n[包含时间戳歌词]")
        else:
            print("\n[不包含时间戳]")
    else:
        print("\n[无歌词信息]")

    # 显示文件大小
    if flac_path.exists():
        size = flac_path.stat().st_size / (1024 * 1024)
        print(f"\n文件大小: {size:.2f} MB")

# 使用方法
if len(sys.argv) > 1:
    # 查看指定文件
    for flac_file in sys.argv[1:]:
        if flac_file.endswith('.flac') and os.path.exists(flac_file):
            view_lyrics(flac_file)
        else:
            print(f"\n错误: 文件不存在或不是FLAC格式 - {flac_file}")
else:
    # 查看当前目录所有FLAC文件
    current_dir = Path('.')
    flac_files = list(current_dir.glob('*.flac'))

    if not flac_files:
        print("\n当前目录没有FLAC文件")
    else:
        print(f"\n找到 {len(flac_files)} 个FLAC文件:\n")
        for flac_file in sorted(flac_files):
            view_lyrics(flac_file)
            print("\n" + "-" * 50 + "\n")