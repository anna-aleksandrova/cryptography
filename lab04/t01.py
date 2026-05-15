import random

def generate_512bit():
    """Generates a random 512-bit odd number."""
    n = random.getrandbits(512)
    n |= (1 << 511) | 1
    return n

def miller_rabin_test(n, k=100):
    """
    Implements the Miller-Rabin primality test.
    """
    if n == 2 or n == 3:
        return True, []
    if n <= 1 or n % 2 == 0:
        return False, []

    # Represent n - 1 as 2^s * d, where d is odd
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    bases_used = []

    # k tests
    for _ in range(k):
        a = random.randint(2, n - 2)
        bases_used.append(a)

        # Calculate x = a^d mod n
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue

        # Repeat s - 1 times
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False, bases_used
        
    return True, bases_used

if __name__ == "__main__":
    print("Generating a test number 'n' of binary length 512...")
    n = generate_512bit()
    # big prime
    # n = 693180815473961672401040726837
    print(f"n = {n}\n")
    print("-" * 50)

    print("Running the Miller-Rabin test (k=100)...\n")
    is_prime, bases = miller_rabin_test(n, k=100)

    for i, a in enumerate(bases):
        print(f"Test {i+1}: chosen random a = {a}")

    print("-" * 50)
    if is_prime:
        print('Answer: probably prime')
    else:
        print('Answer: composite')
