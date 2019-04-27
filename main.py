import socket
import threading
import os
from Crypto.Cipher import DES

# port = 7777


def pad(s):
	while len(s) % 8:
		s += " "
	return s


def encrypt(key, plaintext):

	cipher = DES.new(key, DES.MODE_ECB)
	c = cipher.encrypt(pad(plaintext))
	return c
# m = cipher.decrypt(c)
# print(m)


class Comm:

	sock = []
	is_server = True
	server_address = ""
	client_address = ""
	conn = ""
	conf = ""
	inbox = []

	def __init__(self, server="127.0.0.1", port=7777):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server_address = ('localhost', port)
			self.sock.connect((server, port))
			self.is_server = False
			print("Switching to client mode")

			# Get the config set it and send it to the server
			print("Please enter the DES configuration")
			config = input()
			self.send(config)
			return
		except:
			self.is_server = True
			print("Switching to server mode")
			self.sock = socket.socket()
			self.sock.bind(('', port))
			self.sock.listen(5)
			print("Waiting for connector on port: ", port)
			self.conn, self.client_address = self.sock.accept()
			print("Got connection from", self.client_address)

			# Receive the config from the client
			print("Waiting for initial configuration from client")
			self.rec()

			# Remove the configuration message from the inbox
			self.inbox.pop()

	def rec(self, loop=False):
		try:
			while True:
				if self.is_server:
					data = self.conn.recv(200)
				else:
					data = self.sock.recv(200)
				if data:
					self.inbox.append(data)
					if not loop:
						break
					# conn.sendall(data)
				else:
					print('No more data from', self.client_address)
					break
		except:
			# Clean up the connection
			print("closing connection")
			self.conn.close()

	def send(self, data):
		if self.is_server:
			self.conn.sendall(bytes(data, encoding="utf8"))
		else:
			self.sock.sendall(bytes(data, encoding="utf8"))

	# def set_config(self,config):


comm = Comm()
threading.Thread(target=comm.rec, args=(True,)).start()
while True:
	print("Enter 1 to send a message")
	print("Enter 2 to check for available messages")
	choice = input()
	choice = str(choice)
	if choice == "1":
		print("Enter the message you want to send")
		msg = input()
		comm.send(msg)
	if choice == "2":
		if len(comm.inbox) == 0:
			print("No new messages")
		else:
			print(comm.inbox.pop())
