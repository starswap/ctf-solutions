import binascii
import itertools

def solve_msg(msg):
    bytes_of_msg = binascii.unhexlify(msg)
    all_poss = []
    for offset in range(16):
        poss = []
        for kb in range(256):
            ok = True
            for block_start in range(0, len(bytes_of_msg) , 16):
                if block_start + offset < len(bytes_of_msg):
                    decoded = bytes_of_msg[block_start + offset] ^ kb
                    if not(decoded == 0x20 or 0x61 <= decoded <= 0x7a or 0x41 <= decoded <= 0x5a):
                        ok = False
            if ok:
                poss.append(kb)
        all_poss.append(poss)  
    return all_poss

msg1 = "734d7d95f6436cdf7f723f751c4b82fc6f4c3084fe527d8d3b65217d114782ee6051309efe576cdf7f643b661a4582ea64417798ef0160c32b7521710c5482ee714d7c9cbb4760c1333032731a00c5f47344309cf2527dc83130247c1643cabd6c477e95e20161c82d7573631a52c7bd725c7580bb4e67c126303e750d4b82f16e5f3092fe4668c37f63267a"
msg2 = "62496295bb5561c82d7573671a4cc4bd6d4d7194bb4666db3a623d340c4dc3f16d086485e94f29c93a733a701a00c5ef6e5d7e94bb5566ca3a643b710d00cefc6f4f6591fc4429d937753d340f49c1e9745a75d0f84e65c97f7c36605f54c3f16a087891e8017edf366436341945c7e9214e7f85e9017ec53a6236341052c6f8730844a2ce6429da37753d340c45c3"

solve_msg(msg1)

final_poss = []
for (first, second) in zip(solve_msg(msg1), solve_msg(msg2)):
    final_poss.append(first if len(first) < len(second) else second)

if not(all(map(lambda x : len(x) == 1, final_poss))):
    print(final_poss)
else:
    FLAG = binascii.unhexlify("476451b7e05939df0071627a0b7fc5ad314c4f95f5117cca376d")
    result = ''
    key = [*itertools.chain(*final_poss)]
    for (first, second) in zip(FLAG, key * (1 + len(FLAG) // len(key))):
        result += chr(first ^ second)

    print(result)
