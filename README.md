# 视频转 FLAC 音频工具

[English](README_en.md) | 中文说明

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange.svg)](https://ffmpeg.org)

这是一个功能完整的视频转 FLAC 音频工具，支持歌词嵌入和元数据管理。项目提供了命令行界面和图形用户界面两种使用方式。

![GUI](dist/gui.png)

## ✨ 主要功能

- 🎵 **视频转音频**：将视频文件（MP4、AVI、MKV 等）转换为 FLAC 无损音频
- 📝 **歌词嵌入**：支持 LRC 格式歌词嵌入，保留时间戳
- 🏷️ **元数据管理**：添加歌曲信息（标题、艺术家、专辑、日期、流派等）
- 🖼️ **封面支持**：支持多种格式的封面图片
  - 本地图片路径
  - 网络图片 URL
  - Base64 编码图片
  - B 站特殊格式 URL
- 🔧 **格式转换**：自动转换 AVIF 等格式为 JPEG
- ✂️ **音频裁剪**：支持精确的时间定位和时长控制
- 🌐 **多编码支持**：自动检测 UTF-8、GBK、GB2312 等编码

## 📦 安装

### 环境要求

- Python 3.7 或更高版本
- FFmpeg（用于音视频处理）

### 安装依赖

```bash
pip install Pillow requests
```

### 安装 FFmpeg

- **Windows**: 从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

或使用项目提供的下载助手：

```bash
python download_ffmpeg.py
```

## 🚀 快速开始

### 1. GUI 方式（推荐）

#### 运行 GUI 程序

```bash
python video_to_audio_gui.py
# 或双击运行：启动GUI.bat
```

#### 打包成独立 EXE

```bash
# 方法1：使用批处理脚本（推荐）
双击运行：一键打包.bat

# 方法2：使用Python脚本
pip install pyinstaller
python build_exe.py
```

打包后的 exe 文件位于 `dist` 目录中，可以在没有 Python 环境的 Windows 电脑上运行。

### 2. 命令行方式

#### 基本使用

```bash
# 基本转换
python video_to_audio.py input.mp4

# 嵌入歌词
python video_to_audio.py input.mp4 -l lyrics.lrc

# 添加元数据
python video_to_audio.py input.mp4 -metadata metadata.txt

# 同时嵌入歌词和元数据
python video_to_audio.py input.mp4 -l lyrics.lrc -metadata metadata.txt

# 所有功能组合
python video_to_audio.py video.mp4 -ss 01:00 -t 03:00 -l lyrics.lrc -metadata metadata.txt -c 8
```

#### 参数说明

- `-ss <时间>`: 从指定时间开始（如 30 或 01:30）
- `-t <时长>`: 裁剪指定时长（如 60 或 02:00）
- `-o <输出文件>`: 指定输出文件
- `-l <LRC文件>`: 嵌入歌词文件
- `-metadata <文件>`: 从元数据文件添加元数据
- `-c <级别>`: FLAC 压缩级别 (0-8，默认 5)

## 📁 项目结构

```
videoToAudioWithLRC/
├── video_to_audio.py          # 命令行主程序
├── video_to_audio_gui.py      # GUI图形界面程序
├── flac_metadata_utils.py     # 元数据处理核心模块
├── lrc_time_adjuster.py       # 歌词时间调整工具
├── view_lyrics.py             # 歌词查看工具
├── build_exe.py              # 打包成exe的脚本
├── create_portable_package.py # 创建便携版包的脚本
├── download_ffmpeg.py        # FFmpeg下载助手
├── 一键打包.bat               # 一键打包批处理
├── 启动GUI.bat                # 启动GUI批处理
├── test/                      # 测试文件目录
│   ├── *.mp4                  # 测试视频
│   ├── *.lrc                  # 测试歌词
│   ├── *.txt                  # 测试元数据
│   └── *.flac                 # 生成的音频文件
├── new_test/                  # 单元测试目录
│   ├── test_flac_metadata_utils.py
│   ├── test_video_to_audio.py
│   └── run_all_tests.py
└── README.md                  # 本文档
```

## 📋 元数据文件格式

创建一个 `metadata.txt` 文件：

```text
标题(TITLE)：歌曲名称
艺术家(ARTIST)：歌手名
专辑(ALBUM)：专辑名称
日期(DATE)：2025-12-11
流派(GENRE)：流行
作曲家(COMPOSER)：作曲者
词作者(LYRICIST)：作词者
封面图片(COVER_IMAGE): /path/to/image.jpg
封面图片(COVER_IMAGE): https://example.com/image.jpg
封面图片(COVER_IMAGE): data:image/jpeg;base64,/9j/4AAQ...
```

### 支持的图片格式

#### 网络图片

- 常规 URL: `https://example.com/image.jpg`
- B 站格式: `https://i2.hdslb.com/bfs/archive/xxx.jpg@672w_378h_1c_!web-search-common-cover.avif`

#### Base64 图片

```
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...
```

#### 本地图片

- JPEG/JPG
- PNG（支持透明度）
- AVIF（自动转换为 JPEG）

## 🧪 测试

运行单元测试：

```bash
# 运行所有测试
python new_test/run_all_tests.py

# 创建示例测试文件
python new_test/test_flac_metadata_utils.py --create-samples

# 创建手动测试指南
python new_test/test_video_to_audio.py --create-guide
```

## 🎯 GUI 功能特点

### 1. 文件选择

- 支持选择视频或音频文件作为输入
- 支持选择 LRC 歌词文件（可选）
- 支持选择元数据文件（可选）
- 支持自定义输出文件路径

### 2. 参数设置

- 设置开始时间（裁剪开始位置）
- 设置持续时间（裁剪时长）
- FLAC 压缩级别滑块调节（0-8）

### 3. 执行与反馈

- 实时显示执行日志
- 不同类型的日志颜色区分
- 转换完成后自动通知
- 一键打开输出文件夹

## 🔄 功能流程图

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

## 💡 使用技巧

1. **批量处理**：可以编写批处理脚本批量处理多个文件
2. **元数据模板**：创建不同风格的元数据模板文件，方便复用
3. **自动命名**：不指定输出文件时，程序会自动生成带标记的文件名
4. **错误排查**：查看日志输出可以了解处理过程中的详细信息

## ❓ 常见问题

### 1. FFmpeg 未安装

```
错误: 未找到FFmpeg
```

**解决方案**：

- 运行 `python download_ffmpeg.py` 自动下载
- 或从 https://ffmpeg.org/download.html 下载安装

### 2. 内存不足

处理大文件时可能出现内存不足
**解决方案**：分批处理或使用更强大的机器

### 3. 编码问题

```
UnicodeDecodeError
```

**解决方案**：确保文件使用 UTF-8 编码保存

### 4. 权限问题

```
错误: 无法写入文件
```

**解决方案**：检查文件权限，确保有写入权限

## 🛠️ 开发说明

### 技术栈

- **Python 3**：主要编程语言
- **Tkinter**：GUI 界面框架
- **FFmpeg**：音视频处理引擎
- **PIL/Pillow**：图像处理
- **PyInstaller**：打包工具

### 代码结构

- `video_to_audio.py`: 命令行主程序，调用 flac_metadata_utils 处理元数据
- `video_to_audio_gui.py`: GUI 主程序，提供图形化操作界面
- `flac_metadata_utils.py`: 核心元数据处理功能
  - 歌词处理（parse_lrc_file, embed_lyrics_to_flac）
  - 元数据读写（parse_metadata_file, write_metadata_to_flac）
  - 图片处理（download_image, prepare_cover_image）
  - 信息提取（get_flac_metadata, display_metadata）

### 扩展功能

可以通过修改相应模块来添加更多功能：

- 支持更多音频格式（AAC、OGG 等）
- 添加更多元数据字段
- 支持更多图片格式
- 实现批量转换功能

## 📝 更新日志

### v2.0.0 (2025-12-11)

- ✨ 新增 GUI 图形界面
- ✨ 支持打包成独立 exe 文件
- ✨ 添加 FFmpeg 自动下载功能
- 🐛 优化图片处理，支持 B 站特殊 URL
- 📚 完善文档和测试用例

### v1.0.0 (2025-12-10)

- 🎉 初始版本发布
- ✨ 支持视频转 FLAC
- ✨ 支持歌词嵌入
- ✨ 支持元数据管理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [FFmpeg](https://ffmpeg.org) - 强大的音视频处理工具
- [Pillow](https://pillow.readthedocs.io) - 友好的 Python 图像处理库
- [PyInstaller](https://pyinstaller.readthedocs.io) - Python 程序打包工具

---

如果这个项目对你有帮助，请给它一个 ⭐️！
