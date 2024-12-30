import os
import re
from datetime import datetime
import openai
import ast

from openai import OpenAI

from Google.Folder_management import upload_folder
from mediaLab.main import download_video, feed_back, feedb_download, collection_suggester
from suggesterLab.functions import formatter_srt, get_char, mp3_to_wav_slice, formatter_srtV2


def insert_a_roll(folder, footages):
    folder_edit = folder
    # Enlever le séparateur final si présent
    if folder.endswith("/") or folder.endswith("\\"):
        folder_edit = folder.rstrip("/\\")
    # Maintenant, obtenir le nom du dossier
    name = os.path.basename(folder_edit)
    flag= ""
    time_count = 0
    a_roll_path = os.path.join(folder, "a-roll")
    footage_path = os.path.join("/Users/emmanuellandau/Documents/EditLab/READY",name,"a-roll", f"1.mp4")
    result = [[footage_path, "0.0"]]  # Commencer avec un A-roll au timestamp 0.0
    y = 0  # Compteur pour sauter les éléments après chaque A-roll inséré
    z = 2

    for i in range(len(footages)):
        # Après le premier A-roll, ajouter directement les B-roll à la liste résultat
        # sauf si la règle spécifique pour un nouvel A-roll est rencontrée
        if i + 1 < len(footages):
            current_timestamp = float(footages[i][1])
            next_timestamp = float(footages[i + 1][1])
            if current_timestamp <= 2.5:
                continue

            # Si la différence de timestamp avec le prochain élément est <= 8 secondes,
            # insérer un A-roll et sauter les 3 prochains éléments B-roll
            elif 2 <= (next_timestamp - current_timestamp) <= 8 and time_count <= 15 and y >= 3:
                output_path = os.path.join(a_roll_path, f"{str(i)}.wav")
                footage_path = os.path.join("/Users/emmanuellandau/Documents/EditLab/READY",name, "a-roll",f"{str(z)}.mp4")
                input_path = os.path.join(folder, f"audio.mp3")
                result.append([footage_path, footages[i][1]])
                mp3_to_wav_slice(input_path,current_timestamp, next_timestamp, output_path )
                time_count += next_timestamp - current_timestamp
                flag = current_timestamp
                y=0
                z += 1
            elif current_timestamp != flag:
                # print(footages[i], current_timestamp)
                # Ajouter le B-roll actuel car il n'est pas remplacé par un A-roll
                result.append(footages[i])
                y += 1
        else:
            # Ajouter le dernier B-roll si on est à la fin de la liste
            result.append(footages[i])
    print(time_count)


    current_timestamp = float(result[0][1])
    next_timestamp = float(result[1][1])
    output_path = os.path.join(a_roll_path, f"{str(0)}.wav")
    input_path = os.path.join(folder, f"audio.mp3")
    mp3_to_wav_slice(input_path, current_timestamp, next_timestamp, output_path)
    upload_folder(a_roll_path, f"TODO/{name}")
    return result
def do_feedback(feedback_l, txt):
    prompt = f"""Je te fourni le script de ma vidéo avec le num de sous-titre qui correspond a chaque portion du texte
    A partir d'un dict où tu as la description de footages et de quel sous-titre a quel sous titre il seront affiché
    tu me choisi footage le plus en lien avec la phrase après le num srt. Ta réponse est un dictionnaire qui a numéro de srt en clé et en valeur l'id du footage
    que tu as choisi. Note importante : ta réponse ne doit contenir que le dictionnaire amendé qui est envoyé directement à un programme informatique de montage, donc il est impératif que ta réponse soit qu'un dictionnaire.

script_video :{txt}
dict {feedback_l}"""

    print(prompt)
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "Tu es un assistant"},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # print(response['choices'][0]['message']['content'])
    # output = response['choices'][0]['message']['content']
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    output = str(completion.choices[0].message.content)
    print('dict_feedback', output)

    start = output.find("{")
    end = output.rfind("}") + 1
    output = ast.literal_eval(output[start:end])
    return(output)

def calculate_durations_from_srt(folder, dict2, feedback=True):
    """Calcule les durées entre les sous-titres spécifiés dans dict2 à partir du contenu SRT."""

    def parse_srt_time(time_str):
        """Parse un temps de sous-titre SRT en objet datetime."""
        return datetime.strptime(time_str, '%H:%M:%S,%f')

    def calculate_duration(start_time, end_time):
        """Calcule la durée en secondes entre deux temps."""
        return (parse_srt_time(end_time) - parse_srt_time(start_time)).total_seconds()
    # Parsing du fichier SRT
    srt_dict = {}
    with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
        srt_content = file.read().strip().split('\n\n')

    for block in srt_content:
        num, time_range, _ = block.split('\n', 2)
        start, end = time_range.split(' --> ')
        srt_dict[int(num)] = (start, end)

    # Calcul des durées pour dict2
    durations = {}
    id_l = []
    feedback_l = {}
    for key, footage_desc in dict2.items():
        # try:
        #     # start_subtitle, end_subtitle = key
        #     # start_time = srt_dict[int(start_subtitle)][0]
        #     # end_time = srt_dict[int(end_subtitle)][1]
        #     # duration = calculate_duration(start_time, end_time)
        # except KeyError:
        #     continue
        if not feedback:
            footage_path, id_l = download_video(footage_desc, id_l, duration=0.0)
            if footage_path:
                durations[key] = footage_path
        else:
            feedback_l, id_l = feed_back(footage_desc,id_l, key, feedback_l)

    if feedback:
        with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
            txt = formatter_srtV2(file.read())

        feedback_l = do_feedback(feedback_l, txt)
        durations = feedb_download(feedback_l)

    return durations


from collections import OrderedDict

def create_dict3(dict1, dict2, interval=2):
    dict3 = dict1.copy()  # Copie toutes les entrées de dict1 dans dict3

    keys_dict1 = list(dict1.keys())
    # Commence après les deux premières entrées et s'arrête avant les deux dernières
    for i in range(2, len(keys_dict1) - 2, interval):
        key = keys_dict1[i]
        # Trouve une entrée correspondante dans dict2
        # Puisqu'on sait que les clés de dict2 sont des entiers, on utilise directement key pour l'accès
        if int(key) in dict2:
            dict2_entry = dict2[int(key)]
            if dict2_entry:
                dict3[key] = dict2_entry

    # Tri du dictionnaire en fonction des clés converties en nombres à virgule flottante
    dict3 = dict(OrderedDict(sorted(dict3.items(), key=lambda x: float(x[0]))))

    return dict3

def get_footage_dict(folder, niche):

    with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
        txt = formatter_srtV2(file.read())
    prompt = get_char(niche, "prompt_footage")
    prompt = prompt.replace("{text}", str(txt))
    print(prompt)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = completion.choices[0].message.content

    start = script_text.find("{")
    end = script_text.rfind("}") + 1

    dict2 = ast.literal_eval(script_text[start:end])
    print('------dict2------', dict2)
    dict2 = calculate_durations_from_srt(folder, dict2)

    return dict2


def get_footageV2_dict(folder, niche):

    with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
        txt = formatter_srtV2(file.read())
    prompt = get_char(niche, "prompt_footageV2")
    prompt = prompt.replace("{text}", str(txt))
    print(prompt)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = completion.choices[0].message.content

    start = script_text.find("{")
    end = script_text.rfind("}") + 1
    dict2 = ast.literal_eval(script_text[start:end])
    print(dict2)
    dict2 = collection_suggester(dict2)
    # dict2 = calculate_durations_from_srt(folder, dict2, feedback=False)
    print(dict2)
    return dict2

# get_footageV2_dict("/Users/emmanuellandau/Documents/EditLab/TODO/3/", "reddit_stories")

def get_midjourney_dict(folder, prompt=f"""
    Crée un dictionnaire en anglais de 14 clés maximums distribué uniformément où chaque clé correspond au numéro de
     sous-titre du début d'une phrase entière dans le script : {{
  "num_srt de la phrase 1": independant description of an image, 
  "num_srt de la phrase 2": ...
}}. La clé 0 doit être incluse pour la première phrase. Pour chaque phrase fournie, créez un prompt destiné à générer
 une image en lien avec cette phrase de manière autonome (rien d'abstrait, situations concrete avec description
  uniquement physique des perso, objets... Chaque prompt doit être conçu de façon à ce que l'image puisse être générée.
   Il est crucial de décrire en détail l'environnement et l'atmosphère de l'image pour l'IA générative d'images.
    Les descriptions doivent être factuelles et centrées sur le contenu immédiat de la phrase
     (tu n'inclues pas la phrase du txt dans le prompt), sans faire allusion à un contexte plus large.
      Les prompts doivent respecter la classification PG-13, etre clairs et sans mots ou expressions sensuels.
       Chaque prompt est direct, indépendant et doit se suffir pour réaliser l'illustration.
        Assure-toi que les guillemets dans les valeurs soient échappés. Le résultat final doit être un dictionnaire
         formaté pour une utilisation informatique, avec une seule entrée par phrase complète.
          Ta réponse doit être uniquement le dictionnaire formaté correctement pour un usage direct dans un programme informatique.
           Voici le texte : .

    """):
    if os.path.exists(folder + "audio.srt"):
        with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
            txt = formatter_srtV2(file.read(), saut=0)
        prompt = prompt+txt



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
    print(script_text)
    start = script_text.find("{")
    end = script_text.rfind("}") + 1
    dict_img = ast.literal_eval(script_text[start:end])

    return dict_img

def get_descri(prompt):

    print(prompt)
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un astrologue storyteller."},
            {"role": "user", "content": prompt}
        ]
    )

    script_text = str(completion.choices[0].message.content)
    script_text = script_text.replace("*", "")
    print(script_text)

    return script_text

# get_footage_dict("/Users/emmanuellandau/Documents/EditLab/TODO/6 qualités des Cancers que personne ne remarque/", "reddit_stories")

# with open("/Users/emmanuellandau/Documents/EditLab/TODO/6 qualités des Cancers que personne ne remarque/" + "audio.srt", 'r', encoding='utf-8') as file:
#     txt = formatter_srt(file.read())
# print(txt)

# dict2 = {
#     (0, 7): ["thoughtful"],
#     (8, 14): ["happy"],
#     (15, 25): ["intuitive", "thoughtful"],
#     (26, 40): ["sensitive", "protective"],
#     (41, 51): ["caring", "loving"],
#     (52, 61): ["smart", "reflective"],
#     (62, 80): ["strong", "determined"],
#     (81, 92): ["informative", "inviting"]
# }

# durations = calculate_durations_from_srt(folder, dict2)
# print(durations)
