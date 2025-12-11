# Video to Audio with LRC

[中文说明](README_cn.md) | English

A powerful video-to-audio conversion toolkit that extracts audio from videos and embeds LRC lyrics, specializing in FLAC lossless format conversion.

## Features

### ✅ Completed Features

- [x] **Video to Audio Conversion** - Convert multiple video formats to FLAC lossless audio
- [x] **LRC Lyrics Embedding** - Embed timestamped LRC lyrics into FLAC files
- [x] **Audio Clipping** - Extract audio from specified time with duration control
- [x] **Lyrics Time Adjustment** - Shift lyrics forward or backward by specified seconds
- [x] **Multi-encoding Support** - Auto-detect UTF-8, GBK, GB2312 and other encodings
- [x] **Metadata Extraction** - Extract artist, title, album info from LRC files
- [x] **Lyrics Viewer** - Quickly view embedded lyrics in FLAC files
- [x] **NetEase Cloud Music Support** - Lyrics display properly in NetEase Cloud Music (other players to be tested)

### 🚧 Upcoming Features

- [ ] Add cover art, artist, album name metadata editing
- [ ] One-click Bilibili video and lyrics download, one-click lossless music conversion (under consideration)

## Tool List

### 1. video_to_audio.py - Video to FLAC Converter
Specialized in video to FLAC format conversion and lyrics embedding with timestamp support for synchronized lyrics.

**Basic Usage:**
```bash
python video_to_audio.py <input_file> [options]
```

**Common Examples:**
```bash
# Extract audio from MP4, remove first 7 seconds, convert to FLAC and embed lyrics
python video_to_audio.py input.mp4 -ss 7 -l lyrics.lrc

# Extract audio from MP4, remove first 30 seconds, convert to FLAC and embed lyrics
python video_to_audio.py input.mp4 -ss 00:30 -l lyrics.lrc

# Start conversion from 30 seconds and embed lyrics
python video_to_audio.py video.mp4 -ss 30 -l lyrics.lrc

# Highest FLAC compression level
python video_to_audio.py audio.wav -c 8

# Specify output file
python video_to_audio.py audio.wav -o output.flac -l lyrics.lrc
```

**Parameters:**
- `-ss <time>` - Start trimming from specified time
- `-t <duration>` - Trim for specified duration
- `-o <output_file>` - Specify output file path
- `-l <LRC_file>` - Embed LRC lyrics file (keep timestamps)
- `-c <level>` - FLAC compression level (0-8, default 5)
- `-h, --help` - Show help information

### 2. lrc_time_adjuster.py - LRC Lyrics Time Adjuster
Adjust LRC file timestamps by shifting all lyrics forward or backward.

```bash
# Shift lyrics 7 seconds forward
python lrc_time_adjuster.py song.lrc -7

# Shift lyrics 5 seconds backward
python lrc_time_adjuster.py song.lrc 5
```

### 3. view_lyrics.py - FLAC Lyrics Viewer
Quickly view lyrics embedded in FLAC files.

```bash
# View lyrics in specified FLAC file
python view_lyrics.py music.flac

# View lyrics in all FLAC files in current directory
python view_lyrics.py
```

## Adding Lyrics to Existing Audio Files

You can also add lyrics to existing FLAC audio files without converting the audio:

### Basic Usage for Adding Lyrics

```bash
# Add lyrics to existing FLAC file (will modify the file in place)
python video_to_audio.py audio.flac -l lyrics.lrc

# Add lyrics and create a new file (recommended)
python video_to_audio.py audio.flac -l lyrics.lrc -o audio_with_lyrics.flac
```

### Workflow Example

```bash
# Step 1: Check if the audio file already has lyrics
python view_lyrics.py music.flac

# Step 2: Add lyrics to the audio file
python video_to_audio.py music.flac -l song.lrc -o music_with_lyrics.flac

# Step 3: Verify lyrics were added successfully
python view_lyrics.py music_with_lyrics.flac

# Step 4: If lyrics timing is incorrect, adjust them
python lrc_time_adjuster.py song.lrc -5  # Move lyrics 5 seconds forward
python video_to_audio.py music.flac -l song_-5s.lrc -o music_fixed.flac
```

### Notes
- The program automatically detects when input is already FLAC and no audio processing is needed
- Lyrics are embedded as metadata with timestamps preserved
- Maximum lyrics length is 2000 characters (will be truncated if longer)
- Supported LRC format: `[mm:ss.xx]lyrics` with standard metadata tags

## Test Files

Test files are provided in the `test` directory:

- `测试.mp4` - Test video file
- `胡彦斌——《纸短情长》_哔哩哔哩_bilibili.lrc` - Original lyrics file
- `胡彦斌——《纸短情长》_哔哩哔哩_bilibili-6.5s.lrc` - Time-adjusted lyrics file
- `测试2_trimmed_with_lyrics.flac` - FLAC file with embedded lyrics

## Bilibili Video Download

For downloading Bilibili videos, you can use the following Tampermonkey scripts:

1. **Bilibili Video Downloader**
   - Download URL: https://update.greasyfork.org/scripts/413228/bilibili%E8%A7%86%E9%A2%91%E4%B8%8B%E8%BD%BD.user.js
   - Install Tampermonkey browser extension
   - Visit the script URL and click "Install"
   - Go to any Bilibili video page and use the download button

2. **Bilibili CC Subtitle Tool**
   - Download URL: https://update.greasyfork.org/scripts/378513/Bilibili%20CC%E5%AD%97%E5%B9%95%E5%B7%A5%E5%85%B7.user.js
   - Use this tool to download CC subtitles which can be converted to LRC format

## Requirements

- Python 3.x
- FFmpeg (required)

### Install FFmpeg

1. Visit [FFmpeg official website](https://ffmpeg.org/download.html)
2. Download the version for your platform
3. Add FFmpeg to system PATH environment variable

## FAQ

1. **Q: Getting "FFmpeg not found" error?**
   A: Make sure FFmpeg is installed and added to your system PATH.

2. **Q: Do I need special software for FLAC lyrics?**
   A: No, lyrics are embedded directly into FLAC files using FFmpeg.

3. **Q: What audio formats are supported?**
   A: Input supports all FFmpeg-supported formats, output currently focuses on FLAC lossless format.

4. **Q: Lyrics timing is inaccurate?**
   A: Use the `lrc_time_adjuster.py` tool to adjust lyrics time offset.

## Technical Features

- **Lossless Compression**: FLAC format ensures no quality loss
- **Synchronized Lyrics**: Support timestamped lyrics for synchronized display in supporting music players
- **Metadata Preservation**: Automatically extract and preserve basic song information
- **Multi-encoding Support**: Intelligent detection of multiple text encodings
- **Flexible Trimming**: Support precise time positioning and duration control

## Development Status

The project is under continuous development. Welcome to submit issue reports and feature suggestions.

## License

This project is open source. Please check the LICENSE file for details.