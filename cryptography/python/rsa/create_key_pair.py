import os
from Crypto.PublicKey import RSA

working_dir = os.path.dirname(os.path.realpath(__file__))


key = RSA.generate(2048)
f = open(working_dir + '\mykey.pem','wb')
f.write(key.export_key('PEM'))
f.close()

f = open(working_dir + '\mypublickey.pem','wb')
f.write(key.public_key().export_key('PEM'))
f.close()


# Get the key from the file!
f = open(working_dir + '\mykey.pem','r')
key = RSA.import_key(f.read())
print("PUBLIC KEY: " + key.public_key().export_key().hex())
print("\nPRIVATE KEY: " + key.export_key().hex())
