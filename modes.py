from Crypto.Cipher import DES



def padding(ptxt, blk_size):
    x = len(ptxt) % blk_size
    if x > 0:
    	x = blk_size - x
    while x > 0:
        x = x - 1
        ptxt += ' '
    return ptxt


class Crypt:
#	iv = b'STUVWXYZ'
#	ctr = b'00000009'
#	blk_size = 8
#	key = b'ABCDEFGH'
#	mode = "ECB"

    def __init__(self, _key="ABCDEFGH", _mode="ECB", _blk_size=8, _iv="STUVWXYZ", _ctr="00000009"):
    	self.key = bytes(_key, encoding="utf8")
    	self.iv = bytes(_iv, encoding="utf8")
    	self.ctr = bytes(_ctr, encoding="utf8")
    	self.blk_size = _blk_size
    	self.mode = _mode

    def encrypt(self, ptxt):

    	if self.mode == "ECB":
    	    return self.enc_ecb(ptxt)
    	if self.mode == "CBC":
    	    return self.enc_cbc(ptxt)
    	if self.mode == "CFB":
    	    return self.enc_cfb(ptxt)
    	if self.mode == "CTR":
    	    return self.enc_ctr(ptxt)
    	if self.mode == "OFB":
            return self.enc_ofb(ptxt)

    def decrypt(self, ctxt):
    	if self.mode == "ECB":
    	    return self.dec_ecb(ctxt)
    	if self.mode == "CBC":
    	    return self.dec_cbc(ctxt)
    	if self.mode == "CFB":
    	    return self.dec_cfb(ctxt)
    	if self.mode == "CTR":
    	    return self.dec_ctr(ctxt)
    	if self.mode == "OFB":
    	    return self.dec_ofb(ctxt)

    def enc_ecb(self, ptxt):
    	ptxt = padding(ptxt, self.blk_size)
    	i = 0
    	ctxt = ""
    	cipher = DES.new(self.key, DES.MODE_ECB)
    	while i < len(ptxt):
    	    block = ptxt[i:i + self.blk_size]
    	    i = i + self.blk_size
    	    pblk = block
    	    cblk = cipher.encrypt(pblk)
    	    ctxt += cblk.decode('cp437')

    	return ctxt.encode('cp437')

    def dec_ecb(self, ctxt):
    	i = 0
    	ptxt = ""
    	cipher = DES.new(self.key, DES.MODE_ECB)
    	while i < len(ctxt):
    	    block = ctxt[i:i + self.blk_size]
    	    i = i + self.blk_size
    	    cblk = block
    	    pblk = cipher.decrypt(cblk)
    	    ptxt += pblk.decode('cp437')

    	return ptxt

    def enc_cbc(self, ptxt):
        iv = self.iv
        ptxt = padding(ptxt, self.blk_size)
        i = 0
        ctxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ptxt):
            block = ptxt[i:i + self.blk_size]
            i = i + self.blk_size
            pblk = bytes(blk ^ iv for blk, iv in zip(block.encode('cp437'), iv))
            cblk = cipher.encrypt(pblk)
            ctxt += cblk.decode('cp437')
            iv = cblk
            
        return ctxt.encode('cp437')

    def dec_cbc(self, ctxt):
        i = 0
        iv = self.iv
        ptxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ctxt):
            block = ctxt[i:i + self.blk_size]
            i = i + self.blk_size
            cblk = block
            pblk = cipher.decrypt(cblk)
            pblk = bytes(blk ^ iv for blk, iv in zip(pblk, iv))
            ptxt += pblk.decode('cp437')
            iv = cblk
            
        return ptxt

    def enc_cfb(self, ptxt):
        ptxt = padding(ptxt, self.blk_size)
        i = 0
        iv = self.iv
        ctxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ptxt):
            block = ptxt[i:i + 1]
            pblk = block
            i = i + 1
            cblk = cipher.encrypt(iv)
            cblk = bytes(c_blk ^ p_blk for c_blk, p_blk in zip(cblk[:1], pblk.encode('cp437')))
            ctxt += cblk.decode('cp437')
            iv = iv[1:] + cblk
            
        return ctxt.encode('cp437')

    def dec_cfb(self, ctxt):
        i = 0
        iv = self.iv
        ptxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ctxt):
            block = ctxt[i:i + 1]
            cblk = block
            i = i + 1
            pblk = cipher.encrypt(iv)
            pblk = bytes(p_blk ^ c_blk for p_blk, c_blk in zip(pblk[:1], cblk))
            ptxt += pblk.decode('cp437')
            iv = iv[1:] + cblk
            
        return ptxt

    def enc_ofb(self, ptxt):
        ptxt = padding(ptxt, self.blk_size)
        i = 0
        iv = self.iv
        ctxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ptxt):
            block = ptxt[i:i + 1]
            pblk = block
            i = i + 1
            cblk = cipher.encrypt(iv)
            iv = iv[1:] + cblk[:1]
            cblk = bytes(c_blk ^ p_blk for c_blk, p_blk in zip(cblk[:1], pblk.encode('cp437')))
            ctxt += cblk.decode('cp437')
            
        return ctxt.encode('cp437')

    def dec_ofb(self, ctxt):
        i = 0
        iv = self.iv
        ptxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ctxt):
            block = ctxt[i:i + 1]
            cblk = block
            i = i + 1
            pblk = cipher.encrypt(iv)
            iv = iv[1:] + pblk[:1]
            pblk = bytes(p_blk ^ c_blk for p_blk, c_blk in zip(pblk[:1], cblk))
            ptxt += pblk.decode('cp437')
            
        return ptxt

    def enc_ctr(self, ptxt):
        ptxt = padding(ptxt, self.blk_size)
        i = 0
        ctr = self.ctr
        ctxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ptxt):
            block = ptxt[i:i + self.blk_size]
            i = i + self.blk_size
            pblk = block
            cblk = cipher.encrypt(ctr)
            cblk = bytes(p_blk ^ c_blk for p_blk, c_blk in zip(pblk.encode('cp437'), cblk))
            ctxt += cblk.decode('cp437')
            ctr = (str(int(ctr.decode('cp437')) + 1).zfill(8)).encode('cp437')
        
        return ctxt.encode('cp437')

    def dec_ctr(self, ctxt):
        i = 0
        ctr = self.ctr
        ptxt = ""
        cipher = DES.new(self.key, DES.MODE_ECB)
        while i < len(ctxt):
            block = ctxt[i:i + self.blk_size]
            i = i + self.blk_size
            cblk = block
            pblk = cipher.encrypt(ctr)
            pblk = bytes(c_blk ^ p_blk for c_blk, p_blk in zip(cblk, pblk))
            ptxt += pblk.decode('cp437')
            ctr = (str(int(ctr.decode('cp437')) + 1).zfill(8)).encode('cp437')
            
        return ptxt

#
# msg = "A B C Hello World"
# IV = b'STUVWXYZ'
# CTR = b'00000009'
# blk_size = 8
# key = b'ABCDEFGH'
# print("MESSAGE : ", msg)
#
# ctxt = enc_ecb(key, msg, blk_size)
# print("cipher text (ECB) : ", ctxt)
# ptxt = dec_ecb(key, ctxt, blk_size)
# print("cipher text (ECB) : ", ptxt)
#
# ctxt = enc_cbc(key, IV, msg, blk_size)
# print("cipher text (CBC) : ", ctxt)
# ptxt = dec_cbc(key, IV, ctxt, blk_size)
# print("cipher text (CBC) : ", ptxt)
#
# ctxt = enc_cfb(key, IV, msg, blk_size)
# print("cipher text (CFB) : ", ctxt)
# ptxt = dec_cfb(key, IV, ctxt, blk_size)
# print("cipher text (CFB) : ", ptxt)
#
# ctxt = enc_ofb(key, IV, msg, blk_size)
# print("cipher text (OFB) : ", ctxt)
# ptxt = dec_ofb(key, IV, ctxt, blk_size)
# print("cipher text (OFB) : ", ptxt)
#
# ctxt = enc_ctr(key, CTR, msg, blk_size)
# print("cipher text (CTR) : ", ctxt)
# ptxt = dec_ctr(key, CTR, ctxt, blk_size)
# print("cipher text (CTR) : ", ptxt)
