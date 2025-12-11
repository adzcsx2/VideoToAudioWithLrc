# 音乐视频转无损音乐工具 (视频转 FLAC 带歌词)

[English](README_en.md) | 中文说明

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange.svg)](https://ffmpeg.org)

一个专业的音乐视频转换工具，将音乐视频（MV、现场演出、音乐直播等）转换为高质量的无损 FLAC 音频，并自动嵌入同步歌词。支持 GUI 图形界面和命令行两种操作方式。

![GUI](dist/gui.png)

## ✨ 主要功能

- 🎵 **音乐视频转换**：将 MV、现场演出、音乐直播等视频转换为高品质 FLAC 无损音乐
- 📝 **歌词同步嵌入**：完美支持 LRC 格式歌词，保留精确时间戳，实现歌词同步显示
- 🎼 **专业元数据**：完整的歌曲信息管理（标题、艺术家、专辑、日期、流派、作曲、作词等）
- 🖼️ **智能封面处理**：多种封面图片支持
  - 本地图片文件（JPG/PNG/AVIF 等）
  - 网络图片 URL（自动下载）
  - Base64 编码图片
  - B 站、微博等特殊格式 URL（自动优化）
- ✂️ **精准音频裁剪**：支持指定开始时间和持续时间，提取音频片段
- 🌐 **智能编码识别**：自动处理 UTF-8、GBK、GB2312 等多种歌词文件编码
- 🎚️ **可调压缩级别**：0-8 级 FLAC 压缩，平衡文件大小与音质

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
├── 🎯 核心程序
│   ├── video_to_audio_gui.py      # GUI图形界面主程序
│   └── video_to_audio.py          # 命令行版本
├── 🔧 核心模块
│   └── flac_metadata_utils.py     # 歌词嵌入和元数据处理核心
├── 🛠️ 辅助工具
│   ├── lrc_time_adjuster.py       # 歌词时间调整工具
│   ├── view_lyrics.py             # 歌词查看工具
│   └── download_ffmpeg.py        # FFmpeg自动下载助手
├── 📦 打包工具
│   ├── build_exe.py              # 打包成独立exe
│   └── create_portable_package.py # 创建便携版
├── 🚀 快速启动
│   ├── 一键打包.bat               # Windows一键打包脚本
│   └── 启动GUI.bat                # Windows快速启动GUI
├── 🧪 测试相关
│   └── new_test/                  # 单元测试目录
└── 📚 文档
    └── README.md                  # 项目说明文档
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

## 🔄 音乐视频转换流程

```
📹 音乐视频 (MV/现场演出/音乐直播)
     ↓
🎵 提取音频并转换为FLAC无损格式
     ↓
📝 嵌入LRC同步歌词 (保留时间戳)
     ↓
🎼 添加歌曲元数据 (标题/艺术家/专辑等)
     ↓
🖼️ 嵌入封面图片
     ↓
🎧 输出完整FLAC文件 (无损音乐+歌词+封面)
```

## 💡 使用技巧

1. **歌词文件准备**：

   - 使用与视频完全匹配的歌词文件
   - 确保时间戳准确，以便歌词同步显示
   - 支持多种编码，中文歌词无需转换

2. **批量处理音乐视频**：

   - 编写批处理脚本一次处理多个 MV
   - 使用统一的元数据模板提高效率
   - 建议每个视频配备对应的歌词文件

3. **音质优化建议**：

   - 选择较高的 FLAC 压缩级别（5-8）获得更好音质
   - 保留原始音频采样率，避免降采样
   - 确保视频源音频质量足够高

4. **元数据完善**：
   - 准确填写歌曲信息，便于音乐播放器识别
   - 使用高清封面图片，推荐 1000x1000 像素以上
   - 包含作曲、作词等详细信息

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

- ✨ 全新 GUI 图形界面，操作更直观
- ✨ 支持打包成独立 exe，无需安装 Python
- ✨ FFmpeg 自动下载和配置
- 🎵 优化音乐视频处理逻辑
- 📝 改进歌词嵌入算法，完美保留时间戳
- 🖼️ 增强图片处理，支持 B 站、微博等特殊 URL
- 📚 完善文档和使用指南

### v1.0.0 (2025-12-10)

- 🎉 项目初始发布
- ✨ 核心功能：音乐视频转 FLAC
- ✨ LRC 歌词嵌入支持
- ✨ 完整元数据管理系统

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
