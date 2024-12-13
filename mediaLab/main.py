
import json
import os
import random
import requests
from pexels_api import API
from pexelsapi.pexels import Pexels
import subprocess

API_KEY = '0UtWYfv1TiXjERUIbSxB4KLQAYQr1AnlMg2Jjrj4oDDB7ytX90BdKJ3l'

def check_file_exists(folder_path, file_name):
    # Liste tous les fichiers dans le dossier
    files_in_folder = os.listdir(folder_path)

    # Ajoute l'extension .mp4 au nom de fichier si ce n'est pas déjà fait
    if not file_name.endswith('.mp4'):
        file_name += '.mp4'

    # Vérifie si le fichier existe dans le dossier
    if file_name in files_in_folder:
        print(f"Le fichier {file_name} existe dans le dossier {folder_path}.")
        return True
    else:
        return False

def set_finder_comment(file_path, comment):
    subprocess.run(["xattr", "-w", "com.apple.metadata:kMDItemFinderComment", comment, file_path])

def get_finder_comment(file_path):
    result = subprocess.run(["xattr", "-p", "com.apple.metadata:kMDItemFinderComment", file_path], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None


def write_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + '\n')


def download_video(type_of_videos, id_l, vertical=True, duration=0.0, pic=False):
    bibli_path = "/Users/emmanuellandau/Documents/mediaLibrary"
    tags = type_of_videos
    api = Pexels(API_KEY)
    num_page = 1

    for tag in tags:

        output = api.search_videos(query=tag, page=num_page, per_page=10)
        try:
            videos = output["videos"]
        except KeyError:
            continue

        if len(output["videos"]) == 0:
            print("not found")
            continue

        test_duration = [video for video in videos if video[
                               "duration"] >= duration]
        test_width = [video for video in videos if
                           video["width"] < video["height"]]
        test_idl = [video for video in videos if
                            str(video["id"]) not in id_l ]

        filtered_videos = [video for video in videos if str(video["id"]) not in id_l and video["id"] not in id_l and video["width"] < video["height"] and video["duration"] >= duration]

        if len(filtered_videos) == 0:
            print("not found there")
            continue

        idx = 0
        id = filtered_videos[idx]["id"]
        url = filtered_videos[idx]["url"]
        parts = url.split("/")
        name = parts[-2]
        url_video = f"https://www.pexels.com/download/video/{str(id)}/"  # create the url with the video id
        path = '/Users/emmanuellandau/Documents/mediaLibrary/' + str(id) + '.mp4'

        if not check_file_exists(bibli_path, str(id)) and id not in id_l:
            r = requests.get(url_video)
            with open(path, 'wb') as outfile:
                outfile.write(r.content)

        set_finder_comment(path, name)
        id_l.append(id)
        print("id_l", id_l)
        return path, id_l
    # if pic :
    #     # si aucune vidéo chercher des phots
    #     for tag in tags:
    #
    #         output = api.search_photos(query=tag, page=num_page, per_page=10)
    #         print(output)
    #         videos = output["photos"]
    #         # output = api.popular_videos(query=tag)
    #         print(output)
    #         if len(output["photos"]) == 0:
    #             print("not found")
    #             continue
    #
    #         filtered_videos = [video for video in videos if video["width"] < video["height"] and str(video["id"]) not in id_l]
    #
    #         if len(filtered_videos) == 0:
    #             print("not found")
    #             continue
    #
    #         idx = 0
    #         id = filtered_videos[idx]["id"]
    #         url = filtered_videos[idx]["url"]
    #         parts = url.split("/")
    #         name = parts[-2]
    #         url_video = filtered_videos[idx]['src']['original']  # create the url with the video id
    #         path = '/Users/emmanuellandau/Documents/mediaLibrary/' + str(id) + ".png"
    #         if not check_file_exists("/Users/emmanuellandau/Documents/mediaLibrary", str(id)):
    #             r = requests.get(url_video)
    #             with open(path, 'wb') as outfile:
    #                 outfile.write(r.content)
    #             set_finder_comment(path, name)
    #
    #         print(get_finder_comment(path))
            # id_l.append(id)
            # return path, id_l  # download the picture
    return None, id_l


import requests


def search_videos(api_key, tag):
    # URL de base pour la recherche de vidéos sur Pexels
    url = f"https://api.pexels.com/videos/search?query={tag}"

    # En-têtes de la requête avec la clé API pour l'autorisation et un User-Agent similaire à curl
    headers = {
        'Authorization': api_key,
        'User-Agent': 'curl/7.64.1',  # Utiliser un User-Agent similaire à curl
    }

    try:
        # Envoyer une requête GET à l'API Pexels
        response = requests.get(url, headers=headers)

        # Vérifier le code de statut HTTP
        if response.status_code == 200:
            # Convertir la réponse en JSON et la retourner
            return response.json()
        else:
            # Afficher un message d'erreur si le code de statut n'est pas 200
            print(f"Erreur HTTP {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # Gérer les exceptions de requête
        print(f"Erreur de requête: {e}")
        return None





def feed_back(type_of_videos, id_l, timestamps, feedback_l, duration=0.0):
    tags = type_of_videos
    api = Pexels(API_KEY)
    num_page = 1
    ids = []

    for tag in tags:
        print('tag', tag)

        # output = api.search_videos(query=tag)
        output = search_videos('0UtWYfv1TiXjERUIbSxB4KLQAYQr1AnlMg2Jjrj4oDDB7ytX90BdKJ3l', tag)
        print(output)

        try:
            videos = output["videos"]
        except KeyError:
            continue

        if len(output["videos"]) == 0:
            print("not found")
            continue

        filtered_videos = [video for video in videos if str(video["id"]) not in id_l and video["id"] not in id_l and video["width"] < video["height"] and video["duration"] >= duration]

        if len(filtered_videos) == 0:
            print("not found there")
            continue

        idx = 0
        id = filtered_videos[idx]["id"]
        url = filtered_videos[idx]["url"]
        parts = url.split("/")
        name = parts[-2]
        url_video = f"https://www.pexels.com/download/video/{str(id)}/"  # create the url with the video id
        path = '/Users/emmanuellandau/Documents/mediaLibrary/' + str(id) + '.mp4'
        id_l.append(id)
        ids.append({id:name})
        print("id_l : ", id_l)

    feedback_l[timestamps] = ids

    return feedback_l, id_l

def feedb_download(feedb_dict):
    bibli_path = "/Users/emmanuellandau/Documents/mediaLibrary"
    for timestamps, id in feedb_dict.items():
        url_video = f"https://www.pexels.com/download/video/{str(id)}/"  # create the url with the video id
        path = '/Users/emmanuellandau/Documents/mediaLibrary/' + str(id) + '.mp4'
        if not check_file_exists(bibli_path, str(id)):
            r = requests.get(url_video)
            with open(path, 'wb') as outfile:
                outfile.write(r.content)
        feedb_dict[timestamps] = path

    return feedb_dict


# Remplacez 'YOUR_API_KEY' par votre clé d'API réelle
def get_collections():
    url = 'https://api.pexels.com/v1/collections/'

    # Les paramètres pour la requête
    params = {
        'sort': 'desc'
    }

    # Ajout de l'en-tête d'autorisation
    headers = {
        'Authorization': API_KEY
    }

    # Effectuer la requête GET
    response = requests.get(url, headers=headers, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Imprimer le contenu de la réponse (ou vous pouvez le traiter comme vous voulez)
        output = response.json()
        collections = output["collections"]
        collections_repo = {}

        collection_idx = 0
        for collection in collections:
            collection_title = output["collections"][collection_idx]['title']
            collection_url = f"{url}/{collection['id']}/"
            collection_data = requests.get(collection_url, headers=headers)
            collection_data = collection_data.json()
            filtered_videos = collection_data["media"]
            collections_repo[collection_title] = filtered_videos
            collection_idx += 1

        with open(os.path.join("repo.json"), 'w') as file:
            json.dump(collections_repo, file, indent=1)

    else:
        print(f"Erreur lors de la requête: {response.status_code}")

def download_collections():
    with open('repo.json', 'r') as file:
        collections = json.load(file)
    headers = {'Authorization': API_KEY}
    bibli_path = "/Users/emmanuellandau/PycharmProjects/SubtiPy/mediaLab/bibli"
    for collections_title, collection in collections.items():
        filtered_videos = collection
        for i in range(len(collection)):
            id = filtered_videos[i]["id"]
            print(id)
            download_url = f"https://www.pexels.com/download/video/{str(id)}/"
            local_path = '/Users/emmanuellandau/PycharmProjects/SubtiPy/mediaLab/bibli/' + str(id) + '.mp4'
            if not check_file_exists(bibli_path, str(id)):
                r = requests.get(download_url, headers=headers)
                if r.status_code == 200:
                    with open(local_path, 'wb') as outfile:
                        outfile.write(r.content)
                else:
                    print('erreur',r)
            else:
                print("fichier déjà enregistré")

            filtered_videos[i]["local_path"] = local_path

    with open('repo.json', 'w') as file:
        json.dump(collections, file, indent=1)


def collection_suggester(feedb_dict):
    with open('/Users/emmanuellandau/PycharmProjects/SubtiPy/mediaLab/repo.json', 'r') as file:
        collections = json.load(file)
    for timestamps, emotion in feedb_dict.items():
        footage_path = None


        for collections_title, collection in collections.items():
            # print(collections_title, emotion_safe)
            if collections_title == emotion:
               footage_data =  random.choice(collection)
               footage_path = footage_data["local_path"]
               break
            else:
                continue

        feedb_dict[timestamps] = footage_path

    return feedb_dict

# api = Pexels(API_KEY)

# feed_back(['thoughtful', 'idea'],[], (0,13), {})
# output = api.search_videos(query='intelligent')
# print(output)


# Exemple d'utilisation de la fonction
# api_key = "0UtWYfv1TiXjERUIbSxB4KLQAYQr1AnlMg2Jjrj4oDDB7ytX90BdKJ3l"  # Remplace par ta clé API
# tag = "thoughtful"
# videos = search_videos(api_key, tag)
#
# if videos:
#     print("Résultats de la recherche :", videos)

# id = 28571261
# headers = {
#         'Authorization': API_KEY
#     }
# url = f"https://www.pexels.com/download/video/{str(id)}/"

# # Envoyer une requête GET à l'API Pexels
# response = requests.get(url, headers=headers)
#
# # Vérifier le code de statut HTTP
# if response.status_code == 200:
#     # Convertir la réponse en JSON et la retourner
#     print(response.content)
# else:
#     # Afficher un message d'erreur si le code de statut n'est pas 200
#     print(f"Erreur HTTP {response.status_code}: {response.text}")
#     print(None)


import os
import requests



# Fonction pour télécharger les vidéos à partir de feedb_dict
def feedb_download_(feedb_dict):
    bibli_path = "/Users/emmanuellandau/Documents/mediaLibrary"
    for id in feedb_dict:
        url_video = f"https://www.pexels.com/download/video/{str(id)}/"  # créer l'URL avec l'ID vidéo
        path = os.path.join(bibli_path, str(id) + '.mp4')
        r = requests.get(url_video)
        # Écraser toujours le fichier existant
        with open(path, 'wb') as outfile:
            outfile.write(r.content)
        print(f"Vidéo {id} téléchargée à {path}")

# Fonction pour récupérer les noms de dossiers dans un répertoire
def get_files_added_yesterday(directory):
    # Obtenir la date et l'heure d'hier

    from datetime import timedelta
    from datetime import datetime
    yesterday = datetime.now() - timedelta(days=1)
    # Convertir la date d'hier à minuit pour comparaison
    yesterday_start = datetime(yesterday.year, yesterday.month, yesterday.day)

    # Liste pour stocker les fichiers ajoutés hier
    files_added_yesterday = []

    # Parcourir les fichiers dans le répertoire
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Vérifier si c'est un fichier (pas un dossier)
        if os.path.isfile(file_path):
            # Obtenir la date de modification du fichier
            file_mod_time = os.path.getmtime(file_path)
            file_mod_datetime = datetime.fromtimestamp(file_mod_time)

            # Vérifier si le fichier a été modifié hier
            if file_mod_datetime >= yesterday_start and file_mod_datetime < yesterday_start + timedelta(days=1):
                files_added_yesterday.append(file_name)

    return files_added_yesterday

# # Chemin du répertoire où récupérer les dossiers
# media_library_path = "/Users/emmanuellandau/Documents/mediaLibrary"
#
# # Récupérer les noms des dossiers
# folder_names = get_files_added_yesterday(media_library_path)
# l = []
# for folder_name in folder_names:
#     folder_name.replace('.mp4', '')
#     l.append(folder_name.replace('.mp4', ''))
#
#
# # print(l)
# #
# # # Appel de la fonction de téléchargement
# feedb_download_(l)
