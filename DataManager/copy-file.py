import os
import shutil
import os
import shutil

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
        dossier = os.path.join(dossier_parent, phrase)
        os.mkdir(dossier)
        description_fichier = os.path.join(dossier, "description.txt")
        with open(description_fichier, "x") as file:
            pass
        script_fichier = os.path.join(dossier, "script.txt")
        with open(script_fichier, "x") as file:
            pass
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

titres_videos = [
    "La colère du Bélier",
    "La colère du Taureau",
    "La colère du Gémeaux",
    "La colère du Cancer",
    "La colère du Lion",
    "La colère de la Vierge",
    "La colère de la Balance",
    "La colère du Scorpion",
    "La colère du Sagittaire",
    "La colère du Capricorne",
    "La colère du Verseau",
    "La colère du Poissons",
    "Pourquoi les Béliers sont si impulsifs",
    "Pourquoi les Taureaux sont si tenaces",
    "Pourquoi les Gémeaux sont si curieux",
    "Pourquoi les Cancers sont si protecteurs",
    "Pourquoi les Lions sont si fiers",
    "Pourquoi les Vierges sont si méticuleux",
    "Pourquoi les Balances sont si équilibrés",
    "Pourquoi les Scorpions sont si intenses",
    "Pourquoi les Sagittaires sont si aventuriers",
    "Pourquoi les Capricornes sont si disciplinés",
    "Pourquoi les Verseaux sont si originaux",
    "Pourquoi les Poissons sont si rêveurs",
    "Si tu es Bélier et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Taureau et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Gémeaux et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Cancer et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Lion et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Vierge et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Balance et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Scorpion et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Sagittaire et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Capricorne et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Verseau et que tu vois cette vidéo avant le 30 janvier",
    "Si tu es Poissons et que tu vois cette vidéo avant le 30 janvier",
    "Les trois signes compatibles en amour avec les Béliers",
    "Les trois signes compatibles en amour avec les Taureaux",
    "Les trois signes compatibles en amour avec les Gémeaux",
    "Les trois signes compatibles en amour avec les Cancers",
    "Les trois signes compatibles en amour avec les Lions",
    "Les trois signes compatibles en amour avec les Vierges",
    "Les trois signes compatibles en amour avec les Balances",
    "Les trois signes compatibles en amour avec les Scorpions",
    "Les trois signes compatibles en amour avec les Sagittaires",
    "Les trois signes compatibles en amour avec les Capricornes",
    "Les trois signes compatibles en amour avec les Verseaux",
    "Les trois signes compatibles en amour avec les Poissons"
]














create_folders_concept("/Users/emmanuellandau/Documents/EditLab/TODO", titres_videos)
