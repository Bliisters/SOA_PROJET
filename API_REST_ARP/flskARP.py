from flask import Flask, jsonify, request
import zmq
import sys
app = Flask(__name__)

"""
ARP Microservices
"""

@app.route('/api', methods=['GET'])
def my_microservice():
	print(request)
	print(request.environ)
	print(request.headers)

	if('Authorization' in request.headers):
		port = "5557"
		context = zmq.Context()
		print("Connecting to server...")
		socket = context.socket(zmq.REQ)
		socket.connect ("tcp://localhost:%s" % port)

		if(confirmToken(request, socket)):
			response = jsonify("Ressource : https://www.youtube.com/watch?v=JUsW-1mn-aM ")
			print(response)
			return response, 200
		else:
			response = jsonify({'msg': 'Wrong Token !'})
			print(response)
			return response, 404

	else:
		response = jsonify({'msg': 'No Token !'})
		return response, 404

def confirmToken(request, socket):
	try:
		socket.send_string(request.environ["HTTP_AUTHORIZATION"], zmq.NOBLOCK)
		print("message send")
	except:
		print("no server")
		return False
	#  Get the reply.
	message = socket.recv()
	print("Received reply [", message, "]")
	if(message.decode('utf-8')=="True"):
		return True
	else:
		return False
	#return message


if __name__ == '__main__':
    print(app.url_map)

app.run(host='127.0.0.1',port='5001')
