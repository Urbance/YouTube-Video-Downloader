import tkinter as tk
import os
from tkinter import ttk
from tkinter import filedialog, messagebox

def get_targetdirectory():
    if e_targetdirectory.get() == '' and not isOutputFolderExists:
        os.mkdir(user_music)
        e_targetdirectory.insert(1, user_music)
        return

    if e_targetdirectory.get() == '' and isOutputFolderExists:
        e_targetdirectory.insert(1, user_music)
        return

    path = filedialog.askdirectory()
    e_targetdirectory.insert(1, path)

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
    get_targetdirectory()

    b_browse = tk.Button(settings, text="Durchsuchen", command=get_targetdirectory)
    b_browse.grid(row=2, column=0)

def download_process():
    print("Test")
    format_value = format.get()

    match format_value:
        case "Video":
            return
        case "Audio":
            return
        case _:
            messagebox.showerror("Fehler", "Bitte gebe ein gültiges Format an!")


def main_window():
    global format

    # window setup
    root.resizable(False, False)
    root.title("YouTube Video Downloader")

    # setup and set layouts
    label1 = tk.Label(text="Link zum YouTube-Video:")
    label1.grid(row=0, column=0)

    entry1 = tk.Entry()
    entry1.grid(row=0, column=1)

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
user_music = user_profile + "\Music\PyTube"

isOutputFolderExists = os.path.exists(user_music)

if not isOutputFolderExists:
    os.mkdir(user_music)


main_window()

root.mainloop()
