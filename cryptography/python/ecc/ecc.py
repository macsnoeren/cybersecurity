import os

from Crypto.PublicKey import ECC

working_dir = os.path.dirname(os.path.realpath(__file__))

key = ECC.generate(curve='P-256')

f = open(working_dir + '\myprivatekey.pem','wt')
f.write(key.export_key(format='PEM'))
f.close()


f = open(working_dir + '\myprivatekey.pem','rt')
key = ECC.import_key(f.read())