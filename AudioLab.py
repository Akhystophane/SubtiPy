import json
import os
import whisper
from moviepy.editor import *
from pydub import AudioSegment
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
        male_radio = "1ns94GwK9YDCJoL6Nglv"
        male_origin = 'G7xH3hmwHsuqBz5TIhkC'
        male = "Hbb2NXaf6CKJnlEHYM1D"
        female = "8IBKhZKqVZolbCCcNSPI"
        chemin_description = os.path.join(dossier, "description.txt")
        with open(chemin_description, 'r', encoding='utf8') as txt_file:
          txt_content = txt_file.read()
        print(txt_content)
        audio = generate(
          text=txt_content,
          voice= male_origin,
          model="eleven_multilingual_v2"
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

def process_videos_and_transcribe(input_folder, output_folder, model_size="large-v3"):
    """
    Process all MP4 files in a directory, extract audio as MP3, and transcribe using Whisper.

    Args:
        input_folder (str): Path to the folder containing MP4 files.
        output_folder (str): Path to the folder where MP3 and transcription files will be saved.
        model_size (str): Whisper model size to use (default: "medium").
    """
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Load the Whisper model
    model = whisper.load_model(model_size)

    # Loop through all MP4 files in the directory
    for file_name in os.listdir(input_folder):
      if file_name.lower().endswith(".mp4"):
        video_path = os.path.join(input_folder, file_name)
        base_name = os.path.splitext(file_name)[0]
        mp3_path = os.path.join(output_folder, f"{base_name}.mp3")
        transcription_path = os.path.join(output_folder, f"{base_name}.srt")

        try:
          # Extract audio from video
          print(f"Processing video: {video_path}")
          video = VideoFileClip(video_path)
          audio = video.audio
          audio.write_audiofile(mp3_path)
          audio.close()

          # Convert to MP3 (if needed)
          mp3_audio = AudioSegment.from_file(mp3_path, format="mp3")
          mp3_audio.export(mp3_path, format="mp3")
          print(f"Audio saved to: {mp3_path}")

          # Transcribe using Whisper
          print(f"Transcribing audio: {mp3_path}")
          result = model.transcribe(mp3_path, fp16=False)
          with open(transcription_path, "w") as f:
            f.write(result["text"])
          print(f"Transcription saved to: {transcription_path}")
        except Exception as e:
          print(f"Error processing {file_name}: {e}")


# process_videos_and_transcribe("/Users/emmanuellandau/Documents/EditLab/TODO/retranscription", "/Users/emmanuellandau/Documents/EditLab/TODO/retranscription")

# folder = "/Users/emmanuellandau/Documents/EditLab/TODO/retranscription"
# dump_srt(folder)
# transcribe_audio()
#make_voice(dossier_principal)
# dump_                                                                                                                                                                                                                                       srt(folder)


# Load your M4A file
# m4a_audio = AudioSegment.from_file("/Users/emmanuellandau/Documents/EditLab/TODO/test/audio.m4a", format="m4a")

# Convert to MP3
# m4a_audio.export("/Users/emmanuellandau/Documents/EditLab/TODO/test/audio.mp3", format="mp3")
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