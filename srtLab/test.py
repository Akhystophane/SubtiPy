import pysrt
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def text_to_srt_segments(text):
    # Séparation des mots et des signes de ponctuation
    words = [word for word in text.replace(".", " .").replace(",", " ,").replace("?", " ?").replace("!", " !").split()
             if word]

    segments = []
    current_segment = []

    for word in words:
        if word in [".", ",", "?", "!"] or len(current_segment) >= 2:
            if current_segment:
                segments.append(" ".join(current_segment))
                current_segment = []
            if word not in [".", ",", "?", "!"]:
                current_segment.append(word)
        else:
            current_segment.append(word)

    if current_segment:
        segments.append(" ".join(current_segment))

    return segments


def audio_to_timings(audio_file, silence_thresh=-39.1, silence_min_len=10):
    audio = AudioSegment.from_wav(audio_file)
    non_silence = detect_nonsilent(audio, min_silence_len=silence_min_len, silence_thresh=silence_thresh)
    return [(start / 1000.0, end / 1000.0) for start, end in non_silence]

def create_srt(text, audio_file, output_file):
    def seconds_to_subrip_time(seconds):
        """Convertit des secondes en objet SubRipTime."""
        return pysrt.srttime.SubRipTime(0, int(seconds / 60), int(seconds % 60), int((seconds % 1) * 1000))

    segments = text_to_srt_segments(text)
    timings = audio_to_timings(audio_file)

    subs = pysrt.SubRipFile()

    for idx, (segment, (start, end)) in enumerate(zip(segments, timings)):
        item = pysrt.SubRipItem(idx, start=seconds_to_subrip_time(start), end=seconds_to_subrip_time(end), text=segment)
        subs.append(item)

    subs.save(output_file, encoding='utf-8')
nom_fichier = "/Users/emmanuellandau/Documents/TODO/Les métiers selon ton signe astro/description.txt"  # Remplacez par le nom de votre fichier
with open(nom_fichier, "r") as fichier:
    text = fichier.read()
audio_path = "/Users/emmanuellandau/Documents/TODO/Les métiers selon ton signe astro/sample.wav"
output_path = "/Users/emmanuellandau/Documents/TODO/Les métiers selon ton signe astro/st.srt"

create_srt(text, audio_path, output_path)
