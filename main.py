
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
from pathlib import Path


def download_audio():
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning(
            "Missing URL",
            "Please enter a YouTube URL."
        )
        return

    folder = filedialog.askdirectory(
        title="Choose download folder"
    )

    if not folder:
        return

    download_button.config(state="disabled")
    status_label.config(text="Preparing download...")

    def worker():
        try:
            quality = quality_var.get()

            options = {
                "format": "bestaudio/best",
                "outtmpl": str(
                    Path(folder) / "%(title)s.%(ext)s"
                ),
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality,
                }],
                "quiet": True,
            }

            with yt_dlp.YoutubeDL(options) as downloader:
                downloader.download([url])

            root.after(
                0,
                lambda: status_label.config(
                    text="Download completed!"
                )
            )
            root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success",
                    "Your audio download is complete!"
                )
            )

        except Exception as error:
            error_message = str(error)

            root.after(
                0,
                lambda msg=error_message: status_label.config(
                    text="Download failed."
                )
            )
            root.after(
                0,
                lambda msg=error_message: messagebox.showerror(
                    "Download Error", msg
                )
            )

        finally:
            root.after(
                0,
                lambda: download_button.config(state="normal")
            )

    threading.Thread(target=worker, daemon=True).start()


root = tk.Tk()
root.title("YT Music Downloader")
root.geometry("480x300")
root.resizable(False, False)
root.configure(bg="#151515")

title = tk.Label(
    root,
    text="YT MUSIC DOWNLOADER",
    font=("Arial", 18, "bold"),
    fg="#1DB954",
    bg="#151515"
)
title.pack(pady=(25, 18))

url_entry = tk.Entry(
    root,
    width=48,
    font=("Arial", 11),
    bg="#252525",
    fg="white",
    insertbackground="white",
    relief="flat"
)
url_entry.pack(ipady=9, padx=20)
url_entry.insert(0, "Paste YouTube URL here")

quality_var = tk.StringVar(value="192")

quality_row = tk.Frame(root, bg="#151515")
quality_row.pack(pady=15)

tk.Label(
    quality_row,
    text="MP3 quality:",
    fg="white",
    bg="#151515",
    font=("Arial", 10)
).pack(side="left", padx=8)

quality_menu = ttk.Combobox(
    quality_row,
    textvariable=quality_var,
    values=["128", "192", "256", "320"],
    width=10,
    state="readonly"
)
quality_menu.pack(side="left")

download_button = tk.Button(
    root,
    text="DOWNLOAD AUDIO",
    command=download_audio,
    bg="#1DB954",
    fg="black",
    activebackground="#1ed760",
    font=("Arial", 11, "bold"),
    relief="flat",
    cursor="hand2"
)
download_button.pack(pady=8, ipadx=25, ipady=8)

status_label = tk.Label(
    root,
    text="Ready to download",
    fg="#bbbbbb",
    bg="#151515",
    font=("Arial", 9)
)
status_label.pack(pady=8)

root.mainloop()
