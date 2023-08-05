import os
import shutil


class Download:
    def __init__(self, video, output_folder):
        self.output_folder = output_folder
        self.file = None
        self.raw_file = None
        self.video = video
        self.video_title = video.title

#    def download_

    def download_audio(self):
        create_temporary_folder()
        print(f"Download audio file \"{self.video_title}\"")
        self.download_audio_file()
        self.transform_file_to_mp3()
        move_file(self.file, self.output_folder)
        remove_temporary_folder()

    def download_audio_file(self):
        self.video = self.video.streams.filter(only_audio=True).first().download(temp_download_folder)


    def transform_file_to_mp3(self):
        self.raw_file, ext = os.path.splitext(self.video)
        self.file = self.raw_file + '.mp3'
        os.rename(self.video, self.file)


def create_temporary_folder():
    os.mkdir(temp_download_folder)


def remove_temporary_folder():
    if os.path.exists(temp_download_folder):
        shutil.rmtree(temp_download_folder)


def move_file(file, destination_path):
    shutil.move(file, destination_path)

temp_download_folder = "download"
remove_temporary_folder()
