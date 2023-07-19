from hashlib import sha256
from Crypto.Cipher import AES
from base64 import standard_b64decode
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad, unpad

def long_to_base64(n):
    return standard_b64encode(long_to_bytes(n)).decode()

def encrypt(cipher, msg):
    return standard_b64encode(cipher.encrypt(pad(msg, 16))).decode()

def base64_to_long(e):
    return bytes_to_long(standard_b64decode(e))

def decrypt(cipher, e):
    return unpad(cipher.decrypt(standard_b64decode(e)), 16)

p = 2272978429
g = 2
A = 1116819144
b = 620620105

shared = pow(A, b, p)
shared = sha256(long_to_bytes(shared)).digest()
cipher = AES.new(shared, AES.MODE_ECB)

cmd_1 = "6+lX9noxcSrRAnTbQMYdPg=="
response_1 = "GkSU2VwQyFe5Jt0Vd0cfxw=="
cmd_2 = "15AsYtxN//27mQ/lDUAJOjApyeXQx65dFso1oP7w8Qw="
response_2 = "TMxn+S2kBNd/4YsXYhtH0qgvBmUZiArgyTNOCqPsuFQOwcAo4SjQ4T4K14JvHvBX"

print(decrypt(cipher, cmd_1))
print(decrypt(cipher, cmd_2))
print(decrypt(cipher, response_1))
print(decrypt(cipher, response_2))

# def handle(cmd):            
#     cmd = decrypt(cipher, j['rpc'])
#     return {
#         'return': encrypt(cipher, subprocess.check_output(cmd))
#     }


# c2utils.start_listener(handle)
