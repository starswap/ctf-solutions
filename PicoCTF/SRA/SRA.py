from Crypto.Util.number import getPrime, inverse, bytes_to_long


e = 65537
d = 63291719055537736569090281238578505201225992375991855778915571405269909738433
val = e * d - 1

primes = [2]
for i in range(2,10000):
    ok = True
    for prime in primes:
        ok = ok and i % prime != 0
    if ok:
        primes.append(i)

facts = []
while val != 1:
    print(val)
    print(facts)
    for prime in primes:
        if val % prime == 0:
            facts.append(prime)
            val /= prime

factors = [192233, 21146831, 2, 31, 61, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

counts = {}
for item in factors:
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1

def get_p_and_q(counts, p, q, i):
    if len(counts) == 0:
        if isPrime(p + 1) and isPrime(q + 1):
            return (p + 1, q + 1)
        else:
            return None
    else:
        newq = q
        newp = p
        for np in range(0, counts[i][1] + 1):
            nwqp *= counts[i][0]
            for nq in range(0, counts[i][1] + 1 - np):
                newq *= counts[i][0]
            
            if (get_p_and_q(counts, newp, newq, i + 1)):
                return get_p_and_q(counts, newp, newq, i + 1)

cnts = counts.items()
print(get_p_and_q(cnts, 1, 1, 0))
