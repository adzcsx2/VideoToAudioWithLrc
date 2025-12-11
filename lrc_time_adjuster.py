#!/usr/bin/env python3
"""
LRC歌词时间调整工具
用于将LRC文件的歌词整体往前或往后移动指定秒数
"""

import sys
import re
import os
from pathlib import Path
from typing import List, Tuple

# Pre-compile regex pattern for better performance
TIMESTAMP_PATTERN = re.compile(r'\[(\d{2}):(\d{2})(?:\.(\d{2}))?\]')


def parse_lrc_line(line: str) -> Tuple[str, List[float]]:
    """解析LRC行，提取时间标签和歌词"""
    matches = TIMESTAMP_PATTERN.findall(line)

    if not matches:
        return line, []

    # 提取所有时间标签
    time_tags = []
    for match in matches:
        minutes = int(match[0])
        seconds = int(match[1])
        centiseconds = int(match[2]) if match[2] else 0
        total_seconds = minutes * 60 + seconds + centiseconds / 100
        time_tags.append(total_seconds)

    # 提取歌词部分（去掉所有时间标签）
    lyrics = TIMESTAMP_PATTERN.sub('', line).strip()

    return lyrics, time_tags


def format_time_tag(seconds: float) -> str:
    """将秒数转换为LRC时间标签格式 [mm:ss.xx]"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    secs = int(seconds)
    centiseconds = int((seconds - secs) * 100)

    return f"[{minutes:02d}:{secs:02d}.{centiseconds:02d}]"


def adjust_lrc_file(file_path: str, time_offset: float) -> List[str]:
    """调整LRC文件的时间"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    lines = None

    # 尝试不同编码读取
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue

    if lines is None:
        raise ValueError(f"Unable to read file {file_path} with any supported encoding")

    # 处理每一行
    adjusted_lines = []
    for line in lines:
        line = line.rstrip('\n\r')
        if not line:
            adjusted_lines.append('')
            continue

        # 解析行
        lyrics, time_tags = parse_lrc_line(line)

        if not time_tags:
            # 没有时间标签的行（如元数据或空行）
            if line.startswith('[offset:'):
                # 调整offset元数据
                try:
                    current_offset = int(line[8:-1])
                    new_offset = current_offset + int(time_offset * 1000)
                    adjusted_lines.append(f"[offset:{new_offset}]")
                except:
                    adjusted_lines.append(line)
            else:
                adjusted_lines.append(line)
        else:
            # 调整时间标签
            adjusted_tags = []
            for tag_time in time_tags:
                new_time = tag_time + time_offset
                # 确保时间不为负
                if new_time < 0:
                    new_time = 0
                adjusted_tags.append(format_time_tag(new_time))

            # 重建行
            adjusted_line = ''.join(adjusted_tags) + lyrics
            adjusted_lines.append(adjusted_line)

    return adjusted_lines


def main():
    # 检查参数
    if len(sys.argv) != 3:
        print("用法: python lrc_time_adjuster.py <LRC文件路径> <时间偏移(秒)>")
        print("示例: python lrc_time_adjuster.py song.lrc -7  # 歌词往前移动7秒")
        print("示例: python lrc_time_adjuster.py song.lrc 5   # 歌词往后移动5秒")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        time_offset = float(sys.argv[2])
    except ValueError:
        print("错误: 时间偏移必须是数字")
        sys.exit(1)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)

    # 检查文件扩展名
    if not file_path.lower().endswith('.lrc'):
        print("警告: 文件扩展名不是 .lrc")

    # 调整时间
    adjusted_lines = adjust_lrc_file(file_path, time_offset)

    # 生成输出文件名
    path = Path(file_path)
    if time_offset >= 0:
        output_path = path.parent / f"{path.stem}_+{time_offset}s.lrc"
    else:
        output_path = path.parent / f"{path.stem}{time_offset}s.lrc"

    # 写入调整后的文件
    try:
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(line + '\n' for line in adjusted_lines)

        print(f"成功调整歌词时间: {time_offset}秒")
        print(f"输出文件: {output_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()