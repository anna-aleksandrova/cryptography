import hashlib
import os
import math
from t02 import generate_rsa_keys, rsa_encrypt, rsa_decrypt_crt

def mgf1(seed, length, hash_func=hashlib.sha256):
    h_len = hash_func().digest_size
    if length > (2**32) * h_len:
        raise ValueError("Mask too long")
    
    t = b""
    for i in range(math.ceil(length / h_len)):
        c = i.to_bytes(4, byteorder='big')
        t += hash_func(seed + c).digest()
    
    return t[:length]

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def oaep_encode(message, modulus_len, label=b"", hash_func=hashlib.sha256):
    m_len = len(message)
    h_len = hash_func().digest_size
    l_hash = hash_func(label).digest()
    
    if m_len > modulus_len - 2 * h_len - 2:
        raise ValueError("Message too long for the given RSA modulus.")
    
    ps = b"\x00" * (modulus_len - m_len - 2 * h_len - 2)
    db = l_hash + ps + b"\x01" + message
    seed = os.urandom(h_len)
    
    db_mask = mgf1(seed, modulus_len - h_len - 1, hash_func)
    masked_db = xor_bytes(db, db_mask)
    
    seed_mask = mgf1(masked_db, h_len, hash_func)
    masked_seed = xor_bytes(seed, seed_mask)
    
    return b"\x00" + masked_seed + masked_db

def oaep_decode(em, modulus_len, label=b"", hash_func=hashlib.sha256):
    h_len = hash_func().digest_size
    l_hash = hash_func(label).digest()
    
    if len(em) != modulus_len or em[0] != 0:
        raise ValueError("Decoding error: Invalid encoded message format.")
    
    masked_seed = em[1 : h_len + 1]
    masked_db = em[h_len + 1 :]
    
    seed_mask = mgf1(masked_db, h_len, hash_func)
    seed = xor_bytes(masked_seed, seed_mask)
    
    db_mask = mgf1(seed, modulus_len - h_len - 1, hash_func)
    db = xor_bytes(masked_db, db_mask)
    
    l_hash_prime = db[:h_len]
    if l_hash != l_hash_prime:
        raise ValueError("Decoding error: Label hash mismatch.")
    
    i = h_len
    while i < len(db) and db[i] == 0:
        i += 1
    
    if i == len(db) or db[i] != 1:
        raise ValueError("Decoding error: Separator 0x01 not found.")
    
    return db[i + 1 :]

if __name__ == "__main__":
    pub_key, priv_key_crt = generate_rsa_keys(bits=512)
    e, n = pub_key
    mod_len = (n.bit_length() + 7) // 8
    
    original_text = "Hello, world!"
    message_bytes = original_text.encode('utf-8')

    encoded_message = oaep_encode(message_bytes, mod_len)
    m_int = int.from_bytes(encoded_message, byteorder='big')
    c_int = rsa_encrypt(m_int, pub_key)

    dec_m_int = rsa_decrypt_crt(c_int, priv_key_crt)
    dec_encoded_bytes = dec_m_int.to_bytes(mod_len, byteorder='big')
    
    try:
        final_message = oaep_decode(dec_encoded_bytes, mod_len)
        print(f"Decrypted: {final_message.decode('utf-8')}")
        print(f"Success: {final_message == message_bytes}")
    except ValueError as err:
        print(f"Error: {err}")
        