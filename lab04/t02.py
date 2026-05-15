import random
import math
from t01 import miller_rabin_test 


def generate_prime(bits=512):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1 
        
        is_prime, _ = miller_rabin_test(n, k=40) 
        if is_prime:
            return n

def generate_rsa_keys(bits=512):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2

    d = pow(e, -1, phi)

    # CRT parameters
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = pow(q, -1, p)

    public_key = (e, n)
    private_key_crt = (p, q, dp, dq, q_inv)

    return public_key, private_key_crt

def rsa_encrypt(message, public_key):
    e, n = public_key
    ciphertext = pow(message, e, n)
    return ciphertext

def rsa_decrypt_crt(ciphertext, private_key_crt):
    p, q, dp, dq, q_inv = private_key_crt

    m1 = pow(ciphertext, dp, p)
    m2 = pow(ciphertext, dq, q)

    h = (q_inv * (m1 - m2)) % p
    m = m2 + h * q

    return m

if __name__ == "__main__":
    print("--- 1. Key Generation ---")
    pub_key, priv_key_crt = generate_rsa_keys(bits=512)
    e, n = pub_key
    print(f"Public key (e): {e}")
    print(f"Modulus n (binary length {n.bit_length()}): {n}\n")

    print("--- 2. Encryption ---")
    original_message = 1234567890987654321
    print(f"Original message (number): {original_message}")

    ciphertext = rsa_encrypt(original_message, pub_key)
    print(f"Ciphertext (c): {ciphertext}\n")

    print("--- 3. Decryption (using CRT) ---")
    decrypted_message = rsa_decrypt_crt(ciphertext, priv_key_crt)
    print(f"Decrypted message: {decrypted_message}")

    print(original_message == decrypted_message)
        