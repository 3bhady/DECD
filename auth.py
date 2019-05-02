import Crypto.Hash as Crypto

class MAC:

	def __init__(self, key=""):
		self.key = key
		self.o_key_pad = key ^ [0x5c]

	def authenticate(self, message):
		if len(message.split(" ")) == 1:


	def hmac(self, message):
		data = self.key+
		Crypto.MD5(bytes(self.key,encoding="utf8"), )


