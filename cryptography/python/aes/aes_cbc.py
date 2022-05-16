import json

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Encryption AES CBC mode - Block cipher
# Ciphertext Block Chaining, defined in NIST SP 800-38A, section 6.2. It is a mode of operation
# where each plaintext block gets XOR-ed with the previous ciphertext block prior to encryption.

data = b"Cybersecurity rulez!!"
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'iv':iv, 'ciphertext':ct})
print("Encrypted data:")
print(result)

# Example result:
# {"iv": "bWRHdzkzVDFJbWNBY0EwSmQ1UXFuQT09", "ciphertext": "VDdxQVo3TFFCbXIzcGpYa1lJbFFZQT09"}

# Decryption

json_input = result

try:
    b64 = json.loads(json_input)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("Decrypted data:")
    print("The message was: ", pt)

except (ValueError, KeyError):
    print("Incorrect decryption")

