import json
from functions import mp4_to_mp3
import os
import re
import sys
sys.path.append('/Users/emmanuellandau/PycharmProjects/whisperX')
from diarization.main import diarize, generate_srt_from_words
from diarization.test import update_result_from_srt
from diarization.split_audio import create_speaker_audio
from diarization.functions import create_special_srt



directory = "/Users/emmanuellandau/Documents/EditLab/TODO"
def firt_part(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)

    # generate diarized dict
    mp4_to_mp3(folder_path)
    result = diarize(folder_path)
    result_path = os.path.join(folder_path, 'result.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    # Generating SRT content
    srt_path = os.path.join(folder_path, 'audio.srt')
    srt_content = generate_srt_from_words(result)
    with open(srt_path, "w") as file:
        file.write(srt_content)

def correct_result(directory, folder_name):
    folder_path= os.path.join(directory, folder_name)
    srt_path = os.path.join(folder_path, 'audio.srt')
    result_path = os.path.join(folder_path, 'result.json')
    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content_example = file.read()
    with open(result_path, 'r', encoding='utf-8') as f:
        result_example = json.load(f)
    # Example usage
    updated_result = update_result_from_srt(srt_content_example, result_example)
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(updated_result, f, ensure_ascii=False, indent=4)


def extract_speakers_and_create_audios(folder_path):
    srt_file_path = os.path.join(folder_path, 'audio.srt')
    audio_path = os.path.join(folder_path, 'audio.mp3')
    result_path = os.path.join(folder_path, 'result.json')
    with open(result_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Lire le contenu du fichier SRT
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Trouver tous les noms des intervenants uniques dans le fichier SRT
    speakers = set(re.findall(r"SPEAKER_\d\d", content))

    # Créer un dictionnaire pour stocker les audios de chaque intervenant
    speaker_audios = {}

    # Créer l'audio pour chaque intervenant
    for speaker in speakers:
        audio_speaker_path = os.path.join(folder_path, f"{speaker}.mp3")
        speaker_audio = create_speaker_audio(audio_path, data, speaker)
        speaker_audios[speaker] = speaker_audio
        speaker_audio.export(audio_speaker_path, format="mp3")

    return speaker_audios

# Utiliser la fonction


def enhanced_srt(folder_path):
    result_path = os.path.join(folder_path, 'result.json')
    srt_path = os.path.join(folder_path, 'audio.srt')

    with open(result_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    final_srt = create_special_srt(data)

    with open(srt_path, "w") as file:
        file.write(final_srt)

folder_path = os.path.join(directory, "1")
# firt_part(directory, "1")
# correct_result(directory, "12")
# extract_speakers_and_create_audios(folder_path)
enhanced_srt(folder_path)

# extract_speakers_and_create_audios(folder_path)

# speaker_audios contient maintenant les audios pour chaque intervenant
