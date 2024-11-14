import redis
import json

# on se connecte au serveur redis en local
r = redis.Redis(host='localhost', decode_responses=True, port="6379")

# on ouvre le fichier des pilotes
piloteFile = open("txt/PILOTES.txt", 'r', encoding='utf-8')
pilotes = {}

# on parcourt chaque ligne du fichier pour récupérer les infos des pilotes
for line in piloteFile:
    line = line.split('\t')  # on sépare les champs avec la tabulation
    # on remplit le dictionnaire pilotes avec les infos de chaque pilote
    pilotes[line[0]] = {"nom": line[1], "naissance": line[2], "ville": line[3].rstrip()}

# on ouvre le fichier des clients
clientFile = open("txt/CLIENTS.txt", 'r', encoding='utf-8')
clients = {}

# on parcourt chaque ligne du fichier pour récupérer les infos des clients
for line in clientFile:
    line = line.split('\t')  # on sépare les champs avec la tabulation
    # on remplit le dictionnaire clients avec les infos de chaque client
    clients[line[0]] = {"nom": line[1], "numeroRue": line[2], "nomRue": line[3], "codePostal": line[4], "ville": line[5].rstrip()}

# on ouvre le fichier des classes de vol
classesFile = open('txt/DEFCLASSES.txt', 'r', encoding="utf-8")
classes = {}

# on parcourt chaque ligne du fichier pour récupérer les classes
for line in classesFile:
    line = line.split('\t')  # on sépare les champs avec la tabulation
    # si le vol n'existe pas dans classes, on l'ajoute
    if line[0] not in classes:
        classes[line[0]] = {line[1]: int(line[2].rstrip())}
    else:
        # sinon, on ajoute juste la nouvelle classe au vol existant
        classes[line[0]][line[1]] = int(line[2].rstrip())

# on ouvre le fichier des avions
avionsFile = open("txt/AVIONS.txt", 'r', encoding='utf-8')
avions = {}

# on parcourt chaque ligne du fichier pour récupérer les infos des avions
for line in avionsFile:
    line = line.rstrip().split("\t")  # on sépare les champs avec la tabulation et on enlève les espaces
    # on remplit le dictionnaire avions avec les infos de chaque avion
    avions[line[0]] = {"nom": line[1], "capacite": line[2], "ville": line[3]}

# on ouvre le fichier des vols
volsFile = open('txt/VOLS.txt', 'r', encoding="utf-8")
vols = {}

# on parcourt chaque ligne du fichier pour récupérer les infos des vols
for line in volsFile:
    line = line.split("\t")  # on sépare les champs avec la tabulation
    # on crée une entrée pour chaque vol et on associe les infos du pilote et de l'avion
    vols[line[0]] = {"villeDepart": line[1], "villeArrivee": line[2], "dateDepart": line[3], "heureDepart": line[4], "dateArrivee": line[5], "heureArrivee": line[6], "pilote": pilotes[line[7]], "avion": avions[line[8].rstrip()]}

# on ouvre le fichier des réservations
reservationFile = open("txt/RESERVATIONS.txt", 'r', encoding='utf-8')
reservations = []

# on parcourt chaque ligne du fichier pour récupérer les infos des réservations
for line in reservationFile:
    line = line.split('\t')  # on sépare les champs avec la tabulation
    # on crée une réservation en associant le client, le vol et la classe avec le coefficient de prix
    reservations.append({"client": clients[line[0]], "vol": vols[line[1]], "classe": {"nom": line[2], "coeffPrix": classes[line[1]][line[2]]}, "places": int(line[3].rstrip())})

# on enregistre chaque réservation dans redis
for i in range(len(reservations)):
    # chaque réservation est stockée sous une clé unique avec un index
    r.set(f"reservation:{i+1}", json.dumps({"reservation": reservations[i]}))
