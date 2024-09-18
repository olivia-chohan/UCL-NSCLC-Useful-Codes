# Input hashed patient ID tag (0010,0020)
# Decrypt hashed ID to give NHS number

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys,binascii


def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = b"1234567891234567"#Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    #return base64.b64encode(data).decode("latin-1") if encode else data
    return data.hex()

def decrypt(key, source, decode=True):
    if decode:
        #source =  base64.b64decode(source)#.encode("latin-1"))
        source =  binascii.unhexlify(source)
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding

### ENSURE PASSWORD IS CORRECT ###
password  = "find password on NHS computer"
password  = password.encode()

### HASHED NHS ID GOES HERE ###
data      = '31323334353637383931323334353637329d80d3348e1d80ce9e00b851546a00'
data      = data.encode()
decrypted = decrypt(password, data)

print("dec:  {}".format(decrypted))
