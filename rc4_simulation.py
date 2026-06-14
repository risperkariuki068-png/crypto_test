def ksa(key):
    """Key Scheduling Algorithm (KSA) to initialize the 256-byte state vector."""
    key_length = len(key)
    # Initialize state vector S with values 0 to 255
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        # Swap values
        S[i], S[j] = S[j], S[i]
    return S

def prga(S, text_length):
    """Pseudo-Random Generation Algorithm (PRGA) to generate the keystream bytes."""
    i = 0
    j = 0
    keystream = []
    for _ in range(text_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        # Swap values
        S[i], S[j] = S[j], S[i]
        # Generate keystream byte
        k = S[(S[i] + S[j]) % 256]
        keystream.append(k)
    return keystream

def rc4_encrypt_decrypt(text, key_string):
    """Executes the complete symmetric RC4 transformation."""
    # Convert string parameters to byte arrays
    key_bytes = [ord(c) for c in key_string]
    text_bytes = [ord(c) for c in text]
    
    # 1. Run KSA to get initialized state permutation vector
    S = ksa(key_bytes)
    
    # 2. Run PRGA to get matching keystream length bytes
    keystream = prga(S, len(text_bytes))
    
    # 3. XOR the plaintext bytes with keystream bytes
    output_bytes = [text_bytes[i] ^ keystream[i] for i in range(len(text_bytes))]
    
    # Return both raw byte representation and a readable hex format
    return output_bytes, ''.join(f'{b:02x}' for b in output_bytes)

def run_rc4_simulation():
    print("--- Stream Ciphers: RC4 Simulation Evaluation ---")
    
    plaintext = "Stream Cipher Evaluation 2026"
    secret_key = "SECRET_KEY"
    
    print(f"Original Plaintext : {plaintext}")
    print(f"Secret Stream Key  : {secret_key}\n")
    
    # 1. Run Encryption Process
    raw_cipher, hex_cipher = rc4_encrypt_decrypt(plaintext, secret_key)
    print(f"[1/2] Encrypted Ciphertext (Hex): {hex_cipher}")
    
    # 2. Run Decryption Process (Convert ciphertext bytes back using the same key)
    # In RC4, passing ciphertext to the same XOR structure reverses the encryption
    cipher_as_string = ''.join(chr(b) for b in raw_cipher)
    raw_decrypted, _ = rc4_encrypt_decrypt(cipher_as_string, secret_key)
    decrypted_text = ''.join(chr(b) for b in raw_decrypted)
    print(f"[2/2] Decrypted Plaintext Result: {decrypted_text}")
    
    # 3. Verify System Output Integrity
    print("\n--- SIMULATION RUN VERIFICATION ---")
    if plaintext == decrypted_text:
        print("Integrity Match: SUCCESS")
    else:
        print("Integrity Match: FAILED")
    print("-----------------------------------")

if __name__ == "__main__":
    run_rc4_simulation()