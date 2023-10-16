longue_str = """
personne_mystère_peur1.png Quel est le signe astrologique le plus généreux ? Prends un moment pour réfléchir. 

personne_mystère_peur2.png As-tu une idée en tête ? 

personne_mystère_peur3.png Allez, je te mets au défi de deviner et d'écrire ta réponse en commentaire avant que je ne te dévoile la réponse. 

personne_angélique1.png Cette générosité dont je parle n'est pas seulement liée à l'argent ou aux cadeaux, mais également à la générosité du cœur, à la capacité d'écouter et de comprendre. 

personne_angélique2.png Les personnes nées sous ce signe sont souvent prêtes à sacrifier leurs propres besoins pour le bien-être des autres. 

personne_angélique3.png Elles ont une empathie naturelle, un désir inné d'aider et de protéger ceux qu'elles aiment. 

personne_angélique4.png Elles donnent sans attendre en retour, leur amour est incommensurable, et elles possèdent une chaleur qui illumine la pièce dès leur entrée. 

personne_mystère_positive1.png Leur esprit charitable est si fort qu'il peut même parfois les mettre dans des situations délicates, car elles sont prêtes à tout pour soutenir une cause ou un être cher. 

personne_mystère_positive2.png Alors, as-tu deviné ? 

Cancer_beautiful.png Si tu as pensé au Cancer, tu as tout bon ! 

Cancer_charismatic.png Les Cancer sont réputés pour leur cœur généreux et leur amour inconditionnel. 

personne_mystère_positive3.png Si l'astrologie t'intéresse, like et abonne-toi pour ne pas rater ma prochaine vidéo.


"""
# Supprimez les sauts de ligne et les espaces inutiles
str_nettoyee = ' '.join(mot.strip() for mot in longue_str.split())

print(str_nettoyee)