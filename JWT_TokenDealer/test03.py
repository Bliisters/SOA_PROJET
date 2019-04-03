import zmq
import time
import sys
import json
import jwtToken

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv()
    binary = message.content
	output = json.loads(binary)

    encoded = jwtToken.chiffre(output['pseudo'],output['nom'],output['prenom'])

    time.sleep (1)

    socket.send(encoded)
