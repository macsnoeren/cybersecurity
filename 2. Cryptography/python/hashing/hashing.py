from Crypto.Hash import MD5, SHA256, SHA512 # pip install pycryptodome

md5 = MD5.new(data=b'This is my message!')
print("MD5:    " + md5.hexdigest())

sha256 = SHA256.new(data=b'This is my message!')
print("SHA256: " + sha256.hexdigest())

sha512 = SHA512.new(data=b'This is my message!')
print("SHA512: " + sha512.hexdigest())

# For larger chunks of data
hash_object1 = SHA256.new(data=b'This')
hash_object1.update(b' is ')
hash_object1.update(b'my message!')
print("SHA256: " + hash_object1.hexdigest())
