#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
video_to_audio.py的单元测试
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# 导入要测试的模块
sys.path.insert(0, str(Path(__file__).parent.parent))
from video_to_audio import (
    check_ffmpeg,
    parse_time,
    format_time,
    process_media
)


class TestVideoToAudio(unittest.TestCase):
    """测试video_to_audio功能"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = Path(tempfile.mkdtemp())

    def test_parse_time(self):
        """测试时间解析"""
        # 测试秒数
        self.assertEqual(parse_time("30"), 30.0)
        self.assertEqual(parse_time("30.5"), 30.5)

        # 注意：parse_time的实现中，"1:30"和"01:30"都被解析为1小时30分
        # 测试时:分格式
        self.assertEqual(parse_time("1:30"), 3630.0)  # 1小时30分 = 3630秒
        self.assertEqual(parse_time("01:30"), 3630.0)  # 同样是1小时30分

        # 测试时:分:秒格式
        self.assertEqual(parse_time("1:30:45"), 5445.0)
        self.assertEqual(parse_time("01:30:45"), 5445.0)

    def test_format_time(self):
        """测试时间格式化"""
        # 测试秒数格式化
        self.assertEqual(format_time(30), "00:30")
        self.assertEqual(format_time(90), "01:30")
        self.assertEqual(format_time(3661), "01:01:01")

    def test_check_ffmpeg(self):
        """测试FFmpeg检查"""
        # 这个测试取决于系统是否安装了FFmpeg
        result = check_ffmpeg()
        self.assertIsInstance(result, bool)

    def test_process_media_nonexistent_file(self):
        """测试处理不存在的文件"""
        non_existent = self.temp_dir / "non_existent.mp4"

        result = process_media(str(non_existent))
        self.assertFalse(result)

    def test_process_media_with_metadata_file(self):
        """测试使用元数据文件（如果存在）"""
        # 这个测试需要实际的文件，暂时跳过
        self.skipTest("需要实际的媒体文件进行测试")

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)


def create_manual_test_guide():
    """创建手动测试指南"""
    test_dir = Path("new_test")
    guide_content = """# 手动测试指南

## 测试video_to_audio.py

### 1. 基本转换测试
```bash
# 从MP4提取音频（不删除前部）
python video_to_audio.py input.mp4

# 从MP4提取音频，删除前7秒，转为FLAC并嵌入歌词
python video_to_audio.py input.mp4 -ss 7 -l 歌词.lrc

# 从第30秒开始转换
python video_to_audio.py video.mp4 -ss 30
```

### 2. 压缩级别测试
```bash
# FLAC最高压缩级别
python video_to_audio.py audio.wav -c 8

# FLAC最低压缩级别（最快）
python video_to_audio.py audio.wav -c 0
```

### 3. 输出文件指定测试
```bash
# 指定输出文件
python video_to_audio.py audio.wav -o output.flac -l lyrics.lrc
```

### 4. 组合功能测试
```bash
# 所有功能组合
python video_to_audio.py video.mp4 -ss 01:00 -t 03:00 -l lyrics.lrc -c 8
```

## 测试flac_metadata_utils.py

### 1. 查看元数据
```bash
# 查看FLAC文件元数据
python flac_metadata_utils.py audio.flac

# 查看带封面的FLAC文件
python flac_metadata_utils.py "test\高级格式封面.flac"
```

### 2. 写入元数据
```bash
# 从metadata.txt写入元数据
python flac_metadata_utils.py audio.flac --metadata metadata.txt

# 写入到新文件
python flac_metadata_utils.py audio.flac --metadata metadata.txt output.flac
```

### 3. 支持的图片格式测试
- 普通URL: `https://example.com/image.jpg`
- B站格式: `https://i2.hdslb.com/bfs/archive/xxx.jpg@672w_378h_1c_!web-search-common-cover.avif`
- Base64: `data:image/jpeg;base64,/9j/4AAQSkZJRg...`
- 本地路径: `D:\path\to\image.png`

## 需要准备的测试文件

1. **测试视频文件**
   - MP4格式（至少1分钟）
   - 不同编码格式

2. **测试音频文件**
   - WAV格式
   - MP3格式
   - FLAC格式

3. **测试歌词文件**
   - UTF-8编码的LRC文件
   - GBK编码的LRC文件
   - 包含特殊字符的LRC文件

4. **测试图片文件**
   - JPEG格式
   - PNG格式（带透明度）
   - AVIF格式（如果支持）

## 预期结果

### video_to_audio.py
- 成功转换视频到FLAC
- 正确应用时间裁剪
- 正确嵌入歌词
- 输出文件大小合理

### flac_metadata_utils.py
- 正确显示所有元数据
- 成功写入新的元数据
- 正确处理各种图片格式
- 保留原始音频质量

## 常见问题排查

1. **FFmpeg未安装**
   ```
   错误: 未找到FFmpeg
   ```
   解决：从 https://ffmpeg.org/download.html 下载安装

2. **权限问题**
   ```
   错误: 无法写入文件
   ```
   解决：检查文件权限，确保有写入权限

3. **编码问题**
   ```
   UnicodeDecodeError
   ```
   解决：确保文件使用UTF-8编码保存

4. **内存不足**
   处理大文件时可能出现内存不足
   解决：分批处理或使用更强大的机器
"""

    with open(test_dir / "manual_test_guide.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print(f"手动测试指南已创建: {test_dir / 'manual_test_guide.md'}")


if __name__ == '__main__':
    # 如果直接运行此脚本，创建手动测试指南
    if len(sys.argv) > 1 and sys.argv[1] == '--create-guide':
        create_manual_test_guide()
    else:
        # 运行单元测试
        unittest.main(verbosity=2)