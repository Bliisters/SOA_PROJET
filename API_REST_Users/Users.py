from flask import Flask, jsonify, request
from pymongo import MongoClient
import datetime
import pprint
import random
import string
import json

app = Flask(__name__)

"""
Less Basics Microservices
With usage of variables in the app.route
"""

@app.route('/api', methods=['POST', 'DELETE', 'GET'])


def my_microservice():
    print(request)
    print(request.environ)
    response = jsonify({'Hello': 'World!'})
    print(response)
    print(response.data)
    return response


@app.route('/api/person/<int:person_id>')
def person(person_id):
    response = jsonify({'Hello': person_id})
    return response
	
@app.route('/api/test')
def test(nom):
	client = MongoClient()
	db = client.test_database
	collection = db.posts
	print("HELLO")
	doc = pprint.pprint(collection.find_one())
	return ("WORLD")
	
@app.route('/api/add', methods = ['POST'])
def addUser():

	# Récupération des données de POST 
	nom = request.form['nom']
	prenom = request.form['prenom']
	pseudo = request.form['pseudo']
	mdp = request.form['mdp']
	
	# Vérification de la taille du mot de passe
	if len(mdp)<10:
		print("Mot de passe trop court : 10 caractères minimum")
		return("")
	
	# Connection à la base de donnée
	client = MongoClient()
	db = client.soa_db
	collection_user = db.usagers
	collection_salt = db.baleine
	
	# Récupération de l'utilisateur dans la table par son pseudo
	doc = collection_user.find_one({"pseudo": pseudo})
	
	if doc:
		print("Ce pseudo est déjà pris, réessayez")	
		return ("")
		
	
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
	return("")

	
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
	print(user)
	sel = collection_salt.find_one({"user":user},{"_id":0})
	sel = sel["salt"]
	print(sel)
	
	
	if sel:
		print("mdp : "+str(hash(str(mdp)+sel)))
		#print()
		return("")
	else:
		print("Connection impossible : vérifiez vos identifiants::::::")
	return("")
	
	# Vérification de l'existence du profil
	#doc = collection.find_one({"pseudo": pseudo, "mdp": mdp})
	
	#if doc == None:
	#	print("Identifiants invalides")
	#else:
	#	print("Vous êtes connecté !")
		
	return("")
		
	
	


if __name__ == '__main__':
    print(app.url_map)
app.run()