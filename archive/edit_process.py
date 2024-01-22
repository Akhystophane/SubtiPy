from moviepy.editor import *


def main():
    video_clips = []

    # Charger les vidéos
    for i in range(1, 6):
        video = VideoFileClip(f"{i}.mp4").subclip(0, 6)
        video_clips.append(video)

    transitions = []

    # Créer les transitions entre les clips
    for i in range(4):
        transition = video_clips[i].crossfade(video_clips[i + 1], 1)
        transitions.append(transition)

    # Concaténer les clips vidéo avec les transitions
    final_clip = concatenate_videoclips(transitions)

    # Réduire la durée de la vidéo finale à 30 secondes
    final_clip = final_clip.subclip(0, 30)

    # Enregistrer la vidéo finale
    final_clip.write_videofile("video_finale.mp4", fps=24)


if __name__ == "__main__":
    main()
