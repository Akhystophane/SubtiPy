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

liste_signes_astro = [
    "Si tu es Bélier voilà ce que les gens pensent secrètement de toi",
    "Si tu es Taureau voilà ce que les gens pensent secrètement de toi",
    "Si tu es Gémeaux voilà ce que les gens pensent secrètement de toi",
    "Si tu es Cancer voilà ce que les gens pensent secrètement de toi",
    "Si tu es Lion voilà ce que les gens pensent secrètement de toi",
    "Si tu es Vierge voilà ce que les gens pensent secrètement de toi",
    "Si tu es Balance voilà ce que les gens pensent secrètement de toi",
    "Si tu es Scorpion voilà ce que les gens pensent secrètement de toi",
    "Si tu es Sagittaire voilà ce que les gens pensent secrètement de toi",
    "Si tu es Capricorne voilà ce que les gens pensent secrètement de toi",
    "Si tu es Verseau voilà ce que les gens pensent secrètement de toi",
    "Si tu es Poissons voilà ce que les gens pensent secrètement de toi",
    "10 raisons de ne pas énerver un Bélier",
    "10 raisons de ne pas énerver un Taureau",
    "10 raisons de ne pas énerver un Gémeaux",
    "10 raisons de ne pas énerver un Cancer",
    "10 raisons de ne pas énerver un Lion",
    "10 raisons de ne pas énerver une Vierge",
    "10 raisons de ne pas énerver une Balance",
    "10 raisons de ne pas énerver un Scorpion",
    "10 raisons de ne pas énerver un Sagittaire",
    "10 raisons de ne pas énerver un Capricorne",
    "10 raisons de ne pas énerver un Verseau",
    "10 raisons de ne pas énerver un Poissons",
    "Pourquoi les Béliers sont si impulsifs",
    "Pourquoi les Taureaux sont si obstinés",
    "Pourquoi les Gémeaux sont si communicatifs",
    "Pourquoi les Cancers sont si sensibles",
    "Pourquoi les Lions sont si charismatiques",
    "Pourquoi les Vierges sont si méticuleuses",
    "Pourquoi les Balances sont si indécises",
    "Pourquoi les Scorpions sont si mystérieux",
    "Pourquoi les Sagittaires sont si optimistes",
    "Pourquoi les Capricornes sont si disciplinés",
    "Pourquoi les Verseaux sont si indépendants",
    "Pourquoi les Poissons sont si rêveurs"
]




create_folders_concept("/Users/emmanuellandau/Documents/EditLab/TODO", liste_signes_astro)
