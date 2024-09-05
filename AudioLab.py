import json
import os

import pipeline as pipeline
from elevenlabs import set_api_key, save
from elevenlabs import voices, generate, play
key = "22329c3dd35a33d7cd8997d7cdaabacf"
set_api_key(key)
from mutagen.mp3 import MP3
def check_mp3_size(chemin_fichier):
  # Obtenir les métadonnées du fichier MP3
  audio = MP3(chemin_fichier)
  # Obtenir la durée en secondes
  duree = audio.info.length
  # Vérifier si la durée est inférieure à 60 secondes
  if duree < 60:
      print(f"Alerte : Le fichier MP3{chemin_fichier} fait moins de 60 secondes.")
  else:
    return True

dossier_principal = "/Users/emmanuellandau/Documents/EditLab/TODO"
def make_voice(dossier_principal):
  # Parcours des sous-dossiers
  for dossier, sous_dossiers, fichiers in os.walk(dossier_principal):
    print(dossier)
    # Recherche du fichier "description.txt"
    if "description.txt" in fichiers:
      if not 'audio.mp3' in fichiers:
        male = "G7xH3hmwHsuqBz5TIhkC"
        female = "8IBKhZKqVZolbCCcNSPI"
        chemin_description = os.path.join(dossier, "description.txt")
        with open(chemin_description, 'r', encoding='utf8') as txt_file:
          txt_content = txt_file.read()
        print(txt_content)
        audio = generate(
          text=txt_content,
          voice= male,
          model="eleven_multilingual_v1"
        )

        # Construction du chemin du fichier audio
        chemin_audio = os.path.join(dossier, "audio.mp3")
        save(audio, chemin_audio)
        check_mp3_size(chemin_audio)
      else:
        print(dossier)



from datetime import timedelta
import os
import whisper
from transformers import pipeline
# def transcribe_audio(path):
#
#     model = whisper.load_model("large-v2") # Change this to your desired model
#
#
#
#     # # This line will load your desired model
#     # model = pipeline("automatic-speech-recognition", )
#     print("Whisper model loaded.")
#     transcribe = model.transcribe(audio=path, fp16=False, language="french")
#     segments = transcribe['segments']
#
#     for segment in segments:
#         startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
#         endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
#         text = segment['text']
#         segmentId = segment['id']+1
#         segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"
#
#         srtFilename = os.path.join("/Users/emmanuellandau/Documents/EditLab/TODO/La plus grande force des ENFPs", "audio.srt")
#         with open(srtFilename, 'a', encoding='utf-8') as srtFile:
#             srtFile.write(segment)
#
#     return srtFilename
import faster_whisper
import stable_whisper
def dump_srt(folder, max_words=2):

  srt_path = os.path.join(folder, "audio.srt")
  audio_path = os.path.join(folder, "audio.mp3")
  txt_path = os.path.join(folder, "description.txt")

  if os.path.exists(srt_path):
    print("there")
    return True
  # model = stable_whisper.load_faster_whisper('medium', compute_type="float32")
  # result = model.transcribe_stable(audio_path, language="fr")
  model = stable_whisper.load_model('large-v3')
  # result = model.align(audio_path, txt)
  # initial_prompt="signes astrologiques : Bélier, Taureau, Gémeaux, Cancer, Lion, Vierge, Balance, Scorpion, Sagittaire, Capricorne, Verseau, Poissons"
  result = model.transcribe(audio_path, fp16=False, prompt="bien orthographier: Bélier, Taureau, Gémeaux, Cancer, Lion, Vierge, Balance, Scorpion, Sagittaire, Capricorne, Verseau, Poissons, j'aime, like")
  print(result)
  result = (
      result
      .split_by_length(max_words=max_words)
      .split_by_gap(max_gap=0.1)
      .merge_by_punctuation(["'","-"])
      # .split_by_length(max_words=3)
  )
  result.to_srt_vtt(srt_path, segment_level=True, word_level=False)
  return True


# folder = "/Users/emmanuellandau/Documents/EditLab/TODO/conseil"

# transcribe_audio()
make_voice(dossier_principal)
# dump_                                                                                                                                                                                                                                       srt(folder)
from moviepy.editor import *
from pydub import AudioSegment

# Load your M4A file
# m4a_audio = AudioSegment.from_file("/Users/emmanuellandau/Documents/EditLab/TODO/test/audio.m4a", format="m4a")

# Convert to MP3
# m4a_audio.export("/Users/emmanuellandau/Documents/EditLab/TODO/test/audio.mp3", format="mp3")
import whisper
# mp3_path = "/Users/emmanuellandau/Documents/EditLab/TODO/test/audio.mp3"
# text_path = "/Users/emmanuellandau/Downloads/marketing_interview_txt.mp3"
# video = VideoFileClip("/Users/emmanuellandau/Downloads/Download (1).mp4")
# audio = video.audio
#
# audio.write_audiofile(mp3_path)



# model=stable_whisper.load_model('medium')
# model.transcribe(mp3_path, fp16=False)
# result = model.transcribe(mp3_path)
# result.to_srt_vtt(text_path, segment_level=True, word_level=False)
# dump_srt("/Users/emmanuellandau/Documents/EditLab/TODO/test")