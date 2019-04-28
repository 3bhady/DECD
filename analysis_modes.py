from Crypto.Cipher import DES
import modes
import time
import matplotlib.pyplot as plt




#########################################################################
cryp = modes.Crypt(_mode="ECB")
#cryp = modes.Crypt(_mode="CBC")
#cryp = modes.Crypt(_mode="CFB")
#cryp = modes.Crypt(_mode="OFB")
#cryp = modes.Crypt(_mode="CTR")

msg = ""
bits_time = []
for i in range (1,1000):
    print(i)
    msg += "ABCDEFGH"
#    print("Message : ",msg)
    
    start = time.time()
    ctxt = cryp.encrypt(msg)
    end = time.time()
    bits_time.append([i, end-start])
    
#    print("Cipher text : ",ctxt)
    ptxt = cryp.decrypt(ctxt)
#    print("Plain text : ",ptxt)


x = [a for (a,b) in bits_time]
y = [b for (a,b) in bits_time]
plt.plot(x,y)
plt.show()





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
