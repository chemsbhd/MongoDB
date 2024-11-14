# On importe les modules nécessaires pour se connecter à MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# URI de connexion à la base de données MongoDB. Ce sont les infos pour se connecter à ton cluster.
uri = "mongodb+srv://chems1:chems@cluster0.4gaue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Création de la connexion à la base de données avec l'URI et l'API serveur.
client = MongoClient(uri, server_api=ServerApi('1'))
# Sélection de la base de données "Aeroport"
db = client['Aeroport']
# Sélection de la collection "Garges" dans la base de données
collection = db['Garges']

# Fonction pour compter le nombre de pilotes uniques
def compter_pilotes_uniques():
    # On récupère tous les noms de pilotes distincts dans la collection
    pilotes = collection.distinct('reservation.vol.pilote.nom')
    # On met à jour ou on crée un document avec le nombre de pilotes uniques
    collection.update_one({"type": "unique_pilots"}, {"$set": {"count": len(pilotes)}}, upsert=True)
    # On retourne le nombre de pilotes uniques
    return len(pilotes)

# On appelle la fonction pour compter les pilotes et on affiche le résultat
nombre_pilotes = compter_pilotes_uniques()
print(f"Nombre de pilotes uniques: {nombre_pilotes}")

# Fonction pour récupérer les villes d'arrivée uniques des réservations
def villes_arrivee_reservations():
    # On récupère toutes les villes d'arrivée distinctes
    villes = collection.distinct('reservation.vol.villeArrivee')
    # On met à jour ou on crée un document avec la liste des villes d'arrivée
    collection.update_one({"type": "arrival_cities"}, {"$set": {"cities": villes}}, upsert=True)
    # On retourne la liste des villes d'arrivée
    return villes

# On appelle la fonction pour obtenir les villes d'arrivée et on les affiche
villes_arrivee = villes_arrivee_reservations()
print(f"Villes d'arrivée uniques: {villes_arrivee}")

# Fonction pour créer un classement des pilotes en fonction du nombre de vols
def classement_pilotes():
    # Pipeline d'agrégation pour grouper par pilote et compter le nombre de vols
    pipeline = [
        {"$group": {"_id": "$reservation.vol.pilote.nom", "vols": {"$sum": 1}}},
        {"$sort": {"vols": -1}}  # Tri décroissant par nombre de vols
    ]
    # On exécute l'agrégation et on récupère le résultat sous forme de liste
    classement = list(collection.aggregate(pipeline))
    # On met à jour ou on crée un document avec le classement des pilotes
    collection.update_one({"type": "pilot_rankings"}, {"$set": {"ranking": classement}}, upsert=True)
    # On retourne le classement des pilotes
    return classement

# On appelle la fonction pour obtenir le classement des pilotes et on l'affiche
classement = classement_pilotes()
print("Classement des pilotes par nombre de vols :", classement)
