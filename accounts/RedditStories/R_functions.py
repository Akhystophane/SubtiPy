import json
import os.path

from selenium import webdriver

from mediaLab.DiscordBot import load_bot, generate_img, patterned
from suggesterLab.SuggesterAi import find_path, remplacer_numeros_par_timestamps, get_bibli, get_relevant_signs, \
    sont_similaires
from suggesterLab.footageSuggester import get_footage_dict, create_dict3, get_midjourney_dict, insert_a_roll, \
    get_footageV2_dict
from suggesterLab.functions import update_json, extract_dict, get_char, formatter_srt, time_to_seconds
from PIL import Image
import os
import requests
from openai import OpenAI

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


def edit_element(liste_de_listes, element, nouvelle_valeur):
    """
    Modifie un élément dans une liste de listes.

    :param liste_de_listes: Liste de listes dans laquelle chercher.
    :param élément_recherché: Élément à rechercher et à modifier dans la liste de listes.
    :param nouvelle_valeur: Nouvelle valeur à assigner à l'élément trouvé.
    :return: Booléen indiquant si la modification a été effectuée.
    """
    for i, sous_liste in enumerate(liste_de_listes):
        if element in sous_liste:
            index_element = sous_liste.index(element)
            liste_de_listes[i][index_element] = nouvelle_valeur
            return liste_de_listes
    return False


def filtrer_elements(elements, n_epargnes):
    if len(elements) <= n_epargnes:  # Si la longueur de la liste est inférieure ou égale à n_epargnes, retourner la liste telle quelle.
        return elements

    # Initialiser la liste filtrée avec les n premiers éléments à épargner
    elements_filtrés = elements[:n_epargnes]

    # Parcourir la liste à partir de l'élément après les n épargnés
    for i in range(n_epargnes, len(elements)):
        # Convertir les timestamps en float pour la comparaison
        timestamp_actuel = float(elements[i][1])
        timestamp_précédent = float(elements_filtrés[-1][1])

        # Si la différence est de 2 secondes ou plus, ajouter l'élément à la liste filtrée
        if timestamp_actuel - timestamp_précédent >= 4:
            elements_filtrés.append(elements[i])

    return elements_filtrés


def add_signs_footages(folder, timestamps_l, niche):
    bibli = get_bibli(niche)
    dico = bibli.copy()
    signes_astrologiques = []


    elements_a_conserver = get_relevant_signs(folder, signes_astrologiques)

    dico['signes'] = [element for element in dico['signes'] if
                                  any(sont_similaires(sub, element, levenshtein_tolerance=0) for sub in elements_a_conserver)]

def do_script_file(folder, fichiers_supprimes, niche, d_id=False, dalee=False, script=False):
    def image_creator(prompts):
        prompts_path = []

        if not dalee:
            driver = webdriver.Chrome()
            load_bot(driver)
        for prompt in prompts:
            if not dalee:
                if os.path.exists(f'/Users/emmanuellandau/Documents/MidjourneyBibli/{patterned(prompt)}.png'):
                    path = f'/Users/emmanuellandau/Documents/MidjourneyBibli/{patterned(prompt)}.png'
                else:
                    path = generate_img(driver, prompt, folder)
            else:
                client = OpenAI()
                print(prompt)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1792",
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url
                print(image_url)
                path = os.path.join("/Users/emmanuellandau/Documents/MidjourneyBibli", f"{patterned(prompt)}.png")

                # Téléchargement et sauvegarde de l'image
                response = requests.get(image_url)
                # if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
            edit_timestamps_l = edit_element(timestamps_l, prompt, path)
            with open(backup_path, 'w') as fichier:
                fichier.write(json.dumps(edit_timestamps_l, indent=4))

            prompts_path.append(path)

        return prompts_path

    backup_path = folder + 'backup.json'
    if not os.path.exists(folder + 'backup.json'):
        script_text = get_midjourney_dict(folder)

        # dict2 = get_footage_dict(folder, niche)
        dict2 = get_footageV2_dict(folder, niche)

        timestamps_l = create_dict3(script_text, dict2, interval=3)
        timestamps_l = remplacer_numeros_par_timestamps(timestamps_l, folder + "audio.srt")
        timestamps_l = [[valeur, time_to_seconds(cle)] for cle, valeur in timestamps_l.items()]
        timestamps_l = filtrer_elements(timestamps_l, 2)
        if d_id:
            a_roll_path = os.path.join(folder,"a-roll")
            if not os.path.exists(a_roll_path):
                os.makedirs(a_roll_path)
            timestamps_l = insert_a_roll(folder, timestamps_l)
        print(timestamps_l)
        with open(backup_path, 'w') as fichier:
            fichier.write(json.dumps(timestamps_l, indent=4))
    else:
        with open(backup_path, 'r') as fichier:
            timestamps_l = json.load(fichier)

    chemin_fichier = folder + "edit_data.json"

    if script:
        print("dico3", timestamps_l)
        update_json(chemin_fichier, "Timestamps", timestamps_l)


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



