import ast
import string
import unicodedata
from Levenshtein import distance
import json
import shutil
import re
import openai
from openai import OpenAI
from suggesterLab.Emojis import convert_emoji
from suggesterLab.footageSuggester import get_footage_dict, create_dict3
from suggesterLab.functions import update_json, extract_dict, get_char, formatter_srt, time_to_seconds, formatter_srtV2
import tiktoken
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

signes_astrologiques = [
    "Bélier",
    "Taureau",
    "Gémeaux",
    "Cancer",
    "Lion",
    "Vierge",
    "Balance",
    "Scorpion",
    "Sagittaire",
    "Capricorne",
    "Verseau",
    "Poisson"
]
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

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

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def emoji_suggester(folder):
    def save_png_emoji(emojis_l):
        for num_srt in emojis_l.keys():
            convert_emoji(emojis_l[num_srt], folder)

    niche = "astrologie"
    l_srt = []
    sentence = {}
    flag = False
    with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n\n')
        for subtitle in content:
            lines = subtitle.split('\n')
            if not flag:
                num_srt = 1
                flag = True
            else:
                num_srt = lines[0]

            text_only = '\n'.join(lines[2:])

            sentence[num_srt] = text_only

            if "." in text_only:
                l_srt.append(sentence)
                sentence = {}

    prompt2 = f"""Je réalise en Python des sous-titres pour une vidéo sur l'{niche}. Voici une liste qui contient des
     dicts de phrases avec chaque srt :{l_srt}, tu dois me renvoyer un dictionnaire avec comme clés: num du srt et
      valeur: un émoji pertinent (au format lisible Python comme : \U0001F47D) qui pourrait être affiché. 
      Par phrases quelques srt doivent avoir un émoji, environ 1/3 des srt (les autres srt ne sont pas dans 
      le dict renvoyé). Ta réponse ne doit contenir que le dictionnaire, pas d'autre texte parasite qui fera
       crasher mon programme."""

    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "Tu es un assistant programmeur rigoureux"},
    #         {"role": "user", "content": prompt2}
    #     ]
    # )
    # print({response['choices'][0]['message']['content']})
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt2}
        ]
    )
    print(str(completion.choices[0].message.content))
    chemin_fichier = folder + "edit_data.json"
    emojis_l = extract_dict(str(completion.choices[0].message.content))
    update_json(chemin_fichier, "Emojis", emojis_l)
    save_png_emoji(emojis_l)
    return emojis_l

def lister_dossier(dossier):
    """
    Liste de manière récursive tous les fichiers d'un dossier et ses sous-dossiers.

    :param dossier: Le chemin du dossier à lister
    :return: un dictionnaire où chaque clé est un chemin de sous-dossier ou un fichier
             et chaque valeur est soit une liste de fichiers (pour un dossier) soit None (pour un fichier).
    """
    result = {}

    # Listons tous les éléments dans le dossier
    for nom in os.listdir(dossier):
        chemin_complet = os.path.join(dossier, nom)
        # Si c'est un fichier, ajoutez-le avec une valeur None
        if os.path.isfile(chemin_complet):
            result[chemin_complet] = None
        # Si c'est un sous-dossier, l'ajouter au dictionnaire de manière récursive
        elif os.path.isdir(chemin_complet):
            result[chemin_complet] = lister_dossier(chemin_complet)

    return result

def lister_dossier_dans_dossier(dossier):
    fichiers = [f for f in os.listdir(dossier) if os.path.isdir(os.path.join(dossier, f))]
    l_dossier = []
    for fichier in fichiers:
        l_dossier.append(fichier)
    return l_dossier

def lister_fichiers_dans_dossier(dossier):
    """
    Liste uniquement les fichiers dans un dossier spécifié sans parcourir ses sous-dossiers.

    :param dossier: Le chemin du dossier à lister
    :return: une liste des fichiers du dossier spécifié
    """
    fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    l_sign = []
    for fichier in fichiers:
        if fichier != ".DS_Store":
            l_sign.append(fichier)
    return l_sign


def append_files(sous_dossiers, dossier_principal, num=True):
    folders = {}
    for sous_dossier in sous_dossiers:
        path_sous_dossier = os.path.join(dossier_principal, sous_dossier)
        if num:
            folders[sous_dossier] = len(lister_fichiers_dans_dossier(path_sous_dossier))
        else:
            folders[sous_dossier] = lister_fichiers_dans_dossier(path_sous_dossier)
    return folders

def relevant_l(sign_names,niche):
    bibli = get_bibli(niche, num=False)

    signes = bibli["signes"]
    signe_l = []
    for sign_name in sign_names:
        for signe in signes:
            if sign_name in signe:
                signe_l.append(signe)
    return signe_l
def sont_similaires(s1, s2, levenshtein_tolerance=2):

    # Convertir en minuscules
    s1, s2 = s1.lower(), s2.lower()

    # Supprimer les espaces au début et à la fin
    s1, s2 = s1.strip(), s2.strip()

    # Supprimer tous les espaces
    s1, s2 = s1.replace(" ", ""), s2.replace(" ", "")

    # Supprimer la ponctuation
    translator = str.maketrans('', '', string.punctuation)
    s1, s2 = s1.translate(translator), s2.translate(translator)

    # Normaliser (supprimer les accents)
    s1 = unicodedata.normalize('NFD', s1).encode('ascii', 'ignore').decode("utf-8")
    s2 = unicodedata.normalize('NFD', s2).encode('ascii', 'ignore').decode("utf-8")
    if levenshtein_tolerance == 3:
        print(s1, s2, distance(s1, s2))
    # Comparer les chaînes nettoyées ou vérifier la distance de Levenshtein
    if s1 == s2 or distance(s1, s2) <= levenshtein_tolerance or s1 in s2:
        return True
    return False


def get_relevant_signs(folder, signes):
    relevant_signs = set()  # Utilisez un ensemble pour éviter les doublons
    chemin_fichier = folder + "description.txt"

    with open(chemin_fichier, 'r') as fichier:
        contenu = fichier.read()

    # Divisez le contenu en mots
    mots = contenu.split()

    for mot in mots:
        for signe in signes:
            if sont_similaires(signe, mot):
                relevant_signs.add(signe)  # Ajoutez le signe à l'ensemble s'il est similaire

    return list(relevant_signs)



def get_relevant_signsV2(folder, seuil_max=1):
    relevant_signs = []  # Liste pour garder la trace des sous-titres pertinents
    chemin_fichier = folder + "/audio.srt"  # Assurez-vous d'ajouter un slash ici pour le chemin correct

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        content = fichier.read().strip().split('\n\n')
        for subtitle in content:
            lines = subtitle.split('\n')
            subtitle_number = lines[0]
            subtitle_text = ' '.join(lines[2:])  # Concatène toutes les lignes de texte du sous-titre
            found_signs = []
            words = subtitle_text.split()
            for sign in signes_astrologiques:
                # Cherche chaque signe dans le texte en utilisant la distance de Levenshtein
                if any(distance(sign.lower(), word.lower()) <= seuil_max for word in words):
                    # print(subtitle_number, subtitle_text)
                    found_signs.append(sign)
            if found_signs:
                relevant_signs.append([subtitle_number] + found_signs)  # Ajoute le numéro de sous-titre et les signes trouvés

    return relevant_signs


def find_path(png_name, niche):
    """
    Trouve le chemin d'un png depuis un dictionnaire jusqu'à un dossier principal.

    Args:
    - png_name (str) : Nom du fichier png.
    - data_dict (dict) : Dictionnaire contenant les données.
    - main_folder (str) : Nom du dossier principal.

    Returns:
    - str : Chemin complet du png.
    """
    main_folder = get_char(niche, "bibli")
    for racine, _, fichiers in os.walk(main_folder):
        if png_name in fichiers:
            return os.path.join(racine, png_name)
    print("pas de ", png_name)
    return None

#-----------------------------------------------------------------------------------------------------------------------




def get_bibli(niche, num=False):
    dossier_principal = get_char(niche, "bibli")

    sous_dossiers = lister_dossier_dans_dossier(dossier_principal)

    folders = append_files(sous_dossiers, dossier_principal, num=num)
    folders = {normaliser_cle(cle): valeur for cle, valeur in folders.items()}
    # print("folders", niche, folders)
    return folders


def remplacer_numeros_par_timestamps(dictionnaire, fichier_srt):
    # Lire le fichier SRT et construire un dictionnaire de mapping numéro -> timestamp
    mapping = {}
    dernier_timestamp = None
    with open(fichier_srt, 'r', encoding='utf-8') as file:
        contenu = file.read().strip().split('\n\n')
        for bloc in contenu:
            lignes = bloc.split('\n')
            numero = int(lignes[0].strip())
            timestamp = lignes[1].split(' --> ')[0]
            mapping[numero] = timestamp
            dernier_timestamp = lignes[1].split(' --> ')[1]  # Mise à jour du dernier timestamp

    # Remplacer les clés dans le dictionnaire original par les timestamps
    nouveau_dictionnaire = {}
    for numero, valeur in dictionnaire.items():
        timestamp = mapping.get(int(numero))
        if timestamp:
            nouveau_dictionnaire[timestamp] = valeur

    # Vérifier que le dictionnaire n'est pas trop petit
    if len(nouveau_dictionnaire) <= 4:
        raise Exception("Le dictionnaire est trop petit: ", nouveau_dictionnaire)

    # Ajouter le dernier timestamp avec la clé "last.mp4"
    if dernier_timestamp:
        nouveau_dictionnaire[dernier_timestamp] = "last.mp4"

    return nouveau_dictionnaire

def do_script_file(folder, fichiers_supprimes, niche):
    def remplacer_par_fichier_aleatoire(bibli, fichiers_supprimes, script_text):
        print("bibli", bibli)
        fichiers_disponibles = None
        cles_a_supprimer = []  # Liste pour stocker les clés à supprimer
        for num_sous_titre, sous_dossier in script_text.items():
            if sous_dossier == "last.mp4":
                continue
            # Liste des fichiers disponibles dans le sous-dossier
            elif ".png" in sous_dossier:
                fichier_choisi = re.search(r'[^/\[\]]+\.png', sous_dossier).group()
                script_text[num_sous_titre] = find_path(fichier_choisi, niche)
                print(f"le chemin de {sous_dossier} est {find_path(fichier_choisi, niche)}")

            # if not ".png" in sous_dossier:
            #     fichiers_disponibles = [f for f in bibli[sous_dossier] if f not in fichiers_supprimes.get(sous_dossier, [])]

            elif not ".png" in sous_dossier:
                # Choix aléatoire d'un fichier
                fichiers_disponibles = [f for f in bibli[sous_dossier] ]
                fichier_choisi = random.choice(fichiers_disponibles)

                # Mise à jour du script_text
                script_text[num_sous_titre] = find_path(fichier_choisi, niche)

                # # Ajout du fichier aux fichiers supprimés pour éviter les duplicatas
                # if sous_dossier in fichiers_supprimes:
                #     fichiers_supprimes[sous_dossier].append(fichier_choisi)
                # else:
                #     fichiers_supprimes[sous_dossier] = [fichier_choisi]
            else:
                cles_a_supprimer.append(num_sous_titre)

            # Suppression des clés après l'itération
        for cle in cles_a_supprimer:
            del script_text[cle]
        return fichiers_supprimes, script_text

    bibli = get_bibli(niche)
    dico = bibli.copy()
    for cle in fichiers_supprimes:
        if cle in dico:
            # Créer un nouvel ensemble pour dico2[cle] excluant les éléments de dico1[cle]
            dico[cle] = [element for element in dico[cle] if element not in fichiers_supprimes[cle]]

    elements_a_conserver = get_relevant_signs(folder, signes_astrologiques)

    dico['signes'] = [element for element in dico['signes'] if
                                  any(sont_similaires(sub, element, levenshtein_tolerance=0) for sub in elements_a_conserver)]
    if niche == "astrologenial":
        for cle, valeur in dico.items():
            if cle != 'signes' and isinstance(valeur, list):
                dico[cle] = len(valeur)
        with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
            txt = formatter_srtV2(file.read())
    # elif niche == "mbti":
    #     dico, txt = get_dico_mbti()
    # else:
    #     dico, txt = None, None
    # print(dico_num)
    prompt = get_char(niche, "prompt_test")
    # prompt = get_char(niche, "prompt_suspens")

    prompt = prompt.replace("{dico_num}", str(dico))
    prompt = prompt.replace("{txt}", str(txt))

    print(prompt)

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = str(completion.choices[0].message.content)


    #ligne pour tester sans utiliser les credits du LLM
    # script_text = "{0: 'signes/Poisson_evil.png', 5: 'personne_mystère_peur', 15: 'signes/Poisson.png', 18: 'personne_mystère_positive', 29: 'signes/Poisson_smiling.png', 40: 'personne_angélique', 50: 'signes/Poisson_apeuré.png', 61: 'couples_de_signes', 72: 'signes/Cancer_dark.png', 81: 'personne_démoniaque'}"
    start = script_text.find("{")
    end = script_text.rfind("}") + 1
    script_text = ast.literal_eval(script_text[start:end])
    print('-------------------------------------------------------------------------------------')
    print('dict1: ', script_text)
    print('-------------------------------------------------------------------------------------')

    fichiers_supprimes, script_text = remplacer_par_fichier_aleatoire(bibli, fichiers_supprimes, script_text)
    # timestamps_l = [[valeur, time_to_seconds(cle)] for cle, valeur in script_text.items()]
    # dict1 = {time_to_seconds(time_str): video_path for time_str, video_path in script_text.items()}

    dict2 = get_footage_dict(folder, niche)
    dict2 = {cle: valeur for cle, valeur in dict2.items() if valeur is not None and not isinstance(valeur, str) or (
                isinstance(valeur, str) and "none" not in valeur.lower())}
    timestamps_l = create_dict3(script_text, dict2)
    timestamps_l = remplacer_numeros_par_timestamps(timestamps_l, folder + "audio.srt")
    timestamps_l = [[valeur, time_to_seconds(cle)] for cle, valeur in timestamps_l.items() if
                    cle is not None and valeur is not None]
    timestamps_l = zeroed_timestamp(timestamps_l)
    chemin_fichier = folder + "edit_data.json"
    print("dico3", timestamps_l)

    update_json(chemin_fichier, "Timestamps", timestamps_l)

    return fichiers_supprimes

def normaliser_cle(cle):
    return unicodedata.normalize('NFC', cle)

import os
import random

def trouver_premier_chiffre(chaine):
    for caractere in chaine:
        if caractere.isdigit():
            return caractere
    return None  # Retourne None si aucun chiffre n'est trouvé

def get_random_file_path(base_folder, var):
    # Sélectionnez le sous-dossier en fonction de la variable
    if var == 1:
        subfolder = 'epic'
    elif var == 2:
        subfolder = 'bad'
    else:
        subfolder = 'neutral'

    # Construisez le chemin complet du sous-dossier
    subfolder_path = os.path.join(base_folder, subfolder)

    # Vérifiez si le sous-dossier existe et contient des fichiers
    if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
        files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
        if files:
            return os.path.join(subfolder_path, random.choice(files))
    print("erreuuuuuuuuuur---------------------------------------------------------------------------------------------")
    # Si le sous-dossier n'existe pas, ne contient pas de fichiers ou si une autre erreur se produit, retournez None
    return None



def music_suggester(folder):
    titre = os.path.basename(os.path.normpath(folder))
    prompt = f""""
        Voici le titre de ma vidéo {titre}, mon algorithme utilise ta réponse pour attribuer lui associer une musique.
        Si le titre t'inspire  des émotions positives renvoie 1 s'il t'inspire de la négativté, ou de la peur renvoie 2.
        Ta réponse ne contient qu'un seul caractère, le chiffre 1 ou 2.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un assistant consciencieux"},
            {"role": "user", "content": prompt}
        ]
    )
    num = response['choices'][0]['message']['content']
    try:
        num = int(trouver_premier_chiffre(num))
    except:
        print(f"num est{num} ce n'est pas valide !!!!")
        num = 3
    path_music = get_random_file_path("/Users/emmanuellandau/Documents/music", num)

    # Copie le fichier.
    shutil.copy(path_music, folder)
    return True

def renommer_fichiers(dossier_principal):
    """
    Parcourt tous les sous-dossiers d'un dossier principal et remplace les espaces
    dans les noms de fichier par des underscores (_).
    :param dossier_principal: Le chemin du dossier principal.
    """
    for racine, _, fichiers in os.walk(dossier_principal):
        for nom_fichier in fichiers:
            if " " in nom_fichier:
                chemin_original = os.path.join(racine, nom_fichier)
                nouveau_nom = nom_fichier.replace(" ", "_")
                chemin_nouveau = os.path.join(racine, nouveau_nom)
                os.rename(chemin_original, chemin_nouveau)
                print(f"'{chemin_original}' a été renommé en '{chemin_nouveau}'")

def save_settings():

    text_astro = f""""
Je développe un contenu vidéo avec sous-titres numérotés et un dictionnaire Python. Script : {{text}}
 Besoin d'ajouter des mot clés émotions de base ressenti par l'être humain (anger, sad, friendship, thoughtful, lovers, 
 intelligent, evil, caring) anglais toute les  phrases du script illustrant le passage lié au sous titre, exemple
{{(num_start, num_end): liste python ["emotion"]}}. S'il te plaît, cree le dictionnaire avec une entrée  pertinentes
 par phrase. Note importante : ta réponse ne doit contenir que le dictionnaire amendé qui est envoyé directement à un 
 programme informatique de montage, donc il est impératif que ta réponse soit qu'un dictionnaire.
    
    """

    # Convertir la chaîne en une seule ligne pour le stockage JSON
    texte_single_line = text_astro.replace("\n", "\\n")

    # Créer un dictionnaire pour stocker vos données
    data = {
    "astrologenial": {
        "prompt": "\"\\n\\nJe r\u00e9alise des vid\u00e9os de mani\u00e8re automatis\u00e9e \u00e0 partir d'un script. j'ai besoin qu'\u00e0 partir du texte de ma vid\u00e9o tu me\\n sugg\u00e8res les endroits o\u00f9 je dois changer d'image de mani\u00e8re \u00e0 r\u00e9aliser le montage \u00e0 posteriori. \\n    Ta r\u00e9ponse est envoy\u00e9 directement a un programme informatique de montage  donc il est imp\u00e9ratif que ta r\u00e9ponse ne comporte uniquement\\n    le texte amend\u00e9 (pas de texte parasite) avec les noms d'images ajout\u00e9s dans le texte comme un mot sans quote.\\n  Tu devras ajouter le nom de l'image ou de la vid\u00e9o o\u00f9 elle devra commencer \u00e0 s'afficher. Tu auras \u00e0 ta disposition\\n   un set d'images qui contiennent dans leur nom des indications. en fonction de ces indications tu choisiras une photo\\n    pertinente . Une image doit toujours \u00eatre affich\u00e9e, ton texte COMMENCE donc avec une image! et se termine avec une phrase.\\n    Je change d'image toutes les phrases ou rarement apr\u00e8s un temps fort comme une virgule. Je veux entre 7 et 9 images.\\n      Le th\u00e8me de la vid\u00e9o et du dataset est l'astrologie, tu ne dois pas utiliser deux fois\\n      la m\u00eame image. Si la valeur de la cl\u00e9 est un chiffre n, tu as n images diff\u00e9rentes avec le m\u00eame effet, tu peux \\n      ins\u00e9rer ange4.png et ange8.png par exemple. \\n\\n\\nVoici le texte de la vid\u00e9o:{txt}\\n\\nVoici le set d\u2019images: {dico_num}\\nIl est imp\u00e9ratif que le nom de l'image soit comme dans le set ou dans le format sp\u00e9cifi\u00e9 en amont car c'est envoy\u00e9 a un algo.\\nSi c'est une vid\u00e9o myst\u00e8re privil\u00e9gie les images qui ne r\u00e9f\u00e8rent pas \u00e0 un signe en particulier jusqu'au moment o\u00f9 son identit\u00e9 et d\u00e9voil\u00e9\\n\\n",
        "prompt_test": "\"\\n        Je r\u00e9alise des vid\u00e9os de mani\u00e8re automatis\u00e9e \u00e0 partir d'un script. J'ai besoin que, \u00e0 partir du texte de ma vid\u00e9o, tu me sugg\u00e8res les endroits o\u00f9 je dois changer d'image pour r\u00e9aliser le montage \u00e0 posteriori au format d'un dictionnaire  de 10 cl\u00e9s maximum qui a comme cl\u00e9 le num\u00e9ro du sous titre et comme valeur le nom de l'image ou du dossier, le  sous-titre 0 a necessairement une image, les nuumeros que tu choisiras par le suite seront ceux des debuts de phrases, ou mdu moins pas trop rapproche. Mon texte est compos\u00e9 du script de ma video avec le num\u00e9ro des sous-titres entre accolades. Ta r\u00e9ponse ne doit contenir que le dictionnaire qui est envoy\u00e9e directement \u00e0 un programme informatique de montage, donc il est imp\u00e9ratif que ta r\u00e9ponse soi un dictionnaire. Tu auras \u00e0 ta disposition un set de noms de sous dossiers et d'images qui contiennent dans leur nom des indications. En fonction de ces indications, tu choisiras une photo ou un sous-dossier pertinent. Je change d'image \u00e0 chaque phrase ou rarement apr\u00e8s un temps fort comme une virgule. Je veux entre 7 et 9 images. Le th\u00e8me de la vid\u00e9o et du dataset est l'astrologie, tu peux utiliser plusieur fois le meme nom de dossier mais tu ne dois pas utiliser deux fois la m\u00eame image.\\n        Texte vid\u00e9o = {txt}\\n        Dataset = {dico_num}\\n    \\n    ",
        "prompt_footage":texte_single_line,
        "bibli": "/Users/emmanuellandau/Documents/Astrologie/bibliothe\u0300que"
    },
    "mbti": {
        "prompt": "\"\\n\\nJe r\u00e9alise des vid\u00e9os de mani\u00e8re automatis\u00e9e \u00e0 partir d'un script. j'ai besoin qu'\u00e0 partir du texte de ma vid\u00e9o tu me\\n sugg\u00e8res les endroits o\u00f9 je dois changer d'image de mani\u00e8re \u00e0 r\u00e9aliser le montage \u00e0 posteriori. \\n    Ta r\u00e9ponse est envoy\u00e9 directement a un programme informatique de montage  donc il est imp\u00e9ratif que ta r\u00e9ponse ne comporte uniquement\\n    le texte amend\u00e9 (pas de texte parasite) avec les noms d'images ajout\u00e9s dans le texte comme un mot sans quote.\\n  Tu devras ajouter le nom de l'image ou de la vid\u00e9o o\u00f9 elle devra commencer \u00e0 s'afficher. Tu auras \u00e0 ta disposition\\n   un set d'images qui contiennent dans leur nom des indications. en fonction de ces indications tu choisiras une photo\\n    pertinente . Une image doit toujours \u00eatre affich\u00e9e, ton texte COMMENCE donc avec une image! et se termine avec une phrase.\\n    Je change d'image toutes les phrases ou rarement apr\u00e8s un temps fort comme une virgule. Je veux entre 7 et 9 images.\\n      Le th\u00e8me de la vid\u00e9o et du dataset est le MBTI, tu ne dois pas utiliser deux fois\\n      la m\u00eame image.\\n\\n\\nVoici le texte de la vid\u00e9o:{txt}\\n\\nVoici le set d\u2019images: {dico_num}\\nIl est imp\u00e9ratif que le nom de l'image soit exactement comme dans le set ou dans le format sp\u00e9cifi\u00e9 en amont car c'est envoy\u00e9 a un algo.\\nSi c'est une vid\u00e9o myst\u00e8re privil\u00e9gie les images qui ne r\u00e9f\u00e8rent pas \u00e0 un signe en particulier jusqu'au moment o\u00f9 son identit\u00e9 et d\u00e9voil\u00e9\\n\\n",
        "bibli": "/Users/emmanuellandau/Documents/MBTI_bibliothe\u0300que 2"
    }
}

    # Écrire dans un fichier JSON
    with open('niche_settings.json', 'w') as f:
        json.dump(data, f, indent=4)

num = num_tokens_from_string("""feedback_l:  [((0, 1), {'': {4864929: 'woman-bookshop-faceless-stack-4864929', 3833491: 'a-heart-shaped-made-from-palm-leaves-for-photo-shots-background-3833491', 5857311: 'pregnant-woman-drinking-coffee-on-the-balcony-5857311'}}), ((0, 1), {'': {4864929: 'woman-bookshop-faceless-stack-4864929', 3833491: 'a-heart-shaped-made-from-palm-leaves-for-photo-shots-background-3833491', 5857311: 'pregnant-woman-drinking-coffee-on-the-balcony-5857311'}}), ((0, 1), {'': {4864929: 'woman-bookshop-faceless-stack-4864929', 3833491: 'a-heart-shaped-made-from-palm-leaves-for-photo-shots-background-3833491', 5857311: 'pregnant-woman-drinking-coffee-on-the-balcony-5857311'}}), ((2, 3), {'': {7280175: 'a-woman-crying-lying-down-on-the-ground-7280175', 7089379: 'a-woman-completing-her-scanning-test-7089379', 6707479: 'two-women-in-meditation-6707479'}}), ((2, 3), {'': {7280175: 'a-woman-crying-lying-down-on-the-ground-7280175', 7089379: 'a-woman-completing-her-scanning-test-7089379', 6707479: 'two-women-in-meditation-6707479'}}), ((2, 3), {'': {7280175: 'a-woman-crying-lying-down-on-the-ground-7280175', 7089379: 'a-woman-completing-her-scanning-test-7089379', 6707479: 'two-women-in-meditation-6707479'}}), ((4, 5), {'': {5728974: 'parents-5728974', 8875677: 'a-person-examining-a-man-s-eyes-8875677'}}), ((4, 5), {'': {5728974: 'parents-5728974', 8875677: 'a-person-examining-a-man-s-eyes-8875677'}}), ((6, 7), {'': {6010760: 'a-young-girl-suffering-from-cancer-6010760', 3779849: 'star-gazers-positioned-themselves-in-a-view-deck-on-a-starry-night-3779849', 3709511: 'a-couple-having-a-misunderstanding-3709511'}}), ((6, 7), {'': {6010760: 'a-young-girl-suffering-from-cancer-6010760', 3779849: 'star-gazers-positioned-themselves-in-a-view-deck-on-a-starry-night-3779849', 3709511: 'a-couple-having-a-misunderstanding-3709511'}}), ((6, 7), {'': {6010760: 'a-young-girl-suffering-from-cancer-6010760', 3779849: 'star-gazers-positioned-themselves-in-a-view-deck-on-a-starry-night-3779849', 3709511: 'a-couple-having-a-misunderstanding-3709511'}}), ((8, 10), {'': {6014527: 'a-woman-using-a-crystal-ball-6014527', 7859983: 'a-female-model-behind-a-glass-7859983', 4034130: 'light-man-sitting-glasses-4034130'}}), ((8, 10), {'': {6014527: 'a-woman-using-a-crystal-ball-6014527', 7859983: 'a-female-model-behind-a-glass-7859983', 4034130: 'light-man-sitting-glasses-4034130'}}), ((8, 10), {'': {6014527: 'a-woman-using-a-crystal-ball-6014527', 7859983: 'a-female-model-behind-a-glass-7859983', 4034130: 'light-man-sitting-glasses-4034130'}}), ((11, 13), {'': {3713693: 'a-man-slapping-and-grabbing-his-face-in-frustration-3713693', 6002038: 'a-young-man-jumping-from-high-places-6002038'}}), ((11, 13), {'': {3713693: 'a-man-slapping-and-grabbing-his-face-in-frustration-3713693', 6002038: 'a-young-man-jumping-from-high-places-6002038'}}), ((14, 15), {'': {3712708: 'a-person-walking-his-fingers-through-the-ray-of-light-3712708'}}), ((16, 17), {'': {4101314: 'man-people-office-emotions-4101314'}}), ((18, 20), {'': {4038499: 'couple-love-table-home-4038499', 4628755: 'a-stingray-underwater-4628755'}}), ((18, 20), {'': {4038499: 'couple-love-table-home-4038499', 4628755: 'a-stingray-underwater-4628755'}}), ((21, 23), {'': {4883894: 'a-man-digging-money-from-the-sand-4883894', 3888268: 'a-woman-model-hairdo-partially-covering-her-face-3888268'}}), ((21, 23), {'': {4883894: 'a-man-digging-money-from-the-sand-4883894', 3888268: 'a-woman-model-hairdo-partially-covering-her-face-3888268'}}), ((24, 26), {'': {6670687: 'video-of-man-with-face-covered-with-words-6670687', 4662088: 'hands-hand-sign-strong-4662088'}}), ((24, 26), {'': {6670687: 'video-of-man-with-face-covered-with-words-6670687', 4662088: 'hands-hand-sign-strong-4662088'}}), ((27, 30), {'': {4772527: 'hands-woman-clinic-doctor-4772527', 3894710: 'fashion-model-posing-black-background-3894710'}}), ((27, 30), {'': {4772527: 'hands-woman-clinic-doctor-4772527', 3894710: 'fashion-model-posing-black-background-3894710'}}), ((31, 34), {'': {7515918: 'a-dog-with-red-sunglasses-7515918'}}), ((35, 36), {'': {5199861: 'woman-in-white-dress-shirt-using-her-ipad-while-writing-5199861'}}), ((37, 39), {'': {3704109: 'a-couple-embracing-each-other-3704109', 7515910: 'a-dog-with-red-sunglasses-7515910'}}), ((37, 39), {'': {3704109: 'a-couple-embracing-each-other-3704109', 7515910: 'a-dog-with-red-sunglasses-7515910'}}), ((40, 41), {'': {3704911: 'a-couple-in-love-sharing-on-a-plated-pancakes-with-melted-chocolate-toppings-3704911', 5135860: 'couple-dancing-on-bed-5135860'}}), ((40, 41), {'': {3704911: 'a-couple-in-love-sharing-on-a-plated-pancakes-with-melted-chocolate-toppings-3704911', 5135860: 'couple-dancing-on-bed-5135860'}}), ((44, 47), {'': {4630687: 'a-couple-discreetly-holding-hands-4630687'}}), ((48, 51), {'': {7189100: 'an-animal-skull-7189100', 5839079: 'person-detected-of-a-virus-5839079'}}), ((48, 51), {'': {7189100: 'an-animal-skull-7189100', 5839079: 'person-detected-of-a-virus-5839079'}}), ((52, 54), {'': {5973873: 'two-persons-doing-fencing-5973873'}}), ((55, 59), {'': {6835570: 'performing-theatrical-woman-6835570'}}), ((60, 61), {'': {6010765: 'a-young-patient-confined-in-the-hospital-6010765', 6388396: 'a-woman-exercising-using-battle-ropes-6388396'}}), ((60, 61), {'': {6010765: 'a-young-patient-confined-in-the-hospital-6010765', 6388396: 'a-woman-exercising-using-battle-ropes-6388396'}}), ((62, 64), {'': {10140476: 'a-woman-wearing-ring-10140476'}}), ((65, 67), {'': {3860469: 'a-filipino-man-recording-a-video-at-a-beach-3860469', 5044272: 'man-portrait-player-male-5044272'}}), ((65, 67), {'': {3860469: 'a-filipino-man-recording-a-video-at-a-beach-3860469', 5044272: 'man-portrait-player-male-5044272'}}), ((68, 70), {'': {18069863: 'an-artist-s-depiction-of-artificial-intelligence-ai-this-video-explores-how-humans-can-creatively-collaborate-with-artificial-general-intelligence-agi-in-the-future-and-how-it-can-off-18069863', 5961111: 'a-woman-explaining-about-work-with-her-coworkers-5961111'}}), ((68, 70), {'': {18069863: 'an-artist-s-depiction-of-artificial-intelligence-ai-this-video-explores-how-humans-can-creatively-collaborate-with-artificial-general-intelligence-agi-in-the-future-and-how-it-can-off-18069863', 5961111: 'a-woman-explaining-about-work-with-her-coworkers-5961111'}}), ((71, 72), {'': {7579339: 'a-doctor-explaining-a-coronavirus-test-result-7579339'}}), ((73, 75), {'': {4770649: 'a-couple-s-feet-on-an-upward-escalator-4770649', 5799410: 'woman-paiting-a-wall-5799410'}}), ((73, 75), {'': {4770649: 'a-couple-s-feet-on-an-upward-escalator-4770649', 5799410: 'woman-paiting-a-wall-5799410'}}), ((80, 82), {'': {3944327: 'food-pizza-hands-friends-3944327', 3761657: 'man-in-blue-shirt-using-virtual-reality-3761657'}}), ((80, 82), {'': {3944327: 'food-pizza-hands-friends-3944327', 3761657: 'man-in-blue-shirt-using-virtual-reality-3761657'}}), ((83, 84), {'': {6943710: 'crystal-gems-on-esoteric-table-6943710', 6691596: 'chinese-new-year-decorations-hanging-on-display-6691596'}}), ((83, 84), {'': {6943710: 'crystal-gems-on-esoteric-table-6943710', 6691596: 'chinese-new-year-decorations-hanging-on-display-6691596'}}), ((85, 86), {'': {12908925: 'hands-of-a-woman-writing-on-a-sticky-note-12908925'}}), ((87, 90), {'': {3831766: 'a-worded-message-stenciled-on-a-board-3831766', 3709163: 'a-woman-copying-from-a-book-3709163'}}), ((87, 90), {'': {3831766: 'a-worded-message-stenciled-on-a-board-3831766', 3709163: 'a-woman-copying-from-a-book-3709163'}}), ((91, 91), {'': {7801554: 'woman-using-laptop-and-smartphone-while-working-7801554'}})]
""", "cl100k_base")

# print(num)
# save_settings()








