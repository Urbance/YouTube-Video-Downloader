import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def startup_logic():
    # Erstellen eines Ausgabe-Ordners, falls nicht vorhanden und Pfad direkt im Entry speichern
    print("Work in Progress")

def get_targetdirectory():
    path = filedialog.askdirectory()
    e_targetdirectory.insert(1, path)

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

    b_browse = tk.Button(settings, text="Durchsuchen", command=get_targetdirectory)
    b_browse.grid(row=2, column=0)

def main_window():
    # window setup
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

    b_addline = tk.Button(text="+")
    b_addline.grid(row=3, column=0)

    b_delline = tk.Button(text="-")
    b_delline.grid(row=3, column=1)

    b_download = tk.Button(text="Herunterladen")
    b_download.grid(row=4, column=1)

    b_settings = tk.Button(text="⚙️", bd=0, highlightthickness=0, command=settings_window)
    b_settings.grid(row=4, column=3)

root = tk.Tk()

main_window()

root.mainloop()
