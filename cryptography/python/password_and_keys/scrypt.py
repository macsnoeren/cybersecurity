from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

password = b'my super secret password'
salt = get_random_bytes(16)
key = scrypt(password, salt, 16, N=2**14, r=8, p=1)

print("KEY: " + key.hex())