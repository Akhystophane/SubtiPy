import csv
import os

# Set the path to the FFmpeg executable
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"  # Replace with the actual path to the FFmpeg executable

# Set the IMAGEIO_FFMPEG_EXE environment variable
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
imagemagick_path = "/opt/homebrew/bin/magick"  # Replace with the actual path to the ImageMagick executable

# Set the IMAGEMAGICK_BINARY environment variable
os.environ["IMAGEMAGICK_BINARY"] = imagemagick_path
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from datetime import datetime, timedelta
def convert(timestamp_string):
    timestamp_string = timestamp_string.rsplit(':', 1)[0] + '.' + timestamp_string.rsplit(':', 1)[1]
    return(timestamp_string)

def generate_subtitles(video_file, csv_file, output_file):

    exe = os.getenv("IMAGEIO_FFMPEG_EXE", None)

    # Load the video clip
    video_clip = VideoFileClip(video_file)

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        subtitles = list(reader)
        del subtitles[0]

    # Create a TextClip for each subtitle
    subtitle_clips = []
    for subtitle in subtitles:
        start_time = convert(subtitle[0]) # Start time in seconds
        end_time = convert(subtitle[1]) # End time in seconds
        text = subtitle[2]  # Subtitle text
        print(start_time, end_time)
        subtitle_clip = TextClip(text, fontsize=24, color='white', font='Arial', method='caption')
        subtitle_clip = subtitle_clip.set_start(start_time).set_end(end_time)
        subtitle_clips.append(subtitle_clip)

    # Concatenate the subtitle clips
    final_clip = concatenate_videoclips(subtitle_clips)

    # Overlay the subtitle clip on the video clip
    final_clip = CompositeVideoClip([video_clip, final_clip.set_position(("center", "bottom"))])

    # Write the final clip with subtitles to a file
    final_clip.write_videofile(output_file, codec='libx264')


# Example usage
video_file = '/Users/emmanuellandau/Documents/AV5.mp4'
csv_file = '/Users/emmanuellandau/Documents/Sequence 01.csv'
output_file = '/Users/emmanuellandau/Documents/AV5-V2.mp4'


# generate_subtitles(video_file, csv_file, output_file)

from moviepy.video.tools.subtitles import SubtitlesClip

generator = lambda txt: TextClip(txt, font='Arial', fontsize=16, color='white')
subtitles = SubtitlesClip("/Users/emmanuellandau/Documents/AV5.srt", generator)

video = VideoFileClip(video_file)
result = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])

result.write_videofile("output_file.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")