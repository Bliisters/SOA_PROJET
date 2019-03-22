import zmq
import time
import sys
import jwtToken

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv()
    encoded = jwtToken.chiffre('dd','dd','dd')
    time.sleep (1)
    socket.send(encoded)
