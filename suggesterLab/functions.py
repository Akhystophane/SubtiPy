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
def get_char(niche, char):
    # Lire à partir d'un fichier JSON
    with open('/Users/emmanuellandau/PycharmProjects/SubtiPy/suggesterLab/niche_settings.json', 'r') as f:
        data = json.load(f)
    # Récupérer et convertir la chaîne en multilignes
    texte = data[niche][char].replace("\\n", "\n")

    return texte

def formatter_srt(srt_text):
    # Diviser le texte SRT en blocs
    blocs = srt_text.strip().split('\n\n')

    resultat = ""
    for bloc in blocs:
        # Séparer les lignes dans chaque bloc
        lignes = bloc.split('\n')

        # Le premier élément est le numéro du sous-titre
        numero = lignes[0].strip()

        # Le reste est le texte du sous-titre
        texte = ' '.join(lignes[2:])

        # Ajouter au résultat avec le format souhaité
        resultat += f"{{{numero}}} {texte} "

    return resultat.strip()

def formatter_srtV2(srt_text, saut=0):
    # Diviser le texte SRT en blocs
    blocs = srt_text.strip().split('\n\n')

    resultat = ""
    afficher_numero = True  # Pour toujours afficher le premier numéro
    compteur_saut = 0  # Compteur pour le nombre de sauts effectués

    for bloc in blocs:
        # Séparer les lignes dans chaque bloc
        lignes = bloc.split('\n')

        # Le premier élément est le numéro du sous-titre
        numero = lignes[0].strip()

        # Le reste est le texte du sous-titre
        texte = ' '.join(lignes[2:])

        if afficher_numero:
            # Ajouter au résultat avec le numéro du sous-titre
            resultat += f"{{{numero}}} {texte} "
            compteur_saut = saut  # Réinitialiser le compteur de saut après avoir affiché un numéro
        else:
            # Ajouter au résultat sans le numéro du sous-titre
            resultat += f"{texte} "

        # Déterminer si le numéro doit être affiché pour le prochain sous-titre
        # Si le compteur de saut est 0, vérifier la fin de la phrase pour déterminer l'affichage du numéro
        if compteur_saut == 0:
            afficher_numero = texte.strip().endswith('.')
        else:
            # Décrémenter le compteur de saut si un numéro ne doit pas être affiché
            compteur_saut -= 1
            afficher_numero = False  # S'assurer que le numéro n'est pas affiché tant que le compteur n'est pas 0

    return resultat.strip()




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


from pydub import AudioSegment


def mp3_to_wav_slice(input_mp3_path, start_seconds, end_seconds, output_wav_path):
    """
    Découpe une partie d'un fichier audio MP3 et enregistre l'extrait en format WAV.

    :param input_mp3_path: Chemin vers le fichier MP3 source.
    :param start_ms: Timestamp de début en millisecondes.
    :param end_ms: Timestamp de fin en millisecondes.
    :param output_wav_path: Chemin où enregistrer le fichier WAV résultant.
    """
    start_ms = int(start_seconds * 1000)
    end_ms = int(end_seconds * 1000)
    # Charger le fichier MP3
    audio = AudioSegment.from_mp3(input_mp3_path)

    # Découper l'audio du timestamp de début à fin
    sliced_audio = audio[start_ms:end_ms]

    # Enregistrer l'extrait en format WAV
    sliced_audio.export(output_wav_path, format="wav")


