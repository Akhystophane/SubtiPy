import json
import os

from AudioLab import dump_srt
from functions import mp4_to_mp3
from suggesterLab.functions import get_srt_txt, formatter_srt

folder = "/Users/emmanuellandau/Documents/EditLab/TODO/test"
# mp4_to_mp3(folder)
# dump_srt(folder)
with open(os.path.join(folder, "audio.srt"), 'r', encoding='utf-8') as file:
    srt_txt = file.read()

srt_txt = formatter_srt(srt_txt)
print(srt_txt)
