from pymongo import MongoClient 
from bson import ObjectId 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connexion à MongoDB avec l'URI spécifique du cluster
uri = "mongodb+srv://chems1:chems@cluster0.4gaue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))  # Connexion à MongoDB
db = client['Aeroport']  # Sélection de la base de données 'Aeroport'
collection = db['']  # Collection vide spécifiée, mais il manque le nom de la collection ici

# Fonction pour définir un document avec une clé et une valeur
def set_key(collection, key, value):
    """
    Définit un document avec une clé et une valeur.
    Utilise 'upsert' pour créer un document si aucun document avec la clé n'existe.
    """
    result = collection.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)
    print(f"Document avec '_id' '{key}' défini avec la valeur '{value}'")

# Fonction pour récupérer la valeur associée à une clé
def get_key(collection, key):
    """
    Récupère la valeur d'un document avec une clé spécifique.
    Si le document n'existe pas, retourne None.
    """
    document = collection.find_one({"_id": key})  # Recherche du document par son '_id'
    if document:
        print(f"Valeur pour '{key}': {document['value']}")
        return document['value']
    else:
        print(f"Le document avec '_id' '{key}' n'existe pas.")
        return None

# Fonction pour récupérer des documents dont l'_id correspond à un motif
def get_pattern(collection, pattern=""):
    """
    Récupère les documents dont les _id contiennent un motif spécifique (via une expression régulière).
    """
    regex = {"$regex": pattern} if pattern else {}  # Applique une regex si un motif est spécifié
    documents = collection.find({"_id": regex})  # Recherche les documents qui correspondent au motif
    print(f"Documents correspondant au motif '{pattern}': {[doc['_id'] for doc in documents]}")

# Fonction pour mettre à jour la valeur d'un document existant
def update_key(collection, key, new_value):
    """
    Met à jour la valeur d'un document existant avec un nouvel attribut 'value'.
    """
    result = collection.update_one({"_id": key}, {"$set": {"value": new_value}})
    if result.modified_count > 0:
        print(f"Valeur du document avec '_id' '{key}' mise à jour à '{new_value}'")
    else:
        print(f"Le document avec '_id' '{key}' n'existe pas pour mise à jour.")

# Fonction pour supprimer un document par sa clé
def delete_key(collection, key):
    """
    Supprime un document de la collection MongoDB en fonction de son '_id'.
    """
    result = collection.delete_one({"_id": key})
    if result.deleted_count > 0:
        print(f"Document avec '_id' '{key}' supprimé.")
    else:
        print(f"Le document avec '_id' '{key}' n'existe pas.")

# Fonction pour incrémenter la valeur numérique d'un document
def increment_key(collection, key):
    """
    Incrémente la valeur d'un document numérique.
    Si la valeur n'existe pas, l'opération échoue.
    """
    result = collection.find_one_and_update(
        {"_id": key},
        {"$inc": {"value": 1}},  # Incrémente la valeur de 1
        return_document=True  # Retourne le document mis à jour
    )
    if result:
        print(f"Valeur du document avec '_id' '{key}' incrémentée à {result['value']}")
        return result['value']
    else:
        print(f"Le document avec '_id' '{key}' n'existe pas pour incrémentation.")
        return None

# Fonction pour afficher tous les '_id' des documents présents dans la collection
def get_all_keys(collection):
    """
    Affiche tous les '_id' des documents dans la collection MongoDB.
    """
    documents = collection.find()  # Récupère tous les documents
    keys = [doc['_id'] for doc in documents]  # Liste des _id des documents
    if keys:
        print("Documents dans la collection MongoDB :")
        for key in keys:
            print(f"- {key}")
    else:
        print("Aucun document dans la collection MongoDB.")

# Fonction pour supprimer tous les documents d'une collection MongoDB
def delete_all_keys(collection):
    """
    Supprime tous les documents présents dans la collection MongoDB.
    """
    result = collection.delete_many({})  # Supprime tous les documents
    if result.deleted_count > 0:
        print("Tous les documents ont été supprimés de la collection MongoDB.")
    else:
        print("Aucun document à supprimer dans la collection MongoDB.")

# Exemples d'utilisation des fonctions (commentées pour éviter l'exécution)
# delete_all_keys(collection)  # Supprime tous les documents
# get_all_keys(collection)  # Affiche tous les _id des documents
# get_pattern(collection, "pattern")  # Recherche les documents avec un motif d'_id
# set_key(collection, "test", "1")  # Définit un document avec une clé "test" et une valeur "1"
