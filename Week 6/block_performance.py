import time
import os
from aes_block_cipher import aes_256_cbc_encrypt
from rc4_simulation import rc4_encrypt_decrypt

def evaluate_block_performance():
    print("==================================================")
    print("      BLOCK VS STREAM PERFORMANCE EVALUATION       ")
    print("==================================================")
    
    # Generate 50 KB of random test data
    payload_size_kb = 50
    raw_bytes = os.urandom(payload_size_kb * 1024)
    plaintext_string = ''.join(chr(b % 26 + 65) for b in raw_bytes)
    
    print(f"Testing Payload Size: {payload_size_kb} KB ({len(raw_bytes)} bytes)")
    print("--------------------------------------------------")

    # 1. Benchmark AES-256 Block Cipher
    aes_key = os.urandom(32)
    start_aes = time.perf_counter()
    aes_256_cbc_encrypt(raw_bytes, aes_key)
    end_aes = time.perf_counter()
    aes_time_ms = (end_aes - start_aes) * 1000
    print(f"1. AES-256 Block Cipher Speed : {aes_time_ms:.2f} ms")

    # 2. Benchmark RC4 Stream Cipher
    rc4_key = "PERFORMANCE_KEY"
    start_rc4 = time.perf_counter()
    rc4_encrypt_decrypt(plaintext_string, rc4_key)
    end_rc4 = time.perf_counter()
    rc4_time_ms = (end_rc4 - start_rc4) * 1000
    print(f"2. RC4 Stream Cipher Speed    : {rc4_time_ms:.2f} ms")
    
    print("--------------------------------------------------")
    print("PERFORMANCE VERDICT:")
    if aes_time_ms < rc4_time_ms:
        print("AES-256 is FASTER due to hardware acceleration optimization.")
    else:
        print("RC4 is FASTER due to lightweight byte-permutation loops.")
    print("==================================================")

if __name__ == "__main__":
    evaluate_block_performance()