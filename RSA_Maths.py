# Maths functions required for RSA functionality.

# Represents an iteration of the Euclidean algorithm, where:
# r = a - b*q
class step:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.q = a // b
        self.r = a % b

# Use the Euclidean algorithm to find the greatest common divisor of a and b.
# If full == True, returns an array containing every step that was performed.
def euclid(a, b, full = False, log = False):
    i = step(a, b)
    steps = [i]
    while i.r != 0:
        if log:
            print("{} = {} - {} * {}".format(i.r, i.a, i.b, i.q))
        i = step(i.b, i.r)
        if i.r != 0:
            steps.append(i)
    if log:
        print("GCD({}, {}) = {}".format(a, b, steps[-1].r))
    if full:
        return steps
    else:
        return steps[-1].r

# Use the extended Euclidean algorithm to find x and y where:
# GCD(a, b) = a*x + b*y
def extendedEuclid(a, b, log = False):
    steps = euclid(a, b, full = True)
    # The full algebra of each step can be skipped by boiling it steps to:
    # x[i-1] = y[i]
	# y[i-1] = -q[i-1] * y[i] + x[i]
    x, y = 1, 0 - (steps[-1].q)
    i = len(steps) - 2
    while steps[0].a * x + steps[0].b * y != steps[-1].r:
        if log:
            print("x: {}, y: {}".format(x, y))
        x, y = y, 0 - steps[i].q * y + x
        i -= 1
    if log:
        print("{} = {} * {} + {} * {}".format(steps[-1].r, a, x, b, y))
    return [x, y]

# Find modular multiplicative inverse of a (mod m).
def modInverse(m, a, log = False):
    x = extendedEuclid(a, m, log = log)[0]
    # Things get screwy if x is returned negative.
    if x < 0:
        x = x + m
    if log:
        print("{} * {} = 1 (mod {})".format(a, x, m))
    return x

# Euler's totient function, using the shortcut where n = p * q and p and q are primes:
# phi(n) = (p-1) * (q-1)
def totient(p, q, log = False):
    t = (p - 1) * (q - 1)
    if log:
        print("phi({}*{}) = {}".format(p, q, t))
    return t