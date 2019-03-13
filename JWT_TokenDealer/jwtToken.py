import jwt
import os
import secrets
import time

def setKey() :
    month3Time = 7884000 #3 mois en secondes
    time2 = os.path.getmtime("tokenUltraUltraSecret.txt")
    if((time.time()-time2)>month3Time) :
        token = secrets.token_urlsafe()
        fichier = open("tokenUltraUltraSecret.txt", "w")
        fichier.write(token)
        fichier.close()
    return True

def getKey() :
    fichier = open("tokenUltraUltraSecret.txt","r")
    key = fichier.read()
    fichier.close()
    return key

def chiffre(id,pseudo,name,lastname) :
    setKey()
    key = getKey()
    encoded = jwt.encode({'id': id, 'pseudo': pseudo, 'name': name, 'lastname': lastname}, key, algorithm='HS256')
    return encoded

def dechiffre(encoded) :
    key = getKey()
    try:
        decoded = jwt.decode(encoded, key, algorithms='HS256')
        return True
    except:
        return False

encoded=chiffre(15,'dd','dd','dd')
print(dechiffre(encoded))