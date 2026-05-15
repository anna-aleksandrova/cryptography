import math

def baby_step_giant_step(a, b, p):
    """
    Solves the discrete logarithm problem: a^x = b (mod p)
    Returns x such that (a**x) % p == b, or None if no solution exists.
    """
    n = p - 1
    m = math.ceil(math.sqrt(n))

    # Store a^j mod p in a hash map (dictionary) for j in [0, m-1] in format { value: index }
    baby_steps = {}
    current_val = 1
    for j in range(m):
        if current_val not in baby_steps:
            baby_steps[current_val] = j
        current_val = (current_val * a) % p

    # Compute a^(-m) mod p
    # Since p is prime, we use Fermat's Little Theorem: a^(p-2) is the inverse.
    a_m = pow(a, m, p)
    giant_step_factor = pow(a_m, p - 2, p)

    gamma = b
    for i in range(m):
        if gamma in baby_steps:
            return i * m + baby_steps[gamma]
        gamma = (gamma * giant_step_factor) % p

    return None

if __name__ == "__main__":
    p = 1048573
    a = 3
    
    x = 123456
    b = pow(a, x, p)
    
    res = baby_step_giant_step(a, b, p)
    
    if res is not None and pow(a, res, p) == b:
        print("Solution is correct.")
    else:
        print("Solution not found.")
