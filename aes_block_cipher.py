import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def aes_256_cbc_encrypt(plaintext, key):
    # 1. Generate a random 16-byte Initialization Vector (IV)
    # The IV ensures identical plaintexts result in completely different ciphertexts
    iv = os.urandom(16)
    
    # 2. Apply PKCS7 Padding to align data to the 16-byte (128-bit) block boundary
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    # 3. Initialize the AES-256 Engine in CBC Mode
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    
    # 4. Perform the block transformation
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return both the IV and ciphertext; the IV is required to decrypt the message later
    return iv, ciphertext

def aes_256_cbc_decrypt(ciphertext, key, iv):
    # 1. Initialize the matching decryption structure
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    
    # 2. Decrypt the ciphertext blocks back to padded bytes
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # 3. Strip away the PKCS7 padding bytes to recover original content length
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext

def run_block_cipher_evaluation():
    print("--- Block Ciphers: Advanced Encryption Standard (AES-256) ---")
    
    # Define an unaligned message (29 bytes long - not a multiple of 16)
    secret_data = b"AES block cipher verification"
    
    # Generate a cryptographically strong 32-byte (256-bit) secret key
    secret_key = os.urandom(32)
    
    print(f"Original Plaintext : {secret_data.decode('utf-8')}")
    print(f"Plaintext Length   : {len(secret_data)} bytes")
    print(f"Secret Key (Hex)   : {secret_key.hex()[:32]}...\n")
    
    # 1. Evaluate block encryption
    iv, ciphertext = aes_256_cbc_encrypt(secret_data, secret_key)
    print(f"[1/2] Initialization Vector (Hex) : {iv.hex()}")
    print(f"[1/2] Encrypted Ciphertext (Hex)   : {ciphertext.hex()}")
    print(f"      Ciphertext Output Length     : {len(ciphertext)} bytes (Aligned to 32 bytes)")
    
    # 2. Evaluate block decryption
    decrypted_data = aes_256_cbc_decrypt(ciphertext, secret_key, iv)
    print(f"\n[2/2] Decrypted Plaintext Output   : {decrypted_data.decode('utf-8')}")
    
    # 3. Verify System Integrity
    print("\n--- BLOCK RUN VERIFICATION ---")
    if secret_data == decrypted_data:
        print("Integrity Status: SUCCESS (Block structure matched and fully verified)")
    else:
        print("Integrity Status: FAILED")
    print("------------------------------")

if __name__ == "__main__":
    run_block_cipher_evaluation()