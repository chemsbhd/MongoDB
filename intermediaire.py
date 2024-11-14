# Importation des modules nécessaires
import time 
from pymongo.mongo_client import MongoClient 
from pymongo.server_api import ServerApi 
import json 

# Connexion à la base de données MongoDB (la connexion est établie mais non utilisée dans ce code)
uri = "mongodb+srv://chems1:chems@cluster0.4gaue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Aeroport']
collection = db['Garges']

# Chargement des données à partir de deux fichiers JSON différents
# Ces fichiers contiennent des réservations et sont chargés en mémoire pour être traités
with open('reservations1.json') as file1, open('reservations2.json') as file2:
    reservations1 = json.load(file1)
    reservations2 = json.load(file2)

# Fonction pour accéder à une valeur spécifique dans un dictionnaire imbriqué
# Par exemple, si on cherche un "pilote" dans un objet "vol", on peut obtenir cette valeur en utilisant un chemin comme "vol.pilote"
def obtenir_valeur(data, chemin):
    attributs = chemin.split(".")
    valeur = data
    for attribut in attributs:
        valeur = valeur.get(attribut)
        if valeur is None:
            return None
    return valeur

# Fonction pour effectuer une jointure entre deux ensembles de données
# La jointure se fait sur un attribut commun (par exemple, "vol.pilote")
def jointure(d1, d2, chemin_attribut):
    jointures = []
    for id1, data1 in d1.items():
        for id2, data2 in d2.items():
            if obtenir_valeur(data1, chemin_attribut) == obtenir_valeur(data2, chemin_attribut):
                jointure = {
                    "reservation1": data1,
                    "reservation2": data2
                }
                jointures.append(jointure)
    return jointures

# Effectue la jointure entre les deux ensembles de données basés sur l'attribut "vol.pilote"
resultat_jointure = jointure(reservations1, reservations2, "vol.pilote")

# Affiche les résultats de la jointure
# Chaque jointure correspond à deux réservations ayant le même pilote
print("Jointures trouvées :")
for idx, jointure in enumerate(resultat_jointure, start=1):
    print(f"Jointure {idx}:")
    print("RESERVATION 1:", jointure["reservation1"])
    print("RESERVATION 2:", jointure["reservation2"])
    print("------------------------------------------------------------")
