import os

# not yet finished!
# https://pycryptodome.readthedocs.io/en/latest/src/protocol/ss.html

from binascii import hexlify, unhexlify
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.SecretSharing import Shamir

working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)

key = get_random_bytes(16)
print("Key: %s" % (hexlify(key)))
shares = Shamir.split(2, 5, key)
for idx, share in shares:
    print("Index #%d: %s" % (idx, hexlify(share)))

with open("./clear.txt", "rb") as fi, open("./enc.txt", "wb") as fo:
    cipher = AES.new(key, AES.MODE_EAX)
    ct, tag = cipher.encrypt(fi.read()), cipher.digest()
#    fo.write(nonce + tag + ct)
    fo.write(tag + ct)

# Als twee personen bij elkaar komen kunnen ze het geheim ontrafelen

in_str = int( input("Enter index and share separated by comma: ") )
idx, share = [ s.strip() for s in in_str.split(",") ]
shares.append((idx, unhexlify(share)))
key = Shamir.combine(shares)

with open("enc.txt", "rb") as fi:
    tag = [ fi.read(16) for x in range(1) ]
    cipher = AES.new(key, AES.MODE_EAX)
    try:
        result = cipher.decrypt(fi.read())
        cipher.verify(tag)
        with open(working_dir + "\clear2.txt", "wb") as fo:
            fo.write(result)
    except ValueError:
        print("The shares were incorrect")