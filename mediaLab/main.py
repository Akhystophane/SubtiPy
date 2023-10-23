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


def download_video(type_of_videos, folder, id_l, vertical=True):
    bibli_path = "/Users/emmanuellandau/Documents/mediaLibrary"
    tags = type_of_videos

    api = Pexels(API_KEY)
    num_page = 1

    for tag in tags:

        output = api.search_videos(query=tag, page=num_page, per_page=10)
        videos = output["videos"]
        # output = api.popular_videos(query=tag)
        print(output)
        if len(output["videos"]) == 0:
            print("not found")
            continue

        filtered_videos = [video for video in videos if video["width"] < video["height"] and str(video["id"]) not in id_l]

        if len(filtered_videos) == 0:
            print("not found")
            continue

        idx = 0
        id = filtered_videos[idx]["id"]
        url = filtered_videos[idx]["url"]
        parts = url.split("/")
        name = parts[-2]
        url_video = 'https://www.pexels.com/video/' + str(id) + '/download'  # create the url with the video id
        path = '/Users/emmanuellandau/Documents/mediaLibrary/' + str(id) + '.mp4'
        if not check_file_exists(bibli_path, str(id)):
            r = requests.get(url_video)
            with open(path, 'wb') as outfile:
                outfile.write(r.content)

        set_finder_comment(path, name)
        id_l.append(id)
        return path, id_l
    # si aucune vidéo chercher des phots
    for tag in tags:

        output = api.search_photos(query=tag, page=num_page, per_page=10)
        print(output)
        videos = output["photos"]
        # output = api.popular_videos(query=tag)
        print(output)
        if len(output["photos"]) == 0:
            print("not found")
            continue

        filtered_videos = [video for video in videos if video["width"] < video["height"] and str(video["id"]) not in id_l]

        if len(filtered_videos) == 0:
            print("not found")
            continue

        idx = 0
        id = filtered_videos[idx]["id"]
        url = filtered_videos[idx]["url"]
        parts = url.split("/")
        name = parts[-2]
        url_video = filtered_videos[idx]['src']['original']  # create the url with the video id
        path = '/Users/emmanuellandau/Documents/mediaLibrary/' + str(id) + ".png"
        if not check_file_exists("/Users/emmanuellandau/Documents/mediaLibrary", str(id)):
            r = requests.get(url_video)
            with open(path, 'wb') as outfile:
                outfile.write(r.content)
            set_finder_comment(path, name)



        print(get_finder_comment(path))
        id_l.append(id)
        return path, id_l  # download the picture

    return None


def download_media(api, tag, media_type,folder, vertical=True):

    bibli_path = os.path.join(folder, "library")
    MEDIA_LIBRARY_PATH = bibli_path
    search_function = api.search_videos if media_type == 'videos' else api.search_photos
    output = search_function(query=tag, page=1, per_page=10)
    print(output)

    if not output[media_type]:
        print("not found")
        return None

    media_list = output[media_type]
    filtered_media = [media for media in media_list if
                      (media["width"] < media["height"]) == vertical and not check_file_exists(MEDIA_LIBRARY_PATH,
                                                                                               str(media["id"]))]

    if not filtered_media:
        print("not found")
        return None

    media = filtered_media[0]  # Select the first media
    id = media["id"]
    url = media["url"] if media_type == 'videos' else media['src']['original']

    response = requests.get(url)
    if response.status_code == 200:
        extension = '.mp4' if media_type == 'videos' else '.png'
        path = f'{MEDIA_LIBRARY_PATH}{id}{extension}'
        with open(path, 'wb') as outfile:
            outfile.write(response.content)

        set_finder_comment(path, tag)
        print(get_finder_comment(path))
        return path
    else:
        print("Failed to download media.")
        return None


def download_videoV2(type_of_videos, vertical=True):
    api = Pexels(API_KEY)

    for media_type in ['videos', 'photos']:
        for tag in type_of_videos:
            path = download_media(api, tag, media_type, vertical)
            if path:
                return path  # Return the path of the first successfully downloaded media

    return None



# Exemple d'utilisation

# download_video(["personality test chart", "ISTP keyword", "psychology diagram"])