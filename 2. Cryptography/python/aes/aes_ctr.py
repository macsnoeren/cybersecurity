import json

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Encryption AES CTR mode - stream cipher
# CounTeR mode, defined in NIST SP 800-38A, section 6.5 and Appendix B. This mode turns 
# the block cipher into a stream cipher. Each byte of plaintext is XOR-ed with a byte taken 
# from a keystream: the result is the ciphertext. The keystream is generated by encrypting 
# a sequence of counter blocks with ECB.

data = b"Cybersecurity rulez!!"
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CTR)
ct_bytes = cipher.encrypt(data)
nonce = b64encode(cipher.nonce).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'nonce':nonce, 'ciphertext':ct})
print("Encrypted data:")
print(result)

# Decryption

json_input = result

try:
    b64 = json.loads(json_input)
    nonce = b64decode(b64['nonce'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ct)
    print("Decrypted data:")
    print("The message was: ", pt)

except (ValueError, KeyError):
    print("Incorrect decryption")

