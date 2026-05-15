def get_prime_factors(n):
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def find_primitive_element(p):
    if p == 2:
        return 1
    
    phi = p - 1
    factors = get_prime_factors(phi)
    
    for a in range(2, p):
        is_primitive = True
        for q in factors:
            if pow(a, phi // q, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return a
    return None

if __name__ == "__main__":
    p = 1048573 
    print(f"Prime p: {p} (bits: {p.bit_length()})")
    
    a = find_primitive_element(p)
    print(f"Primitive element a: {a}")
