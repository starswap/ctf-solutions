#!/usr/bin/env python3
import binascii
import itertools

def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return itertools.chain.from_iterable(itertools.combinations(xs,n) for n in range(len(xs)+1))

with open("output.txt", "r") as f:
    ctxt = binascii.unhexlify(f.read())

def decrypt(ctxt, key):
    ptxt = b''
    for i in range(len(ctxt)):
        a = ctxt[i]
        b = key[i % len(key)]
        ptxt += bytes([a ^ b])
    return ptxt

random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]

ctxt_orig = ctxt
for subset in powerset(random_strs):
    ctxt = ctxt_orig
    for key in subset:
        ctxt = decrypt(ctxt, key)
    
    print(decrypt(ctxt, b"Africa!"))