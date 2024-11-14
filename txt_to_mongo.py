from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://chems1:chems@cluster0.4gaue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Aeroport']
collection = db['Garges']

# chargement des pilotes
pilotes = {}
with open("txt/PILOTES.txt", 'r', encoding='utf-8') as piloteFile:
    for line in piloteFile:
        line = line.split('\t')
        pilotes[line[0]] = {"nom": line[1], "naissance": line[2], "ville": line[3].rstrip()}

# chargement des clients
clients = {}
with open("txt/CLIENTS.txt", 'r', encoding='utf-8') as clientFile:
    for line in clientFile:
        line = line.split('\t')
        clients[line[0]] = {"nom": line[1], "numeroRue": line[2], "nomRue": line[3], "codePostal": line[4], "ville": line[5].rstrip()}

# chargement des classes de vol
classes = {}
with open('txt/DEFCLASSES.txt', 'r', encoding="utf-8") as classesFile:
    for line in classesFile:
        line = line.split('\t')
        vol_id, classe_nom, coeff_prix = line[0], line[1], int(line[2].rstrip())
        if vol_id not in classes:
            classes[vol_id] = {}
        classes[vol_id][classe_nom] = coeff_prix

# chargement des avions
avions = {}
with open("txt/AVIONS.txt", 'r', encoding='utf-8') as avionsFile:
    for line in avionsFile:
        line = line.rstrip().split("\t")
        avions[line[0]] = {"nom": line[1], "capacite": line[2], "ville": line[3]}

# chargement des vols
vols = {}
with open('txt/VOLS.txt', 'r', encoding="utf-8") as volsFile:
    for line in volsFile:
        line = line.split("\t")
        vol_id = line[0]
        vols[vol_id] = {
            "villeDepart": line[1],
            "villeArrivee": line[2],
            "dateDepart": line[3],
            "heureDepart": line[4],
            "dateArrivee": line[5],
            "heureArrivee": line[6],
            "pilote": pilotes[line[7]],       # association avec les données du pilote
            "avion": avions[line[8].rstrip()]  # association avec les données de l'avion
        }

# insertion des réservations dans MongoDB
reservations = []
with open("txt/RESERVATIONS.txt", 'r', encoding='utf-8') as reservationFile:
    for line in reservationFile:
        line = line.split('\t')
        client_id, vol_id, classe_nom, places = line[0], line[1], line[2], int(line[3].rstrip())
        
        # création du document de réservation complet
        reservation = {
            "client": clients[client_id],
            "vol": vols[vol_id],
            "classe": {
                "nom": classe_nom,
                "coeffPrix": classes[vol_id][classe_nom]
            },
            "places": places
        }
        
        # ajout de la réservation dans la liste
        reservations.append({"reservation": reservation})

# insérer toutes les réservations dans MongoDB
collection.insert_many(reservations)

print("Toutes les réservations ont été insérées dans MongoDB avec succès.")
