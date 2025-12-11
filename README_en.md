# Music Video to Lossless Audio Converter (Video to FLAC with Lyrics)

[English](README_en.md) | [中文说明](README.md)

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange.svg)](https://ffmpeg.org)

A professional music video converter tool that transforms music videos (MVs, live performances, music streams, etc.) into high-quality lossless FLAC audio with automatically embedded synchronized lyrics. Supports both GUI and command-line interfaces.

![GUI](dist/gui.png)

## Key Features

- 🎵 **Music Video Conversion**: Convert MVs, live performances, music streams to high-quality FLAC lossless audio
- 📝 **Synchronized Lyrics Embedding**: Perfect LRC format support with precise timestamps for synchronized display
- 🎼 **Professional Metadata**: Complete song information management (title, artist, album, date, genre, composer, lyricist, etc.)
- 🖼️ **Smart Cover Art Processing**: Multiple cover art support
  - Local image files (JPG/PNG/AVIF, etc.)
  - Web image URLs (auto-download)
  - Base64 encoded images
  - Special URLs from Bilibili, Weibo, etc. (auto-optimized)
- ✂️ **Precise Audio Trimming**: Support custom start time and duration for audio extraction
- 🌐 **Intelligent Encoding Detection**: Automatically handle UTF-8, GBK, GB2312 and various lyrics file encodings
- 🎚️ **Adjustable Compression Level**: 0-8 level FLAC compression to balance file size and audio quality

## Installation

### Requirements

- Python 3.7 or higher
- FFmpeg (for audio/video processing)

### Install Dependencies

```bash
pip install Pillow requests
```

### Install FFmpeg

- **Windows**: Download from [FFmpeg Official Website](https://ffmpeg.org/download.html)
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

Or use the project's download helper:

```bash
python download_ffmpeg.py
```

## Quick Start

### 1. GUI Mode (Recommended)

#### Run GUI Application

```bash
python video_to_audio_gui.py
```

#### Package as Standalone EXE

```bash
# Method 1: Using batch script (Recommended)
Double-click: 一键打包.bat

# Method 2: Using Python script
pip install pyinstaller
python build_exe.py
```

The packaged exe file will be located in the `dist` directory and can run on Windows computers without Python environment.

### 2. Command Line Mode

#### Basic Usage

```bash
# Basic conversion
python video_to_audio.py input.mp4

# Embed lyrics
python video_to_audio.py input.mp4 -l lyrics.lrc

# Add metadata
python video_to_audio.py input.mp4 -metadata metadata.txt

# Embed lyrics and metadata simultaneously
python video_to_audio.py input.mp4 -l lyrics.lrc -metadata metadata.txt

# All features combined
python video_to_audio.py video.mp4 -ss 01:00 -t 03:00 -l lyrics.lrc -metadata metadata.txt -c 8
```

#### Parameters

- `-ss <time>`: Start from specified time (e.g., 30 or 01:30)
- `-t <duration>`: Trim specified duration (e.g., 60 or 02:00)
- `-o <output_file>`: Specify output file
- `-l <LRC_file>`: Embed lyrics file
- `-metadata <file>`: Add metadata from metadata file
- `-c <level>`: FLAC compression level (0-8, default 5)

## Project Structure

```
videoToAudioWithLRC/
├── 🎯 Core Programs
│   ├── video_to_audio_gui.py      # GUI application main program
│   └── video_to_audio.py          # Command-line version
├── 🔧 Core Modules
│   └── flac_metadata_utils.py     # Lyrics embedding and metadata processing core
├── 🛠️ Utility Tools
│   ├── lrc_time_adjuster.py       # Lyrics time adjustment tool
│   ├── view_lyrics.py             # Lyrics viewer tool
│   └── download_ffmpeg.py        # FFmpeg auto-download helper
├── 📦 Packaging Tools
│   ├── build_exe.py              # Package as standalone exe
│   └── create_portable_package.py # Create portable version
├── 🚀 Quick Start
│   ├── 一键打包.bat               # Windows one-click packaging script
│   └── 启动GUI.bat                # Windows quick GUI launch script
├── 🧪 Testing
│   └── new_test/                  # Unit test directory
└── 📚 Documentation
    └── README.md                  # Project documentation
```

## Metadata File Format

Create a `metadata.txt` file:

```text
Title(TITLE): Song Name
Artist(ARTIST): Artist Name
Album(ALBUM): Album Name
Date(DATE): 2025-12-11
Genre(GENRE): Pop
Composer(COMPOSER): Composer
Lyricist(LYRICIST): Lyricist
Cover Image(COVER_IMAGE): /path/to/image.jpg
Cover Image(COVER_IMAGE): https://example.com/image.jpg
Cover Image(COVER_IMAGE): data:image/jpeg;base64,/9j/4AAQ...
```

### Supported Image Formats

#### Web Images

- Regular URL: `https://example.com/image.jpg`
- Bilibili format: `https://i2.hdslb.com/bfs/archive/xxx.jpg@672w_378h_1c_!web-search-common-cover.avif`

#### Base64 Images

```
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...
```

#### Local Images

- JPEG/JPG
- PNG (with transparency support)
- AVIF (automatically converted to JPEG)

## Testing

Run unit tests:

```bash
# Run all tests
python new_test/run_all_tests.py

# Create sample test files
python new_test/test_flac_metadata_utils.py --create-samples

# Create manual test guide
python new_test/test_video_to_audio.py --create-guide
```

## GUI Features

### 1. File Selection

- Support selecting video or audio files as input
- Support selecting LRC lyrics files (optional)
- Support selecting metadata files (optional)
- Support custom output file paths

### 2. Parameter Settings

- Set start time (trim start position)
- Set duration (trim length)
- FLAC compression level slider adjustment (0-8)

### 3. Execution and Feedback

- Real-time execution log display
- Different log types with color differentiation
- Automatic notification upon completion
- One-click open output folder

## Music Video Conversion Workflow

```
📹 Music Video (MV/Live Performance/Music Stream)
     ↓
🎵 Extract Audio and Convert to FLAC Lossless Format
     ↓
📝 Embed LRC Synchronized Lyrics (preserve timestamps)
     ↓
🎼 Add Song Metadata (title/artist/album/etc.)
     ↓
🖼️ Embed Cover Art
     ↓
🎧 Output Complete FLAC File (lossless audio + lyrics + cover)
```

## Usage Tips

1. **Lyrics File Preparation**:
   - Use lyrics files that exactly match the video content
   - Ensure timestamps are accurate for synchronized lyrics display
   - Multiple encodings supported, no conversion needed for Chinese lyrics

2. **Batch Processing Music Videos**:
   - Write batch scripts to process multiple MVs at once
   - Use unified metadata templates for efficiency
   - Recommend each video to have its corresponding lyrics file

3. **Audio Quality Optimization**:
   - Choose higher FLAC compression levels (5-8) for better audio quality
   - Preserve original audio sample rate, avoid downsampling
   - Ensure video source has sufficient audio quality

4. **Metadata Completion**:
   - Accurately fill song information for music player recognition
   - Use high-resolution cover art, recommend 1000x1000 pixels or above
   - Include detailed information like composer and lyricist

## Frequently Asked Questions

### 1. FFmpeg Not Installed

```
Error: FFmpeg not found
```

**Solution**:

- Run `python download_ffmpeg.py` to download automatically
- Or download and install from https://ffmpeg.org/download.html

### 2. Insufficient Memory

Memory issues may occur when processing large files
**Solution**: Process in batches or use a more powerful machine

### 3. Encoding Issues

```
UnicodeDecodeError
```

**Solution**: Ensure files are saved with UTF-8 encoding

### 4. Permission Issues

```
Error: Unable to write file
```

**Solution**: Check file permissions and ensure write access

## Development Notes

### Tech Stack

- **Python 3**: Main programming language
- **Tkinter**: GUI framework
- **FFmpeg**: Audio/video processing engine
- **PIL/Pillow**: Image processing
- **PyInstaller**: Packaging tool

### Code Structure

- `video_to_audio.py`: Command-line main program, calls flac_metadata_utils for metadata processing
- `video_to_audio_gui.py`: GUI main program, provides graphical operation interface
- `flac_metadata_utils.py`: Core metadata processing functionality
  - Lyrics processing (parse_lrc_file, embed_lyrics_to_flac)
  - Metadata read/write (parse_metadata_file, write_metadata_to_flac)
  - Image processing (download_image, prepare_cover_image)
  - Information extraction (get_flac_metadata, display_metadata)

### Extending Features

You can add more features by modifying corresponding modules:

- Support more audio formats (AAC, OGG, etc.)
- Add more metadata fields
- Support more image formats
- Implement batch conversion functionality

## Changelog

### v2.0.0 (2025-12-11)

- ✨ Brand new GUI interface for more intuitive operation
- ✨ Support packaging as standalone exe, no Python installation required
- ✨ FFmpeg automatic download and configuration
- 🎵 Optimized music video processing logic
- 📝 Improved lyrics embedding algorithm, perfectly preserves timestamps
- 🖼️ Enhanced image processing, supports special URLs from Bilibili, Weibo, etc.
- 📚 Improved documentation and usage guides

### v1.0.0 (2025-12-10)

- 🎉 Project initial release
- ✨ Core functionality: music video to FLAC conversion
- ✨ LRC lyrics embedding support
- ✨ Complete metadata management system

## Contributing

Welcome to submit Issues and Pull Requests!

1. Fork this project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- [FFmpeg](https://ffmpeg.org) - Powerful audio/video processing tool
- [Pillow](https://pillow.readthedocs.io) - Friendly Python image processing library
- [PyInstaller](https://pyinstaller.readthedocs.io) - Python program packaging tool

---

If this project helps you, please give it a ⭐️!
