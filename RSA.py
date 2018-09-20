# RSA encryption / decryption functions.

import secrets, RSA_Primes, RSA_Maths

# Pick a number < t that is coprime to t.
def findE(t):
    e = 2
    while RSA_Maths.euclid(t, e) != 1:
        e = secrets.randbelow(t)
    return e

# Choose private and public keys for the encryption.
# b is the number of bits desired for the prime factors.
def chooseKeys(b = 16):
    # Rather than find every prime with b bits, choose from two random slices of the search space.
    limit = 1 << b
    # To make optimising the prime calculation easier, p is always < q.
    pLo = secrets.randbits(b)
    pHi = pLo + secrets.randbelow(limit - pLo)
    qLo = pHi + secrets.randbelow(limit - pHi)
    qHi = qLo + secrets.randbelow(limit - qLo)
    # The lower primes aren't considered but still need calculating to find the higher ones.
    primes = RSA_Primes.findPrimes(pLo)
    skip = len(primes)
    # Find primes between pLo and pHi, randomly choose one.
    primes = RSA_Primes.findPrimes(pHi, primes)
    p = secrets.choice(primes[skip:])
    # Repeat for qHi and qLo.
    primes = RSA_Primes.findPrimes(qLo, primes)
    skip = len(primes)
    primes = RSA_Primes.findPrimes(qHi, primes)
    q = secrets.choice(primes[skip:])
    # Calculate the key values.
    n = p * q
    t = RSA_Maths.totient(p, q)
    e = findE(t)
    d = RSA_Maths.modInverse(t, e)
    return {"n": n, "e": e, "d": d}

# Encrypt a plaintext string to an RSA encrypted ciphertext.
# txt is given as a UTF-8 string, the ciphertext is returned as a hex string.
def encrypt(plainStr, e, n):
    # Expanding the process to multiple lines for readability.
    plainHex = plainStr.encode('utf-8').hex()
    plainInt = int(plainHex, 16)
    if plainInt > n:
        print("Message to large for given modulus.")
        return None
    ciphInt = pow(plainInt, e, n)
    return hex(ciphInt)
    
# Decrypt an RSA encrypted string.
# Ciphertext is given as a hex string, the plaintext returned as a UTF-8 string.
def decrypt(ciphHex, d, n):
    ciphInt = int(ciphHex, 16)
    plainInt = pow(ciphInt, d, n)
    plainHex = hex(plainInt)
    # I want to see the garbled plaintext if an error occurred, so this will decode it character by character.
    plainChar = []
    # Skipping the 0x prefix of the hex string.
    i = 2
    while i < len(plainHex):
        try:
            c = bytes.fromhex(plainHex[i:i+2]).decode("utf-8")
            plainChar.append(c)
        except UnicodeDecodeError:
            plainChar.append(f"[0x{plainHex[i]}{plainHex[i+1]}]")
        i += 2
    return "".join(plainChar)

# Attempt to brute force crack a private RSA key given the public key.
# incr can be adjusted to report progress at different intervals.
def crackPrivate(e, n, incr = 500):
    primes = []
    i, j = 1, incr
    while i < n:
        print("Finding primes to {}, remaining search space: {}".format(j, n-j))
        # Remember which primes have already been searched through.
        skip = len(primes)
        # Add incr to the search space for new primes.
        primes = RSA_Primes.findPrimes(j + 1, primes)
        print("Finding prime factors using {} new primes.".format(len(primes) - skip))
        # Search for prime factors of n including the newly found primes.
        for k in RSA_Primes.primeFactors(n, primes, skip):
            p, q = k[0], k[1]
            t = RSA_Maths.totient(p, q)
            if RSA_Maths.euclid(t, e) == 1:
                print("p, q: {}, {}.".format(p, q))
                # Found t, now to calculate d.
                d = RSA_Maths.modInverse(t, e)
                print("Private key: ({}, {}).".format(d, n))
                return [d, n]
        # Update the loop variables.
        i, j = j, j + incr
        if j > n:
            j = n
    print("Failure.")
    return None