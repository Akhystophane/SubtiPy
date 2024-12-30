import ast
import json
import os.path
import plistlib
import random
import sys
import xattr as xattr

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from mediaLab.DiscordBot import load_bot, generate_img, patterned
from suggesterLab.SuggesterAi import find_path, remplacer_numeros_par_timestamps, get_bibli, get_relevant_signs, \
    sont_similaires, get_relevant_signsV2
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


def replace_paths(l1, l2, tolerance=6):
    # Convertir les clés de l1 en entiers pour faciliter les comparaisons
    l1_dict = {int(k): v for k, v in l1.items()}
    updates = []  # Pour enregistrer les mises à jour effectuées
    # Parcourir chaque élément dans l2
    for num2_str, path2 in l2:
        num2 = int(num2_str)
        # Trouver et remplacer les chemins dans l1 si les numéros sont suffisamment proches
        for num1 in list(l1_dict.keys()):
            if 0<= num2 - num1 <= tolerance:
                updates.append((str(num1), l1_dict[num1], path2))  # Enregistrer l'ancien et le nouveau chemin
                l1_dict[num1] = path2
                break

    # Reconstruire l1 avec les chemins mis à jour
    updated_l1 = {str(num): path for num, path in l1_dict.items()}
    print("updates : ",updates)

    return updated_l1


def add_signs_footages(folder, niche, timestamps_l):
    bibli = get_bibli(niche)
    dico = bibli.copy()
    sup_footages = []
    vrai_elements = []


    elements = get_relevant_signsV2(folder)
    print("elements_a_conserver: ", elements)

    for couple in elements:
        elements_a_conserver = [couple[1]]


        footages_l = [element for element in dico['signes'] if
                                      any(sont_similaires(sub, element, levenshtein_tolerance=0) for sub in elements_a_conserver) and element not in sup_footages]

        if footages_l:
            random_footage_name = random.choice(footages_l)
            couple[1] = find_path(random_footage_name, "astrologenial")
            sup_footages.append(random_footage_name)
            if '/' in couple[1]:
                vrai_elements.append(couple)
        else:
            print("plus de footages pour ce signe")
            # elements.remove(couple)
    print(vrai_elements)

    timestamps_l = replace_paths(timestamps_l, vrai_elements)
    print(timestamps_l)
    return timestamps_l

# add_signs_footages("/Users/emmanuellandau/Documents/EditLab/archive/Es-tu compatible avec un Poisson", "astrologenial", )


def do_script_file(folder, fichiers_supprimes, niche, aspect_ratio,
                   d_id=False, dalee=False, script=False, check_up=False, img_creation=True):
    def image_creator(prompts):
        prompts_path = []
        first = True
        profile_path = "/Users/emmanuellandau/Library/Application Support/Google/Chrome/Profile 1"

        if not dalee:
            chrome_options = Options()
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument(f"user-data-dir={profile_path}")
            driver = webdriver.Chrome( options=chrome_options)

            # driver = webdriver.Chrome()
            load_bot(driver)
        for prompt in prompts:
            prompt = prompt.replace(",","").lower()
            prompt = prompt.replace(".", "").lower()

            if not dalee:
                if os.path.exists(f'/Users/emmanuellandau/Documents/MidjourneyBibli/{patterned(prompt)}.png'):
                    path = f'/Users/emmanuellandau/Documents/MidjourneyBibli/{patterned(prompt)}.png'
                else:
                    path = generate_img(driver, prompt, first, aspect_ratio=aspect_ratio)
                    first = False
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

        script_text = get_midjourney_dict(folder, prompt="""Crée un dictionnaire  de 14 clés maximums
         distribué uniformément où chaque clé correspond au numéro de
     sous-titre du début d'une phrase entière dans le script : {{
  "num_srt de la phrase 1": independant description of an image, 
  "num_srt de la phrase 2": ...
}}. La clé 0 doit être incluse pour la première phrase. L'idee es de decrire succintement le passage dont il est question 
en le ratachant a un concept simple le choc, la tristesse, la joie, immagine une scene simple du type un individu sous le choc (pas plus de trois phrases). Assure-toi que les guillemets dans les valeurs soient échappés. Le résultat final doit être un dictionnaire
         formaté pour une utilisation informatique, avec une seule entrée par phrase complète.
          Ta réponse doit être uniquement le dictionnaire formaté correctement pour un usage direct dans un programme informatique.
           Voici le texte :""")
        if niche == "astrologenial":
            script_text = add_signs_footages(folder, niche, script_text)
            dict2 = get_footage_dict(folder, niche)
        else:
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
        if check_up:
            raise ValueError("Erreur check_up")
    else:
        with open(backup_path, 'r') as fichier:
            timestamps_l = json.load(fichier)

    chemin_fichier = folder + "edit_data.json"

    if script:
        print("dico3", timestamps_l)
        update_json(chemin_fichier, "Timestamps", timestamps_l)

    if img_creation:
        prompts = [item[0] for item in timestamps_l if not item[0].startswith('/') and "last" not in item[0]]
        path_prompts = image_creator(prompts)
        print(path_prompts)
        for i, item in enumerate(timestamps_l):
            if not item[0].startswith('/') and "last" not in item[0]:
                # Remplacer la clé par le chemin correspondant
                timestamps_l[i][0] = path_prompts.pop(0)

    print("dico3", timestamps_l)
    update_json(chemin_fichier, "Timestamps", timestamps_l)
    inspector(folder)



    return fichiers_supprimes



import json
import re
import os
import subprocess


def editor(folder):
    def srt_time_to_seconds(t):
        # t au format "hh:mm:ss,mmm"
        h, m, s = t.split(':')
        s, ms = s.split(',')
        return int(h) * 3600 + int(m) * 60 + float(s) + float(ms) / 1000.0

    def parse_srt(srt_file):
        # Retourne une liste de tuples (start, end, text)
        # start/end en secondes, text concaténé des lignes sous-titre
        entries = []
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        blocks = re.split(r'\n\n+', content)
        for block in blocks:
            lines = block.split('\n')
            if len(lines) < 3:
                continue
            time_line = lines[1]
            start_str, end_str = time_line.split(' --> ')
            start = srt_time_to_seconds(start_str)
            end = srt_time_to_seconds(end_str)
            text = ' '.join(l.strip() for l in lines[2:] if l.strip())
            entries.append((start, end, text))
        return entries

    def load_json(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def save_json(data, json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_intervals(timestamps):
        intervals = []
        for i in range(len(timestamps) - 1):
            current_file, current_ts = timestamps[i]
            next_file, next_ts = timestamps[i + 1]
            start = float(current_ts)
            end = float(next_ts)
            if 'last.mp4' in next_file:
                pass
            intervals.append((start, end, current_file))
        return intervals

    def find_subtitles_for_interval(entries, start, end):
        texts = []
        for (s_sub, e_sub, txt) in entries:
            if e_sub > start and s_sub < end:
                texts.append(txt)
        return ' '.join(texts)

    # Construire les chemins des fichiers
    json_file = os.path.join(folder, 'edit_data.json')
    srt_file = os.path.join(folder, 'audio.srt')

    # Charger les données
    data = load_json(json_file)
    timestamps = data["Timestamps"]

    entries = parse_srt(srt_file)
    intervals = get_intervals(timestamps)

    # Génération d'editor.txt
    editor_txt_path = os.path.join(folder, 'editor.txt')
    with open(editor_txt_path, 'w', encoding='utf-8') as out:
        for (start, end, filename) in intervals:
            txt = find_subtitles_for_interval(entries, start, end)
            # Ajouter une ligne vide entre chaque entrée
            out.write(f"{txt} : \n{filename}\n\n")



    print(f"Fichier 'editor.txt' généré à : {editor_txt_path}")

    # Ouvrir automatiquement le fichier dans l'application par défaut
    try:
        if os.name == 'nt':  # Windows
            os.startfile(editor_txt_path)
        elif os.name == 'posix':  # macOS ou Linux
            subprocess.run(['open', editor_txt_path] if sys.platform == 'darwin' else ['xdg-open', editor_txt_path])
    except Exception as e:
        print(f"Impossible d'ouvrir le fichier automatiquement : {e}")

    # Demande confirmation
    choice = input("Les changements conviennent ? (yes/no): ").strip().lower()
    if choice == 'yes':
        # L'utilisateur a peut-être modifié editor.txt, on le relit
        new_lines = []
        with open(editor_txt_path, 'r', encoding='utf-8') as f:
            new_lines = f.readlines()

        # Mise à jour des noms de fichiers dans le JSON
        i = 0
        for line_num in range(1, len(new_lines), 3):  # Saute les blocs de 3 lignes (texte, fichier, ligne vide)
            new_filename = new_lines[line_num].strip()  # Ligne du chemin du fichier
            data["Timestamps"][i][0] = new_filename  # Mise à jour du nom de fichier
            i += 1

        # Sauvegarde
        save_json(data, json_file)
        print(f"Fichier '{json_file}' mis à jour avec les nouveaux noms de fichiers.")
    else:
        print(f"Aucun changement n'a été apporté à '{json_file}'.")

# editor('/Users/emmanuellandau/Documents/EditLab/READY/La pleine lune du 15 decembre')

def inspector(folder):
    def load_json(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def save_json(data, json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def collect_files_with_comments(directories):
        files_dict = {}

        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)

                    try:
                        # Essaye de lire le commentaire via l'attribut étendu macOS
                        raw_comment = xattr.getxattr(file_path, 'com.apple.metadata:kMDItemFinderComment')
                        # Décodage du commentaire encodé en plist binaire

                        comment = plistlib.loads(raw_comment)
                        # Le commentaire est souvent dans une liste
                    except (OSError, KeyError, IndexError):
                        # Si le commentaire n'existe pas ou une erreur survient, laisse une chaîne vide
                        comment = ""

                    # Ajoute le fichier et son commentaire au dictionnaire
                    files_dict[file] = comment

        return files_dict

    # Répertoires à analyser
    directories = [
        "/Users/emmanuellandau/Documents/Astrologie/bibliothèque/Ai_videos"
    ]

    # Collecte des fichiers et commentaires
    fichiers = collect_files_with_comments(directories)

    client = OpenAI()
    json_file = os.path.join(folder, "edit_data.json")

    data = load_json(json_file)
    timestamps = data['Timestamps']
    descriptions = {}
    i=0

    for timestamp in timestamps:

        if '/Users' not in timestamp[0] and 'last' not in timestamp[0]:
            print(timestamp[0])
            descriptions[i] = timestamp[0]
            timestamp[0] = i
            i += 1
    print(fichiers)
    print(descriptions)

    prompt = f"""Tu dois à partir des descriptions suivantes me sélectionner le fichier qui correspond le mieux à chaque
    description parmi un groupe de fichiers qui sera au format {{nom_du_fichier:description du fichier}}.
    Tu ne peux pas réutiliser le même fichier deux fois. Ta réponse est au
    format JSON, echappe bien les caracteres car apres ta reponse sera parsée {{1: "nom_du_fichier.mp4", }}. Voici les descriptions : {descriptions} et voici les fichiers : {fichiers}."""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un assistant concentré."},
            {"role": "user", "content": prompt}
        ]
    )

    output = str(completion.choices[0].message.content)
    print(output)

    start = output.find("{")
    end = output.rfind("}") + 1

    dict = ast.literal_eval(output[start:end])
    print(timestamps)
    print(dict)

    for nbr, path in dict.items():
        for element in timestamps:
            media_path = os.path.join(directories[0], path)
            if element[0] == int(nbr) :
                if os.path.exists(media_path):
                    element[0] = media_path
                else:
                    raise FileNotFoundError(f"The path '{media_path}' does not exist.")

    data['Timestamps'] = timestamps
    # print(timestamps)
    save_json(data, json_file)


# inspector('/Users/emmanuellandau/Documents/EditLab/READY/Ne trahis jamais la confiance d’un Taureau')