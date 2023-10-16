import os

def get_file_names_in_directory(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != ".DS_Store":
                file_names.append(file)
    return file_names

# Liste des noms de fichiers
file_names = [
    # ... (insérez tous les noms de fichiers ici)
    "INFP_charismatic.png",
    "INFJ_reading.png",
    # ...
    "ISFP_thinking2.png"
]
def create_list(directory, keywords):
    for keyword in keywords:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if keyword in file:
                    print(file)













folder_path = "/Users/emmanuellandau/Documents/MBTI_bibliothèque"
file_names = get_file_names_in_directory(folder_path)

create_list(folder_path, ['INFP', 'ESFJ'])