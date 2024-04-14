import json
import os.path

from selenium import webdriver

from mediaLab.DiscordBot import load_bot, generate_img, patterned
from suggesterLab.SuggesterAi import find_path, remplacer_numeros_par_timestamps
from suggesterLab.footageSuggester import get_footage_dict, create_dict3, get_midjourney_dict
from suggesterLab.functions import update_json, extract_dict, get_char, formatter_srt, time_to_seconds
from PIL import Image
import os

def do_script_file(folder, fichiers_supprimes, niche):


    backup_path = folder + 'backup.json'
    if not os.path.exists(folder + 'backup.json'):
        script_text = get_midjourney_dict(folder)

        dict2 = get_footage_dict(folder, niche)


        timestamps_l = create_dict3(script_text, dict2)
        timestamps_l = remplacer_numeros_par_timestamps(timestamps_l, folder + "audio.srt")
        timestamps_l = [[valeur, time_to_seconds(cle)] for cle, valeur in timestamps_l.items()]
        print(timestamps_l)
        with open(backup_path, 'w') as fichier:
            fichier.write(json.dumps(timestamps_l, indent=4))
    else:
        with open(backup_path, 'r') as fichier:
            timestamps_l = json.load(fichier)

    chemin_fichier = folder + "edit_data.json"
    prompts = [item[0] for item in timestamps_l if not item[0].startswith('/') and "last" not in item[0]]
    path_prompts = image_creator(prompts)
    print(path_prompts)
    for i, item in enumerate(timestamps_l):
        if not item[0].startswith('/') and "last" not in item[0]:
            # Remplacer la clé par le chemin correspondant
            timestamps_l[i][0] = path_prompts.pop(0)

    print("dico3", timestamps_l)
    update_json(chemin_fichier, "Timestamps", timestamps_l)



    return fichiers_supprimes