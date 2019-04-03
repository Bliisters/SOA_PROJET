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
		port_push = "5556"
		context_push = zmq.Context()
		print("Connecting to server...")
		socket_push = context_push.socket(zmq.PUSH)
		try:
			socket_push.bind ("tcp://localhost:%s" % port)
		except:
			response = jsonify({'msg': 'Service Indisponible'})
			print(response)
			return response, 404

		if(confirmToken(request, socket)):
			response = "Good token : " + request.environ["HTTP_AUTHORIZATION"]
			print(response)
			return response
		else:
			response = jsonify({'msg': 'Wrong Token !'})
			print(response)
			return response, 404

	else:
		response = jsonify({'msg': 'No Token !'})
		return response, 404

def confirmToken(request, socket):
	try:
		socket.send("Hello", zmq.NOBLOCK)
		print("message send")
	except:
		print("no server")
		return False
	#  Get the reply.
	message = socket.recv()
	print("Received reply [", message, "]")
	if(request.environ["HTTP_AUTHORIZATION"] == message.decode('utf-8')):
		return True
	else:
		return False
	#return message


if __name__ == '__main__':
    print(app.url_map)

app.run()
