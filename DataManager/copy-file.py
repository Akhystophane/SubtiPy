import os
import shutil
import os
import shutil

from suggesterLab.footageSuggester import get_descri


def copy_files(src_dir):
    # Parcourir tous les sous-dossiers dans le dossier source
    for root, dirs, files in os.walk(src_dir):
        for dir in dirs:
            # Construire le chemin du fichier source
            src_file = os.path.join(root, dir, "description.txt")

            # S'assurer que le fichier script.txt existe
            if os.path.isfile(src_file):
                # Construire le chemin du fichier de destination
                dst_file = os.path.join(root, dir, "script.txt")

                # Copier le fichier
                shutil.copy2(src_file, dst_file)

def determine_file_type(filepath):
    with open(filepath, 'rb') as f:
        first_bytes = f.read(8)  # Lire les 8 premiers octets
        if first_bytes.startswith(b'\x89PNG\r\n\x1A\n'):
            return 'png'
        elif first_bytes.startswith(b'\xFF\xD8'):
            return 'jpg'
    return None

def correct_file_extension(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            filetype = determine_file_type(filepath)

            if filetype:
                correct_extension = '.' + filetype
                if not filename.endswith(correct_extension):
                    base, _ = os.path.splitext(filename)
                    new_name = base + correct_extension
                    new_path = os.path.join(root, new_name)
                    os.rename(filepath, new_path)
                    print(f"Renamed {filename} to {new_name}")

def check_extension():
    # Mettez le chemin de votre dossier ici
    source_folder = "/Users/emmanuellandau/Documents/crépus/TODO"
    for nom in os.listdir(source_folder):
        chemin = os.path.join(source_folder, nom)
        if os.path.isdir(chemin):
            print(chemin)
            correct_file_extension(chemin)

    # Appeler la fonction avec le chemin du dossier source
    copy_files("/Users/emmanuellandau/Documents/crépus/TODO")

def move_video(source_directory, destination_directory ):
    # Chemin du dossier source contenant les sous-dossiers
    # source_directory = "/Users/emmanuellandau/Documents/DONE"
    # Chemin du dossier de destination où vous souhaitez copier les fichiers Montage.mp4
    # destination_directory = "/Users/emmanuellandau/Documents/data_insta/astrologie_2"
    i = 0
    # Parcourir chaque sous-dossier du dossier source
    for subdir, _, files in os.walk(source_directory):
        # Vérifier si Montage.mp4 est dans la liste des fichiers du sous-dossier courant
        if "Montage.mp4" in files:
            i += 1
            print(subdir)
            source_file = os.path.join(subdir, "Montage.mp4")

            # Récupérer le nom du sous-dossier pour renommer le fichier
            new_name = os.path.basename(subdir) + ".mp4"
            destination_file = os.path.join(destination_directory,str(i), new_name)
            # Copier le fichier vers le dossier de destination
            shutil.copy2(source_file, destination_file)
            source_file = os.path.join(subdir, "description.txt")

            # Récupérer le nom du sous-dossier pour renommer le fichier
            new_name = "description.txt"
            destination_file = os.path.join(destination_directory,str(i), new_name)
            # Copier le fichier vers le dossier de destination
            shutil.copy2(source_file, destination_file)
    print("Les fichiers ont été copiés avec succès !")
def create_folders_concept(dossier_parent, phrases):

    # Vérifier si le dossier parent existe, sinon le créer
    if not os.path.exists(dossier_parent):
        os.mkdir(dossier_parent)

    # Créer un dossier et ajouter un fichier "description" pour chaque phrase
    for phrase in phrases:
        txt = ""
        prompt = f"""realise moi un script dynamique, fluide et mystérieux ( un bloc, un seul paragraphe, plain text) de
         280 mots avec suspens sur titre : Voici les {phrase}!  La première phrase est le titre pour impacter, Puis juste après tu dis Mais avant de tout te dévoiler ...,
          dans la deuxième phrase tu dois  demander promptement de mettre leur date de naissance en commentaire pour trouver leur
           jumeau astrologique en commentaire (ici tu le tutoies). tu peux
            parler au masculin neutre, tu dois avoir un ton franc voire choquant. Puis tu réalise un développement franc et provocant, TU NE FAIS PAS DE CONCLUSION c'est mauvais pour la rétention, TU FINIS PAR TA DERNIERE IDEE BRUTALEMENT par le CTA : et si tu veux en savoir plus sur ton theme astral clique sur le lien dans ma bio, . Note importante, s'il y a des chiffres dans
             ta réponse, écrit les en lettres et évite les tirets longs.  Attention ta réponse contient UNIQUEMENT le paragraphe sans
texte introductif ou parasite."""
        dossier = os.path.join(dossier_parent, phrase)
        description_fichier = os.path.join(dossier, "description.txt")
        txt = get_descri(prompt)
        os.mkdir(dossier)
        with open(description_fichier, "w") as file:
            file.write(txt)


    return print("tâche effectuée")

# copy_files("/Users/emmanuellandau/Documents/Astrologie/14_vidéos")
# create_folders_concept("/Users/emmanuellandau/Documents/Astrologie/aout_astro")

# move_video()

# copy_files("/Users/emmanuellandau/Documents/Astrologie/aout_astro")

# check_extension()

def lister_fichiers(dossier):
    # Liste tous les fichiers du dossier
    fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    return fichiers
# mbti_types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
#               "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]

# questions = [f"La plus grande force des {mbti_type}s" for mbti_type in mbti_types]

titres_videos =  ['six chose a ne jamais faire devant un Bélier',
                  'six chose a ne jamais faire devant un Taureau',
                  'six chose a ne jamais faire devant un Gémeaux',
                  'six chose a ne jamais faire devant un Cancer',
                  'six chose a ne jamais faire devant un Lion',
                  'six chose a ne jamais faire devant une Vierge',
                  'six chose a ne jamais faire devant une Balance',
                  'six chose a ne jamais faire devant un Scorpion',
                  'six chose a ne jamais faire devant un Sagittaire',
                  'six chose a ne jamais faire devant un Capricorne',
                  'six chose a ne jamais faire devant un Verseau',
                  'six chose a ne jamais faire devant un Poisson']





















create_folders_concept("/Users/emmanuellandau/Documents/EditLab/TODO", titres_videos)
