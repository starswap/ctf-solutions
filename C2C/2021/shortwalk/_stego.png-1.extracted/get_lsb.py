bytes_out = b""
with open("notes.wav", "rb") as f:
    curr = 7 
    res = 0
    while (byte := f.read(1)):
        b = int.from_bytes(byte)
#         print(b)
        lsb = b % 2
        res |= lsb << curr
        curr += 1
#      print(res)
        if curr == 8:
            curr = 0
#           print(res)
            bytes_out += res.to_bytes(1)
            res = 0
print(bytes_out) 

