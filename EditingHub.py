import os
import shutil
import subprocess


from AudioLab import dump_srt
from getEndTime import dump_points
from SubtiLab import make_sub
from suggesterLab.SuggesterAi import emoji_suggester, do_script_file, get_bibli, music_suggester, check_json
from word_interest import words_highlight


def ae_script():
    # Commande à exécuter
    command = '''osascript -e "tell application \\"Adobe After Effects 2023\\" to activate" -e "tell application \\"Adobe After Effects 2023\\" to DoScriptFile \\"/Users/emmanuellandau/Scripts_Adobe/aE-test.jsx\\""'''
    command = '''osascript -e "with timeout of 300 seconds" -e "tell application \\"Adobe After Effects 2023\\" to activate" -e "tell application \\"Adobe After Effects 2023\\" to DoScriptFile \\"/Users/emmanuellandau/Scripts_Adobe/aE-test.jsx\\"" -e "end timeout"'''

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




def get_ready(Lab_path, niche):
    source_folder = os.path.join(Lab_path, "READY")
    destination_folder = os.path.join(Lab_path, "READY")
    fichiers_supprimes = {}
    dico = get_bibli(niche)
    for nom in os.listdir(source_folder):
        chemin = os.path.join(source_folder, nom)
        print(nom)
        if os.path.isdir(chemin):
            folder = chemin
            fold = folder
            folder = folder + "/"
            # check_json(folder)
            # dump_srt(folder)
            # chemin_fichier = folder + "edit_data.json"
            # if not os.path.exists(chemin_fichier):
            # dico, fichiers_supprimes = do_script_file(folder, fichiers_supprimes, dico, niche)
            # os.remove(chemin_fichier)
            # dump_points(folder, niche)
            words_highlight(folder)
            emoji_suggester(folder)
            music_suggester(folder)
            # break
            # shutil.move(fold, destination_folder)
            # break
    return True

# get_ready("/Users/emmanuellandau/Documents/EditLab")
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

# get_ready("/Users/emmanuellandau/Documents/EditLab", "astrologenial")
get_done("/Users/emmanuellandau/Documents/EditLab")



