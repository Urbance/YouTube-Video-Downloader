import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def browse_directory():
    path = filedialog.askdirectory()
    return path
    entry2.insert(1, path)

def setup_settings():

    Window = tk.Toplevel()
    canvas = tk.Canvas(Window)
    canvas.grid(row=5, column=0)

    label2 = tk.Label(text="Pfad zum Speicherort")
    label2.grid(row=0, column=0)

    entry2 = tk.Entry()
    entry2.grid(row=0, column=0)

# window setup
root = tk.Tk()
root.resizable(False, False)
root.title("YouTube Video Downloader")


# setup and set layouts
label1 = tk.Label(text="Link zum YouTube-Video:")
label1.grid(row=0, column=0)

entry1 = tk.Entry()
entry1.grid(row=0, column=1)

combobox1 = ttk.Combobox(values=["Video", "Audio"])
combobox1.current(0)
combobox1.grid(row=0, column=2)

b_browse = tk.Button(text="Durchsuchen", command=browse_directory)
b_browse.grid(row=2, column=1)

b_addline = tk.Button(text="+")
b_addline.grid(row=3, column=0)

b_delline = tk.Button(text="-")
b_delline.grid(row=3, column=1)

b_download = tk.Button(text="Herunterladen")
b_download.grid(row=4, column=1)

b_settings = tk.Button(text="⚙️", bd=0, highlightthickness=0, command=setup_settings)
b_settings.grid(row=4, column=3)

root.mainloop()


# Multi-Downloading with adding more fields with button