from moviepy.editor import *
import re


def convert_mp4_to_mp3(video_path, audio_path):
    video = VideoFileClip(video_path)
    # Extraire l'audio
    audio = video.audio
    # Enregistrer l'audio
    audio.write_audiofile(audio_path)

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


import re



def extract_complete_phrases(file_path, start_subtitle_number, end_subtitle_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Construire les phrases complètes
    phrases = []
    current_text = ""
    subtitle_nums = []

    for line in lines:
        if line.strip().isdigit():
            subtitle_nums.append(int(line.strip()))
        elif '-->' in line:
            continue
        elif line.strip():
            current_text += line.strip() + " "
            if re.search(r'[.!?]$', line.strip()):
                phrases.append((current_text, list(subtitle_nums)))
                current_text = ""
                subtitle_nums = []

    # Si la dernière phrase n'a pas été ajoutée
    if current_text:
        phrases.append((current_text, list(subtitle_nums)))

    # Trouver les phrases correspondant aux numéros de sous-titres
    extracted_phrases = []
    start_found = False
    for phrase, nums in phrases:
        if start_subtitle_number in nums:
            start_found = True
        if start_found:
            extracted_phrases.append(phrase)
        if end_subtitle_number in nums:
            break

    return ' '.join(extracted_phrases)


def zeroed_timestamp(obj):
    """
    Ajuste le plus petit timestamp de la liste à 0.0 et convertit tous les timestamps en str.

    :param obj: Liste des objets contenant les chemins des fichiers et leurs timestamps.
    :return: La liste ajustée avec le plus petit timestamp à 0.0 et tous les timestamps en str.
    """
    # Convertir les timestamps en flottants pour les manipulations
    for item in obj:
        item[1] = float(item[1])

    # Trouver le plus petit timestamp
    min_timestamp = min(item[1] for item in obj)

    # Ajuster uniquement le premier timestamp à 0.0 si nécessaire
    if min_timestamp != 0.0:
        for item in obj:
            if item[1] == min_timestamp:
                item[1] = 0.0
                break  # Ajuster seulement le premier trouvé et sortir de la boucle

    # Convertir les timestamps en chaînes de caractères
    for item in obj:
        item[1] = str(item[1])

    return obj

import sys
import os
import datetime as dt
import glob
from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET


def convert_time(ttml_time):
    # Convertit le temps de TTML (en ticks) en temps de SRT (HH:MM:SS,mmm)
    ticks = int(ttml_time[:-1])
    seconds, milliseconds = divmod(ticks, 10000000)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds//10000:03}"

def ttml_to_srt(file_path):
    # Charge le contenu TTML depuis un fichier
    tree = ET.parse(file_path)
    root = tree.getroot()
    subtitles = []

    for subtitle in root.iter('{http://www.w3.org/ns/ttml}p'):
        start = convert_time(subtitle.attrib['begin'])
        end = convert_time(subtitle.attrib['end'])
        text = ''.join(subtitle.itertext()).replace('\n', ' ').strip()
        subtitles.append((start, end, text))

    # Crée le contenu SRT
    srt_content = ''
    for i, (start, end, text) in enumerate(subtitles, 1):
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

    return srt_content


import re
from datetime import datetime, timedelta


def parse_time(srt_time):
    return datetime.strptime(srt_time, '%H:%M:%S,%f')


def time_to_str(delta):
    return str(delta)[:-3]


def subset_srt(file_path, start_srt_num, end_srt_num):
    with open(file_path, 'r') as file:
        content = file.readlines()

    entries = []
    entry = []
    for line in content:
        if line.strip() == '':
            entries.append(entry)
            entry = []
        else:
            entry.append(line.strip())
    if entry:
        entries.append(entry)

    # Sélectionner le sous-ensemble de sous-titres
    subset = entries[start_srt_num - 1:end_srt_num]

    # Réajuster les timestamps
    start_time = parse_time(re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', subset[0][1])[0])
    offset = start_time - datetime(1900, 1, 1)

    with open('subset_output.srt', 'w') as file:
        for i, entry in enumerate(subset, 1):
            times = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', entry[1])
            start = (parse_time(times[0]) - offset).time()
            end = (parse_time(times[1]) - offset).time()

            file.write(f'{i}\n')
            file.write(f'{time_to_str(start)} --> {time_to_str(end)}\n')
            file.write('\n'.join(entry[2:]) + '\n\n')

# Remplacez 'path/to/your/file.ttml' par le chemin de votre fichier TTML
file_path = '/Users/emmanuellandau/PycharmProjects/SubtiPy/you1.ttml'
# srt_content = ttml_to_srt(file_path)
# subset_srt(file_path, 580, )

# Écrire le contenu SRT dans un fichier
# with open('subtitles.srt', 'w') as file:
#     file.write(srt_content)

# Example usage
file_path = '/Users/emmanuellandau/Documents/EditLab/DONE/test/audio.srt'  # Replace with your actual SRT file path
start_subtitle_number = 5  # Replace with your actual start subtitle number
end_subtitle_number = 19  # Replace with your actual end subtitle number
# extracted_sentences = extract_complete_phrases(file_path, start_subtitle_number, end_subtitle_number)
# print(extracted_sentences)



# convert_mp4_to_mp3("//Users/emmanuellandau/Documents/EditLab/TODO/bazncamp/audio.mp4", "//Users/emmanuellandau/Documents/EditLab/TODO/bazncamp/audio.mp3")