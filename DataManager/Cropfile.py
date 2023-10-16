from moviepy.editor import *
import os

input_folder = "/Users/emmanuellandau/Documents/TODO/radin-test"  # Remplacez par le chemin de votre dossier d'entrée
output_folder = input_folder # Remplacez par le chemin de votre dossier de sortie

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Liste des fichiers image dans le dossier
image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov'))]

for media_file in image_files:
    input_path = os.path.join(input_folder, media_file)
    output_path = os.path.join(output_folder, media_file)

    # Charger l'image ou la vidéo
    if media_file.endswith(('.png', '.jpg', '.jpeg')):
        clip = ImageClip(input_path)
    else:
        clip = VideoFileClip(input_path)

    # Cadrer l'image ou la vidéo pour avoir un format 9:16
    new_width = (9 / 16) * clip.size[1]
    resized_clip = clip.resize(height=clip.size[1], width=new_width)

    # Sauvegarder l'image ou la vidéo redimensionnée
    if media_file.endswith(('.png', '.jpg', '.jpeg')):
        resized_clip.save_frame(output_path)
    else:
        codec = "libx264" if media_file.endswith('.mp4') else "libx264"  # vous pouvez changer le codec pour .mov si nécessaire
        resized_clip.write_videofile(output_path, codec=codec)

print("Traitement terminé!")

print("Traitement terminé!")
