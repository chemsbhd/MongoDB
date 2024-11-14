from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from pybloom_live import BloomFilter
import time

uri = "mongodb+srv://chems1:chems@cluster0.4gaue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# lecture du fichier CSV
file_name = 'aeroport.csv'
try:
    df = pd.read_csv(file_name, sep=';', on_bad_lines='skip')  # change le séparateur à point-virgule
except Exception as e:
    print(f"Erreur lors du chargement du fichier CSV : {e}")
    exit()

# Afficher les premières lignes du DataFrame
print("Voici les premières lignes du fichier CSV :")
print(df.head())

# créer un filtre de Bloom
bloom_filter = BloomFilter(capacity=len(df), error_rate=0.001)

# remplir le filtre de Bloom avec les noms des passagers
start_time = time.time()
for index, row in df.iterrows():
    passager = f"{row['Nom']} {row['Prénom']}"  # on crée le nom complet
    bloom_filter.add(passager)

# calculer le temps de remplissage du filtre
elapsed_time = time.time() - start_time
print(f"Temps pour remplir le Bloom Filter : {elapsed_time:.5f} secondes")

# fonction pour vérifier si un passager est enregistré
def check_passager(nom, prenom):
    full_name = f"{nom} {prenom}"
    if full_name in bloom_filter:
        return f"{full_name} est probablement enregistré."
    else:
        return f"{full_name} n'est pas enregistré."

# exemples
print(check_passager("Dupont", "Jean"))
print(check_passager("Martin", "Sophie"))
print(check_passager("Durand", "Marc"))
print(check_passager("Leroy", "Claire"))
print(check_passager("Bernard", "Lucie"))
print(check_passager("Mbappé", "Kylian"))
