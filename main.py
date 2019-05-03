import socket
import threading
import modes
import hashlib
import time


def hmac(plain_text, _key="S3CUR1TY"):
	plain_text = plain_text.strip()
	if _key == "":
		_key = "S3CUR1TY"
	block_size = 64
	if len(_key) > block_size:
		_key = hashlib.sha1(_key.encode()).hexdigest()
	while len(_key) < block_size:
		_key += "0"

	_key = bytes(_key, encoding="utf8")
	o_key_pad = "".join([chr(k ^ 0x5c) for k in _key])

	i_key_pad = "".join([chr(k ^ 0x36) for k in _key])

	return hashlib.md5(
		o_key_pad.encode()
		+
		hashlib.md5(
			i_key_pad.encode()
			+
			plain_text.encode()
		).hexdigest().encode()
	).hexdigest()


class Comm:
	inbox = []
	mode = "ECB"
	finish = False

	def __init__(self, server="127.0.0.1", port=5112):
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
			while True and not self.finish:
				if self.is_server:
					data = self.conn.recv(buff_size)
				else:
					data = self.sock.recv(buff_size)
				if data:
					self.inbox.reverse()
					self.inbox.append(data)
					self.inbox.reverse()
					if not loop:
						return
				else:
					print('No more data from', self.client_address)
					self.finish = True
					print("Connection Closed!")
					print("Bye Bye!")
					exit(0)
		except:
			self.finish = True
			print("Connection Closed!")
			print("Bye Bye!")
			exit(0)

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
		self.finish = True
		# Clean up the connection
		print("* Closing connection.")
		time.sleep(.300)
		print("* Closing connection..")
		time.sleep(.300)
		print("* Closing connection...")
		if self.is_server:
			self.conn.shutdown(0)
			self.conn.close()
		else:
			self.sock.shutdown(0)
			self.sock.close()
		exit(0)



buff_size = 1024

# Read Configurations from user:
print("* What Do you want to do?:")
print("> 1) Use default configurations.")
print("> 2) Enter custom configurations.")
# choice = input()
choice = "1"
if choice == "2":
	print("* Enter key for DES. Key must be 8 bytes.")
	key = input()
	if len(key) != 8:
		print("* Wrong key length. Choosing the default key")

	print("* Enter block size.")
	blk_size = input()
	if blk_size == "":
		print("* Choosing the default block size.")

	print("* Enter the IV.")
	iv = input()
	if iv == "":
		print("* Choosing the default IV.")

	print("* Enter the Counter value.")
	ctr = input()
	if ctr == "":
		print("* Choosing the default counter value.")

	print("* Enter the key for the HMAC.")
	hkey = input()
else:
	print("* Choosing the default configuration.")
	time.sleep(0.300)
	print("* Choosing the default configuration..")
	key = ""
	blk_size = ""
	iv = ""
	ctr = ""
	hkey = ""

# Create a communication object
comm = Comm()
crypt = modes.Crypt(_mode=comm.mode, _key=key, _iv=iv, _ctr=ctr, _blk_size=blk_size)
# Keep receiving messages infinitely
thread = threading.Thread(target=comm.rec, args=(True,), daemon=True)
thread.start()

while True:

	# TODO: add an option to exit the program and close opened thread
	print("* Type the number of what you want to do.")
	print("> 1) Send a message.")
	print("> 2) Check for available messages.")
	print("> 3) To go bye bye.")

	choice = input()
	if comm.finish:
		print("***********Bye Bye***********")
		try:
			comm.close_conn()
		finally:
			exit(0)
	choice = str(choice)
	if choice == "1":
		print("* Enter the message you want to send.")
		msg = input()
		msg_parts = [msg[i:i+int(buff_size/2)] for i in range(0, len(msg), int(buff_size/2))]
		for msg in msg_parts:
			c = crypt.encrypt(msg)
			print("* Encrypted text: ", c)
			mac = hmac(msg, hkey)
			print("* MAC: ", mac)
			comm.send(c + " ".encode("cp437") + mac.encode("cp437"))

	if choice == "2":
		if len(comm.inbox) == 0:
			print("* No new messages. Send a message to your friend and start a conversation :)")
		else:
			msg = comm.inbox.pop()
			try:
				enc_msg = msg[:-33]
				mac = msg[-32:].decode("cp437")
				if len(mac) != 32:
					print(0/0)
				dec_msg = crypt.decrypt(enc_msg)
				if mac == hmac(dec_msg, hkey):
					print("* Encrypted message: ", enc_msg)
					print("* Obtained MAC: ", mac)
					print("* Obtained Plaintext: ", dec_msg)
				else:
					print("* Wrong MAC !")
					print("* Possible tampering of the message")
			except:
				print("No MAC found.")

	if choice == "3":
		print("***********Bye Bye***********")
		try:
			comm.close_conn()
		finally:
			exit(0)
