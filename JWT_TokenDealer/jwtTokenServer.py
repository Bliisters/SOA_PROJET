import zmq
import time
import sys
import jwtToken
from  multiprocessing import Process

def serverDealer(port="5556"):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print ("Running server on port: ", port)
    while(True) :
        message = socket.recv()
        binary = message.content
        output = json.loads(binary)
        encoded = jwtToken.chiffre(output['pseudo'],output['nom'],output['prenom'])
        time.sleep (1)
        socket.send_string(encoded)

def serverVerif(port="5557"):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print ("Running server on port: ", port)
    while(True) :
        message = socket.recv()
        decoded = jwtToken.dechiffre(message)
        time.sleep (1)
        socket.send_string(decoded)

if __name__ == "__main__":
    # Now we can run a few servers
    Process(target=serverDealer, args=(5556,)).start()
    Process(target=serverVerif, args=(5557,)).start()
