import json

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Encryption AES ECB mode - block cipher
# Electronic CodeBook. The most basic but also the weakest mode of operation. Each 
# block of plaintext is encrypted independently of any other block.

data = b"Cybersecurity rulez!!"
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'ciphertext':ct})
print("Encrypted data:")
print(result)

# Example result:
# {"iv": "bWRHdzkzVDFJbWNBY0EwSmQ1UXFuQT09", "ciphertext": "VDdxQVo3TFFCbXIzcGpYa1lJbFFZQT09"}

# Decryption

json_input = result

try:
    b64 = json.loads(json_input)
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("Decrypted data:")
    print("The message was: ", pt)

except (ValueError, KeyError):
    print("Incorrect decryption")

