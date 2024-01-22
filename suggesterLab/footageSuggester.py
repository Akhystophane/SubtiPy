import re
from datetime import datetime
import openai
import ast
from mediaLab.main import download_video
from suggesterLab.functions import formatter_srt, get_char


def calculate_durations_from_srt(folder, dict2):
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
    for key, footage_desc in dict2.items():
        start_subtitle, end_subtitle = key
        start_time = srt_dict[int(start_subtitle)][0]
        end_time = srt_dict[int(end_subtitle)][1]
        duration = calculate_duration(start_time, end_time)
        footage_path, id_l = download_video(footage_desc, id_l, duration=float(duration))
        if footage_path:
            durations[key] = footage_path
    return durations


from collections import OrderedDict

def create_dict3(dict1, dict2, interval=2):
    dict3 = dict1.copy()  # Copie toutes les entrées de dict1 dans dict3

    keys_dict1 = list(dict1.keys())
    # Commence après les deux premières entrées et s'arrête avant les deux dernières
    for i in range(2, len(keys_dict1) - 2, interval):
        key = keys_dict1[i]
        # Trouve une entrée correspondante dans dict2
        dict2_entry = next((v for (k1, k2), v in dict2.items() if int(k1) <= int(key) <= int(k2)), None)
        if dict2_entry:
            dict3[key] = dict2_entry

    # Tri du dictionnaire en fonction des clés converties en nombres à virgule flottante
    dict3 = dict(OrderedDict(sorted(dict3.items(), key=lambda x: float(x[0]))))

    return dict3

def get_footage_dict(folder, niche):

    with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
        txt = formatter_srt(file.read())
    prompt = get_char(niche, "prompt_footage")
    prompt = prompt.replace("{text}", str(txt))

    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    print(response['choices'][0]['message']['content'])

    script_text = response['choices'][0]['message']['content']
    start = script_text.find("{")
    end = script_text.rfind("}") + 1
    dict2 = ast.literal_eval(script_text[start:end])
    dict2 = calculate_durations_from_srt(folder, dict2)
    return dict2


def get_midjourney_dict(folder):

    with open(folder + "audio.srt", 'r', encoding='utf-8') as file:
        txt = formatter_srt(file.read())

    prompt = f"""
    Je développe un contenu vidéo avec sous-titres numérotés et un dictionnaire Python. Script :{txt}.

Besoin de générer des prompts descriptifs en anglais qui me permettront de créer des images d’illustrations pour toute les phrases du script illustrant le passage lié au sous titre au format d'un dictionnaire de 14 clés maximum qui a comme clé le numéro du sous titre et comme valeurle prompt en anglais, le sous-titre 0 a necessairement un prompt, les numeros que tu choisiras par la suite seront ceux des debuts de phrases, ou du moins pas trop rapproché. S'il te plaît, cree le dictionnaire de 14 clés maximums avec une entrée pertinente par phrase. Les prompts doivent représenter des situations simples et précise sur le genre des individus, facile a représenter, n’utilise pas de mots borderline comme “érotique”. Note importante : ta réponse ne doit contenir que le dictionnaire amendé qui est envoyé directement à un programme informatique de montage, donc il est impératif que ta réponse soit qu'un dictionnaire.
    """
    # prompt = prompt.replace("{text}", str(txt))
    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    print(response['choices'][0]['message']['content'])

    script_text = response['choices'][0]['message']['content']
    start = script_text.find("{")
    end = script_text.rfind("}") + 1
    dict_img = ast.literal_eval(script_text[start:end])

    return dict_img




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
