import tkinter as tk
import os
import pytube
from tkinter import ttk
from tkinter import filedialog, messagebox

def update_directory():
    global outputfolder
    outputfolder = filedialog.askdirectory()
    e_targetdirectory.delete(0, "end")
    e_targetdirectory.insert(1, outputfolder)

def set_targetdirectory():
    if not isOutputFolderExists and e_targetdirectory.get() == '':
        os.mkdir(outputfolder)
        e_targetdirectory.insert(1, outputfolder)

    if isOutputFolderExists and e_targetdirectory.get() == '':
        e_targetdirectory.insert(1, outputfolder)

def open_outputfolder():
    os.startfile(outputfolder)

def settings_window():
    global e_targetdirectory

    # window setup
    settings = tk.Toplevel()
    settings.title("YouTube Video Downloader - Einstellungen")
    settings.resizable(False, False)

    # setup objects
    label2 = ttk.Label(settings, text="Pfad zum Speicherort")
    label2.grid(row=0, column=0)
    e_targetdirectory = ttk.Entry(settings)
    e_targetdirectory.grid(row=1, column=0, ipadx=20)
    b_browse = ttk.Button(settings, text="Durchsuchen", command=update_directory)
    b_browse.grid(row=2, column=0)
    l_language = ttk.Label(settings, text="Sprache")
    l_language.grid(row=3, column=0)
    c_language = ttk.Combobox(settings, values=["Deutsch"], state="readonly")
    c_language.current(0)
    c_language.grid(row=4, column=0)

    set_targetdirectory()

def download_process():
    format_value = format.get()
    youtubelink = e_youtubelink.get()
    targetdirectory = outputfolder
    get_video = pytube.YouTube(youtubelink)
    video_title = get_video.title

    try:
        match format_value:
            case "Video":
                get_video.streams.filter(file_extension='mp4').get_highest_resolution().download(outputfolder)
            case "Audio":
                get_video = get_video.streams.filter(only_audio=True).first().download(targetdirectory)
                file, ext = os.path.splitext(get_video)
                new_file = file + '.mp3'
                os.rename(get_video, new_file)
            case _:
                messagebox.showerror("Fehler", "Bitte gebe ein gültiges Format an!")
    except FileExistsError:
        messagebox.showerror("Fehler", "Die Datei existiert bereits!")

    messagebox.showinfo("YouTube Video Downloader",
                        'Das Video "' + video_title + '"\n' + "wurde unter folgenden Pfad gespeichert:\n" + outputfolder)

def main_window():
    global format
    global e_youtubelink

    # window setup
    # TODO center main window
    root.resizable(False, False)
    root.title("YouTube Video Downloader")
    root.geometry("+300+300")

    # setup and set layouts
    label1 = tk.Label(text="Link zum YouTube-Video:")
    label1.grid(row=0, column=0)
    e_youtubelink = tk.Entry()
    e_youtubelink.grid(row=0, column=1)
    c_format = ttk.Combobox(values=["Video", "Audio"], state="readonly")
    c_format.current(0)
    c_format.grid(row=0, column=2)
    # b_addline = tk.Button(text="+")
    # b_addline.grid(row=3, column=0)
    # b_delline = tk.Button(text="-")
    # b_delline.grid(row=3, column=1)
    b_download = tk.Button(text="Herunterladen", command=download_process)
    b_download.grid(row=4, column=1)
    b_open_outputfolder = tk.Button(text="Ausgabe-Ordner", command=open_outputfolder)
    b_open_outputfolder.grid(row=4, column=0)
    b_settings = tk.Button(text="⚙️", bd=0, highlightthickness=0, command=settings_window)
    b_settings.grid(row=4, column=3)

root = tk.Tk()

user_profile = os.environ['USERPROFILE']
outputfolder = user_profile + "\Music\PyTube"

isOutputFolderExists = os.path.exists(outputfolder)

main_window()

root.mainloop()