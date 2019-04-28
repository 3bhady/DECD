from Crypto.Cipher import DES
import modes
import time
import matplotlib.pyplot as plt




#########################################################################
#cryp = modes.Crypt(_mode="ECB")
#cryp = modes.Crypt(_mode="CBC")
#cryp = modes.Crypt(_mode="CFB")
#cryp = modes.Crypt(_mode="OFB")
cryp = modes.Crypt(_mode="CTR")

msg = ""
enc_time = []
dec_time = []
blocks = 100
tot = 20
for i in range (1,blocks):
    print(blocks," : ",i)
    msg += "ABCDEFGH"
#    print("Message : ",msg)
    
    x = 0
    y = 0
    for j in range (1,tot):
        start = time.time()
        ctxt = cryp.encrypt(msg)
        end = time.time()
        x = x + end - start

        
        start = time.time()
        ptxt = cryp.decrypt(ctxt)
        end = time.time()
        y = y + end - start

    enc_time.append([i, x/tot])
    dec_time.append([i, x/tot])




x = [a for (a,b) in enc_time]
y = [b for (a,b) in enc_time]
plt.plot(x,y)
plt.show()


x = [a for (a,b) in dec_time]
y = [b for (a,b) in dec_time]
plt.plot(x,y)
plt.show()
