from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

password = b'my super secret password'
salt = get_random_bytes(16)
keys = PBKDF2(password, salt, 64, count=1000000, hmac_hash_module=SHA512)
key1 = keys[:32]
key2 = keys[32:]

print("Two 32 bit keys are created:")
print("key 1: " + key1.hex())
print("key 2: " + key2.hex())
