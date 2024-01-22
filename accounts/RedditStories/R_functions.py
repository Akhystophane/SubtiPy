import os.path

from selenium import webdriver

from mediaLab.DiscordBot import load_bot, generate_img, patterned
from suggesterLab.SuggesterAi import find_path, remplacer_numeros_par_timestamps
from suggesterLab.footageSuggester import get_footage_dict, create_dict3, get_midjourney_dict
from suggesterLab.functions import update_json, extract_dict, get_char, formatter_srt, time_to_seconds
from PIL import Image
import os

def convert_webp_to_png(directory):
    # Parcourir tous les fichiers dans le répertoire
    for filename in os.listdir(directory):
        if filename.endswith('.webp'):
            # Chemin complet de l'image WebP
            webp_path = os.path.join(directory, filename)

            # Ouvrir l'image WebP
            image = Image.open(webp_path)

            # Définir le nom du fichier PNG
            png_filename = filename[:-5] + '.png'
            png_path = os.path.join(directory, png_filename)

            # Enregistrer l'image au format PNG
            image.save(png_path, 'PNG')

            print(f"Converti: {webp_path} en {png_path}")

# Utilisation de la fonction
# convert_webp_to_png("/Users/emmanuellandau/Documents/EditLab/READY/test")



def do_script_file(folder, fichiers_supprimes, niche):
    def image_creator(prompts):
        prompts_path = []
        driver = webdriver.Chrome()
        load_bot(driver)
        for prompt in prompts:
            if os.path.exists(f'/Users/emmanuellandau/Documents/MidjourneyBibli/{patterned(prompt)}.png'):
                path = f'/Users/emmanuellandau/Documents/MidjourneyBibli/{patterned(prompt)}.png'
            else:
                path = generate_img(driver, prompt, folder)

            prompts_path.append(path)

        return prompts_path


    script_text = get_midjourney_dict(folder)
#     script_text = {
# 0: "Two children, a boy and a girl close in age, playing together.",
# 1: "A group of children sitting in a circle, a sense of confidentiality between them.",
# 10: "A girl and a boy, presumably siblings, growing up together closely.",
# 26: "The elder brother packing his bags for university in a foreign country.",
# 35: "Bustling airport scene with the brother waving goodbye to his family.",
# 42: "The sister being proposed to by her long-term boyfriend.",
# 50: "The brother alone in a new city, feeling homesick and struggling with depression.",
# 62: "The brother boarding a plane back home.",
# 69: "Some glimpse of a wedding preparation, showcasing the excitement of a wedding ceremony.",
# 81: "A rich father-in-law presented in an opulent setting.",
# 110: "The brother going back to studying in a university library.",
# 132: "The brother returning home during the holidays beaming with excitement.",
# 142: "A surprise birthday party for the parents with the entire family present.",
# 170: "The brother and sister getting into a taxi after a fun night out.",
# 206: "The brother and sister sitting in the guest room, chatting and catching up."
# }
    dict2 = get_footage_dict(folder, niche)

    timestamps_l = create_dict3(script_text, dict2)
    timestamps_l = remplacer_numeros_par_timestamps(timestamps_l, folder + "audio.srt")
    timestamps_l = [[valeur, time_to_seconds(cle)] for cle, valeur in timestamps_l.items()]
    print(timestamps_l)

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


