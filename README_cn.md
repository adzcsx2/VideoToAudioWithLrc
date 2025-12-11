# Video to Audio with LRC

中文 | [English](README.md)

一个功能强大的视频转音频工具集，支持从视频中提取音频并嵌入LRC歌词，专注于FLAC无损格式转换。

## 功能特性

### ✅ 已完成功能

- [x] **视频转音频转换** - 支持多种视频格式转换为FLAC无损音频
- [x] **LRC歌词嵌入** - 支持将带时间戳的LRC歌词嵌入到FLAC文件中
- [x] **音频裁剪功能** - 支持从指定时间开始提取，可设置裁剪时长
- [x] **歌词时间调整** - 支持将歌词整体往前或往后移动指定秒数
- [x] **多编码支持** - 自动识别UTF-8、GBK、GB2312等多种编码
- [x] **元数据提取** - 从LRC文件中提取艺术家、标题、专辑等信息
- [x] **歌词查看器** - 快速查看FLAC文件中的嵌入歌词
- [x] **网易云音乐支持** - 已测试支持网易云音乐歌词显示（其他播放器待测试）

### 🚧 待完成功能

- [ ] 添加封面、艺术家、专辑名称等元信息编辑功能
- [ ] 一键下载B站视频和歌词，一键转换无损音乐（考虑是否必要）

## 工具清单

### 1. video_to_audio.py - 视频转FLAC格式转换工具
专门处理视频转FLAC格式转换和歌词嵌入，支持保留时间戳的同步歌词。

**基本用法：**
```bash
python video_to_audio.py <输入文件> [选项]
```

**常用示例：**
```bash
# 从MP4提取音频，删除前7秒，转为FLAC并嵌入歌词
python video_to_audio.py input.mp4 -ss 7 -l 歌词.lrc

# 从MP4提取音频，删除前30秒，转为FLAC并嵌入歌词
python video_to_audio.py input.mp4 -ss 00:30 -l 歌词.lrc

# 从第30秒开始转换，并嵌入歌词
python video_to_audio.py video.mp4 -ss 30 -l 歌词.lrc

# FLAC最高压缩级别
python video_to_audio.py audio.wav -c 8

# 指定输出文件
python video_to_audio.py audio.wav -o output.flac -l lyrics.lrc
```

**参数说明：**
- `-ss <时间>` - 从指定时间开始裁剪
- `-t <时长>` - 裁剪指定时长
- `-o <输出文件>` - 指定输出文件路径
- `-l <LRC文件>` - 嵌入LRC歌词文件（保留时间戳）
- `-c <级别>` - FLAC压缩级别 (0-8，默认5)
- `-h, --help` - 显示帮助信息

### 2. lrc_time_adjuster.py - LRC歌词时间调整工具
用于将LRC文件的歌词整体往前或往后移动指定秒数。

```bash
# 将歌词往前移动7秒
python lrc_time_adjuster.py song.lrc -7

# 将歌词往后移动5秒
python lrc_time_adjuster.py song.lrc 5
```

### 3. view_lyrics.py - FLAC歌词查看器
快速查看FLAC文件中嵌入的歌词内容。

```bash
# 查看指定FLAC文件的歌词
python view_lyrics.py music.flac

# 查看当前目录所有FLAC文件的歌词
python view_lyrics.py
```

## 为现有音频文件添加歌词

您也可以为现有的FLAC音频文件添加歌词，而无需转换音频：

### 为音频添加歌词的基本用法

```bash
# 为现有FLAC文件添加歌词（会直接修改原文件）
python video_to_audio.py audio.flac -l lyrics.lrc

# 为现有FLAC文件添加歌词并创建新文件（推荐）
python video_to_audio.py audio.flac -l lyrics.lrc -o audio_with_lyrics.flac
```

### 完整工作流程示例

```bash
# 步骤1：检查音频文件是否已有歌词
python view_lyrics.py music.flac

# 步骤2：为音频文件添加歌词
python video_to_audio.py music.flac -l song.lrc -o music_with_lyrics.flac

# 步骤3：验证歌词是否添加成功
python view_lyrics.py music_with_lyrics.flac

# 步骤4：如果歌词时间不对，可以进行调整
python lrc_time_adjuster.py song.lrc -5  # 歌词前移5秒
python video_to_audio.py music.flac -l song_-5s.lrc -o music_fixed.flac
```

### 注意事项
- 程序会自动检测输入是否为FLAC文件，当不需要音频处理时会直接复制
- 歌词以元数据形式嵌入，保留时间戳信息
- 歌词最大长度限制为2000字符（超出部分会被截断）
- 支持的LRC格式：`[mm:ss.xx]歌词`，支持标准元数据标签

## 测试文件

在 `test` 目录中提供了测试文件：

- `测试.mp4` - 测试用的视频文件
- `胡彦斌——《纸短情长》_哔哩哔哩_bilibili.lrc` - 原始歌词文件
- `胡彦斌——《纸短情长》_哔哩哔哩_bilibili-6.5s.lrc` - 调整时间后的歌词文件
- `测试2_trimmed_with_lyrics.flac` - 已嵌入歌词的FLAC文件

## B站视频下载

下载B站视频可以使用以下油猴脚本：

1. **bilibili视频下载**
   - 下载地址：https://update.greasyfork.org/scripts/413228/bilibili%E8%A7%86%E9%A2%91%E4%B8%8B%E8%BD%BD.user.js
   - 安装Tampermonkey浏览器扩展
   - 访问脚本地址点击"安装"
   - 在任意B站视频页面使用下载功能

2. **Bilibili CC字幕工具**
   - 下载地址：https://update.greasyfork.org/scripts/378513/Bilibili%20CC%E5%AD%97%E5%B9%95%E5%B7%A5%E5%85%B7.user.js
   - 使用此工具下载CC字幕，可转换为LRC格式

## 环境要求

- Python 3.x
- FFmpeg（必须安装）

### 安装FFmpeg

1. 访问 [FFmpeg官网](https://ffmpeg.org/download.html)
2. 下载对应平台的版本
3. 将FFmpeg添加到系统PATH环境变量中

## 常见问题

1. **Q: 提示"未找到FFmpeg"怎么办？**
   A: 请确保已安装FFmpeg并将其添加到系统PATH环境变量中。

2. **Q: FLAC歌词需要特殊软件吗？**
   A: 不需要，歌词直接嵌入到FLAC文件中，使用FFmpeg即可处理。

3. **Q: 支持哪些音频格式？**
   A: 输入支持所有FFmpeg支持的格式，输出目前专注于FLAC无损格式。

4. **Q: 歌词时间不准确怎么办？**
   A: 使用 `lrc_time_adjuster.py` 工具调整歌词时间偏移。

## 技术特点

- **无损压缩**：FLAC格式保证音质无损失
- **同步歌词**：支持带时间戳的歌词，可在支持的音乐播放器中显示同步歌词
- **元数据保留**：自动提取并保留歌曲的基本信息
- **多编码支持**：智能识别多种文本编码
- **灵活裁剪**：支持精确的时间定位和时长控制

## 开发状态

项目正在持续开发中，欢迎提交问题报告和功能建议。

## 许可证

本项目采用开源许可证，具体请查看LICENSE文件。