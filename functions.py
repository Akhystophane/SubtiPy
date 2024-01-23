from moviepy.editor import *
import re


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


# Utilisation de la fonction
file_path = 'chemin/vers/le/fichier.srt'

# Example usage
file_path = '/Users/emmanuellandau/Documents/EditLab/DONE/test/audio.srt'  # Replace with your actual SRT file path
start_subtitle_number = 5  # Replace with your actual start subtitle number
end_subtitle_number = 19  # Replace with your actual end subtitle number
# extracted_sentences = extract_complete_phrases(file_path, start_subtitle_number, end_subtitle_number)
# print(extracted_sentences)



