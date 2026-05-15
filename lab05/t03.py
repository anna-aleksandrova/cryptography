import random
from t01 import find_primitive_element

def diffie_hellman(p):
    g = find_primitive_element(p)
    if g is None:
        raise ValueError("Could not find a primitive element for the given prime.")
    
    print(f"Public Parameters:\nPrime (p): {p}\nGenerator (g): {g}\n")


    a_secret = random.randint(1, p - 2)
    a_public = pow(g, a_secret, p)
    print(f"Alice's public key (A): {a_public}")

    b_secret = random.randint(1, p - 2)
    b_public = pow(g, b_secret, p)
    print(f"Bob's public key (B): {b_public}\n")

    alice_shared_secret = pow(b_public, a_secret, p)
    bob_shared_secret = pow(a_public, b_secret, p)

    return alice_shared_secret, bob_shared_secret

if __name__ == "__main__":
    p = 1048573
    
    print("--- Diffie-Hellman Key Exchange ---")
    alice_key, bob_key = diffie_hellman(p)
    
    print(f"Alice's shared secret: {alice_key}")
    print(f"Bob's shared secret:   {bob_key}")
    