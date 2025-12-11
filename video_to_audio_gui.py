#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转音频GUI界面
支持FLAC格式转换、歌词嵌入和元数据添加
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
from pathlib import Path
import subprocess
import queue
import time

# 导入核心功能
from video_to_audio import process_media, parse_time, DEFAULT_FLAC_COMPRESSION

class VideoToAudioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("视频转FLAC音频工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 文件路径
        self.media_file = tk.StringVar()
        self.lrc_file = tk.StringVar()
        self.metadata_file = tk.StringVar()
        self.output_file = tk.StringVar()

        # 参数设置
        self.start_time = tk.StringVar(value="00:00")
        self.duration = tk.StringVar()
        self.compression_level = tk.IntVar(value=5)

        # 日志队列
        self.log_queue = queue.Queue()

        # 创建界面
        self.create_widgets()

        # 启动日志更新
        self.update_log()

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)

        # 视频或音频文件
        ttk.Label(file_frame, text="视频/音频文件:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.media_file, width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(file_frame, text="浏览...", command=self.browse_media_file).grid(row=0, column=2, pady=2)

        # LRC歌词文件
        ttk.Label(file_frame, text="歌词文件 (LRC):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.lrc_file, width=60).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(file_frame, text="浏览...", command=self.browse_lrc_file).grid(row=1, column=2, pady=2)

        # 元数据文件
        ttk.Label(file_frame, text="元数据文件:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.metadata_file, width=60).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(file_frame, text="浏览...", command=self.browse_metadata_file).grid(row=2, column=2, pady=2)

        # 输出文件
        ttk.Label(file_frame, text="输出文件 (可选):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.output_file, width=60).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(file_frame, text="浏览...", command=self.browse_output_file).grid(row=3, column=2, pady=2)

        # 参数设置区域
        param_frame = ttk.LabelFrame(main_frame, text="转换参数", padding="10")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        param_frame.columnconfigure(1, weight=1)

        # 开始时间
        ttk.Label(param_frame, text="开始时间:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.start_time, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Label(param_frame, text="格式: 30 或 01:30").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))

        # 持续时间
        ttk.Label(param_frame, text="持续时间:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.duration, width=20).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(param_frame, text="格式: 60 或 02:00").grid(row=1, column=2, sticky=tk.W, padx=(10, 0))

        # 压缩级别
        ttk.Label(param_frame, text="FLAC压缩级别:").grid(row=2, column=0, sticky=tk.W, pady=2)
        compression_frame = ttk.Frame(param_frame)
        compression_frame.grid(row=2, column=1, sticky=tk.W, pady=2)

        ttk.Scale(compression_frame, from_=0, to=8, orient=tk.HORIZONTAL,
                 variable=self.compression_level, length=150).grid(row=0, column=0)
        self.compression_label = ttk.Label(compression_frame, text="5")
        self.compression_label.grid(row=0, column=1, padx=(5, 0))
        self.compression_level.trace('w', self.update_compression_label)

        # 执行按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.execute_button = ttk.Button(button_frame, text="执行转换", command=self.execute_conversion)
        self.execute_button.grid(row=0, column=0, padx=(0, 5))

        ttk.Button(button_frame, text="清空日志", command=self.clear_log).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="打开输出文件夹", command=self.open_output_folder).grid(row=0, column=2)

        # 日志显示区域
        log_frame = ttk.LabelFrame(main_frame, text="执行日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置标签颜色
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("SUCCESS", foreground="green")
        self.log_text.tag_configure("ERROR", foreground="red")
        self.log_text.tag_configure("WARNING", foreground="orange")

    def update_compression_label(self, *args):
        self.compression_label.config(text=str(self.compression_level.get()))

    def browse_media_file(self):
        filetypes = [
            ("媒体文件", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.mp3 *.wav *.flac"),
            ("视频文件", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv"),
            ("音频文件", "*.mp3 *.wav *.flac"),
            ("所有文件", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.media_file.set(filename)
            # 自动设置输出文件名
            if not self.output_file.get():
                media_path = Path(filename)
                output = media_path.parent / f"{media_path.stem}_output.flac"
                self.output_file.set(str(output))

    def browse_lrc_file(self):
        filetypes = [
            ("LRC文件", "*.lrc"),
            ("所有文件", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.lrc_file.set(filename)

    def browse_metadata_file(self):
        filetypes = [
            ("文本文件", "*.txt"),
            ("所有文件", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.metadata_file.set(filename)

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".flac",
            filetypes=[
                ("FLAC文件", "*.flac"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)

    def execute_conversion(self):
        # 验证输入
        if not self.media_file.get():
            messagebox.showerror("错误", "请选择视频或音频文件")
            return

        # 禁用按钮
        self.execute_button.config(state='disabled')

        # 在新线程中执行转换
        thread = threading.Thread(target=self._execute_conversion_thread)
        thread.daemon = True
        thread.start()

    def _execute_conversion_thread(self):
        try:
            # 解析参数
            media_path = self.media_file.get()
            lrc_path = self.lrc_file.get() if self.lrc_file.get() else None
            metadata_path = self.metadata_file.get() if self.metadata_file.get() else None
            output_path = self.output_file.get() if self.output_file.get() else None

            # 解析时间
            start_time = None
            if self.start_time.get():
                start_time = parse_time(self.start_time.get())
                if start_time is None:
                    self.log("错误: 无法解析开始时间", "ERROR")
                    return
                self.log(f"开始时间: {self.start_time.get()} ({start_time}秒)", "INFO")

            duration = None
            if self.duration.get():
                duration = parse_time(self.duration.get())
                if duration is None:
                    self.log("错误: 无法解析持续时间", "ERROR")
                    return
                self.log(f"持续时间: {self.duration.get()} ({duration}秒)", "INFO")

            self.log("开始转换...", "INFO")
            self.log(f"输入文件: {media_path}", "INFO")
            self.log(f"歌词文件: {lrc_path}", "INFO")
            self.log(f"元数据文件: {metadata_path}", "INFO")
            self.log(f"输出文件: {output_path}", "INFO")
            self.log(f"FLAC压缩级别: {self.compression_level.get()}", "INFO")

            # 执行转换
            success = process_media(
                media_path,
                output_path,
                start_time,
                duration,
                lrc_path,
                self.compression_level.get(),
                metadata_path
            )

            if success:
                self.log("转换成功!", "SUCCESS")
                # 输出文件路径
                if not output_path:
                    media = Path(media_path)
                    suffix = "_trimmed_with_metadata.flac"
                    if lrc_path or metadata_path:
                        suffix = "_trimmed_with_metadata.flac"
                    output_path = str(media.parent / f"{media.stem}{suffix}")

                self.log(f"输出文件: {output_path}", "SUCCESS")

                # 询问是否打开输出文件夹
                self.root.after(0, lambda: messagebox.showinfo("完成",
                    f"转换成功完成!\n\n输出文件:\n{output_path}\n\n是否打开输出文件夹?",
                    type=messagebox.YESNO, command=lambda r: self.open_output_folder() if r == 'yes' else None))
            else:
                self.log("转换失败!", "ERROR")
                self.root.after(0, lambda: messagebox.showerror("错误", "转换失败，请检查日志"))

        except Exception as e:
            self.log(f"错误: {str(e)}", "ERROR")
            self.root.after(0, lambda: messagebox.showerror("错误", f"转换过程中发生错误:\n{str(e)}"))
        finally:
            # 重新启用按钮
            self.root.after(0, lambda: self.execute_button.config(state='normal'))

    def log(self, message, level="INFO"):
        """添加日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_queue.put((f"[{timestamp}] {message}", level))

    def update_log(self):
        """更新日志显示"""
        try:
            while True:
                message, level = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n", level)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.update_log)

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)

    def open_output_folder(self):
        """打开输出文件夹"""
        output_path = self.output_file.get()
        if not output_path:
            # 使用默认输出文件夹
            media_path = self.media_file.get()
            if media_path:
                output_path = Path(media_path).parent
            else:
                output_path = Path.cwd()
        else:
            output_path = Path(output_path).parent

        # 打开文件夹
        if sys.platform == "win32":
            os.startfile(str(output_path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(output_path)])
        else:
            subprocess.run(["xdg-open", str(output_path)])

def main():
    root = tk.Tk()
    app = VideoToAudioGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()