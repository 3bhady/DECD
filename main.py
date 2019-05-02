import socket
import threading
import modes
import sys


class Comm:
	# sock = []
	# is_server = True
	# server_address = ""
	# client_address = ""
	# conn = ""
	# conf = ""
	inbox = []
	mode = "ECB"

	def __init__(self, server="127.0.0.1", port=7171):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server_address = ('localhost', port)
			self.sock.connect((server, port))
			self.is_server = False
			print("* Switching to client mode")
			self.set_config()
			return

		except:
			self.is_server = True
			print("* Switching to server mode")
			self.sock = socket.socket()
			self.sock.bind(('', port))
			self.sock.listen(5)
			print("* Waiting for connector on port: ", port)
			self.conn, self.client_address = self.sock.accept()
			print("* Got connection from", self.client_address)

			# Receive the config from the client
			print("* Waiting for initial configuration from client")
			self.rec()
			self.mode = self.inbox.pop().decode()
			print("* Received preferred mode of operation from client: ", self.mode)

	def rec(self, loop=False):
		try:
			while True:
				if self.is_server:
					data = self.conn.recv(200)
				else:
					data = self.sock.recv(200)
				if data:
					self.inbox.reverse()
					self.inbox.append(data)
					self.inbox.reverse()
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
		if type(data) is str:
			data = bytes(data, encoding="utf8")

		if self.is_server:
			self.conn.sendall(data)
		else:
			self.sock.sendall(data)

	def set_config(self):
		print("* Please enter the DES configuration.")

		print("* Enter the number of the block mode.")
		print("> 1) ECB")
		print("> 2) CBC")
		print("> 3) CFB")
		print("> 4) CTR")
		print("> 5) OFB")
		config = input()
		config = str(config)
		if config == "1":
			self.mode = "ECB"
		elif config == "2":
			self.mode = "CBC"
		elif config == "3":
			self.mode = "CFB"
		elif config == "4":
			self.mode = "CTR"
		elif config == "5":
			self.mode = "OFB"
		else:
			print("* Invalid choice..")
			print("* Choosing the default mode ECB.")
			self.mode = "ECB"

		self.send(self.mode)

	def close_conn(self):
		# Clean up the connection
		print("* Closing connection.")
		print("* Closing connection..")
		print("* Closing connection...")
		self.conn.close()
		sys.exit(0)


# Create a communication object
comm = Comm()
crypt = modes.Crypt(_mode=comm.mode)
# Keep receiving messages infinitely
thread = threading.Thread(target=comm.rec, args=(True,))
thread.start()

while True:

	# TODO: add an option to exit the program and close opened thread
	print("* Type the number of what you want to do.")
	print("> 1) Send a message.")
	print("> 2) Check for available messages.")
	print("> 3) To go bye bye.")

	choice = input()
	choice = str(choice)
	if choice == "1":
		print("* Enter the message you want to send.")
		msg = input()
		c = crypt.encrypt(msg)
		print("* Encrypted text: ", c)
		comm.send(c)
	if choice == "2":
		if len(comm.inbox) == 0:
			print("* No new messages. Send a message to your friend and start a conversation :)")
		else:
			msg = comm.inbox.pop()
			print("* Encrypted message: ", msg)
			print("* Obtained Plaintext: ", crypt.decrypt(msg))
	if choice == "3":
		print("***********Bye Bye***********")
		try:
			comm.close_conn()
		finally:
			exit(0)
