import json
import os

from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import fr_core_news_md

def words_highlight(folder):
    text_path = os.path.join(folder, "description.txt")
    with open(text_path, "r") as fichier:
        text = fichier.read()
    chemin_fichier = folder + "edit_data.json"
    # if os.path.exists(chemin_fichier):
    #     print("pas de words_highlight edit_data existe")
    #     return False
    positif = []
    negatif = []
    neutre = []
    nlp = fr_core_news_md.load()
    doc = nlp(text)
    adjectives = [token.text for token in doc if token.pos_ == 'ADJ']

    # Tokeniser le texte en mots
    tokens = nltk.word_tokenize(text)
    analyzer = SentimentIntensityAnalyzer()
    for word in tokens:
        sentiment = analyzer.polarity_scores(word)
        if "_g" in word:
            positif.append(word.lower().replace(".", "").replace(",","").replace("_g",""))
        elif "_r" in word:
            negatif.append(word.lower().replace(".", "").replace(",","").replace("_r",""))
        elif "_" in word:
            neutre.append(word.lower().replace(".", "").replace(",", "").replace("_",""))
        elif sentiment['compound'] > 0:
            positif.append(word.lower().replace(".", "").replace(",",""))
        elif sentiment['compound'] < 0:
            negatif.append(word.lower().replace(".", "").replace(",", ""))
    for adj in adjectives:
        if adj not in positif and adj not in negatif:
            neutre.append(adj.lower().replace(".", "").replace(",",""))

    # with open(chemin_fichier, 'w') as fichier:
    #     json.dump([positif, negatif, neutre], fichier)
    # Lire le contenu existant
    try:
        with open(chemin_fichier, 'r') as fichier:
            listes_existantes = json.load(fichier)
    except FileNotFoundError:
        listes_existantes = []

    # Ajouter video_manager comme troisième liste
    listes_existantes.append([positif, negatif, neutre])

    # Réécrire le fichier avec les listes mises à jour
    with open(chemin_fichier, 'w') as fichier:
        json.dump(listes_existantes, fichier)
    print([positif, negatif, neutre])
    print(text)
    return[positif, negatif, neutre]


def word_color(highlight_l, word):
    if word in highlight_l[0]:
        w_color = "#13CC00"
        return w_color
    elif word in highlight_l[1]:
        w_color = "#FF1111"
        return w_color
    elif word in highlight_l[2]:
        w_color = "#FFFC18"
        return w_color
    else:
        print(word)
        return "#FFFC18"
