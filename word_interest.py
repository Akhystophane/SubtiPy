import json
import os

from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import fr_core_news_md

from suggesterLab.functions import update_json, get_srt_txt


def words_highlight(folder):
    text_path = os.path.join(folder, "audio.srt")
    text = get_srt_txt(text_path)
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

    update_json(chemin_fichier, "Words", [positif, negatif, neutre])

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
