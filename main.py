import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pytube
import moviepy.editor as mpe
import shutil

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # window setup
        self.resizable(False, False)
        self.title("YouTube Video Downloader")

        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))

class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        global e_youtubelink
        global e_targetdirectory
        global options_var

        # objects setup
        l_output_folder = ttk.Label(self, text=translation['path_to_location'])
        l_output_folder.grid(row=0, column=0, sticky=tk.W)

        e_targetdirectory = ttk.Entry(self)
        e_targetdirectory.insert(1, outputfolder)
        e_targetdirectory.grid(row=1, column=0, ipadx=100)

        b_browse = ttk.Button(self, text=translation['browse'], command=update_directory)
        b_browse.grid(row=2, column=0, pady=10)

        l_youtubelink = ttk.Label(self, text=translation['link_to_youtube_video'])
        l_youtubelink.grid(row=3, column=0, sticky=tk.W)
        e_youtubelink = ttk.Entry(self)
        e_youtubelink.grid(row=4, column=0, ipadx=100)

        b_open_outputfolder = ttk.Button(self, text=translation['output_folder'], command=open_outputfolder)
        b_open_outputfolder.grid(row=5, column=0, sticky=tk.W, pady=10)

        options = ('Video', "Audio")
        options_var = tk.StringVar()
        om_format = ttk.OptionMenu(self, options_var, options[0], *options)
        om_format.grid(row=5, column=0, sticky=tk.E)

        b_next_frame = ttk.Button(self, text=translation['next'], command=lambda:change_frame_to_download_section_and_get_video())
        b_next_frame.grid(row=6, column=0, sticky=tk.E, pady=10)

        b_settings = tk.Button(self, text="⚙", bd=0, highlightthickness=0, command=settings_window)
        b_settings.grid(row=6, column=0, sticky=tk.W)

        self.pack(fill="both", expand=1)
class DownloadSectionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        format_value = options_var.get()

        l_video_informations = ttk.Label(self, text=translation['video_title'] + ": " + video_title + "\n" + translation['video_format'] + ": " + format_value + "\n" + translation['video_resolution'] + ": " + "Highest Resolution")
        l_video_informations.grid(row=1, column=0)

        b_download = ttk.Button(self, text=translation['download'], command=download_process)
        b_download.grid(row=3, column=0)

def change_frame_to_download_section_and_get_video():
    if e_targetdirectory.get() == '':
        messagebox.showerror('YouTube Video Downloader', translation['no_directory_path'])
        return

    if e_youtubelink.get() == '':
        messagebox.showerror('YouTube Video Downloader', translation['invalid_youtube_link'])
        return

    global video_title

    youtubelink = e_youtubelink.get()
    get_video = pytube.YouTube(youtubelink)
    video_title = get_video.title

    frame2 = DownloadSectionFrame(app)
    frame2.pack(fill="both", expand=1)
    frame.forget()

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

def setup_language_files():

    # create english language file
    values = {
        "download": "Download",
        "format_option_audio": "Audio",
        "format_option_video": "Video",
        "link_to_youtube_video": "Link to YouTube-Video",
        "output_folder": "Open output-folder",
        "path_to_location": "Path to location",
        "browse": "Browse",
        "language": "Language",
        "restart_program": "The application is restarted for the change to take effect",
        "window_settings_title": "YouTube Video Downloader - Settings",
        "file_already_exists": "This file is already existing.",
        "no_directory_path": "Please enter a directory path.",
        "unknown_file_format": "Please enter a valid file format.",
        "download_successfully": "The Video \"%video_title%\" successfully downloaded at \"%video_output_path%\".",
        "invalid_youtube_link": "Please enter a valid youtube link.",
        "settings_confirm": "Confirm",
        "credits": "Design \"Radiance\" by RedFantom",
        "next": "Next »",
        "back": "« Back",
        "video_title": "Title",
        "video_format": "Format",
        "video_resolution": "Resolution"
    }

    with open('lang_en.json', 'w') as file:
        json.dump(values, file, indent=4)

    # create german language file
    values = {
        "download": "Herunterladen",
        "format_option_audio": "Audio",
        "format_option_video": "Video",
        "link_to_youtube_video": "Link zum YouTube-Video",
        "output_folder": "Öffne Ausgabe-Ordner",
        "path_to_location": "Pfad zum Speicherort",
        "browse": "Durchsuchen",
        "language": "Sprache",
        "restart_program": "Die Anwendung wird neugestartet, damit die Änderung wirksam wird.",
        "window_settings_title": "YouTube Video Downloader - Einstellungen",
        "file_already_exists": "Die Datei existiert bereits.",
        "no_directory_path": "Bitte gebe einen Ausgabepfad an.",
        "unknown_file_format": "Bitte gebe ein gültiges Format an.",
        "download_successfully": "Das Video \"%video_title%\" wurde unter dem Pfad \"%video_output_path%\" gespeichert.",
        "invalid_youtube_link": "Bitte gebe einen gültigen YouTube-Link an.",
        "settings_confirm": "Bestätigen",
        "credits": "Design \"Radiance\" by RedFantom",
        "next": "Weiter »",
        "back": "« Zurück",
        "video_title": "Titel",
        "video_format": "Format",
        "video_resolution": "Auflösung"
    }

    with open('lang_de.json', 'w') as file:
        json.dump(values, file, indent=4)

def setup_program_language():
    global translation
    global config

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    language = config['language']

    if language == 'Deutsch':
        with open('lang_de.json', 'r') as t_file:
            translation = json.load(t_file)

    if language == 'English':
        with open('lang_en.json', 'r') as t_file:
            translation = json.load(t_file)

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

def fill_language_field():
    global c_language

    match config['language']:
        case 'English':
            c_language.current(0)
        case 'Deutsch':
            c_language.current(1)

def update_language(event):
    selected_language = c_language.get()

    with open('config.json', 'w') as file:
        config['language'] = selected_language
        json.dump(config, file, indent=4)

    messagebox.showinfo("YouTube Video Downloader", translation['restart_program'])
    app.destroy()
    os.startfile("main.py")

def open_outputfolder():
    os.startfile(outputfolder)

def close_settings_window():
    settings.destroy()
    app.deiconify()

def download_process():
    format_value = options_var.get()
    youtubelink = e_youtubelink.get()
    get_video = pytube.YouTube(youtubelink)
    video_title = get_video.title

    try:
        match format_value:
            case "Video":
                vname = "video.mp4"
                aname = "audio.mp3"

                # download video and audio and rename both files
                yt_video = get_video.streams.filter(mime_type="video/mp4", progressive=False).order_by("resolution").desc().first().download()
                os.rename(yt_video, vname)
                audio = get_video.streams.filter(only_audio=True).first().download()
                os.rename(audio, aname)

                video = mpe.VideoFileClip(vname)
                audio = mpe.AudioFileClip(aname)

                final = video.set_audio(audio)
                final.write_videofile("final.mp4")

                video.close()
                audio.close()
                final.close()

                # cleanup
                os.remove(vname)
                os.remove(aname)

                os.rename("final.mp4", yt_video)
                shutil.move(yt_video, outputfolder)
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
    global c_language
    global settings

    # vanish root window
    app.withdraw()

    # window setup
    settings = tk.Toplevel()
    settings.title(translation['window_settings_title'])
    settings.resizable(False, False)

    # setup objects
    l_language = ttk.Label(settings, text=translation['language'])
    l_language.grid(row=1, column=0, sticky="W")

    c_language = ttk.Combobox(settings, values=["English", "Deutsch"], state="readonly")
    fill_language_field()
    c_language.grid(row=2, column=0, ipadx=100)
    c_language.bind('<<ComboboxSelected>>', update_language)

    b_closewindow = ttk.Button(settings, text=translation['settings_confirm'], command=close_settings_window)
    b_closewindow.grid(row=3, column=0, pady=10)

    l_credits = ttk.Label(settings, text=translation['credits'])
    l_credits.grid(row=4, column=0, sticky="W")

if __name__ == "__main__":
    # startup
    setup_config_file()
    setup_language_files()
    setup_program_language()

    # setup window and frame
    app = App()
    frame = MainFrame(app)
    # frame2 = DownloadSection(app)

    # setup style
    style = ttk.Style()
    app.tk.call('source', 'themes/radiance/radiance.tcl')
    style.theme_use('radiance')

    app.mainloop()

    # Query object
    # print(Misc.winfo_class(e_targetdirectory))
