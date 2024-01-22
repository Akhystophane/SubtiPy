import os
import shutil
import subprocess

from suggesterLab.SuggesterAi import emoji_suggester
from suggesterLab.functions import key_exists_in_json
from word_interest import words_highlight


def ae_script():
    # Commande à exécuter
    command = '''osascript -e "with timeout of 300 seconds" -e "tell application \\"Adobe After Effects 2023\\" to activate" -e "tell application \\"Adobe After Effects 2023\\" to DoScriptFile \\"/Users/emmanuellandau/Scripts_Adobe/SketcHub/aE-editor.jsx\\"" -e "end timeout"'''

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


def get_ready(Lab_path, check_condition=False, break_after_first=False):
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
    for nom in os.listdir(source_folder):
        chemin = os.path.join(source_folder, nom)
        print(nom)
        if os.path.isdir(chemin):
            folder = chemin
            folder = folder + "/"

            if check_condition:
                if not key_exists_in_json(os.path.join(folder, "edit_data.json"), "Words"):
                    words_highlight(folder)
                    emoji_suggester(folder)
                else:
                    print("deja fait")
            else:
                words_highlight(folder)
                emoji_suggester(folder)

            shutil.move(folder, destination_folder)

            if break_after_first:
                break

    return True

def get_done(Lab_path):

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

# get_ready("/Users/emmanuellandau/Documents/EditLab")
get_done("/Users/emmanuellandau/Documents/EditLab")

# ae_script()

