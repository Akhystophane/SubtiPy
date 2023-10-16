import ast
import json
import random
import shutil
import unicodedata

import Levenshtein
import openai

from suggesterLab.Emojis import convert_emoji

openai.api_key = "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"

model_engine = "text-davinci-003"
prompt = """"

Je réalise des vidéos de manière automatisée à partir d'un script. j'ai besoin qu'à partir du texte de ma vidéo tu me
 suggères les endroits où je dois changer d'image de manière à réaliser le montage à posteriori. 
    Ta réponse est envoyé directement a un programme informatique de montage  donc il est impératif que ta réponse ne comporte uniquement
    le texte amendé (pas de texte parasite) avec les noms d'images ajoutés dans le texte avec un espace devant et derrière.
  Tu devras ajouter le chemin de l'image ou de la vidéo où elle devra commencer à s'afficher. Tu auras à ta disposition
   un set d'images qui contiennent dans leur nom des indications. en fonction de ces indications tu choisiras une photo
    pertinente . Une image doit toujours être affichée, le texte débute avec une image. 
    Je change d'image  toutes les phrases, ou également à certains temps fort comme à certaines virgules.
      Le thème de la vidéo et du dataset est le MBTI, tu ne dois pas utiliser deux fois
      la même image. Si pour certains noms d’image il y a un numéro c’est juste qu’il s’agit d’une image différente.


Voici le texte de la vidéo:
Es-tu un INFP ? Si c'est le cas, tu fais partie d'un groupe unique de rêveurs passionnés et créatifs ! Les INFP, souvent
 surnommés les "Médiateurs", possèdent une vision intérieure riche et sont guidés par un fort sens des valeurs. 
 Dotés d'une imagination débordante, ils voient la vie comme une grande tapestry, pleine de nuances et de possibilités.
  Leur nature introvertie les rend parfois réservés, mais ne t'y trompe pas ! En eux brûle une flamme d'idéalisme et de passion,
   cherchant constamment à exprimer leur essence et à contribuer au bien du monde. Empathiques et authentiques,
    ils ont cette rare capacité d'établir des connexions profondes avec les personnes qu'ils rencontrent.
     Attirés par l'art, la littérature et la philosophie, les INFP explorent sans cesse le vaste paysage de l'âme humaine.
      Alors, te reconnais-tu dans cette description dynamique et inspirante ? Si en découvrir plus sur ta personnalité
       t'intéresse, like et abonne-toi pour ne pas rater ma prochaine vidéo.

Voici le set d’images:
INFP_charismatic.png
INFP_writing.png
INFP_posing.png
INFP_reading.png
INFP_sad.png
INFP_angry.png
INFP_painting.png
INFP_posing2.png
INFP_thinking.png
INFP_writing2.png
INFP_happy.png
INFP_sad2.png
INFP_thinking2.png
INFP_thoughtful.png
INFP_evil.png
INFJ_reading.png
INFJ_teaching to a child.png
INFJ_charismatic.png
INFJ_intense eyes.png
INFJ_writing.png
INFJ_wise.png
INFJ_helping.png
INFJ_thinking.png
"""

import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# print(num_tokens_from_string(prompt, "cl100k_base"))

# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": "Tu es un programme informatique"},
#         {"role": "user", "content": prompt}
#     ]
# )
# print(response['choices'][0]['message']['content'])
def emoji_suggester(folder):
    def save_png_emoji(emojis_l):
        for num_srt in emojis_l.keys():
            convert_emoji(emojis_l[num_srt], folder)

    niche = "astrologie"
    i=0
    l_srt = []
    text_only = ""
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
    chemin_fichier = folder + "edit_data.json"
    # if os.path.exists(chemin_fichier):
    #     print("pas de emoji_suggester edit_data existe")
    #     return False
    prompt2 = f"Je réalise en Python des sous-titres pour une vidéo sur l'{niche}. Voici une list qui contient des dicts de" \
              f" phrases avec chaque srt :{l_srt}, tu dois" \
              f"me renvoyer un dictionnaire avec comme clés: num du srt et valeur: un émoji pertinent (au format lisible Python comme : a\U0001F47D) qui pourrait être affiché." \
              f"Par phrases quelques srt doivent avoir un émoji, environ 1/3 des srt (les autres srt ne sont pas dans le dict renvoyé) ta" \
              f" réponse ne doit contenir que le dictionnaire, pas d'autre texte parasite qui fera crasher mon programme"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un programme informatique"},
            {"role": "user", "content": prompt2}
        ]
    )
    print({response['choices'][0]['message']['content']})
    emojis_l = ast.literal_eval(response['choices'][0]['message']['content'])

    # Lire le contenu existant
    try:
        with open(chemin_fichier, 'r') as fichier:
            listes_existantes = json.load(fichier)
    except FileNotFoundError:
        listes_existantes = []
    # Ajouter video_manager comme troisième liste
    listes_existantes.append(emojis_l)
    # Réécrire le fichier avec les listes mises à jour
    with open(chemin_fichier, 'w') as fichier:
        json.dump(listes_existantes, fichier)

    save_png_emoji(emojis_l)
    return emojis_l






import os

import os


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
#-----------------------------------------------------------------------------------------------------------------------
import os


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

import string
import unicodedata
from Levenshtein import distance

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

    # Comparer les chaînes nettoyées ou vérifier la distance de Levenshtein
    if s1 == s2 or distance(s1, s2) <= levenshtein_tolerance:
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

    return list(relevant_signs), contenu

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
    return None

#-----------------------------------------------------------------------------------------------------------------------

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



def get_bibli(niche, num=False):
    dossier_principal = get_char(niche, "bibli")

    sous_dossiers = lister_dossier_dans_dossier(dossier_principal)

    folders = append_files(sous_dossiers, dossier_principal, num=num)
    folders = {normaliser_cle(cle): valeur for cle, valeur in folders.items()}
    # print("folders", niche, folders)
    return folders

def do_script_file(folder, fichiers_supprimes, dico, niche):
    def get_dico_astro():
        sign_names, txt = get_relevant_signs(folder, signes_astrologiques) # à modifier
        l_signes = relevant_l(sign_names, niche)
        dico["signes"] = l_signes
        dico_num = dico.copy()
        for key in dico_num.keys():
            if key != "signes":
                dico_num[key] = len(dico_num[key])
        return dico_num, txt
    def get_dico_mbti():
        print("ici")
        sign_names, txt = get_relevant_signs(folder, mbti_types)  # à modifier
        t = 0
        dico_num = {}
        for key, value in dico.items():
            if key in sign_names:
                t +=1
                dico_num[key] = value
        if t < 1:
            print("Pas de personnalité touvé")
            return False
        return dico_num, txt

    def make_bibli_relevant(fichiers_supprimes, dico):
        script_text_l = script_text.split()
        for idx, fichier in enumerate(script_text_l):
            nom_sous_dossier = re.sub(r'\d+\.png$', '', fichier)
            nom_sous_dossier = normaliser_cle(nom_sous_dossier)
            if ".png" in fichier:
                # print(dico)
                # Utilisation d'une regex pour retirer les chiffres et l'extension ".png" à la fin
                dico = {normaliser_cle(cle): valeur for cle, valeur in dico.items()}

                if nom_sous_dossier in dico and dico[nom_sous_dossier]:
                    num = random.randint(0, len(dico[nom_sous_dossier]) - 1)

                    # Modification de l'élément directement dans script_text
                    script_text_l[idx] = dico[nom_sous_dossier][num]


                    # Suppression du premier fichier du sous-dossier correspondant

                    fichier_supprime = dico[nom_sous_dossier].pop(num)


                    # Ajout du fichier supprimé à la liste des fichiers supprimés pour le sous-dossier
                    if nom_sous_dossier not in fichiers_supprimes:
                        fichiers_supprimes[nom_sous_dossier] = []

                    fichiers_supprimes[nom_sous_dossier].append(fichier_supprime)

                    # Si le nombre de fichiers est inférieur à 5, ajoutez tous les fichiers supprimés à la fin
                    if len(dico[nom_sous_dossier]) < 5 and nom_sous_dossier in fichiers_supprimes:
                        # print(
                        #     "------------------------------------------------on a est goatesque on est les roi du monde---------------------")
                        dico[nom_sous_dossier].extend(fichiers_supprimes[nom_sous_dossier])
                        fichiers_supprimes[
                            nom_sous_dossier] = []  # Vider la liste des fichiers supprimés pour le sous-dossier
        return dico, fichiers_supprimes, ' '.join(script_text_l)

    dico = {normaliser_cle(cle): valeur for cle, valeur in dico.items()}

    if niche == "astrologenial":
        dico_num, txt = get_dico_astro()
    elif niche == "mbti":
        dico_num, txt = get_dico_mbti()
    else:
        dico_num, txt = None, None
    print(dico_num)
    prompt = get_char(niche, "prompt")
    prompt = prompt.replace("{dico_num}", str(dico_num))
    prompt = prompt.replace("{txt}", str(txt))

    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un programme informatique"},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = response['choices'][0]['message']['content']
    # script_text = """personne_mystère_peur3.png Quel est le signe astrologique qui se donne trop de mal ? Prends une minute, et tente de deviner. Écris ton pronostic dans les commentaires avant de poursuivre. personne_mystère_peur89.png Es-tu prêt ? Celui dont nous parlons est connu pour son dévouement inébranlable, pour cette ardente passion qui l'anime à tout moment. Dans chaque projet, dans chaque relation, il met tout son cœur, souvent au détriment de lui-même. emma_lnd_divine_realistic_angel_sharp_color_95ad4ad3-f139-4a93-a35a-b25f2cb53869.png Ce signe a tendance à oublier ses propres besoins, se perdant dans le désir de satisfaire les autres. Son altruisme est remarquable, mais parfois, il peut aller trop loin, risquant ainsi l'épuisement ou la déception. Son énergie débordante le pousse souvent à en faire plus que nécessaire. Pour lui, l'abandon n'est pas une option. emma_lnd_Very_dangerous_and_thretening_person_with_no_face_vfx_a474331f-cc44-4bbb-a19c-8db138ac64a7.png Dans le zodiaque, il est représenté par un animal qui ne recule devant aucun obstacle, qui gravit montagne après montagne avec une détermination sans faille. Alors, as-tu deviné de quel signe il s'agit ? Capricorne_wise.png C'est bien sûr le Capricorne ! Si l'astrologie t'intéresse, like et abonne-toi pour ne pas rater ma prochaine vidéo.
    # """
    script_text = ' '.join(mot.strip() for mot in script_text.split())
    dico, fichiers_supprimes, script_text = make_bibli_relevant(fichiers_supprimes, dico)

    chemin = folder + "script.txt"
    print(script_text)

    # Utilisez le mode 'w' pour écrire
    with open(chemin, 'w') as fichier:
        fichier.write(script_text)

    return dico, fichiers_supprimes

def normaliser_cle(cle):
    return unicodedata.normalize('NFC', cle)

import os
import random

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

    # Si le sous-dossier n'existe pas, ne contient pas de fichiers ou si une autre erreur se produit, retournez None
    return None

# Test de la fonction
base_folder = 'chemin_du_dossier_principal'
var = 1
print(get_random_file_path(base_folder, var))


import re
def music_suggester(folder):
    titre = os.path.basename(os.path.normpath(folder))
    prompt = f""""
        Voici le titre de ma vidéo {titre}, mon algorithme utilise ta réponse pour attribuer lui associer une musique.
        Si le titre t'inspire  des émotions positives renvoie 1 s'il t'inspire de la négativté, ou de la peur renvoie 2.
        Ta réponse ne contient qu'un seul caractère, le chiffre 1 ou 2.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un programme informatique"},
            {"role": "user", "content": prompt}
        ]
    )
    num = response['choices'][0]['message']['content']
    try:
        int(num)
    except:
        print(f"num est{num} ce n'est pas valide !!!!")
        num = 3
    path_music = get_random_file_path("/Users/emmanuellandau/Documents/music", num)

    # Copie le fichier.
    shutil.copy(path_music, folder)
    return True









# folder = "/Users/emmanuellandau/Documents/EditLab/TODO/Le signe le plus généreux/"
# sign_names, txt = get_relevant_signs(folder, signes_astrologiques)
# dico = relevant_l(bibli, sign_names)

#
# fichiers_supprimes = {}
# fichiers_a_sup = ['personne_mystère_peur42.png', 'personne_angélique8.png', 'Cancer_beautiful.png']
import os
def get_char(niche, char):
    # Lire à partir d'un fichier JSON
    with open('suggesterLab/niche_settings.json', 'r') as f:
        data = json.load(f)
    # Récupérer et convertir la chaîne en multilignes
    texte = data[niche][char].replace("\\n", "\n")

    return texte

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

def check_json(folder):
    json_path = os.path.join(folder, "edit_data.json")
    # Charger le fichier JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Vérifier si le fichier contient trois éléments et pas quatre
    if len(data) == 3:
        print("Le fichier contient exactement trois éléments.")
    elif len(data) == 4:
        print("--------------------------------------------------Le fichier contient quatre éléments.")
    else:
        print(f"-------------------------------------------------Le fichier contient {len(data)} éléments.")

# Exemple d'utilisation
# dossier_principal = "/Users/emmanuellandau/Documents/MBTI_bibliothèque 2"
# renommer_fichiers(dossier_principal)



























def save_settings():
    text_astro = f""""
    
    Je réalise des vidéos de manière automatisée à partir d'un script. j'ai besoin qu'à partir du texte de ma vidéo tu me
     suggères les endroits où je dois changer d'image de manière à réaliser le montage à posteriori. 
        Ta réponse est envoyé directement a un programme informatique de montage  donc il est impératif que ta réponse ne comporte uniquement
        le texte amendé (pas de texte parasite) avec les noms d'images ajoutés dans le texte comme un mot sans quote.
      Tu devras ajouter le nom de l'image ou de la vidéo où elle devra commencer à s'afficher. Tu auras à ta disposition
       un set d'images qui contiennent dans leur nom des indications. en fonction de ces indications tu choisiras une photo
        pertinente . Une image doit toujours être affichée, ton texte COMMENCE donc avec une image! et se termine avec une phrase.
        Je change d'image toutes les phrases ou rarement après un temps fort comme une virgule. Je veux entre 7 et 9 images.
          Le thème de la vidéo et du dataset est l'astrologie, tu ne dois pas utiliser deux fois
          la même image. Si la valeur de la clé est un chiffre n, tu as n images différentes avec le même effet, tu peux 
          insérer ange4.png et ange8.png par exemple. 
    
    
    Voici le texte de la vidéo:{{txt}}
    
    Voici le set d’images: {{dico_num}}
    Il est impératif que le nom de l'image soit comme dans le set ou dans le format spécifié en amont car c'est envoyé a un algo.
    Si c'est une vidéo mystère privilégie les images qui ne réfèrent pas à un signe en particulier jusqu'au moment où son identité et dévoilé
    
    """

    prompt_mbti = f""""
    
    Je réalise des vidéos de manière automatisée à partir d'un script. j'ai besoin qu'à partir du texte de ma vidéo tu me
     suggères les endroits où je dois changer d'image de manière à réaliser le montage à posteriori. 
        Ta réponse est envoyé directement a un programme informatique de montage  donc il est impératif que ta réponse ne comporte uniquement
        le texte amendé (pas de texte parasite) avec les noms d'images ajoutés dans le texte comme un mot sans quote.
      Tu devras ajouter le nom de l'image ou de la vidéo où elle devra commencer à s'afficher. Tu auras à ta disposition
       un set d'images qui contiennent dans leur nom des indications. en fonction de ces indications tu choisiras une photo
        pertinente . Une image doit toujours être affichée, ton texte COMMENCE donc avec une image! et se termine avec une phrase.
        Je change d'image toutes les phrases ou rarement après un temps fort comme une virgule. Je veux entre 7 et 9 images.
          Le thème de la vidéo et du dataset est le MBTI, tu ne dois pas utiliser deux fois
          la même image.
    
    
    Voici le texte de la vidéo:{{txt}}
    
    Voici le set d’images: {{dico_num}}
    Il est impératif que le nom de l'image soit exactement comme dans le set ou dans le format spécifié en amont car c'est envoyé a un algo.
    Si c'est une vidéo mystère privilégie les images qui ne réfèrent pas à un signe en particulier jusqu'au moment où son identité et dévoilé
    
    """

    # Convertir la chaîne en une seule ligne pour le stockage JSON
    texte_single_line = text_astro.replace("\n", "\\n")

    # Créer un dictionnaire pour stocker vos données
    data = {
        "astrologenial":
                {'prompt': texte_single_line}
         ,
            "mbti":
                {'prompt': prompt_mbti.replace("\n", "\\n")}

    }


    # Écrire dans un fichier JSON
    with open('niche_settings.json', 'w') as f:
        json.dump(data, f, indent=4)













