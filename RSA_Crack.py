# Algorithm for brute forcing a private RSA key given the public key.

# Attempt to brute force crack a private RSA key given the public key.
# incr can be adjusted to report progress at different intervals.
def crackPrivate(e, n, incr = 500):
    p, q, t = 0, 0, 0
    primesFound = []
    i = 1
    while i <= n:
        print("Finding primes to {}, remaining search space: {}".format(i+incr, n-i-incr))
        newPrimes = primes(i, i+incr)
        primesFound += newPrimes
        print("Finding prime factors using {} new primes.".format(len(newPrimes)))
        for i in primeFactors(n, primesFound, len(primesFound)-len(newPrimes)):
            p, q = i[0], i[1]
            t = totient(p, q)
            if euclid(t, e) == 1:
                print("p, q: {}, {}.".format(p, q))
                # Found t, now to calculate d.
                d = inverse(t, e)
                print("Private key: ({}, {}).".format(d, n))
                return [d, n]
        else:
            if n - i < incr:
                incr = n - q
            i += incr
    print("Failure.")
    return None

crackPrivate(findE(120), 143, 4)