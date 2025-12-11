#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLAC文件元数据工具库（查看、写入封面图片）
"""

import sys
import subprocess
import json
import re
import os
import base64
import tempfile
import requests
import urllib.parse
from pathlib import Path
from typing import Dict, Optional, Union, Tuple
from PIL import Image
import io

# 设置Windows控制台编码为UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')


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


def get_flac_metadata(flac_path):
    """获取FLAC文件的元数据"""
    try:
        # 使用ffprobe获取详细的元数据信息
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            '-show_format',
            str(flac_path)
        ]

        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              encoding='utf-8',
                              creationflags=subprocess.CREATE_NO_WINDOW)

        if result.returncode != 0:
            print(f"错误: 无法读取文件 {flac_path}")
            print(f"错误信息: {result.stderr}")
            return None

        # 解析JSON输出
        data = json.loads(result.stdout)

        # 提取格式元数据
        format_tags = data.get('format', {}).get('tags', {})

        # 提取流元数据（对于FLAC通常只有一个音频流）
        stream_tags = {}
        if data.get('streams'):
            stream_tags = data['streams'][0].get('tags', {})

        # 合并元数据
        all_metadata = {}
        all_metadata.update(format_tags)
        all_metadata.update(stream_tags)

        # 提取视频流信息（封面图片）
        video_streams = []
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                video_streams.append({
                    'codec': stream.get('codec_name', 'Unknown'),
                    'width': stream.get('width', 'Unknown'),
                    'height': stream.get('height', 'Unknown'),
                    'pix_fmt': stream.get('pix_fmt', 'Unknown')
                })

        return {
            'metadata': all_metadata,
            'format_info': {
                'format_name': data.get('format', {}).get('format_name', 'Unknown'),
                'duration': data.get('format', {}).get('duration', 'Unknown'),
                'size': data.get('format', {}).get('size', 'Unknown'),
                'bit_rate': data.get('format', {}).get('bit_rate', 'Unknown')
            },
            'stream_info': {
                'codec': data['streams'][0].get('codec_name', 'Unknown') if data.get('streams') else 'Unknown',
                'sample_rate': data['streams'][0].get('sample_rate', 'Unknown') if data.get('streams') else 'Unknown',
                'channels': data['streams'][0].get('channels', 'Unknown') if data.get('streams') else 'Unknown',
                'channel_layout': data['streams'][0].get('channel_layout', 'Unknown') if data.get('streams') else 'Unknown'
            },
            'cover_info': {
                'has_video_cover': len(video_streams) > 0,
                'video_streams': video_streams,
                'has_metadata_cover': any(tag in all_metadata for tag in ['METADATA_BLOCK_PICTURE', 'COVERART', 'COVERARTURL', 'ARTWORK'])
            }
        }

    except json.JSONDecodeError as e:
        print(f"错误: 无法解析ffprobe输出")
        print(f"原始输出: {result.stdout}")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None


def format_size(size_bytes):
    """格式化文件大小"""
    try:
        size = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    except:
        return size_bytes


def format_duration(seconds):
    """格式化时长"""
    try:
        duration = float(seconds)
        hours = int(duration // 3600)
        duration = duration % 3600
        minutes = int(duration // 60)
        seconds = duration % 60
        secs = int(seconds)
        milliseconds = int((seconds - secs) * 1000)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"
        else:
            return f"{minutes:02d}:{secs:02d}.{milliseconds:03d}"
    except:
        return seconds


def display_metadata(file_path):
    """显示FLAC文件的元数据"""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"错误: 文件 '{file_path}' 不存在")
        return

    print(f"\n{'='*60}")
    print(f"FLAC文件: {file_path.name}")
    print(f"路径: {file_path}")
    print(f"{'='*60}\n")

    # 获取元数据
    result = get_flac_metadata(file_path)

    if not result:
        return

    # 显示基本信息
    print("[文件信息]")
    print(f"  格式: {result['format_info']['format_name']}")
    print(f"  大小: {format_size(result['format_info']['size'])}")
    print(f"  时长: {format_duration(result['format_info']['duration'])}")
    print(f"  比特率: {result['format_info']['bit_rate']} bps")
    print()

    # 显示音频流信息
    print("[音频流信息]")
    print(f"  编解码器: {result['stream_info']['codec']}")
    print(f"  采样率: {result['stream_info']['sample_rate']} Hz")
    print(f"  声道数: {result['stream_info']['channels']}")
    print(f"  声道布局: {result['stream_info']['channel_layout']}")
    print()

    # 显示封面图片信息
    cover_info = result['cover_info']
    print("[封面图片信息]")

    # 检查视频流（封面图片）
    if cover_info['has_video_cover']:
        print("  状态: 包含封面图片")
        for stream in cover_info['video_streams']:
            print(f"  编码: {stream['codec']}")
            print(f"  尺寸: {stream['width']} x {stream['height']} 像素")
            print(f"  像素格式: {stream['pix_fmt']}")
    else:
        print("  状态: 未找到视频流封面")

    # 检查元数据中的封面标签
    if cover_info['has_metadata_cover']:
        metadata = result['metadata']
        print("  封面标签:")
        for tag in ['METADATA_BLOCK_PICTURE', 'COVERART', 'COVERARTURL', 'ARTWORK']:
            if tag in metadata:
                print(f"    - {tag}")
                if tag == 'COVERARTURL':
                    print(f"      URL: {metadata[tag]}")
                elif tag in ['METADATA_BLOCK_PICTURE', 'COVERART']:
                    if metadata[tag]:
                        try:
                            if tag == 'METADATA_BLOCK_PICTURE':
                                decoded = base64.b64decode(metadata[tag])
                                if decoded.startswith(b'\xFF\xD8\xFF'):
                                    print(f"      格式: JPEG")
                                elif decoded.startswith(b'\x89PNG'):
                                    print(f"      格式: PNG")
                                print(f"      大小: {len(decoded)} 字节")
                            else:
                                print(f"      数据长度: {len(metadata[tag])} 字符")
                        except:
                            pass
    else:
        print("  状态: 元数据中未找到封面标签")

    print()

    # 显示元数据标签
    metadata = result['metadata']
    # 移除封面相关标签，避免重复显示
    metadata = {k: v for k, v in metadata.items()
                if k not in ['METADATA_BLOCK_PICTURE', 'COVERART', 'COVERARTURL', 'ARTWORK']}

    if metadata:
        print("[元数据标签]")

        # 常见标签优先显示
        important_tags = ['TITLE', 'ARTIST', 'ALBUM', 'DATE', 'GENRE', 'TRACK', 'COMPOSER']

        # 先显示重要标签
        for tag in important_tags:
            if tag in metadata:
                value = metadata[tag]
                if tag == 'LYRICS':
                    # 歌词特殊处理，显示前几行
                    lines = value.split('\n')[:5]
                    preview = '\n        '.join(lines)
                    if len(value) > 200:
                        print(f"  {tag}:")
                        print(f"    {preview}")
                        print(f"    ...(共{len(value)}字符，已截断)")
                    else:
                        print(f"  {tag}:")
                        print(f"    {preview}")
                else:
                    print(f"  {tag}: {value}")
                # 从字典中移除已显示的标签
                metadata.pop(tag, None)

        # 显示其他标签
        for tag, value in sorted(metadata.items()):
            if tag == 'LYRICS' and len(value) > 200:
                # 如果是歌词且很长，显示预览
                lines = value.split('\n')[:5]
                preview = '\n        '.join(lines)
                print(f"  {tag}:")
                print(f"    {preview}")
                print(f"    ...(共{len(value)}字符，已截断)")
            elif '\n' in str(value):
                # 多行值特殊处理
                print(f"  {tag}:")
                for line in str(value).split('\n')[:3]:
                    print(f"    {line}")
                if len(str(value).split('\n')) > 3:
                    print(f"    ...(更多内容)")
            else:
                print(f"  {tag}: {value}")
    else:
        print("没有找到其他元数据标签")

    print("\n" + "="*60)


# ==================== 歌词处理功能 ====================

# Pre-compile regex pattern for better performance
TIMESTAMP_PATTERN = re.compile(r'\[(\d{2}):(\d{2})(?:\.(\d{2}))?\]')

# Constants
MAX_LYRICS_LENGTH = 2000


def parse_lrc_file(lrc_path: Union[str, Path]) -> Tuple[Dict[str, str], str, str]:
    """解析LRC文件，保留时间戳的歌词"""
    lrc_path = Path(lrc_path)
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


def embed_lyrics_to_flac(
    flac_path: Union[str, Path],
    lrc_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None
) -> bool:
    """嵌入歌词到FLAC（保留时间戳）"""
    import shutil
    import time

    flac_path = Path(flac_path)
    lrc_path = Path(lrc_path)

    if output_path is None:
        output_path = flac_path
    output_path = Path(output_path)

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


# ==================== 元数据写入功能 ====================

def parse_metadata_file(metadata_file_path: Union[str, Path]) -> Dict[str, str]:
    """
    解析元数据文件
    支持格式：中文标签(英文标签)：值
    """
    metadata = {}

    try:
        # 尝试不同编码读取
        encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']
        content = None

        for encoding in encodings:
            try:
                with open(metadata_file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            print(f"错误：无法读取元数据文件 {metadata_file_path}")
            return metadata

        # 解析每一行
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # 处理格式：中文(英文)：值
            # 使用冒号或中文冒号分割
            if '：' in line:
                tag_part, value = line.split('：', 1)
            elif ':' in line:
                tag_part, value = line.split(':', 1)
            else:
                continue

            tag_part = tag_part.strip()
            value = value.strip()

            # 提取括号内的英文标签
            if '(' in tag_part and ')' in tag_part:
                # 中文标签(英文标签) -> 提取英文标签
                match = re.search(r'\(([^)]+)\)', tag_part)
                if match:
                    tag = match.group(1)
                else:
                    tag = tag_part
            else:
                # 没有括号，使用整个标签部分
                tag = tag_part

            # 特殊处理标签映射
            tag_mapping = {
                '标题': 'TITLE',
                '艺术家': 'ARTIST',
                '专辑': 'ALBUM',
                '日期': 'DATE',
                '流派': 'GENRE',
                '作曲家': 'COMPOSER',
                '词作者': 'LYRICIST',
                '封面图片': 'COVER_IMAGE'
            }

            # 如果是中文标签，映射到英文
            if tag in tag_mapping:
                tag = tag_mapping[tag]

            if tag and value:
                metadata[tag] = value

        return metadata

    except Exception as e:
        print(f"解析元数据文件时出错：{e}")
        return metadata


def download_image(url: str, save_path: Union[str, Path]) -> bool:
    """
    下载网络图片到本地
    支持各种格式包括bilibili的压缩参数
    """
    try:
        print(f"正在下载图片：{url}")

        # 设置请求头，模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.bilibili.com/',
        }

        # 处理bilibili等特殊URL
        # 移除@后面的参数，只保留基础URL
        clean_url = url
        if '@' in url and ('.jpg@' in url or '.png@' in url or '.webp@' in url):
            clean_url = url.split('@')[0]

        response = requests.get(clean_url, headers=headers, timeout=30)
        response.raise_for_status()

        # 尝试识别图片格式
        image_data = response.content

        # 使用PIL尝试打开并转换图片
        try:
            img = Image.open(io.BytesIO(image_data))

            # 如果是AVIF或其他不支持的格式，转换为JPEG
            if img.format == 'AVIF' or img.format not in ['JPEG', 'PNG', 'JPG']:
                # 转换为RGB模式（如果需要）
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

                # 保存为JPEG
                img.save(save_path, 'JPEG', quality=95)
                print(f"图片已转换为JPEG格式：{save_path}")
            else:
                # 保存原始格式
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                print(f"图片下载完成：{save_path}")

        except Exception as img_error:
            # PIL处理失败，直接保存原始数据
            with open(save_path, 'wb') as f:
                f.write(image_data)
            print(f"图片下载完成（原始格式）：{save_path}")

        return True

    except Exception as e:
        print(f"下载图片失败：{e}")
        return False


def decode_base64_image(base64_data: str) -> Optional[bytes]:
    """
    解码Base64图片数据
    """
    try:
        # 处理data:image/jpeg;base64,格式
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]

        # 检查是否是有效的Base64字符
        if not base64_data:
            return None

        # Base64字符集检查
        base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
        if not base64_pattern.match(base64_data):
            return None

        # 补充padding
        padding_needed = 4 - (len(base64_data) % 4)
        if padding_needed != 4:
            base64_data += '=' * padding_needed

        # 尝试解码
        decoded = base64.b64decode(base64_data, validate=True)
        return decoded
    except Exception as e:
        print(f"Base64解码失败：{e}")
        return None


def prepare_cover_image(cover_input: str, temp_dir: Optional[Path] = None) -> Optional[Path]:
    """
    准备封面图片文件
    支持本地路径、网络URL和Base64编码
    """
    if temp_dir is None:
        temp_dir = Path(tempfile.gettempdir())

    temp_path = temp_dir / f"temp_cover_{os.getpid()}.jpg"

    try:
        # 检查是否是Base64编码
        if cover_input.startswith('data:image/'):
            print("检测到Base64编码图片")
            image_data = decode_base64_image(cover_input)
            if image_data:
                with open(temp_path, 'wb') as f:
                    f.write(image_data)
                print(f"Base64图片已保存：{temp_path}")
                return temp_path
            else:
                print("Base64解码失败")
                return None

        # 判断是URL还是本地路径
        elif cover_input.startswith(('http://', 'https://')):
            # 网络图片，需要下载
            if download_image(cover_input, temp_path):
                return temp_path
            else:
                return None

        else:
            # 本地路径
            cover_path = Path(cover_input)
            if cover_path.exists():
                # 如果本地文件是特殊格式，转换为JPEG
                try:
                    with Image.open(cover_path) as img:
                        if img.format == 'AVIF' or img.format not in ['JPEG', 'PNG', 'JPG']:
                            # 转换为JPEG
                            if img.mode in ('RGBA', 'LA', 'P'):
                                background = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'P':
                                    img = img.convert('RGBA')
                                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                                img = background
                            img.save(temp_path, 'JPEG', quality=95)
                            print(f"本地图片已转换为JPEG：{temp_path}")
                            return temp_path
                        else:
                            return cover_path
                except:
                    # PIL处理失败，直接返回原路径
                    return cover_path
            else:
                print(f"错误：封面图片文件不存在：{cover_path}")
                return None

    except Exception as e:
        print(f"准备封面图片时出错：{e}")
        return None


def write_metadata_to_flac(
    flac_path: Union[str, Path],
    metadata: Dict[str, str],
    cover_image_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None
) -> bool:
    """
    将元数据写入FLAC文件

    Args:
        flac_path: 输入的FLAC文件路径
        metadata: 要写入的元数据字典
        cover_image_path: 封面图片路径（可选）
        output_path: 输出文件路径（可选，如果为None则覆盖原文件）

    Returns:
        bool: 是否成功
    """
    flac_path = Path(flac_path)

    if not flac_path.exists():
        print(f"错误：FLAC文件不存在：{flac_path}")
        return False

    # 如果没有指定输出路径，使用临时文件
    if output_path is None:
        temp_output = flac_path.with_name(f"{flac_path.stem}_temp_{os.getpid()}{flac_path.suffix}")
        final_output = flac_path
    else:
        temp_output = Path(output_path)
        final_output = Path(output_path)

    try:
        # 准备FFmpeg命令
        cmd = ['ffmpeg', '-i', str(flac_path)]

        # 处理封面图片
        cover_file = None
        if cover_image_path:
            cover_input = str(cover_image_path)
            cover_file = prepare_cover_image(cover_input)

            if cover_file and cover_file.exists():
                cmd.extend(['-i', str(cover_file)])
                print(f"使用封面图片：{cover_file}")
            else:
                print("警告：未能准备封面图片")

        # 添加元数据
        cmd.extend(['-c', 'copy'])  # 复制流

        # 添加元数据标签
        for tag, value in metadata.items():
            if tag != 'COVER_IMAGE':  # 跳过封面图片标签，单独处理
                cmd.extend(['-metadata', f"{tag}={value}"])

        # 如果有封面图片，添加映射
        if cover_file and cover_file.exists():
            cmd.extend(['-map', '0:a'])  # 映射音频流
            cmd.extend(['-map', '1:v'])  # 映射图片流
            cmd.extend(['-disposition:v', 'attached_pic'])  # 标记为附加图片

        cmd.extend(['-y', str(temp_output)])

        # 执行命令
        print("正在写入元数据...")
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              encoding='utf-8',
                              creationflags=subprocess.CREATE_NO_WINDOW)

        # 清理临时下载的图片
        if cover_image_path and str(cover_image_path).startswith(('http://', 'https://')):
            if cover_file and cover_file.exists():
                cover_file.unlink()

        if result.returncode == 0:
            # 如果使用临时文件，替换原文件
            if output_path is None:
                flac_path.unlink()
                temp_output.rename(flac_path)

            print("元数据写入成功！")

            # 显示写入的元数据
            print("\n已写入的元数据：")
            for tag, value in metadata.items():
                if tag != 'COVER_IMAGE':
                    print(f"  {tag}: {value}")

            if cover_image_path:
                print(f"  封面图片: {cover_image_path}")

            return True
        else:
            print(f"写入失败：{result.stderr}")
            # 清理临时文件
            if temp_output.exists():
                temp_output.unlink()
            return False

    except Exception as e:
        print(f"写入元数据时出错：{e}")
        # 清理临时文件
        if temp_output.exists():
            temp_output.unlink()
        return False


def write_metadata_from_file(
    flac_path: Union[str, Path],
    metadata_file: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None
) -> bool:
    """
    从元数据文件读取并写入FLAC文件

    Args:
        flac_path: FLAC文件路径
        metadata_file: 元数据文件路径
        output_path: 输出文件路径（可选）

    Returns:
        bool: 是否成功
    """
    # 解析元数据文件
    metadata = parse_metadata_file(metadata_file)

    if not metadata:
        print("错误：没有找到有效的元数据")
        return False

    # 提取封面图片路径
    cover_image = metadata.pop('COVER_IMAGE', None)

    # 写入元数据
    return write_metadata_to_flac(flac_path, metadata, cover_image, output_path)


def print_help():
    """打印帮助信息"""
    print("""
FLAC文件元数据工具库（查看和写入）

用法1: 查看元数据
    python flac_metadata_util.py <FLAC文件路径>

用法2: 写入元数据
    python flac_metadata_util.py <FLAC文件> --metadata <元数据文件> [输出文件]

示例:
    # 查看FLAC文件元数据
    python flac_metadata_util.py audio.flac

    # 从metadata.txt写入元数据
    python flac_metadata_util.py audio.flac --metadata metadata.txt

    # 写入到新文件
    python flac_metadata_util.py audio.flac --metadata metadata.txt output.flac

元数据文件格式:
    标题(TITLE)：歌曲名称
    艺术家(ARTIST)：歌手名
    专辑(ALBUM)：专辑名
    日期(DATE)：2024-01-01
    流派(GENRE)：流行
    作曲家(COMPOSER)：作曲者
    词作者(LYRICIST)：作词者
    封面图片(COVER_IMAGE):/path/to/image.jpg  # 本地路径
    封面图片(COVER_IMAGE):https://example.com/image.jpg  # 网络URL

功能:
    - 显示文件基本信息（大小、时长、格式等）
    - 显示音频流信息（编码、采样率、声道等）
    - 显示封面图片信息（格式、尺寸等）
    - 显示所有元数据标签（标题、艺术家、专辑、歌词等）
    - 写入元数据（支持中文和英文标签）
    - 支持本地和网络图片作为封面
    """)


def main():
    if not check_ffmpeg():
        print("错误: 未找到FFmpeg/FFprobe")
        print("下载地址: https://ffmpeg.org/download.html")
        sys.exit(1)

    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        sys.exit(0)

    # 检查是否是写入元数据的命令
    if '--metadata' in sys.argv:
        # 写入元数据模式
        try:
            flac_index = sys.argv.index('--metadata') - 1
            metadata_index = sys.argv.index('--metadata') + 1
            output_index = metadata_index + 1 if len(sys.argv) > metadata_index + 1 else None

            flac_file = sys.argv[flac_index]
            metadata_file = sys.argv[metadata_index]
            output_file = sys.argv[output_index] if output_index else None

            # 检查文件是否存在
            if not Path(flac_file).exists():
                print(f"错误：FLAC文件不存在：{flac_file}")
                sys.exit(1)

            if not Path(metadata_file).exists():
                print(f"错误：元数据文件不存在：{metadata_file}")
                sys.exit(1)

            # 执行写入
            success = write_metadata_from_file(flac_file, metadata_file, output_file)

            if not success:
                sys.exit(1)

        except (IndexError, ValueError) as e:
            print("错误：参数格式不正确")
            print_help()
            sys.exit(1)
    else:
        # 查看元数据模式（默认）
        if len(sys.argv) != 2:
            print_help()
            sys.exit(1)

        file_path = sys.argv[1]
        display_metadata(file_path)


if __name__ == "__main__":
    main()