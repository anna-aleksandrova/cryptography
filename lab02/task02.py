from task01 import AES

import os
import random

def hamming(bytes1: bytes, bytes2: bytes) -> int:
    """Calculates the number of differing bits between two byte sequences."""
    distance = 0
    for b1, b2 in zip(bytes1, bytes2):
        distance += bin(b1 ^ b2).count('1')
    return distance

def FlipBit(data: bytes) -> bytes:
    """Flips one random bit in a byte sequence."""
    byte_array = bytearray(data)
    random_byte_index = random.randint(0, len(byte_array) - 1)
    random_bit_index = random.randint(0, 7)
    
    byte_array[random_byte_index] ^= (1 << random_bit_index)
    return bytes(byte_array)

def test(trials: int = 100000):
    print(f"Starting the test ({trials} trials)...")
    
    key_sizes = {
        "AES-128": 16,
        "AES-192": 24,
        "AES-256": 32
    }
    
    for aes_name, key_length in key_sizes.items():
        plaintext_diff_sum = 0
        key_diff_sum = 0
        
        for _ in range(trials):
            # generate random plaintext (always 16 bytes) and key
            plaintext = os.urandom(16)
            key = os.urandom(key_length)
            
            aes = AES(key)
            base_ciphertext = aes.encrypt(plaintext)
            
            # test A
            pt_flipped = FlipBit(plaintext)
            ciphertext_changed = aes.encrypt(pt_flipped)
            plaintext_diff_sum += hamming(base_ciphertext, ciphertext_changed)
            
            # test B
            key_flipped = FlipBit(key)
            aes_flipped_key = AES(key_flipped)
            ct_key_changed = aes_flipped_key.encrypt(plaintext)
            key_diff_sum += hamming(base_ciphertext, ct_key_changed)
            
        avg_pt_diff = plaintext_diff_sum / trials
        avg_key_diff = key_diff_sum / trials
        
        print(f"--- {aes_name} ---")
        print(f"a) Average change when flipping a plaintext bit: {avg_pt_diff:.2f} bits")
        print(f"b) Average change when flipping a key bit:       {avg_key_diff:.2f} bits\n")

if __name__ == "__main__":
    test(trials=100000)