import Levenshtein

chaine1 = "exemple1"
chaine2 = "exemple!!"

distance = Levenshtein.distance(chaine1, chaine2)
print("Distance de Levenshtein :", distance)