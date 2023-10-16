import json
import os
from datetime import datetime

import Levenshtein
import pysrt as pysrt

import word_interest
from suggesterLab.SuggesterAi import find_path, get_bibli


def time_to_seconds(time_str):
    try:
        # Remplacer le caractère "," par "."
        time_str = time_str.replace(',', '.')

        # Séparer les heures, minutes, secondes et millisecondes
        hh, mm, ss_milli = time_str.split(":")
        ss, milli = ss_milli.split(".")

        # Convertir en secondes
        total_seconds = int(hh) * 3600 + int(mm) * 60 + int(ss) + float("0." + milli)

        return str(total_seconds)
    except ValueError:
        print("Format de temps invalide")
        return None



def find_subtxt(subs, word, previnPoint):
    inPoint = None
    word = word.replace(".", "").replace(",", "").replace("!", "").lower()
    for sub in subs:
        inPoint_temp = float(time_to_seconds(str(sub.start)))
        sub_txt = sub.text.replace(".", "").replace(",", "").replace("!", "").lower()

        if Levenshtein.distance(sub.text.lower(), word.lower()) <= 4 or word.lower() in sub.text.lower():
            # print("word: ", word, sub_txt, Levenshtein.distance(sub_txt, word), previnPoint + 0.01 < inPoint_temp, previnPoint, str(sub.start))
            if previnPoint + 0.001 < inPoint_temp:
                # print("word: ", word, sub.text.lower())
                # print(previnPoint < inPoint_temp)
                inPoint = sub.start
                return inPoint
    print("----------------------------------------------------------------word not found", word)
    return inPoint

def dump_points(folder, niche):
    notfound = []
    subs = pysrt.open(folder + 'audio.srt', encoding='utf8')
    with open(folder + 'script.txt', 'r', encoding='utf8') as txt_file:
        txt_content = txt_file.read()

    txt_l = txt_content.split()
    video_manager = []
    prev_inPoint = -0.01
    for i in range(len(txt_l)):
        if "signes_" in txt_l[i]:
            txt_l[i] = txt_l[i].replace("signes_", "").capitalize()

        txt_l[i] = txt_l[i].replace("signes[", "").replace("]","")

            # print(txt_l[i])
        path = find_path(txt_l[i], niche)
        if i==0 :
            inPoint = 0.01

            video_manager.append([path, '00,00'])
        elif ".png" in txt_l[i]:


            if path == None:
                print(f"{txt_l[i]} has no path")
            if len(txt_l[i-1]) > 1:
                prev_word = txt_l[i-1]
            else:
                prev_word = txt_l[i - 2]
            # print(prev_word)
            # print(inPoint)
            inPoint = find_subtxt(subs, prev_word, prev_inPoint)
            video_manager.append([path, time_to_seconds(str(inPoint))])
            if inPoint:
                prev_inPoint = float(time_to_seconds(str(inPoint)))
            else:
                # print(inPoint)
                pass

    video_manager.append(['last.mp4', time_to_seconds(str(subs[-1].end))])
    has_none = any(None in sous_liste for sous_liste in video_manager)

    if has_none:
        print("-----------------------------------------None detected-------------------------------------------------")
        for couple, idx in video_manager:
            if not couple or not idx:
                print(idx, couple)
        print(video_manager)
        # print("------------------------------------------------------------------------------------------------------")
        return False
    print(video_manager)
    chemin_fichier = folder + "edit_data.json"
    # os.remove(chemin_fichier)
    # Lire le contenu existant
    # try:
    #     with open(chemin_fichier, 'r') as fichier:
    #         listes_existantes = json.load(fichier)
    #         if listes_existantes[0][0]:
    #             if "Users" in listes_existantes[0][0]:
    #                 listes_existantes[0] = video_manager
    #             else:
    #                 listes_existantes.insert(0, video_manager)
    #
    #     # Écrire les modifications
    #     with open(chemin_fichier, 'w') as fichier:
    #         json.dump(listes_existantes, fichier)
    # except FileNotFoundError:
    listes_existantes = []
    # Ajouter video_manager comme troisième liste
    listes_existantes.append(video_manager)
    # Réécrire le fichier avec les listes mises à jour
    with open(chemin_fichier, 'w') as fichier:
        json.dump(listes_existantes, fichier)
    return True

print(Levenshtein.distance("en commentaire.", "commentaire"))