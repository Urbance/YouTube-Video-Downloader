import json
import os
import tkinter as tk
import tkinter.font as font
from tkinter import W, Misc, filedialog, messagebox, ttk
import pytube

def setup_config_file():
    global outputfolder

    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            data = json.load(config_file)
            outputfolder = data['output_folder']
        return

    outputfolder = os.environ['USERPROFILE'] + "\Music\YouTube-Video-Downloader"
    config_values = {
        "language": "English",
        "output_folder": outputfolder
    }

    with open('config.json', 'w') as file:
        json.dump(config_values, file, indent=4)

def create_lang_en_file():
    if os.path.exists('lang_en.json'):
        return

    values = {
        "download": "Download",
        "format_option_audio": "Audio",
        "format_option_video": "Video",
        "link_to_youtube_video": "Link to YouTube-Video",
        "output_folder": "Open output-folder",
        "path_to_location": "Path to location",
        "browse": "Browse",
        "language": "Language",
        "restart_program": "Please restart the application.",
        "window_settings_title": "YouTube Video Downloader - Settings",
        "file_already_exists": "This file is already existing.",
        "unknown_file_format": "Please enter a valid file format.",
        "download_successfully": "The Video \"%video_title%\" successfully downloaded at \"%video_output_path%\".",
        "invalid_youtube_link": "Please enter a valid youtube link.",
        "settings_confirm": "Confirm"
    }

    with open('lang_en.json', 'w') as file:
        json.dump(values, file, indent=4)


def create_lang_de_file():
    if os.path.exists('lang_de.json'):
        return

    values = {
        "download": "Herunterladen",
        "format_option_audio": "Audio",
        "format_option_video": "Video",
        "link_to_youtube_video": "Link zum YouTube-Video",
        "output_folder": "Öffne Ausgabe-Ordner",
        "path_to_location": "Pfad zum Speicherort",
        "browse": "Durchsuchen",
        "language": "Sprache",
        "restart_program": "Die Anwendung muss neugestartet werden, damit die Änderung sichtbar wird.",
        "window_settings_title": "YouTube Video Downloader - Einstellungen",
        "file_already_exists": "Die Datei existiert bereits.",
        "unknown_file_format": "Bitte gebe ein gültiges Format an.",
        "download_successfully": "Das Video \"%video_title%\" wurde unter dem Pfad \"%video_output_path%\" gespeichert.",
        "invalid_youtube_link": "Bitte gebe einen gültigen YouTube-Link an.",
        "settings_confirm": "Bestätigen"
    }

    with open('lang_de.json', 'w') as file:
        json.dump(values, file, indent=4)


def update_directory():
    global outputfolder

    outputfolder = filedialog.askdirectory()
    e_targetdirectory.delete(0, "end")
    e_targetdirectory.insert(1, outputfolder)

    with open('config.json', 'r') as file:
        data = json.load(file)

    data['output_folder'] = outputfolder

    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def set_language():
    global c_language

    match config['language']:
        case 'English':
            c_language.current(0)
        case 'Deutsch':
            c_language.current(1)

def update_language(event):
    language = c_language.get()

    with open('config.json', 'w') as file:
        config['language'] = language
        json.dump(config, file, indent=4)

    messagebox.showinfo("YouTube Video Downloader", translation['restart_program'])

def open_outputfolder():
    os.startfile(outputfolder)

def close_settings_window():
    settings.destroy()
    root.deiconify()

def download_process():
    if e_youtubelink.get() == '':
        messagebox.showerror('YouTube Video Downloader', translation['invalid_youtube_link'])
        return

    format_value = options_var.get()
    youtubelink = e_youtubelink.get()
    get_video = pytube.YouTube(youtubelink)
    video_title = get_video.title

    try:
        match format_value:
            case "Video":
                get_video.streams.filter(file_extension='mp4').get_highest_resolution().download(outputfolder)
            case "Audio":
                get_video = get_video.streams.filter(only_audio=True).first().download(outputfolder)
                file, ext = os.path.splitext(get_video)
                new_file = file + '.mp3'
                os.rename(get_video, new_file)
            case _:
                messagebox.showerror("YouTube Video Downloader", translation['unknown_file_format'])
    except FileExistsError:
        messagebox.showerror("YouTube Video Downloader", translation['file_already_exists'])
        return

    successfully_downloaded = translation['download_successfully']
    successfully_downloaded = successfully_downloaded.replace('%video_title%', video_title)
    successfully_downloaded = successfully_downloaded.replace('%video_output_path%', outputfolder)
    messagebox.showinfo("YouTube Video Downloader", successfully_downloaded)

def settings_window():
    # global e_targetdirectory
    global c_language
    global settings

    # vanish root window
    root.withdraw()

    # window setup
    settings = tk.Toplevel()
    settings.title(translation['window_settings_title'])
    settings.resizable(False, False)

    # style setup
    style = ttk.Style(settings)
    settings.tk.call('source', 'azure dark/azure dark.tcl')
    style.theme_use('azure')

    # setup objects
    l_language = ttk.Label(settings, text=translation['language'])
    l_language.grid(row=3, column=0)

    c_language = ttk.Combobox(settings, values=["English", "Deutsch"], state="readonly", style="Custom.TCombobox")
    set_language()
    c_language.grid(row=4, column=0)
    c_language.bind('<<ComboboxSelected>>', update_language)

    b_closewindow = ttk.Button(settings, text=translation['settings_confirm'], command=close_settings_window)

    # b_closewindow = ttk.Button(settings, text=translation['settings_confirm'], command=close_settings_window, font=("Arial", 10), background="#83838B", foreground="white", relief="flat")
    b_closewindow.grid(row=5, column=0)

def main_window():
    global options_var
    global e_youtubelink
    global e_targetdirectory

    options = ('Video', "Audio")
    options_var = tk.StringVar()

    # window setup
    root.resizable(False, False)
    root.title("YouTube Video Downloader")
    root.geometry("+300+300")

    # setup and set layouts
    l_output_folder = tk.Label(text=translation['path_to_location'], font=("Arial", 10))
    l_output_folder.grid(row=0, column=0, sticky=tk.W, padx=10)

    e_targetdirectory = tk.Entry(font=("Arial", 12), borderwidth=0)
    e_targetdirectory.insert(1, outputfolder)
    e_targetdirectory.grid(row=1, column=0, ipadx=100, ipady=5, padx=10)

    b_browse = tk.Button(text=translation['browse'], command=update_directory, font=("Arial", 10), background="#83838B", foreground="white", relief="flat")
    b_browse.grid(row=2, column=0, pady=10, ipadx=50, ipady=5)

    l_youtubelink = tk.Label(text=translation['link_to_youtube_video'], font=("Arial", 10))
    l_youtubelink.grid(row=3, column=0, sticky=tk.W, padx=10)
    e_youtubelink = tk.Entry(font=("Arial", 12), borderwidth=0)
    e_youtubelink.grid(row=4, column=0, ipadx=100, ipady=5, padx=10)

    b_open_outputfolder = tk.Button(text=translation['output_folder'], command=open_outputfolder, font=("Arial", 10), background="#83838B", foreground="white", relief="flat")
    b_open_outputfolder.grid(row=5, column=0, sticky=tk.W, pady=10, padx=5 , ipadx=50, ipady=5)

    om_format = ttk.OptionMenu(root, options_var, options[0], *options)
    om_format.grid(row=5, column=0, sticky=tk.E)

    b_download = tk.Button(text=translation['download'], command=download_process, font=("Arial", 10), background="#27a102", foreground="white", relief="flat")
    b_download.grid(row=6, column=0, padx=10, ipadx=50, ipady=5)

    b_settings = tk.Button(text="⚙", bd=0, highlightthickness=0, command=settings_window)
    b_settings.grid(row=7, column=0, ipadx=50)

    # Query object
    # print(Misc.winfo_class(e_targetdirectory))

root = tk.Tk()

setup_config_file()
create_lang_en_file()
create_lang_de_file()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

language = config['language']

if language == 'Deutsch':
    with open('lang_de.json', 'r') as t_file:
        translation = json.load(t_file)

if language == 'English':
    with open('lang_en.json', 'r') as t_file:
        translation = json.load(t_file)

main_window()
root.mainloop()