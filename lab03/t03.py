import hashlib
import time
import os

def get_first_k_bits(hex_str: str, k: int) -> str:
    """Converts a hexadecimal string to binary and returns the first k bits."""
    return bin(int(hex_str, 16))[2:].zfill(256)[:k]

def find_partial_collision(k: int):
    """Finds two different messages with the same first k bits of their hash."""
    seen_hashes = {}
    
    while True:
        msg = os.urandom(8).hex()
        
        full_hash = hashlib.sha256(msg.encode('utf-8')).hexdigest()
        
        k_bits = get_first_k_bits(full_hash, k)
        
        if k_bits in seen_hashes:
            if seen_hashes[k_bits] != msg:
                return msg, seen_hashes[k_bits], k_bits
        else:
            seen_hashes[k_bits] = msg

if __name__ == "__main__":
    attempts = 100
    
    print(f"Searching for partial SHA-256 collisions (average over {attempts} attempts)")
    print("-" * 65)
    print(f"{'k (bits)':<10} | {'Avg Time (sec)':<20} | {'Theoretical attempts ~ 2^(k/2)':<25}")
    print("-" * 65)
    
    for k in range(5, 16):
        total_time = 0.0
        
        for _ in range(attempts):
            start_time = time.perf_counter()
            find_partial_collision(k)
            end_time = time.perf_counter()
            
            total_time += (end_time - start_time)
        
        avg_time = total_time / attempts
        
        # Theoretical number of attempts based on the birthday paradox
        theoretical_complexity = 2**(k / 2)
        
        print(f"{k:<10} | {avg_time:<20.6f} | ~{theoretical_complexity:<24.1f}")
        
    print("-" * 65)
    