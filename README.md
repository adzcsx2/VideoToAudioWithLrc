# FLAC元数据处理工具集

[English](README_en.md) | 中文说明

这是一个用于处理FLAC文件元数据的工具集，包括视频转音频、歌词嵌入、元数据读写等功能。

## 功能特点

- **视频转音频**：将视频文件转换为FLAC格式音频
- **歌词嵌入**：支持LRC格式歌词嵌入，保留时间戳
- **元数据管理**：读取和写入FLAC文件元数据
- **封面图片支持**：支持多种格式的封面图片
  - 本地图片路径
  - 网络图片URL
  - Base64编码图片
  - B站特殊格式URL
- **格式转换**：自动转换AVIF等格式为JPEG
- **音频裁剪**：支持精确的时间定位和时长控制
- **多编码支持**：自动检测UTF-8、GBK、GB2312等编码

## 安装依赖

```bash
pip install Pillow requests
```

系统需要安装FFmpeg：
- Windows: 从 https://ffmpeg.org/download.html 下载
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

## 使用方法

### 1. video_to_audio.py - 视频转音频工具

将视频文件转换为FLAC格式音频，支持歌词嵌入和元数据添加。

```bash
# 基本转换
python video_to_audio.py input.mp4

# 删除前7秒，转换并嵌入歌词
python video_to_audio.py input.mp4 -ss 7 -l lyrics.lrc

# 从第30秒开始转换
python video_to_audio.py video.mp4 -ss 30

# 指定输出文件和压缩级别
python video_to_audio.py audio.wav -o output.flac -c 8

# 从元数据文件添加元数据（包括封面图片）
python video_to_audio.py input.mp4 -metadata metadata.txt

# 同时嵌入歌词和添加元数据
python video_to_audio.py input.mp4 -l lyrics.lrc -metadata metadata.txt

# 所有功能组合
python video_to_audio.py video.mp4 -ss 01:00 -t 03:00 -l lyrics.lrc -metadata metadata.txt -c 8
```

#### 参数说明
- `-ss <时间>`: 从指定时间开始
- `-t <时长>`: 裁剪指定时长
- `-o <输出文件>`: 指定输出文件
- `-l <LRC文件>`: 嵌入歌词文件
- `-metadata <文件>`: 从元数据文件添加元数据（标题、艺术家、封面等）
- `-c <级别>`: FLAC压缩级别 (0-8)

### 2. flac_metadata_utils.py - 元数据处理工具

#### 查看元数据
```bash
# 查看FLAC文件所有元数据
python flac_metadata_utils.py audio.flac
```

#### 写入元数据
```bash
# 从元数据文件写入
python flac_metadata_utils.py audio.flac --metadata metadata.txt

# 写入到新文件
python flac_metadata_utils.py audio.flac --metadata metadata.txt output.flac
```

#### 元数据文件格式示例
```
标题(TITLE)：歌曲名称
艺术家(ARTIST)：歌手名
专辑(ALBUM)：专辑名
日期(DATE)：2024-01-01
流派(GENRE)：流行
作曲家(COMPOSER)：作曲者
词作者(LYRICIST)：作词者
封面图片(COVER_IMAGE):/path/to/image.jpg
封面图片(COVER_IMAGE):https://example.com/image.jpg
封面图片(COVER_IMAGE):data:image/jpeg;base64,/9j/4AAQ...
```

## 测试

### 运行单元测试
```bash
# 运行所有测试
python new_test/run_all_tests.py

# 创建示例测试文件
python new_test/test_flac_metadata_utils.py --create-samples

# 创建手动测试指南
python new_test/test_video_to_audio.py --create-guide
```

### 测试文件结构
```
new_test/
├── __init__.py
├── test_flac_metadata_utils.py  # 元数据处理测试
├── test_video_to_audio.py       # 视频转换测试
├── run_all_tests.py            # 运行所有测试
└── sample_files/               # 示例测试文件
```

## 使用示例

### 视频转音频 + 元数据管理

```bash
# 1. 基本视频转FLAC
python video_to_audio.py video.mp4

# 2. 嵌入歌词
python video_to_audio.py video.mp4 -l lyrics.lrc

# 3. 添加完整元数据（包括封面）
python video_to_audio.py video.mp4 -metadata metadata.txt

# 4. 同时嵌入歌词和元数据
python video_to_audio.py video.mp4 -l lyrics.lrc -metadata metadata.txt

# 5. 复杂组合示例
python video_to_audio.py video.mp4 -ss 01:30 -t 02:00 -l lyrics.lrc -metadata metadata.txt -o output.flac -c 8
```

### 元数据文件格式示例

创建一个 `metadata.txt` 文件：

```text
标题(TITLE)：歌曲名称
艺术家(ARTIST)：歌手名
专辑(ALBUM)：专辑名称
日期(DATE)：2024-12-11
流派(GENRE)：流行
作曲家(COMPOSER)：作曲者
词作者(LYRICIST)：作词者
封面图片(COVER_IMAGE):/path/to/cover.jpg
```

### 支持的图片格式

#### 网络图片
- 常规URL: `https://example.com/image.jpg`
- B站格式: `https://i2.hdslb.com/bfs/archive/xxx.jpg@672w_378h_1c_!web-search-common-cover.avif`

#### Base64图片
```
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...
```

#### 本地图片
- JPEG/JPG
- PNG（支持透明度）
- AVIF（自动转换为JPEG）

## 项目结构

```
videoToAudioWithLRC/
├── video_to_audio.py          # 视频转音频主程序（支持-metadata参数）
├── flac_metadata_utils.py     # 元数据处理工具库
│   ├── 歌词处理功能
│   ├── 元数据读写功能
│   ├── 图片处理功能
│   └── 信息提取功能
├── new_test/                  # 单元测试
│   ├── test_flac_metadata_utils.py
│   ├── test_video_to_audio.py
│   └── run_all_tests.py
├── test/                      # 测试示例文件
│   ├── *.mp4                  # 测试视频
│   ├── *.lrc                  # 测试歌词
│   ├── *.txt                  # 测试元数据
│   └── *.flac                 # 生成的音频文件
└── README.md                  # 本文档
```

## 功能流程图

```
输入文件 (MP4/AVI等)
     ↓
视频转FLAC (FFmpeg)
     ↓
[可选] 嵌入歌词
     ↓
[可选] 添加元数据 (从metadata.txt)
     ↓
输出FLAC文件 (包含歌词和/或元数据)
```

## 常见问题

### 1. FFmpeg未安装
```
错误: 未找到FFmpeg
```
解决：从 https://ffmpeg.org/download.html 下载安装

### 2. 内存不足
处理大文件时可能出现内存不足
解决：分批处理或使用更强大的机器

### 3. 编码问题
```
UnicodeDecodeError
```
解决：确保文件使用UTF-8编码保存

### 4. 权限问题
```
错误: 无法写入文件
```
解决：检查文件权限，确保有写入权限

## 开发说明

### 代码结构
- `video_to_audio.py`: 调用flac_metadata_utils处理元数据
- `flac_metadata_utils.py`: 核心元数据处理功能
  - 歌词处理（parse_lrc_file, embed_lyrics_to_flac）
  - 元数据读写（parse_metadata_file, write_metadata_to_flac）
  - 图片处理（download_image, prepare_cover_image）
  - 信息提取（get_flac_metadata, display_metadata）

### 扩展功能
可以通过修改`flac_metadata_utils.py`来添加更多功能：
- 支持更多音频格式
- 添加更多元数据字段
- 支持更多图片格式

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！