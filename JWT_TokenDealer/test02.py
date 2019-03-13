import zmq
import time
import sys
import jwtToken

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv()
    encoded = jwtToken.chiffre(15,'dd','dd','dd')
    time.sleep (1)
    socket.send(encoded)
