import os

import pipeline as pipeline
from elevenlabs import set_api_key, save
from elevenlabs import voices, generate, play
key = "22329c3dd35a33d7cd8997d7cdaabacf"
set_api_key(key)
import requests


# CHUNK_SIZE = 1024
# url = "https://api.elevenlabs.io/v1/text-to-speech/9VCnXyQHl9BYMLxIwxSxH"
#
# headers = {
#   "Accept": "audio/mpeg",
#   "Content-Type": "application/json",
#   "xi-api-key": key
# }
#
# data = {
#   "text": "C'est un test",
#   "model_id": "eleven_multilingual_v1",
#   "voice_settings": {
#     "stability": 0.56,
#     "similarity_boost": 0.75
#   }
# }
#
# response = requests.post(url, json=data, headers=headers)
# Chemin du dossier principal à parcourir
dossier_principal = "/Users/emmanuellandau/Documents/EditLab/TODO"
def make_voice(dossier_principal):
  # Parcours des sous-dossiers
  for dossier, sous_dossiers, fichiers in os.walk(dossier_principal):
    print(dossier)
    # Recherche du fichier "description.txt"
    if "description.txt" in fichiers:
      if not 'audio.mp3' in fichiers:
        chemin_description = os.path.join(dossier, "description.txt")
        with open(chemin_description, 'r', encoding='utf8') as txt_file:
          txt_content = txt_file.read()
        print(txt_content)
        audio = generate(
          text=txt_content,
          voice="G7xH3hmwHsuqBz5TIhkC",
          model="eleven_multilingual_v1"
        )
        # Construction du chemin du fichier audio
        chemin_audio = os.path.join(dossier, "audio.mp3")
        save(audio, chemin_audio)
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
def dump_srt(folder):

  srt_path = os.path.join(folder, "audio.srt")
  audio_path = os.path.join(folder, "audio.mp3")
  if os.path.exists(srt_path):
    return True
  # model = stable_whisper.load_faster_whisper('medium')
  # result = model.transcribe_stable(audio_path, language="fr")
  model = stable_whisper.load_model('medium')
  result = model.transcribe(audio_path, fp16=False, language="french")
  result = (
      result
      .split_by_length(max_words=2)
      .split_by_gap(max_gap=0.01)
      .merge_by_punctuation(["'","-"])
      # .split_by_length(max_words=3)
  )

  result.to_srt_vtt(srt_path, segment_level=True, word_level=False)
  return True


# folder = "/Users/emmanuellandau/Documents/EditLab/TODO/La plus grande force des ISTPs/"
# dump_srt(folder)
# transcribe_audio()
# make_voice(dossier_principal)