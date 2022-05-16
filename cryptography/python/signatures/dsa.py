import os

from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

working_dir = os.path.dirname(os.path.realpath(__file__))

# Create a new DSA key - private/public key pari
key = DSA.generate(2048)
f = open(working_dir + "\mypublickey.pem", "wb")
f.write(key.public_key().export_key('PEM'))
f.close()

# Sign a message
message = b"Cybersecurity rulez!!"
hash_obj = SHA256.new(message)
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(hash_obj)
print("Signature: " + signature.hex())

# Load the public key
f = open(working_dir + "\mypublickey.pem", "r")
hash_obj = SHA256.new(message)
pub_key = DSA.import_key(f.read())
verifier = DSS.new(pub_key, 'fips-186-3')

# Verify the authenticity of the message
try:
    verifier.verify(hash_obj, signature)
    print("The message is authentic.")

except ValueError:
    print("The message is not authentic.")
