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
		if(confirmToken(request)):
			response = "Good token : " + request.environ["HTTP_AUTHORIZATION"]
			print(response)
			return response
		else:
			response = jsonify({'msg': 'Wrong Token !'})
			return response, 404
		
	else:
		response = jsonify({'msg': 'No Token !'})
		return response, 404
		
def confirmToken(request):
	port = "5556"
	context = zmq.Context()
	print("Connecting to server...")
	socket = context.socket(zmq.REQ)
	socket.connect ("tcp://localhost:%s" % port)
	socket.send_string("Hello")
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

