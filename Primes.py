import math

# Find prime numbers <= stop, using the sieve of Eratosthenes.
def findPrimes(stop, found = [], log = False):
    if len(found) < 3:
        found = [2, 3]
    jMax = int(math.sqrt(stop))
    if log:
        print("Largest factor tested: " + str(jMax))
    # Iterate through canditate odd numbers.
    for i in range(found[-1] + 2, stop + 1, 2):
        # We've already skipped even numbers, so dividing by 2 is unnecessary.
        for j in found[1:]:
            if i % j == 0:
                if log:
                    print("{} % {} = 0, skipping.".format(i, j))
                break
            elif j == found[-1] or j >= jMax:
                found.append(i)
                if log:
                    print("Found prime: " + str(i))
                break
    return found

# Find prime factorisations of n, skipping to an unsearched region of the list if desired.
def primeFactors(n, primes, skipTo = 0):
    found = []
    # Once x * y = n is found, ignore y * x = n.
    dup = {}
    for i in primes[skipTo:]:
        for j in primes:
            if (i not in dup) and i * j == n:
                found.append((i, j))
                dup[j] = 0
    return found
