import tkinter as tk
import os
import pytube
import json
from tkinter import ttk
from tkinter import filedialog, messagebox

def setup_config_file():
    global outputfolder

    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            data = json.load(config_file)
            outputfolder = data['output_folder']
        return

    outputfolder = os.environ['USERPROFILE'] + "\Music\PyTube"
    config_values = {
        "language": "English",
        "output_folder": outputfolder
    }

    with open('config.json', 'w') as file:
        json.dump(config_values, file, indent=4)

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

def settings_window():
    global e_targetdirectory
    global c_language

    # window setup
    settings = tk.Toplevel()
    settings.title(translation['window_settings_title'])
    settings.resizable(False, False)

    # setup objects
    label2 = ttk.Label(settings, text=translation['path_to_location'])
    label2.grid(row=0, column=0)
    e_targetdirectory = ttk.Entry(settings)
    e_targetdirectory.insert(1, outputfolder)
    e_targetdirectory.grid(row=1, column=0, ipadx=20)
    b_browse = ttk.Button(settings, text=translation['browse'], command=update_directory)
    b_browse.grid(row=2, column=0)
    l_language = ttk.Label(settings, text=translation['language'])
    l_language.grid(row=3, column=0)
    c_language = ttk.Combobox(settings, values=["English", "Deutsch"], state="readonly")
    set_language()
    c_language.grid(row=4, column=0)
    c_language.bind('<<ComboboxSelected>>', update_language)

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

def main_window():
    global options_var
    global e_youtubelink

    options = ('Video', "Audio")
    options_var = tk.StringVar()

    # window setup
    root.resizable(False, False)
    root.title("YouTube Video Downloader")
    root.geometry("+300+300")

    # setup and set layouts
    l_youtubelink = tk.Label(text=translation['link_to_youtube_video'])
    l_youtubelink.grid(row=0, column=0, padx=5)
    e_youtubelink = tk.Entry()
    e_youtubelink.grid(row=0, column=1, ipadx=50, pady=5)
    om_format = ttk.OptionMenu(root, options_var, options[0], *options)
    om_format.grid(row=0, column=2, padx=5)
    b_download = tk.Button(text=translation['download'], command=download_process)
    b_download.grid(row=4, column=1)
    b_open_outputfolder = tk.Button(text=translation['output_folder'], command=open_outputfolder)
    b_open_outputfolder.grid(row=4, column=0)
    b_settings = tk.Button(text="⚙️", bd=0, highlightthickness=0, command=settings_window)
    b_settings.grid(row=4, column=3)

root = tk.Tk()

setup_config_file()

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

