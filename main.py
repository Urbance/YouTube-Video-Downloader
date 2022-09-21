"""
YouTube-Video-Downloader
A simple YouTube Video Downloader that supports .mp3 and .mp4 format
"""

import json
import os
import threading
from io import BytesIO

import pytube
import requests
from PIL import ImageTk, Image
from pytube import Playlist
import moviepy.editor as mpe
import shutil
from tkinter import ttk, filedialog, messagebox, W, E, Tk, StringVar, Button, Toplevel


class App(Tk):
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
        l_output_folder.grid(row=0, column=0, sticky=W)

        e_targetdirectory = ttk.Entry(self)
        e_targetdirectory.insert(1, outputfolder)
        e_targetdirectory.grid(row=1, column=0, ipadx=100)

        b_browse = ttk.Button(self, text=translation['browse'], command=update_directory)
        b_browse.grid(row=2, column=0, pady=10)

        l_youtubelink = ttk.Label(self, text=translation['link_to_youtube_video'])
        l_youtubelink.grid(row=3, column=0, sticky=W)
        e_youtubelink = ttk.Entry(self)
        e_youtubelink.grid(row=4, column=0, ipadx=100)

        b_open_outputfolder = ttk.Button(self, text=translation['output_folder'], command=open_outputfolder)
        b_open_outputfolder.grid(row=5, column=0, sticky=W, pady=10)

        options = ('Video', "Audio", "Playlist Audio")
        options_var = StringVar()
        om_format = ttk.OptionMenu(self, options_var, options[0], *options)
        om_format.grid(row=5, column=0, sticky=E)

        b_next_frame = ttk.Button(self, text=translation['download'], command=lambda: self.change_to_download_frame())
        b_next_frame.grid(row=6, column=0, sticky=E, pady=10)

        b_settings = Button(self, text="⚙", bd=0, highlightthickness=0, command=settings_window)
        b_settings.grid(row=6, column=0, sticky=W)

        self.pack(fill="both", expand=1)

    def change_to_download_frame(self):
        global video_title

        if e_targetdirectory.get() == '':
            messagebox.showerror('YouTube Video Downloader', translation['no_directory_path'])
            return
        if e_youtubelink.get() == '':
            messagebox.showerror('YouTube Video Downloader', translation['invalid_youtube_link'])
            return

        format_value = options_var.get()
        youtubelink = e_youtubelink.get()
        if format_value == "Video" or format_value == "Audio":
            get_video = pytube.YouTube(youtubelink)
            video_title = get_video.title
        if format_value == "Playlist Audio":
            playlist = Playlist(youtubelink)
            video_title = playlist.title

        download_frame = DownloadFrame(app)
        download_frame.pack(fill="both", expand=1)
        self.forget()


class DownloadFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        global l_state_line
        global pb

        video_link = e_youtubelink.get()
        video_format = options_var.get()

        l_video_title = ttk.Label(
            self, text=video_title)
        # TODO add video resolution
        l_video_title.grid(row=1, column=0)
        l_video_information = ttk.Label(self, text=f"{video_format}")
        l_video_information.grid(row=2, column=0)
        # setup thumbnail
        thumbnail_url = pytube.YouTube(video_link).thumbnail_url
        response = requests.get(thumbnail_url)
        thumbnail = Image.open(BytesIO(response.content))
        thumbnail = thumbnail.resize((225, 150), Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(thumbnail)
        l_thumbnail = ttk.Label(self, image=thumbnail)
        l_thumbnail.image = thumbnail
        l_thumbnail.grid(row=3, pady=5)
        # setup progressbar
        pb = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        pb.grid(row=4, column=0)
        pb.start(20)
        l_state_line = ttk.Label(
            self, text=" "
        )
        l_state_line.grid(row=5, column=0)

        self.download_setup()

    def download_setup(self):
        # create thread
        new_thread = threading.Thread(target=lambda: self.download_video(), daemon=True)
        new_thread.start()

    def download_video(self):
        temp_download_directory = "temp_download"
        if os.path.exists(temp_download_directory):
            shutil.rmtree(temp_download_directory)

        video_format = options_var.get()
        video_link = e_youtubelink.get()
        video_title = video_link.title()

        try:
            match video_format:
                case "Video":
                    vname = "video.mp4"
                    aname = "audio.mp3"
                    get_video = pytube.YouTube(video_link)
                    video_title = get_video.title

                    # setup download
                    os.mkdir(temp_download_directory)

                    # download video and audio and rename both files and move final file
                    print(f"Start downloading \"{video_title}\"")
                    print("Download video file")
                    l_state_line.config(text="Download video file")
                    # TODO .download paramter file_name
                    yt_video = get_video.streams.filter(mime_type="video/mp4", progressive=False).order_by(
                        "resolution").desc().first().download(temp_download_directory)
                    temp_video_file = os.path.join(temp_download_directory, vname)
                    os.rename(yt_video, temp_video_file)

                    print("Download audio file")
                    l_state_line.config(text="Download audio file")
                    audio = get_video.streams.filter(only_audio=True).first().download(temp_download_directory)
                    temp_audio_file = os.path.join(temp_download_directory, aname)
                    os.rename(audio, temp_audio_file)

                    print("Merge audio and video file ")
                    l_state_line.config(text="Merge audio and video file")
                    video = mpe.VideoFileClip(temp_video_file)
                    audio = mpe.AudioFileClip(temp_audio_file)

                    final = video.set_audio(audio)
                    final.write_videofile(temp_download_directory + "/" + "final.mp4")

                    video.close()
                    audio.close()
                    final.close()

                    os.rename(temp_download_directory + "/" + "final.mp4", yt_video)
                    shutil.move(yt_video, outputfolder)

                    # delete temp_download directory
                    shutil.rmtree(temp_download_directory)

                case "Audio":
                    # setup download
                    os.mkdir(temp_download_directory)

                    # download video
                    get_video = pytube.YouTube(video_link)
                    video_title = get_video.title
                    video = get_video.streams.filter(only_audio=True).first().download(temp_download_directory)

                    print(f"Start downloading audio \"{video_title}\"")

                    # add .mp3 format
                    file, ext = os.path.splitext(video)
                    new_file = file + '.mp3'
                    os.rename(video, new_file)

                    # move video to outputfolder
                    shutil.move(new_file, outputfolder)
                    os.path.dirname(os.path.dirname(__file__))

                    # delete temp_download directory
                    os.removedirs(temp_download_directory)

                case "Playlist Audio":
                    playlist = Playlist(video_link)
                    video_title = playlist.title

                    for video in playlist.videos:
                        video = video.streams.filter(only_audio=True).first()
                        video_file = video.download(outputfolder)

                        print(f"Start downloading audio \"{video_title}\"")

                        file, ext = os.path.splitext(video_file)
                        new_file = file + '.mp3'
                        os.rename(video_file, new_file)
                case _:
                    messagebox.showerror("YouTube Video Downloader", translation['unknown_file_format'])
        except FileExistsError:
            messagebox.showerror("YouTube Video Downloader", translation['file_already_exists'])
            return


        # MMS Start detach FinalFrame and ConfirmationFrame
        pb.destroy()
        successfully_downloaded = translation['download_successfully']
        successfully_downloaded = successfully_downloaded.replace('%video_title%', video_title)
        l_state_line.config(text=successfully_downloaded)
        b_download_new_video = ttk.Button(
            self, text=translation['download_new_video'], command=lambda: self.change_to_main_frame())
        b_download_new_video.grid(
            row=6, column=0, sticky=E)
        b_open_outputfolder = ttk.Button(
            self, text=translation['output_folder'], command=open_outputfolder)
        b_open_outputfolder.grid(
            row=6, column=0, sticky=W, pady=10)
        # MMS End detach final frame


    def change_to_main_frame(self):
        e_youtubelink.delete(0, "end")
        self.forget()
        frame.pack(fill="both", expand=1)


def settings_window():
    global c_language
    global settings

    # vanish root window
    app.withdraw()

    # window setup
    settings = Toplevel()
    settings.title(translation['window_settings_title'])
    settings.resizable(False, False)

    x = (settings.winfo_screenwidth() - settings.winfo_reqwidth()) / 2
    y = (settings.winfo_screenheight() - settings.winfo_reqheight()) / 2
    settings.geometry("+%d+%d" % (x, y))

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


def setup_config_file():
    global outputfolder

    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            data = json.load(config_file)
            outputfolder = data['output_folder']
        return

    outputfolder = os.environ['USERPROFILE'] + "\Music\YouTube-Video-Downloader"

    try:
        os.mkdir(outputfolder)
    except FileExistsError:
        pass

    config_values = {
        "language": "English",
        "output_folder": outputfolder
    }

    with open('config.json', 'w') as file:
        json.dump(config_values, file, indent=4)


def setup_language_files():
    values = {
        "download": "Download »",
        "format_option_audio": "Audio",
        "format_option_video": "Video",
        "link_to_youtube_video": "Link to YouTube-Video",
        "output_folder": "Open output-folder",
        "path_to_location": "Path to output-folder",
        "browse": "Browse",
        "language": "Language",
        "restart_program": "The application is restarted for the change to take effect",
        "window_settings_title": "YouTube Video Downloader - Settings",
        "file_already_exists": "This file is already existing.",
        "no_directory_path": "Please enter a directory path.",
        "unknown_file_format": "Please enter a valid file format.",
        "download_successfully": "The Video \"%video_title%\"\n was successfully downloaded",
        "invalid_youtube_link": "Please enter a valid youtube link.",
        "settings_confirm": "Confirm",
        "credits": "Design \"Radiance\" by RedFantom",
        "download_new_video": "Download new video"
    }
    # create english language file

    with open('lang_en.json', 'w') as file:
        json.dump(values, file, indent=4)

    # create german language file
    values = {
        "download": "Herunterladen »",
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
        "download_successfully": "Das Video \"%video_title%\"\nwurde erfolgreich heruntergeladen",
        "invalid_youtube_link": "Bitte gebe einen gültigen YouTube-Link an.",
        "settings_confirm": "Bestätigen",
        "credits": "Design \"Radiance\" by RedFantom",
        "download_new_video": "Neues Video herunterladen"
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
    try:
        os.startfile(outputfolder)
    except FileNotFoundError:
        os.mkdir(outputfolder)
        os.startfile(outputfolder)


def close_settings_window():
    settings.destroy()
    app.deiconify()


if __name__ == "__main__":
    # startup
    setup_config_file()
    setup_language_files()
    setup_program_language()

    # setup window and frame
    app = App()
    frame = MainFrame(app)

    # setup style
    style = ttk.Style()
    app.tk.call('source', 'themes/azure/azure.tcl')
    app.tk.call('set_theme', 'dark')

    app.mainloop()

    # Query object
    # print(Misc.winfo_class(e_targetdirectory))
