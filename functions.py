from moviepy.editor import *


def mp4_to_mp3(folder):
    def convert_mp4_to_mp3(video_path, audio_path):
        video = VideoFileClip(video_path)
        # Extraire l'audio
        audio = video.audio
        # Enregistrer l'audio
        audio.write_audiofile(audio_path)

    for fichier in os.listdir(folder):
        if fichier.endswith(".mp4") or fichier.endswith(".MP4"):
            video_path = os.path.join(folder, fichier)
            audio_path = os.path.join(folder, "audio.mp3")
            convert_mp4_to_mp3(video_path, audio_path)
        else:
            print("no video in folder")

