#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLAC元数据工具库单元测试
"""

import unittest
import tempfile
import os
import json
import base64
from pathlib import Path

# 导入要测试的模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from flac_metadata_utils import (
    parse_lrc_file,
    embed_lyrics_to_flac,
    parse_metadata_file,
    download_image,
    decode_base64_image,
    prepare_cover_image,
    write_metadata_to_flac,
    get_flac_metadata,
    display_metadata
)


class TestLrcProcessing(unittest.TestCase):
    """测试歌词处理功能"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_lrc_content = """[ar:测试歌手]
[ti:测试歌曲]
[al:测试专辑]
[00:12.34]第一行歌词
[00:23.45]第二行歌词
[00:34.56]第三行歌词"""

        self.test_lrc_path = self.temp_dir / "test.lrc"
        with open(self.test_lrc_path, 'w', encoding='utf-8') as f:
            f.write(self.test_lrc_content)

    def test_parse_lrc_file(self):
        """测试LRC文件解析"""
        metadata, timed_lyrics, pure_lyrics = parse_lrc_file(self.test_lrc_path)

        # 检查元数据
        self.assertEqual(metadata['ARTIST'], '测试歌手')
        self.assertEqual(metadata['TITLE'], '测试歌曲')
        self.assertEqual(metadata['ALBUM'], '测试专辑')

        # 检查歌词
        self.assertIn('[00:12.34]第一行歌词', timed_lyrics)
        self.assertIn('[00:23.45]第二行歌词', timed_lyrics)
        self.assertIn('第一行歌词', pure_lyrics)
        self.assertIn('第二行歌词', pure_lyrics)

    def test_parse_empty_lrc(self):
        """测试空LRC文件"""
        empty_path = self.temp_dir / "empty.lrc"
        empty_path.touch()

        metadata, timed_lyrics, pure_lyrics = parse_lrc_file(empty_path)

        self.assertEqual(metadata, {})
        self.assertEqual(timed_lyrics, "")
        self.assertEqual(pure_lyrics, "")

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestMetadataProcessing(unittest.TestCase):
    """测试元数据文件处理功能"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_metadata_content = """标题(TITLE)：测试标题
艺术家(ARTIST)：测试艺术家
专辑(ALBUM)：测试专辑
日期(DATE)：2024-12-11
封面图片(COVER_IMAGE):https://example.com/image.jpg"""

        self.test_metadata_path = self.temp_dir / "test_metadata.txt"
        with open(self.test_metadata_path, 'w', encoding='utf-8') as f:
            f.write(self.test_metadata_content)

    def test_parse_metadata_file(self):
        """测试元数据文件解析"""
        metadata = parse_metadata_file(self.test_metadata_path)

        self.assertEqual(metadata['TITLE'], '测试标题')
        self.assertEqual(metadata['ARTIST'], '测试艺术家')
        self.assertEqual(metadata['ALBUM'], '测试专辑')
        self.assertEqual(metadata['DATE'], '2024-12-11')
        self.assertEqual(metadata['COVER_IMAGE'], 'https://example.com/image.jpg')

    def test_parse_chinese_only_metadata(self):
        """测试纯中文标签"""
        chinese_content = """标题：测试标题
艺术家：测试艺术家
专辑：测试专辑"""

        chinese_path = self.temp_dir / "chinese.txt"
        with open(chinese_path, 'w', encoding='utf-8') as f:
            f.write(chinese_content)

        metadata = parse_metadata_file(chinese_path)

        self.assertEqual(metadata['TITLE'], '测试标题')
        self.assertEqual(metadata['ARTIST'], '测试艺术家')
        self.assertEqual(metadata['ALBUM'], '测试专辑')

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestImageProcessing(unittest.TestCase):
    """测试图片处理功能"""

    def test_decode_base64_image(self):
        """测试Base64图片解码"""
        # 创建一个简单的1x1像素的红色PNG图片的Base64编码
        red_pixel_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

        decoded = decode_base64_image(red_pixel_base64)
        self.assertIsNotNone(decoded)
        self.assertGreater(len(decoded), 0)

    def test_decode_base64_with_prefix(self):
        """测试带前缀的Base64图片解码"""
        red_pixel_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

        decoded = decode_base64_image(red_pixel_base64)
        self.assertIsNotNone(decoded)
        self.assertGreater(len(decoded), 0)

    def test_decode_invalid_base64(self):
        """测试无效Base64解码"""
        invalid_base64 = "invalid_base64_string"
        decoded = decode_base64_image(invalid_base64)
        self.assertIsNone(decoded)


class TestMetadataWrite(unittest.TestCase):
    """测试元数据写入功能"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # 创建一个测试用的元数据字典
        self.test_metadata = {
            'TITLE': '测试标题',
            'ARTIST': '测试艺术家',
            'ALBUM': '测试专辑'
        }

    def test_write_metadata_to_flac_without_file(self):
        """测试写入不存在的FLAC文件"""
        non_existent_path = self.temp_dir / "non_existent.flac"

        result = write_metadata_to_flac(non_existent_path, self.test_metadata)
        self.assertFalse(result)

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestFlacInfoExtraction(unittest.TestCase):
    """测试FLAC信息提取功能"""

    def test_get_flac_metadata_without_file(self):
        """测试获取不存在文件的元数据"""
        non_existent_path = Path("/non/existent/file.flac")

        result = get_flac_metadata(non_existent_path)
        self.assertIsNone(result)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # 创建测试LRC文件
        self.test_lrc_content = """[ar:集成测试歌手]
[ti:集成测试歌曲]
[al:集成测试专辑]
[00:10.00]测试歌词第一行
[00:20.00]测试歌词第二行"""

        self.lrc_path = self.temp_dir / "test.lrc"
        with open(self.lrc_path, 'w', encoding='utf-8') as f:
            f.write(self.test_lrc_content)

    def test_lrc_to_metadata_integration(self):
        """测试LRC解析到元数据的集成流程"""
        # 解析LRC文件
        metadata, timed_lyrics, pure_lyrics = parse_lrc_file(self.lrc_path)

        # 验证解析结果
        self.assertEqual(metadata['ARTIST'], '集成测试歌手')
        self.assertEqual(metadata['TITLE'], '集成测试歌曲')
        self.assertEqual(metadata['ALBUM'], '集成测试专辑')

        # 验证歌词内容
        self.assertIn('[00:10.00]测试歌词第一行', timed_lyrics)
        self.assertIn('测试歌词第一行', pure_lyrics)

    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)


def create_sample_test_files():
    """创建示例测试文件（用于手动测试）"""
    test_dir = Path("new_test/sample_files")
    test_dir.mkdir(parents=True, exist_ok=True)

    # 创建示例LRC文件
    lrc_content = """[ar:示例歌手]
[ti:示例歌曲]
[al:示例专辑]
[00:10.50]这是第一行歌词
[00:20.30]这是第二行歌词
[00:30.10]这是第三行歌词"""

    with open(test_dir / "sample.lrc", 'w', encoding='utf-8') as f:
        f.write(lrc_content)

    # 创建示例元数据文件
    metadata_content = """标题(TITLE)：示例歌曲标题
艺术家(ARTIST)：示例艺术家
专辑(ALBUM)：示例专辑
日期(DATE)：2024-12-11
流派(GENRE)：流行
作曲家(COMPOSER)：示例作曲
词作者(LYRICIST)：示例作词
封面图片(COVER_IMAGE):https://example.com/cover.jpg"""

    with open(test_dir / "sample_metadata.txt", 'w', encoding='utf-8') as f:
        f.write(metadata_content)

    # 创建Base64图片示例文件（1x1像素红色）
    red_pixel_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    base64_content = f"""标题(TITLE)：Base64图片测试
艺术家(ARTIST)：测试歌手
专辑(ALBUM)：测试专辑
封面图片(COVER_IMAGE):{red_pixel_base64}"""

    with open(test_dir / "base64_metadata.txt", 'w', encoding='utf-8') as f:
        f.write(base64_content)

    print(f"示例测试文件已创建在: {test_dir.absolute()}")


if __name__ == '__main__':
    # 如果直接运行此脚本，创建示例文件
    if len(sys.argv) > 1 and sys.argv[1] == '--create-samples':
        create_sample_test_files()
    else:
        # 运行单元测试
        unittest.main(verbosity=2)