from Crypto.Cipher import DES
key = b'ABCDEFGH'

def padding(ptxt,blk_size):
    x = len(ptxt)%blk_size
    if x > 0:
        x = blk_size - x
    while x > 0:
        x= x-1
        ptxt +=' '
    return ptxt

#############################################################################
def enc_ecb(ptxt, blk_size):
    ptxt = padding(ptxt,blk_size)
    i = 0
    ctxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ptxt):
        block = ptxt[i:i+blk_size]
        i = i+ blk_size
        pblk = block
        cblk = cipher.encrypt(pblk)
        ctxt += cblk.decode('cp437')

    return ctxt.encode('cp437')


#############################################################################
def dec_ecb(ctxt, blk_size):
    i = 0
    ptxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ctxt):
        block = ctxt[i:i+blk_size]
        i = i + blk_size
        cblk = block
        pblk = cipher.decrypt(cblk)
        ptxt += pblk.decode('cp437')

    return ptxt


#############################################################################
def enc_cbc(IV, ptxt, blk_size):
    ptxt = padding(ptxt,blk_size)
    i = 0
    ctxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ptxt):
        block = ptxt[i:i+blk_size]
        i = i + blk_size
        pblk = bytes(blk ^ iv for blk, iv in zip(block.encode('cp437'), IV))
        cblk = cipher.encrypt(pblk)
        ctxt += cblk.decode('cp437')
        IV = cblk

    return ctxt.encode('cp437')


#############################################################################
def dec_cbc(IV, ctxt, blk_size):
    i = 0
    ptxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ctxt):
        block = ctxt[i:i+blk_size]
        i = i + blk_size
        cblk = block
        pblk = cipher.decrypt(cblk)
        pblk = bytes(blk ^ iv for blk , iv in zip(pblk, IV))
        ptxt += pblk.decode('cp437')
        IV = cblk

    return ptxt

#############################################################################
def enc_cfb(IV, ptxt, blk_size):
    ptxt = padding(ptxt,blk_size)
    i = 0
    ctxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ptxt):
        block = ptxt[i:i+1]
        pblk = block
        i = i + 1
        cblk = cipher.encrypt(IV)
        cblk = bytes(  c_blk ^ p_blk for c_blk , p_blk in zip(cblk[:1],pblk.encode('cp437')))
        ctxt += cblk.decode('cp437')
        IV = IV[1:] + cblk

    return ctxt.encode('cp437')


#############################################################################
def dec_cfb(IV, ctxt, blk_size):
    i = 0
    ptxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ctxt):
        block = ctxt[i:i+1]
        cblk = block
        i = i + 1
        pblk = cipher.encrypt(IV)
        pblk = bytes(  p_blk ^ c_blk for p_blk , c_blk in zip(pblk[:1],cblk))
        ptxt += pblk.decode('cp437')
        IV = IV[1:] + cblk

    return ptxt


#############################################################################
def enc_ofb(IV, ptxt, blk_size):
    ptxt = padding(ptxt,blk_size)
    i = 0
    ctxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ptxt):
        block = ptxt[i:i+1]
        pblk = block
        i = i + 1
        cblk = cipher.encrypt(IV)
        IV = IV[1:] + cblk[:1]
        cblk = bytes(  c_blk ^ p_blk for c_blk , p_blk in zip(cblk[:1],pblk.encode('cp437')))
        ctxt += cblk.decode('cp437')

    return ctxt.encode('cp437')



#############################################################################
def dec_ofb(IV, ctxt, blk_size):
    i = 0
    ptxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ctxt):
        block = ctxt[i:i+1]
        cblk = block
        i = i + 1
        pblk = cipher.encrypt(IV)
        IV = IV[1:] + pblk[:1]
        pblk = bytes(  p_blk ^ c_blk for p_blk , c_blk in zip(pblk[:1],cblk))
        ptxt += pblk.decode('cp437')

    return ptxt


#############################################################################
def enc_ctr(CTR, ptxt, blk_size):
    ptxt = padding(ptxt,blk_size)
    i = 0
    ctxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ptxt):
        block = ptxt[i:i+blk_size]
        i = i+ blk_size
        pblk = block
        cblk = cipher.encrypt(CTR)
        cblk = bytes(p_blk ^ c_blk for p_blk, c_blk in zip(pblk.encode('cp437'), cblk))
        ctxt += cblk.decode('cp437')
        update = (str(int(CTR.decode('cp437'))+1).zfill(8)).encode('cp437')

    return ctxt.encode('cp437')



#############################################################################
def dec_ctr(ctr, ctxt, blk_size):
    i = 0
    ptxt = ""
    cipher = DES.new(key, DES.MODE_ECB)
    while i < len(ctxt):
        block = ctxt[i:i+blk_size]
        i = i+ blk_size
        cblk = block
        pblk = cipher.encrypt(CTR)
        pblk = bytes(c_blk ^ p_blk for c_blk, p_blk in zip(cblk, pblk))
        ptxt += pblk.decode('cp437')
        update = (str(int(CTR.decode('cp437'))+1).zfill(8)).encode('cp437')

    return ptxt


#############################################################################
def prep(msg):
    ptxt = ""
    for c in msg:
        ptxt +=('{0:08b}'.format(ord(c)))
    return ptxt




'''
key = b'ABCDEFGH'
cipher = DES.new(key, DES.MODE_ECB)
plaintext = b'ABCDEFGH'
msg = cipher.encrypt(plaintext)
print(msg)
msg = cipher.decrypt(msg)
print(msg)


print("choose the blocking mode:")
print("(1) ECB\n(2) CBC\n(3) CFB\n(4) OFB\n(5) CTR")
mode = input("blocking mode number : ")
if mode == "1":
    ecb(8)
elif mode == "2":
    cbc(8)
elif mode == "3":
    cfb(8)
elif mode == "4":
    ofb(8)
elif mode == "5":
    ctr(8)
else:
    print("wrong choice !\n")

ptxt = msg #prep(msg)
print("plain text : ",ptxt)
'''    



msg = "A B C Hello World"
IV  = b'STUVWXYZ'
CTR = b'00000009'
blk_size = 8

print("MESSAGE : ",msg)


ctxt = enc_ecb(msg, blk_size)
print("cipher text (ECB) : ",ctxt)
ptxt = dec_ecb(ctxt,blk_size)
print("cipher text (ECB) : ",ptxt)


ctxt = enc_cbc(IV, msg, blk_size)
print("cipher text (CBC) : ",ctxt)
ptxt = dec_cbc(b'STUVWXYZ',ctxt,blk_size)
print("cipher text (CBC) : ",ptxt)


ctxt = enc_cfb(IV, msg, blk_size)
print("cipher text (CFB) : ",ctxt)
ptxt = dec_cfb(b'STUVWXYZ',ctxt,blk_size)
print("cipher text (CFB) : ",ptxt)


ctxt = enc_ofb(IV, msg, blk_size)
print("cipher text (OFB) : ",ctxt)
ptxt = dec_ofb(b'STUVWXYZ',ctxt,blk_size)
print("cipher text (OFB) : ",ptxt)


ctxt = enc_ctr(CTR, msg, blk_size)
print("cipher text (CTR) : ",ctxt)
ptxt = dec_ctr(b'00000009',ctxt,blk_size)
print("cipher text (CTR) : ",ptxt)



