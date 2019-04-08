import zmq
import time
import sys
from  multiprocessing import Process

def server(port="5557"):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print ("Running server on port: ", port)
    while(True) :
        message = socket.recv()
        if(port==5556) :
            binary = message.content
            output = json.loads(binary)
            encoded = jwtToken.chiffre(output['pseudo'],output['nom'],output['prenom'])
            time.sleep (1)
            socket.send_string(encoded)
        elif :
            decoded = jwtToken.dechiffre(binary)
            time.sleep (1)
            socket.send_string(decoded)

if __name__ == "__main__":
    # Now we can run a few servers
    server_ports = range(5556,5558,1)
    for server_port in server_ports:
        Process(target=server, args=(server_port,)).start()
