import tkinter as tk
import os
import pytube
from tkinter import ttk
from tkinter import filedialog, messagebox

def get_targetdirectory():
    #e_targetdirectory.insert(1, user_outputfolder)

    filedialog.askdirectory()

    # if e_targetdirectory.get() == '' and not isOutputFolderExists:
    #     os.mkdir(user_music)
    #     e_targetdirectory.insert(1, user_music)
    #     return
    #
    # if e_targetdirectory.get() == '' and isOutputFolderExists:
    #     e_targetdirectory.insert(1, user_music)
    #     return
    #
    # path = filedialog.askdirectory()
    # e_targetdirectory.insert(1, path)

    # Fälle überprüfen

def settings_window():
    global e_targetdirectory

    # window setup
    settings = tk.Toplevel()
    settings.title("YouTube Video Downloader - Einstellungen")
    settings.resizable(False, False)
    settings.geometry("150x100")

    # setup objects
    label2 = tk.Label(settings, text="Pfad zum Speicherort")
    label2.grid(row=0, column=0)

    e_targetdirectory = tk.Entry(settings)
    e_targetdirectory.grid(row=1, column=0)
#    get_targetdirectory(

    b_browse = tk.Button(settings, text="Durchsuchen", command=get_targetdirectory)
    b_browse.grid(row=2, column=0)

def download_process():
    format_value = format.get()
    youtubelink = e_youtubelink.get()
    targetdirectory = user_outputfolder

    get_video = pytube.YouTube(youtubelink)

    match format_value:
        case "Video":
            get_video.streams.filter(file_extension='mp4').get_highest_resolution().download(user_outputfolder)
            messagebox.showinfo("YouTube Video Downloader", "Das Video wurde als .mp4 heruntergeladen.")
            return
        case "Audio":
            get_video = get_video.streams.filter(only_audio=True).first().download(targetdirectory)
            file, ext = os.path.splitext(get_video)
            new_file = file + '.mp3'
            os.rename(get_video, new_file)
            messagebox.showinfo("YouTube Video Downloader", "Das Video wurde als .mp3 heruntergeladen.")
            return
        case _:
            messagebox.showerror("Fehler", "Bitte gebe ein gültiges Format an!")


def main_window():
    global format
    global e_youtubelink

    # window setup
    root.resizable(False, False)
    root.title("YouTube Video Downloader")

    # setup and set layouts
    label1 = tk.Label(text="Link zum YouTube-Video:")
    label1.grid(row=0, column=0)

    e_youtubelink = tk.Entry()
    e_youtubelink.grid(row=0, column=1)

    format = ttk.Combobox(values=["Video", "Audio"], state="readonly")
    format.current(0)
    format.grid(row=0, column=2)

    # b_addline = tk.Button(text="+")
    # b_addline.grid(row=3, column=0)

    # b_delline = tk.Button(text="-")
    # b_delline.grid(row=3, column=1)

    b_download = tk.Button(text="Herunterladen", command=download_process)
    b_download.grid(row=4, column=1)

    b_settings = tk.Button(text="⚙️", bd=0, highlightthickness=0, command=settings_window)
    b_settings.grid(row=4, column=3)

    # create output-folder button

root = tk.Tk()

user_profile = os.environ['USERPROFILE']
user_outputfolder = user_profile + "\Music\PyTube"

isOutputFolderExists = os.path.exists(user_outputfolder)

if not isOutputFolderExists:
    os.mkdir(user_outputfolder)


main_window()

root.mainloop()