# Liste initiale des footages B-roll
import os

from suggesterLab.functions import mp3_to_wav_slice

footages = [
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/A_depiction_of_a_person_waiting_eagerly.png",
        "0.04"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/A_confirmation_message_or_check_mark.png",
        "2.7199999999999998"
    ],
    [
        "/Users/emmanuellandau/Documents/mediaLibrary/9196255.mp4",
        "4.38"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/A_person_who_is_on_the_verge_of_giving.png",
        "9.94"
    ],
    [
        "/Users/emmanuellandau/Documents/mediaLibrary/3806680.mp4",
        "14.46"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/A_depiction_of_the_universe_with_stars.png",
        "21.1"
    ],
    [
        "/Users/emmanuellandau/Documents/mediaLibrary/7088947.mp4",
        "28.26"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/Illustration_of_suspenseful_moment_like.png",
        "34.36"
    ],
    [
        "/Users/emmanuellandau/Documents/mediaLibrary/7203928.mp4",
        "39.04"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/Various_indicators_or_signs_such_as.png",
        "45.3"
    ],
    [
        "/Users/emmanuellandau/Documents/mediaLibrary/7608712.mp4",
        "54.72"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/A_key_suggesting_openness_and_readiness.png",
        "59.46"
    ],
    [
        "/Users/emmanuellandau/Documents/mediaLibrary/4154503.mp4",
        "65.16"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/A_depiction_of_a_shared_experience_with.png",
        "68.98"
    ],
    [
        "/Users/emmanuellandau/Documents/MidjourneyBibli/An_illustration_of_the_universe.png",
        "75.78"
    ],
    [
        "last.mp4",
        "79.38"
    ]
]



def insert_a_roll(folder, footages):

    flag= ""
    time_count = 0
    result = [["A-roll", "0.0"]]  # Commencer avec un A-roll au timestamp 0.0
    y = 0  # Compteur pour sauter les éléments après chaque A-roll inséré

    for i in range(len(footages)):
        # Après le premier A-roll, ajouter directement les B-roll à la liste résultat
        # sauf si la règle spécifique pour un nouvel A-roll est rencontrée
        if i + 1 < len(footages):
            current_timestamp = float(footages[i][1])
            next_timestamp = float(footages[i + 1][1])
            if current_timestamp <= 2.5:
                continue

            # Si la différence de timestamp avec le prochain élément est <= 8 secondes,
            # insérer un A-roll et sauter les 3 prochains éléments B-roll
            if 2 <= (next_timestamp - current_timestamp) <= 8 and time_count <= 15 and y >= 3:
                result.append(["A-roll", footages[i][1]])
                output_path = os.path.join(folder, f"audio{str(i)}.wav")
                input_path = os.path.join(folder, f"audio.mp3")
                mp3_to_wav_slice(input_path,current_timestamp, next_timestamp, output_path )
                time_count += next_timestamp - current_timestamp
                flag = current_timestamp
                # print("A-roll", current_timestamp)
                y=0
            elif current_timestamp != flag:
                # print(footages[i], current_timestamp)
                # Ajouter le B-roll actuel car il n'est pas remplacé par un A-roll
                result.append(footages[i])
                y += 1
        else:
            # Ajouter le dernier B-roll si on est à la fin de la liste
            result.append(footages[i])
    print(time_count)

    return result


# Appliquer la fonction aux footages
new_footages = insert_a_roll("/Users/emmanuellandau/Documents/EditLab/archive/La bonne nouvelle", footages)

# Afficher le résultat
for footage in new_footages:
    print(footage)
