# RSA encryption / decryption functions.

import secrets, Primes, RSA_Maths

# Pick a number < t that is coprime to t.
def findE(t, log = False):
    e = 2
    while RSA_Maths.euclid(t, e) != 1:
        if log:
            print("Randomising e...")
        e = secrets.randbelow(t)
    if log:
        print("e: {}".format(e))
    return e

# Choose private and public keys for the encryption.
# b is the number of bits desired for the prime factors.
def chooseKeys(b, log = False):
    # Rather than find every prime with b bits, choose from two random slices of the search space.
    limit = 1 << b
    # To make optimising the prime calculation easier, p is always < q.
    pLo = secrets.randbits(b)
    pHi = pLo + secrets.randbelow(limit - pLo)
    qLo = pHi + secrets.randbelow(limit - pHi)
    qHi = qLo + secrets.randbelow(limit - qLo)
    # The lower primes aren't considered but still need calculating to find the higher ones.
    primes = Primes.findPrimes(pLo)
    skip = len(primes)
    primes = Primes.findPrimes(pHi, primes)
    p = secrets.choice(primes[skip:])
    if log:
        print("p: " + hex(p))
    primes = Primes.findPrimes(qLo, primes)
    skip - len(primes)
    primes = Primes.findPrimes(qHi, primes)
    q = secrets.choice(primes[skip:])
    if log:
        print("q: " + hex(q))
    n = p * q
    if log:
        print("n: " + hex(n))
    t = RSA_Maths.totient(p, q)
    e = findE(t)
    if log:
        print("e: " + hex(e))
    d = RSA_Maths.modInverse(t, e)
    if log:
        print("d: " + hex(d))
    return {"n": n, "e": e, "d": d}

# Encrypt a plaintext string to an RSA encrypted ciphertext.
def encrypt(txt, e, n):
    print("Plain text: " + txt)
    print("Encoding...")
    txt = txt.encode('utf-8').hex()
    print("Plain hex: " + txt)
    print("Encrypting...")
    txt = hex(pow(int(txt, 16), e, n))
    print("Ciphertext: " + txt)
    return txt
# Decrypt an RSA encrypted string.
def decrypt(txt, d, n):
    print("Ciphertext: " + txt)
    print("Decrypting...")
    txt = hex(pow(int(txt, 16), d, n))
    print("Decrypted hex: " + txt)
    print("Decoding...")
    # I want to see the garbled plaintext if an error occurred, so this will decode it character by character.
    plain = []
    # Skipping the 0x prefix of the hex string.
    i = 2
    while i < len(txt):
        try:
            c = bytes.fromhex(txt[i:i+2]).decode("utf-8")
            plain.append(c)
        except UnicodeDecodeError:
            plain.append("[0x{}]".format(c))
        i += 2
    plain = "".join(plain)
    print("Plaintext: " + plain)
    return plain
