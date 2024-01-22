import json

import word_interest
from word_interest import word_color
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import *


def custom_stroke_generator(txt):

    # List of specific words to modify
    specific_words = ["duo", "signe"]

    # Formatting tags
    start_tag = "<span size='x-large' font_desc='Montserrat Heavy'>"
    end_tag = "</span>"

    # Check if the current word is in the list of specific words
    if any(word.lower() in specific_words for word in txt.split()):
        # Split the text into individual words
        words = txt.split()
        # Iterate over each word in the text
        for i, word2 in enumerate(words):
            # Check if the current word is in the list of specific words
            if word2.lower() in specific_words:
                # Apply custom formatting to the specific word
                words[i] = f'{start_tag}{word2}{end_tag}'
        # Join the modified words back into a single string
        txt = ' '.join(words)
        # Return the TextClip with the modified text
    return TextClip(txt, font='Montserrat Heavy', fontsize=53, color='black', method='pango')

def custom_generator(txt):
    highlight_l = word_interest.words_highlight(txt)
    l_l = highlight_l[0] + highlight_l[1] + highlight_l[2]
    # List of specific words to modify
    specific_words = ["duo", "signe", "crush,", "Verseau", "durer", "couple", "taureau", "balance", "cancer", "capricorne", "gemeaux", "bélier", "vierge", "sagittaire",
                      "scorpion", "poisson", "lion"]

        # Split the text into individual words
    words = txt.split()
    # Iterate over each word in the text

    for i in range(len(words)):
        word3 = words[i].lower().replace(".", "").replace(",", "")

        # Check if the current word is in the list of specific words
        if words[i].lower() in specific_words or word3 in l_l:
            w_color = word_color(highlight_l, word3)
            # Formatting tags
            start_tag = f"<span foreground='{w_color}' size='xx-large' font_desc='Montserrat Heavy'>"
            end_tag = "</span>"
            # Apply custom formatting to the specific word
            words[i] = f'{start_tag}{words[i]}{end_tag}'
    # Join the modified words back into a single string
    txt = ' '.join(words)
    # Return the TextClip with the modified text
    subtitle_clip = TextClip(txt, font='Montserrat Heavy', fontsize=38, color="white", method='pango')
    return subtitle_clip
    # Créez un ColorClip (fond noir) avec des dimensions légèrement plus grandes que celles du TextClip.
    padding_x = 20
    padding_y = 10
    bg_clip = ColorClip(size=(subtitle_clip.size[0] + padding_x, subtitle_clip.size[1] + padding_y), color=(0,0,0))

    # Superposez le TextClip sur le ColorClip
    composite_clip = CompositeVideoClip([bg_clip, subtitle_clip.set_position("center")])
    return composite_clip


def make_sub(folder):
    video_file = folder + 'Sequence.mp4'
    srt_file = folder + 'st.srt'
    output_file = folder + 'Montage.mp4'
    with open(folder + "script.txt", 'r') as fichier:
        text = fichier.read()
    # generator = lambda txt: TextClip(txt, font='Montserrat Heavy', fontsize=50, color='white', stroke_color="black", stroke_width=2)
    subtitles = SubtitlesClip(srt_file, custom_generator)
    # subtitles_stroke = SubtitlesClip("/Users/emmanuellandau/Documents/Séquence 04_1.srt", custom_stroke_generator)

    video = VideoFileClip(video_file)
    result = CompositeVideoClip([video, subtitles.set_pos("center","center")])
    result.write_videofile(output_file, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac", threads= 15)
