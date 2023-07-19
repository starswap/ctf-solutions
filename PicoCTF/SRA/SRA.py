from Crypto.Util.number import isPrime
import functools
import binascii

def to_ascii(number):
    string = str(hex(number))[2:]
    if len(string) % 2 == 1:
        string = "0" + string
    return binascii.unhexlify(string)

e = # INSERT e here
d = # INSERT d here
c = # INSERT c here

val = e * d - 1
factors = [19543, 246508643, 2, 17, 43, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

assert(functools.reduce(lambda x,y : x * y, factors) == val)

counts = {}
for item in factors:
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1

pairs = set()
def get_p_and_q(counts, p, q, i):
    if i == len(counts):
        if isPrime(p + 1) and isPrime(q + 1):
            if p * q > d:
                pairs.add((p + 1, q + 1))
                print(pairs)
                return None
            else:
                return None
    else:
        valp = 1
        for np in range(0, counts[i][1] + 1):
            newp = p * valp
            valp *= counts[i][0] 
            valq = 1
            for nq in range(0, counts[i][1] + 1 - np):
                newq = q * valq 
                valq *= counts[i][0] 
                if (get_p_and_q(counts, newp, newq, i + 1)):
                    return get_p_and_q(counts, newp, newq, i + 1)

cnts = list(counts.items())
get_p_and_q(cnts, 1, 1, 0)

for (p, q) in pairs:
    print(to_ascii(pow(c, d, p * q)))
