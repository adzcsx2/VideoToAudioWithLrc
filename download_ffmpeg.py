#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFmpeg下载助手
帮助用户下载并安装FFmpeg
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

def is_ffmpeg_installed():
    """检查FFmpeg是否已安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_ffmpeg_url():
    """获取FFmpeg下载链接"""
    if sys.platform == "win32":
        return "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    else:
        return None

def download_ffmpeg(url, save_path):
    """下载FFmpeg"""
    def report_progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        progress_bar['value'] = percent
        root.update_idletasks()
        progress_label.config(text=f"下载进度: {percent}%")

    try:
        urllib.request.urlretrieve(url, save_path, reporthook=report_progress)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"下载失败: {str(e)}")
        return False

def extract_ffmpeg(zip_path, extract_to):
    """解压FFmpeg"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # 查找ffmpeg.exe
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                if file.lower() == 'ffmpeg.exe':
                    ffmpeg_path = os.path.join(root, file)
                    # 复制到目标目录
                    target_path = os.path.join(os.path.dirname(extract_to), 'ffmpeg.exe')
                    subprocess.run(['copy', ffmpeg_path, target_path], shell=True)
                    return True
        return False
    except Exception as e:
        messagebox.showerror("错误", f"解压失败: {str(e)}")
        return False

def main():
    global root, progress_bar, progress_label

    root = tk.Tk()
    root.title("FFmpeg下载助手")
    root.geometry("400x200")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 标题
    ttk.Label(main_frame, text="FFmpeg下载助手", font=('', 16)).pack(pady=(0, 20))

    # 检查FFmpeg
    if is_ffmpeg_installed():
        ttk.Label(main_frame, text="✓ FFmpeg已安装", foreground="green", font=('', 12)).pack(pady=10)
        ttk.Button(main_frame, text="退出", command=root.quit).pack(pady=20)
        root.mainloop()
        return

    # 说明文字
    ttk.Label(main_frame, text="FFmpeg是本程序必需的组件", font=('', 12)).pack(pady=(0, 10))

    # 下载按钮
    download_button = ttk.Button(main_frame, text="下载并安装FFmpeg", command=lambda: start_download())
    download_button.pack(pady=10)

    # 进度条
    progress_label = ttk.Label(main_frame, text="")
    progress_label.pack(pady=(10, 5))

    progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
    progress_bar.pack(pady=(0, 20))

    def start_download():
        download_button.config(state='disabled')

        # 获取下载链接
        url = get_ffmpeg_url()
        if not url:
            messagebox.showerror("错误", "不支持的操作系统")
            root.quit()
            return

        # 下载路径
        script_dir = Path(__file__).parent
        zip_path = script_dir / "ffmpeg.zip"

        progress_label.config(text="正在下载...")

        # 下载
        if download_ffmpeg(url, zip_path):
            progress_label.config(text="正在解压...")
            progress_bar.config(mode='indeterminate')
            progress_bar.start()

            # 解压
            if extract_ffmpeg(zip_path, script_dir / "ffmpeg_temp"):
                # 清理
                os.remove(zip_path)
                import shutil
                shutil.rmtree(script_dir / "ffmpeg_temp", ignore_errors=True)

                progress_label.config(text="安装完成！")
                messagebox.showinfo("成功", "FFmpeg已成功安装！\n\nffmpeg.exe已下载到程序目录")
                root.quit()
            else:
                progress_label.config(text="解压失败")
                download_button.config(state='normal')

    root.mainloop()

if __name__ == "__main__":
    main()