import os
import random
import requests
from pexels_api import API

def write_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + '\n')

def read_already_download_files(filename):
    try:
        with open(filename, 'r') as f:
            downloaded_files = f.readlines()
        return [x.strip() for x in downloaded_files]
    except FileNotFoundError:
        return []

def download_video(type_of_videos):
    video_tag = random.choice(type_of_videos)
    api = API('0UtWYfv1TiXjERUIbSxB4KLQAYQr1AnlMg2Jjrj4oDDB7ytX90BdKJ3l') # Using environment variable or fallback to '-'

    retrieved_videos = read_already_download_files('downloaded_files.txt')
    video_found_flag = True
    num_page = 1

    while video_found_flag:

        api.search_videos(video_tag, page=num_page, results_per_page=10)
        videos = api.get_videos()

        if not videos:
            video_found_flag = False
            continue

        for data in videos:
            if data.width > data.height:  # look for horizontal orientation videos
                if data.url not in retrieved_videos:
                    write_file('downloaded_files.txt', data.url)
                    url_video = f'https://www.pexels.com/video/{data.id}/download'
                    r = requests.get(url_video)


download_video(['lion','lionne','wildcat'])