└─$ cat given.py 
from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

pride = "".join(choice(ascii_letters + digits) for _ in range(16))
p = getPrime(16)
q = getPrime(16)
n = p * q
e = 65537
d = inverse(e, (p - 1) * (q - 1))

c = pow(bytes_to_long(pride.encode()), e, n)
print(f"{p = }")
print(f"{q = }")
print(f"{c = }")
print(f"{d = }")

print("vainglory?")
vainglory = input("> ").strip()

if vainglory == pride:
    print("Conquered!")
    with open("/challenge/flag.txt") as f:
        print(f.read())
else:
    print("Hubris!")

