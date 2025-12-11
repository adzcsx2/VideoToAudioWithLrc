# Video to FLAC Audio Converter

[English](README_en.md) | [中文说明](README.md)

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange.svg)](https://ffmpeg.org)

A fully-featured video to FLAC audio converter tool with lyrics embedding and metadata management. The project provides both command-line interface and graphical user interface.

![GUI](dist/gui.png)

## Key Features

- **Video to Audio Conversion**: Convert video files (MP4, AVI, MKV, etc.) to FLAC lossless audio
- **Lyrics Embedding**: Support LRC format lyrics embedding with timestamps
- **Metadata Management**: Add song information (title, artist, album, date, genre, etc.)
- **Cover Art Support**: Support multiple cover art formats
  - Local image paths
  - Web image URLs
  - Base64 encoded images
  - Bilibili special format URLs
- **Format Conversion**: Automatically convert AVIF and other formats to JPEG
- **Audio Trimming**: Support precise time positioning and duration control
- **Multi-encoding Support**: Automatically detect UTF-8, GBK, GB2312 and other encodings

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
├── video_to_audio.py          # Command-line main program
├── video_to_audio_gui.py      # GUI application program
├── flac_metadata_utils.py     # Core metadata processing module
├── lrc_time_adjuster.py       # Lyrics time adjustment tool
├── view_lyrics.py             # Lyrics viewer tool
├── build_exe.py              # Script to package as exe
├── create_portable_package.py # Script to create portable package
├── download_ffmpeg.py        # FFmpeg download helper
├── test/                      # Test files directory
│   ├── *.mp4                  # Test videos
│   ├── *.lrc                  # Test lyrics
│   ├── *.txt                  # Test metadata
│   └── *.flac                 # Generated audio files
├── new_test/                  # Unit test directory
│   ├── test_flac_metadata_utils.py
│   ├── test_video_to_audio.py
│   └── run_all_tests.py
└── README.md                  # This documentation
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

## Workflow Diagram

```
Input File (MP4/AVI/etc.)
     ↓
Video to FLAC (FFmpeg)
     ↓
[Optional] Embed Lyrics
     ↓
[Optional] Add Metadata (from metadata.txt)
     ↓
Output FLAC File (with lyrics and/or metadata)
```

## Usage Tips

1. **Batch Processing**: You can write batch scripts to process multiple files
2. **Metadata Templates**: Create metadata template files in different styles for reuse
3. **Auto Naming**: When output file is not specified, program automatically generates marked file names
4. **Error Debugging**: Check log output for detailed processing information

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

- Added GUI interface
- Support packaging as standalone exe file
- Added FFmpeg auto-download feature
- Optimized image processing, support Bilibili special URLs
- Improved documentation and test cases

### v1.0.0 (2025-12-10)

- Initial release
- Support video to FLAC conversion
- Support lyrics embedding
- Support metadata management

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
