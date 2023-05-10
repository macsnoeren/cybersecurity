# bcrypt is a password hashing function designed by Niels Provos and David Mazières.

from base64 import b64encode
from Cryptodome.Hash import SHA256
from Cryptodome.Protocol.KDF import bcrypt, bcrypt_check

password = b"my_password123"
b64pwd = b64encode(SHA256.new(password).digest())
bcrypt_hash = bcrypt(b64pwd, 12)

print("HASHED PASSWORD: " + bcrypt_hash.hex())

# Check the password - wrong password

password_to_test = b"test"
try:
    b64pwd = b64encode(SHA256.new(password_to_test).digest())
    bcrypt_check(b64pwd, bcrypt_hash)
    print("Correct password")

except ValueError:
    print("Incorrect password")

# Check the password - good password

password_to_test = b"my_password123"
try:
    b64pwd = b64encode(SHA256.new(password_to_test).digest())
    bcrypt_check(b64pwd, bcrypt_hash)
    print("Correct password")

except ValueError:
    print("Incorrect password")