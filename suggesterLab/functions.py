import ast
import json
import re
def update_json(nom_fichier, cle, valeur):
    try:
        # Essayer d'ouvrir le fichier s'il existe
        with open(nom_fichier, 'r+') as fichier:
            try:
                # Charger le contenu du fichier (si le fichier est vide, cela lève une exception JSONDecodeError)
                data = json.load(fichier)
            except json.JSONDecodeError:
                data = {}

            # Mettre à jour la clé avec la valeur fournie
            print("valeur", valeur)
            data[cle] = valeur

            # Réinitialiser le pointeur du fichier au début et écraser le contenu
            fichier.seek(0)
            json.dump(data, fichier)
            fichier.truncate()

    except FileNotFoundError:
        # Créer le fichier s'il n'existe pas
        with open(nom_fichier, 'w') as fichier:
            # Créer un dictionnaire avec la clé et la valeur fournies et écrire dans le fichier
            data = {cle: valeur}
            json.dump(data, fichier)

def time_to_seconds(time_str):
    try:
        # Remplacer le caractère "," par "."
        time_str = time_str.replace(',', '.')

        # Séparer les heures, minutes, secondes et millisecondes
        hh, mm, ss_milli = time_str.split(":")
        ss, milli = ss_milli.split(".")

        # Convertir en secondes
        total_seconds = int(hh) * 3600 + int(mm) * 60 + int(ss) + float("0." + milli)

        return str(total_seconds)
    except ValueError:
        print("Format de temps invalide")
        return None

def get_srt_txt(chemin_fichier_srt):
    # Lire le fichier et extraire le texte
    texte_srt = ''
    with open(chemin_fichier_srt, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            # Ignorer les lignes vides et les lignes qui contiennent des timestamps ou des numéros de séquences
            if not ligne.strip() or '-->' in ligne or ligne.strip().isdigit():
                continue
            # Ajouter le texte à la chaîne finale
            texte_srt += ligne.strip() + ' '

    return texte_srt

def key_exists_in_json(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if key in data:
                    return True
                # Ici, vous pouvez ajouter d'autres traitements si nécessaire
                # Si checked est False, la fonction continue son exécution
            return False
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
        return False
    except json.JSONDecodeError:
        print("Erreur de décodage JSON.")
        return False

def extract_dict(text):
    # Rechercher une chaîne qui ressemble à un dictionnaire Python
    dict_match = re.search(r"\{[^}]*\}", text)
    if dict_match:
        # Extraire la chaîne de caractères correspondante
        dict_str = dict_match.group(0)
        try:
            # Convertir la chaîne en dictionnaire en utilisant `literal_eval` qui est plus sûr que `eval`
            return ast.literal_eval(dict_str)
        except (ValueError, SyntaxError):
            # Gérer l'exception si la conversion échoue
            print("Erreur lors de la conversion de la chaîne en dictionnaire.")
            return None
    else:
        print("Aucun dictionnaire trouvé dans le texte.")
        return None