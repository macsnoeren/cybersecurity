from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes

password = b'my super secret password'
salt = get_random_bytes(16)
key = scrypt(password, salt, 32, N=2**14, r=8, p=1)

print("SALT: " + salt.hex())
print("KEY : " + key.hex())

key2 = scrypt(password, salt, 32, N=2**14, r=8, p=1)
print("VER : " + key2.hex())