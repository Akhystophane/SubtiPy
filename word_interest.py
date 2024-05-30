import ast
import json
import os
from openai import OpenAI
import nltk
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
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

def words_highlight_multilingual(folder):
    text_path = os.path.join(folder, "audio.srt")
    text = get_srt_txt(text_path)
    chemin_fichier = folder + "edit_data.json"
    texts = [
        # Texte original en français
        "Comment les Lions sont réellement en amour ? Même les Lions ne connaissent pas la dernière info, alors visionnez la vidéo jusqu'à la fin pour tout découvrir ! Si tu es Lion, mets ta date de naissance en commentaire pour trouver ton jumeau astrologique et n'oublie pas de liker ! Les Lions, c'est la générosité sans limites. Ils donnent sans attendre en retour, toujours prêts à aider. Leur loyauté est inébranlable : ami ou famille, un Lion sera toujours là pour toi. Leur courage est exceptionnel, face à l'adversité, un Lion ne recule jamais. Leur sens de la justice est très développé, ils défendront toujours ce qui est juste, même contre vents et marées. La créativité des Lions est souvent sous-estimée. Derrière leur force, se cache une âme d'artiste. Leur sens de l'humour est unique. Un Lion sait rire de tout, et surtout de lui-même. En amour, les Lions sont passionnés, généreux et protecteurs. Ils adorent être au centre de l'attention de leur partenaire, tout en offrant un amour inconditionnel. Le Lion est un amant qui aime se surpasser pour faire plaisir à l'autre, mais il attend aussi une reconnaissance et une admiration en retour. Ils aiment les grandes démonstrations d'affection et sont très démonstratifs. Cependant, leur besoin de se sentir valorisés peut parfois les rendre exigeants. Mais la dernière chose que vous devez savoir sur les Lions en amour, c'est leur incroyable résilience émotionnelle. Malgré les défis, ils renaissent toujours de leurs cendres, plus forts et prêts à aimer encore plus intensément. Si tu t'es reconnu ou si tu connais un Lion qui correspond à cette description, laisse un commentaire et partage cette vidéo ! Commente, partage et republie si j'ai vu juste !",

        # Traduction en espagnol
        "¿Cómo son realmente los Leones en el amor? Ni siquiera los Leones conocen la última información, ¡así que mira el video hasta el final para descubrirlo todo! Si eres León, pon tu fecha de nacimiento en los comentarios para encontrar a tu gemelo astrológico y no olvides dar like. Los Leones son generosidad sin límites. Dan sin esperar nada a cambio, siempre dispuestos a ayudar. Su lealtad es inquebrantable: amigo o familia, un León siempre estará ahí para ti. Su coraje es excepcional, frente a la adversidad, un León nunca retrocede. Su sentido de la justicia está muy desarrollado, siempre defenderán lo que es justo, contra viento y marea. La creatividad de los Leones a menudo es subestimada. Detrás de su fuerza, se esconde un alma de artista. Su sentido del humor es único. Un León sabe reírse de todo, y sobre todo de sí mismo. En el amor, los Leones son apasionados, generosos y protectores. Les encanta ser el centro de atención de su pareja, al mismo tiempo que ofrecen un amor incondicional. El León es un amante que le gusta superarse para agradar al otro, pero también espera reconocimiento y admiración a cambio. Les gustan las grandes demostraciones de afecto y son muy expresivos. Sin embargo, su necesidad de sentirse valorados a veces puede hacerlos exigentes. Pero lo último que debes saber sobre los Leones en el amor es su increíble resiliencia emocional. A pesar de los desafíos, siempre renacen de sus cenizas, más fuertes y listos para amar aún más intensamente. Si te has reconocido o conoces a un León que corresponda a esta descripción, ¡deja un comentario y comparte este video! ¡Comenta, comparte y republica si acerté!",

        # Traduction en anglais
        "How are Lions really in love? Even Lions don't know the latest info, so watch the video till the end to discover everything! If you're a Lion, put your birth date in the comments to find your astrological twin and don't forget to like! Lions are boundless generosity. They give without expecting anything in return, always ready to help. Their loyalty is unwavering: friend or family, a Lion will always be there for you. Their courage is exceptional, in the face of adversity, a Lion never backs down. Their sense of justice is highly developed, they will always defend what is right, against all odds. The creativity of Lions is often underestimated. Behind their strength lies an artist's soul. Their sense of humor is unique. A Lion knows how to laugh at everything, especially themselves. In love, Lions are passionate, generous, and protective. They love being the center of their partner's attention, while offering unconditional love. The Lion is a lover who likes to excel to please the other, but they also expect recognition and admiration in return. They love grand gestures of affection and are very demonstrative. However, their need to feel valued can sometimes make them demanding. But the last thing you need to know about Lions in love is their incredible emotional resilience. Despite the challenges, they always rise from the ashes, stronger and ready to love even more intensely. If you see yourself in this or know a Lion who fits this description, leave a comment and share this video! Comment, share, and repost if I got it right!"
    ]
    # text = texts[num]
    prompt = "Je vais te fournir un texte, tu devras me mettre les mots positifs et mélioratif dans une liste (utilise guillemets simples), les mots négatifs dans une autre et quelques adjectifs restants dans une liste neutre. Ta réponse sera UNIQUEMENT une liste de listes de ce format [liste postive, liste negative, liste neutre]" \
             f"texte{text}"
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    output = str(completion.choices[0].message.content)
    print(output)
    start = output.find("[")
    end = output.rfind("]") + 1
    output = ast.literal_eval(output[start:end])
    print(output)

    update_json(chemin_fichier, "Words", output)

    return output


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










