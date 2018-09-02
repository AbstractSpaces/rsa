import Primes, RSA_Maths, RSA

# Attempt to brute force crack a private RSA key given the public key.
# incr can be adjusted to report progress at different intervals.
def crackPrivate(e, n, incr = 500):
    p, q, t = 0, 0, 0
    primes = []
    i, j = 1, incr
    while i < n:
        print("Finding primes to {}, remaining search space: {}".format(j, n-j))
        old = len(primes)
        primes = Primes.findPrimes(j + 1, primes)
        print("Finding prime factors using {} new primes.".format(len(primes) - old))
        for k in Primes.primeFactors(n, primes, old):
            p, q = k[0], k[1]
            t = RSA_Maths.totient(p, q)
            if RSA_Maths.euclid(t, e) == 1:
                print("p, q: {}, {}.".format(p, q))
                # Found t, now to calculate d.
                d = RSA_Maths.modInverse(t, e)
                print("Private key: ({}, {}).".format(d, n))
                return [d, n]
        i, j = j, j + incr
        if j > n:
            j = n
    print("Failure.")
    return None

def testCrack(b):
    k = RSA.chooseKeys(b, log = True)
    p = crackPrivate(k["e"], k["n"])
    print("{} boi".format("yea" if p[0] == k["d"] else "aww"))

testCrack(16)