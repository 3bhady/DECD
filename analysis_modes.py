import modes
import time
import matplotlib.pyplot as plt


#########################################################################
cryp = modes.Crypt(_mode="ECB",_blk_size=8)
# cryp = modes.Crypt(_mode="CBC",_blk_size=80)
# cryp = modes.Crypt(_mode="CFB",_blk_size=32)
# cryp = modes.Crypt(_mode="OFB",_blk_size=32)
# cryp = modes.Crypt(_mode="CTR",_blk_size=800)

msg = ""
enc_time = []
dec_time = []
blocks = 1000
tot = 20
for i in range(0, blocks, 10):
    print(blocks, " : ", i)
    msg += "ABCDEFGH"
#    print("Message : ",msg)

    x = 0
    y = 0
    for j in range(0, tot):
        start = time.time()
        ctxt = cryp.encrypt(msg)
        end = time.time()
        x = x + end - start

        start = time.time()
        ptxt = cryp.decrypt(ctxt)
        end = time.time()
        y = y + end - start

    enc_time.append([i, x/tot])
    dec_time.append([i, y/tot])


x = [a for (a, b) in enc_time]
y = [b for (a, b) in enc_time]
plt.plot(x, y)
plt.show()


x = [a for (a, b) in dec_time]
y = [b for (a, b) in dec_time]
plt.plot(x, y)
plt.show()
