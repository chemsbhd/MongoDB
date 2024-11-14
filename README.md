Guide complet pour configurer MongoDB Atlas avec pymongo
1. Créer un compte sur MongoDB Atlas

    Rendez-vous sur MongoDB Atlas et créez un compte si vous n'en avez pas déjà un.
    Une fois inscrit, connectez-vous à votre compte.

2. Créer un cluster sur MongoDB Atlas

    Après vous être connecté, cliquez sur Build a Cluster.
    Sélectionnez Cloud Provider & Region en fonction de vos préférences (vous pouvez choisir une option gratuite).
    Une fois que vous avez choisi la configuration, cliquez sur Create Cluster.
    Le cluster sera créé et cela peut prendre quelques minutes.

3. Ajouter un utilisateur à la base de données

    Allez dans Database Access dans le menu à gauche.
    Cliquez sur Add New Database User.
    Créez un utilisateur avec un nom d'utilisateur et un mot de passe sécurisé. Donnez-lui des droits d'accès appropriés (par exemple, Read and Write to any database).

4. Activer les connexions IP

    Allez dans Network Access.
    Cliquez sur Add IP Address.
    Si vous souhaitez autoriser toutes les connexions, entrez 0.0.0.0/0 pour permettre l'accès depuis n'importe quelle adresse IP. Si vous avez une IP spécifique, ajoutez-la.

5. Connexion à MongoDB Atlas avec pymongo

    Allez dans Clusters, puis cliquez sur Connect.
    Sélectionnez Connect your application.
    Copiez l'URI de connexion (qui ressemble à mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority).

6. Installer les bibliothèques nécessaires

Avant de pouvoir interagir avec MongoDB à partir de Python, vous devez installer le module pymongo et éventuellement d'autres modules comme pandas pour la manipulation des données.

Exécutez la commande suivante dans votre terminal ou dans votre environnement virtuel Python :

pip install pymongo pandas

Si vous souhaitez utiliser un Bloom Filter (pour une gestion rapide des ensembles), vous pouvez également installer pybloom-live :

pip install pybloom-live

7. Connexion à MongoDB Atlas dans votre code Python

Voici un exemple de script pour vous connecter à votre base de données MongoDB Atlas et interagir avec la collection.

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# URI de connexion à MongoDB Atlas
uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connexion à la base de données
db = client['Aeroport']  # Remplacez par le nom de votre base de données
collection = db['Garges']  # Remplacez par le nom de votre collection

Remplacez <username> et <password> dans l'URI de connexion avec vos informations d'identification MongoDB.
8. Exemple de gestion de données avec MongoDB

Vous pouvez maintenant effectuer des opérations de base telles que l'insertion, la mise à jour, et la récupération des données dans MongoDB.
Insertion de données

def inserer_document(collection, key, value):
    """Insérer un document dans la collection."""
    result = collection.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)
    print(f"Document inséré avec '_id' '{key}' et valeur '{value}'")

inserer_document(collection, "test", "1")

Récupérer des données

def obtenir_document(collection, key):
    """Récupérer un document par sa clé (_id)."""
    document = collection.find_one({"_id": key})
    if document:
        print(f"Valeur pour '{key}': {document['value']}")
        return document['value']
    else:
        print(f"Document avec '_id' '{key}' non trouvé.")
        return None

obtenir_document(collection, "test")

Mettre à jour des données

def mettre_a_jour_document(collection, key, new_value):
    """Mettre à jour la valeur d'un document."""
    result = collection.update_one({"_id": key}, {"$set": {"value": new_value}})
    if result.modified_count > 0:
        print(f"Document avec '_id' '{key}' mis à jour avec valeur '{new_value}'")
    else:
        print(f"Aucune mise à jour trouvée pour le document avec '_id' '{key}'")

mettre_a_jour_document(collection, "test", "2")

Supprimer des données

def supprimer_document(collection, key):
    """Supprimer un document de la collection."""
    result = collection.delete_one({"_id": key})
    if result.deleted_count > 0:
        print(f"Document avec '_id' '{key}' supprimé.")
    else:
        print(f"Document avec '_id' '{key}' non trouvé.")

supprimer_document(collection, "test")

9. Exemple d'intégration avec Bloom Filter et CSV

Si vous souhaitez utiliser un Bloom Filter pour vérifier rapidement les passagers dans un fichier CSV, voici un exemple :

from pybloom_live import BloomFilter
import pandas as pd
import time

# Lecture du fichier CSV
file_name = 'aeroport.csv'
df = pd.read_csv(file_name, sep=';', on_bad_lines='skip')

# Créer un filtre de Bloom
bloom_filter = BloomFilter(capacity=len(df), error_rate=0.001)

# Remplir le filtre de Bloom avec les noms des passagers
start_time = time.time()
for index, row in df.iterrows():
    passager = f"{row['Nom']} {row['Prénom']}"
    bloom_filter.add(passager)

# Afficher le temps pour remplir le Bloom Filter
elapsed_time = time.time() - start_time
print(f"Temps pour remplir le Bloom Filter : {elapsed_time:.5f} secondes")

# Vérifier si un passager est enregistré
def check_passager(nom, prenom):
    full_name = f"{nom} {prenom}"
    if full_name in bloom_filter:
        return f"{full_name} est probablement enregistré."
    else:
        return f"{full_name} n'est pas enregistré."

# Exemple d'utilisation
print(check_passager("Dupont", "Jean"))

10. Conclusion

Vous avez maintenant toutes les informations nécessaires pour configurer MongoDB Atlas, utiliser pymongo pour interagir avec votre base de données et manipuler vos données à travers des techniques comme le Bloom Filter.

Suivez le tutoriel d'ESSAADOUNI Sidi pour plus de détails et d'exemples pratiques. N'oubliez pas que MongoDB Atlas est une plateforme flexible qui vous permet de gérer facilement votre base de données cloud, d'y accéder de manière sécurisée, et de profiter de toutes ses fonctionnalités avancées.
