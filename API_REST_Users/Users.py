from flask import Flask, jsonify, request
from pymongo import MongoClient
import datetime
import requests
import zmq
import pprint
import random
import string
import json

app = Flask(__name__)

"""
Less Basics Microservices
With usage of variables in the app.route
"""

@app.route('/api/add', methods = ['POST'])
def addUser():

	# Récupération des données de POST
    if('nom' in request.form and 'prenom' in request.form and 'pseudo' in request.form and 'mdp' in request.form):
        nom = request.form['nom']
        prenom = request.form['prenom']
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']
    else:
        print("champs incomplets")
        response = jsonify({'error': 'champs incomplets'})
        print(response)
        return response, 404

	# Vérification de la taille du mot de passe
    if len(mdp)<10:
        print("Mot de passe trop court : 10 caractères minimum")
        response = jsonify({'error': 'Mot de passe trop court : 10 caractères minimum'})
        print(response)
        return response

	# Connection à la base de donnée
    client = MongoClient()
    db = client.soa_db
    collection_user = db.usagers
    collection_salt = db.baleine

	# Récupération de l'utilisateur dans la table par son pseudo
    doc = collection_user.find_one({"pseudo": pseudo})

    if doc:
        print("Ce pseudo est déjà pris, réessayez")
        response = jsonify({'error': 'Ce pseudo est déjà pris, réessayez'})
        print(response)
        return response


	# Création d'un sel de 5 caractères aléatoires
    salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))

	# Hashage & salage du mdp
    mdp = str(hash(str(mdp)+salt))


	# Création du post pour la table utilisateur
    post_user = {"nom": nom,
        "prenom": prenom,
        "pseudo": pseudo,
        "mdp": mdp}

	# Publication dans la base de donnée de l'utilisateur
    post_user_id = collection_user.insert_one(post_user).inserted_id

	# Création du post pour la table des sels
    post_salt = {"user": pseudo,
        "salt": salt}

	# Publication dans la base de données du sel de l'utilisateur
    post_salt_id = collection_salt.insert_one(post_salt).inserted_id

    print("Validé !")
    response = jsonify({'accept': 'Compte créé'})
    print(response)
    return response


@app.route('/api/login', methods = ['POST'])
def login():

	# Récupération des données du post
    user = request.form['user']
    mdp = request.form['mdp']

	# Connection à la base de donnée
    client = MongoClient()
    db = client.soa_db
    collection_user = db.usagers
    collection_salt = db.baleine

	# Hashage & salage du mdp
    psw = collection_user.find_one({"pseudo":user})
    psw = psw['mdp']
    print(psw)
    sel = collection_salt.find_one({"user":user},{"_id":0})
    sel = sel["salt"]
    print(sel)

    if sel:
        print("mdp : "+str(hash(str(mdp)+sel)))
        if(str(hash(str(mdp)+sel)) == str(psw)):
            #ici travailler sur ZMQ
            port = "5556"
            context = zmq.Context()
            print("Connecting to server...")
            socket = context.socket(zmq.REQ)
            socket.connect ("tcp://localhost:%s" % port)
            data = {'pseudo': 'tata','nom': 'tata','prenom': 'tata'}
            socket.send_json(data)
            message = socket.recv()
            token = message.decode('utf-8')
            print(token)
            url = 'http://localhost:5001/api'
            headers = {'Authorization':token}
            r = requests.get(url, headers=headers)
            return r.json()
        else:
            print("Connection impossible : vérifiez vos identifiants")
            response = jsonify({'msg': 'mauvais identifiants de connexion'})
            print(response)
            return response

    else:
        print("Connection impossible : vérifiez vos identifiants")
        response = jsonify({'msg': 'mauvais identifiants de connexionsel'})
        print(response)
        return response

if __name__ == '__main__':
    print(app.url_map)
app.run()
