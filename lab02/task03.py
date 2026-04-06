import os
import random
from task01 import AES
from task02 import hamming, FlipBit 

def test_rounds(max_rounds=14, trials=5000):
    key_length = 16
    
    for round_count in range(1, max_rounds + 1):
        diff_sum = 0
        for _ in range(trials):
            plaintext = os.urandom(16)
            key = os.urandom(key_length)
            aes = AES(key)

            aes.Nr = round_count
            aes.round_keys = aes._key_expansion()
            base_ciphertext = aes.encrypt(plaintext)
            pt_flipped = FlipBit(plaintext)
            ct_changed = aes.encrypt(pt_flipped)
            diff_sum += hamming(base_ciphertext, ct_changed)
            
        avg_diff = diff_sum / trials
            
        print(f"Rounds: {round_count:6d} | {avg_diff:19.2f} ")

if __name__ == "__main__":
    test_rounds()