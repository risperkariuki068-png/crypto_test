import time
import os
from rc4_simulation import rc4_encrypt_decrypt
from lfsr_generator import LFSR

def benchmark_stream_ciphers():
    print("==================================================")
    
    payload_size_kb = 10
    raw_data = os.urandom(payload_size_kb * 1024)
    plaintext_string = ''.join(chr(b % 26 + 65) for b in raw_data)
    
    print(f"Testing Payload Size : {payload_size_kb} KB ({len(plaintext_string)} characters)")
    print("==================================================\n")

    # 1. BENCHMARK RC4 STREAM CIPHER
    print("[1/2] Benchmarking RC4 Execution...")
    rc4_key = "PERFORMANCE_KEY"
    
    start_rc4 = time.perf_counter()
    rc4_encrypt_decrypt(plaintext_string, rc4_key)
    end_rc4 = time.perf_counter()
    
    rc4_time_ms = (end_rc4 - start_rc4) * 1000

    # 2. BENCHMARK LFSR GENERATOR 
    print("[2/2] Benchmarking LFSR Execution...")
    seed = [1, 1, 0, 1]
    taps = [3, 4]
    lfsr = LFSR(seed, taps)
    
    start_lfsr = time.perf_counter()
    lfsr.generate_sequence(len(plaintext_string))
    end_lfsr = time.perf_counter()
    
    lfsr_time_ms = (end_lfsr - start_lfsr) * 1000

    # 3. OUTPUT MATRIX RESULTS
    print("\n==================================================")
    print("         ENCRYPTION PERFORMANCE RESULTS           ")
    print("==================================================")
    print(f"RC4 Stream Cipher Execution Time : {rc4_time_ms:.2f} ms")
    print(f"LFSR Stream Generator Time       : {lfsr_time_ms:.2f} ms")
    print("--------------------------------------------------")
    
    if rc4_time_ms < lfsr_time_ms:
        print("Performance Verdict: RC4 processed the data FASTER.")
    else:
        print("Performance Verdict: LFSR processed the data FASTER.")
    print("==================================================")

if __name__ == "__main__":
    benchmark_stream_ciphers()