import math

# Find prime numbers <= stop, using the sieve of Eratosthenes.
# An optional list of already found primes to skip over can be passed in.
def findPrimes(stop, primes = []):
    if len(primes) < 3:
        primes = [2, 3]
    jMax = int(math.sqrt(stop))
    # Iterate through canditate odd numbers.
    for i in range(primes[-1] + 2, stop + 1, 2):
        # We've already skipped even numbers, so dividing by 2 is unnecessary.
        for j in primes[1:]:
            if i % j == 0:
                break
            # If there are no prime divisors up to jMax, we've found a new prime.
            elif j == primes[-1] or j >= jMax:
                primes.append(i)
                break
    return primes

# Find prime factorisations of n, skipping to an unsearched region of the list if desired.
def primeFactors(n, primes, skipTo = 0):
    factors = []
    # Once x * y = n is found, ignore y * x = n.
    dup = {}
    for i in primes[skipTo:]:
        for j in primes:
            if (i not in dup) and i * j == n:
                factors.append((i, j))
                dup[j] = 0
    return factors
