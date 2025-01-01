import json
import os
import shutil
import subprocess
from AudioLab import dump_srt
from Google.Folder_management import synchronize_subfolders, find_folder_id
from accounts.RedditStories.R_functions import do_script_file
from functions import mp4_to_mp3
from suggesterLab.SuggesterAi import emoji_suggester, music_suggester
from suggesterLab.footageSuggester import create_dict3, get_footage_dict
from suggesterLab.functions import key_exists_in_json, update_json, time_to_seconds
from word_interest import words_highlight


def ae_script():
    # Scripts_Adobe/Stories/aE-editor.jsx
    command = '''osascript -e "with timeout of 1200 seconds" -e "tell application \\"Adobe After Effects 2023\\" to activate" -e "tell application \\"Adobe After Effects 2023\\" to DoScriptFile \\"/Users/emmanuellandau/Scripts_Adobe/aE-test.jsx\\"" -e "end timeout"'''

    # Exécuter la commande et récupérer la sortie
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # Lire la sortie de la commande ligne par ligne
    # Attendre que le processus se termine
    process.wait()
    for line in process.stdout:
        # Faire quelque chose avec chaque ligne de sortie
        print(line.decode().strip())
        output = int(line.decode().strip())
    # Récupérer la sortie d'erreur
    error_output = process.stderr.read().decode().strip()
    if error_output:
        print(f"Erreur : {error_output}")
    return output


def get_ready(Lab_path, niche, aspect_ratio='9:16', check_condition=False, break_after_first=False, check_up=False,
              img_creation=True):
    """
      Prepares video folders for editing by adding necessary components like SRT files, scripts, highlighted words, emojis, and music.

      The function works within a 'Lab' environment which contains 'TODO' and 'READY' folders.
      'get_ready' processes each folder in 'TODO', representing videos pending preparation.

      Process:
      - Iterates through each folder in 'TODO':
          - Adds an SRT file to the folder.
          - Executes 'do_script_file' to generate and add scripts tailored to the given 'niche'.
          - If 'check_condition' is True, checks if the 'edit_data.json' file in the folder has a 'Words' key.
              - If not, it adds highlighted words, suggests emojis, and music to the folder.
              - If the key exists, skips these additions, indicating they have already been done.
          - If 'check_condition' is False, it always adds highlighted words, emojis, and music.
      - Moves the processed folder to 'READY', indicating it's prepared for the next stage.
      - Optionally, the function can break after processing the first folder if 'break_after_first' is True.
      """
    source_folder = os.path.join(Lab_path, "TODO")
    destination_folder = os.path.join(Lab_path, "READY")
    fichiers_supprimes = {}
    for nom in os.listdir(source_folder):
        chemin = os.path.join(source_folder, nom)
        print(nom)
        if os.path.isdir(chemin):
            folder = chemin
            folder = folder + "/"
            mp4_to_mp3(folder)
            dump_srt(folder)
            fichiers_supprimes = do_script_file(folder, fichiers_supprimes, niche,aspect_ratio, d_id=False, dalee=False, check_up=check_up, img_creation=img_creation)



            if check_condition:
                if not key_exists_in_json(os.path.join(folder, "edit_data.json"), "Words"):
                    words_highlight(folder)
                    emoji_suggester(folder)
                    # music_suggester(folder)
                else:
                    print("deja fait")
            else:
                words_highlight(folder)
                emoji_suggester(folder)
                music_suggester(folder)

            shutil.move(folder, destination_folder)

            if break_after_first:
                break

    return True


def get_done(Lab_path):
    """
    Automates video processing in a 'Lab' working environment.

    The 'Lab' folder contains three sub-folders: 'TODO', 'READY', and 'DONE'.
    'get_done' manages the folders in 'READY', where each folder represents a video ready for editing.

    Process:
    - For each folder in 'READY', checks if 'edit_data.json' exists. This file contains essential information for video
     editing.
    - Executes 'ae_script()' for editing the video. This script should return 0 to indicate success.
    - Upon success, moves the processed folder to the 'DONE' directory, thus marking the completion of the video's
     processing.
    - If 'ae_script()' fails (returns a non-zero value), the function reports an error and stops, returning 'False'.
    :param Lab_path:
    :return:
    """
    source_folder = os.path.join(Lab_path, "READY")
    destination_folder = os.path.join(Lab_path, "DONE")
    for nom in os.listdir(source_folder):
        chemin = os.path.join(source_folder, nom)
        print(nom)
        if os.path.isdir(chemin):
            folder = chemin
            fold = folder
            folder = folder + "/"
            chemin_fichier = os.path.join(folder, "edit_data.json")
            if os.path.exists(chemin_fichier):
                output = ae_script()
                if output != 0:
                    return False
            shutil.move(fold, destination_folder)
    return True
# get_ready("/Users/emmanuellandau/Documents/EditLab", "astrologenial", aspect_ratio='9:16',
#           break_after_first=False, check_condition=True, check_up=False, img_creation=False)

#get_ready("/Users/emmanuellandau/Documents/EditLab", "reddit_stories", break_after_first=False, check_condition=True)
# id = find_folder_id("TODO")
# synchronize_subfolders("/Users/emmanuellandau/Documents/EditLab/READY", id)

get_done("/Users/emmanuellandau/Documents/EditLab")
#
#


