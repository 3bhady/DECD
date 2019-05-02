import socket
port = 7777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', port)
sock.connect(server_address)
try:

	# Send data
	message = 'This is the message.  It will be repeated.'
	print('sending ', message)
	sock.sendall(bytes(message, encoding='utf8'))

	# Look for the response
	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected:
		data = sock.recv(16)
		amount_received += len(data)
		print('received ', data)

finally:
	print('closing socket')
	sock.close()
