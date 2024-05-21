import os
import rsa
import base64

def set_message():
    with open('main/public-2048.pem', mode='rb') as file:
        keydata = file.read()

    key = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)

    message = 'hello Bob!'.encode('utf8')
    crypto = rsa.encrypt(message, key)

    enc_b64 = base64.b64encode(crypto)
    print(enc_b64)

    return enc_b64

def get_message(enc_b64):
    with open('main/key-2048.pem', mode='rb') as file:
        keydata = file.read()

    key = rsa.PrivateKey._load_pkcs1_pem(keydata)

    enc = base64.b64decode(enc_b64)

    plain = rsa.decrypt(enc, key)

    print(plain)

get_message( set_message() )

enc1 = '''o/FcN2b+TwIbe29Qt2KkMLB17yzYmOOp7OmRm73Iz7Bi1HkhdOIlU2/PV1omT9f98vEUbC8Nb+Xf0o0MiMcH3YgQ4V7n43CyqyVaFSM++h+6IITk6vjrXR2Qun2g25c7atXyoTNf22uYC3yvEJQASu7Tu47+7puQly8DBLlJBeM8+H+cRpy7W7NCZWEuFdiCc5CifQlgFEGBIv+Dh+vwuA9E4ud4or9iJ+ZXzm6zkI8TjotvPVd4+HYNxwCovmtHwQoxqTzLgmO2Cde5Lz/x3jQJtu/W9h0vcWz8mSnHY+TQcKoSkChwVtif0g6ceyGy0aK6sEljBsycmyiaGSwwSw=='''
enc2 = '''gjJgvKVZZ/3GWpJmzHVLjZL658pW0W9diMAFU2Oh9K+hObHzbS2DblaFxAZhqoOFnfedrs0Ty35BRC+xFoLOrmnwyM6M45O7fIvf8u56ZSvnYl3Q0PlqWc3KbZBmTKYSiN0pkmcoRKbahtr3rPSXM2t3q29uwc2qbyGxxLlp3ROnE26525VDnefST9tRGiflZQeCBRXBMagsW0EnutZgXpTnHfujK8ZdCFbiDFkk0lEn4ILgtTv4iE3Ge9kwbLWtyjWTSw8WdvdCgQlIMKGvYyjjZkMSAF81CMk/d4lC7vlvSZtPJrbnqXkVqyXIlLiZGKypyD5D9nd5MLSa2vmosw=='''
enc3 = 'iyldkxTKwNm7mhtdY/7epg8qK0vGGNrD5jg+U3V8umbEQJxmtoUYtFPdKTlxoeNQEGxMDCpaKclW9v9RGz6HrXAnTS/11vGdhTEYI2ljrmv3TXGn85mo4DKKNX6kHH91zn8dLFDTe7mw0gUfJMCFPghBT3YnEyCzN2EqszLAVRRwgUFYbeys8K0kP2Ox32CZi3u4HsIJ7oIgC1gaJZTXGupUX4zGcC1AJ00l0kev+CEoceZSGRC82KuJ3waCGY3vrvCet/+4Pgc6yG4HhbT0EF1j5q4I+es4JN6tU+At3Y36iqttGkGPXT6vw3If7G/q0n1LuA7xJVxkCJZiXNit+Q=='

get_message(enc1)
get_message(enc2)
get_message(enc3)
