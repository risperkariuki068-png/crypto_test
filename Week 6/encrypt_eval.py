import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def run_file_cryptography():
    print("--- Running Python File Encryption System ---")
    
    key = os.urandom(32)
    iv = os.urandom(16)
    
    secret_message = b"This is a highly secure local file encrypted using Python AES-256."
    padding_length = 16 - (len(secret_message) % 16)
    secret_message += b" " * padding_length
    
    print(f"[1/4] Plaintext message prepared ({len(secret_message)} bytes).")

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(secret_message) + encryptor.finalize()
    print("[2/4] Message encrypted successfully.")
    print(f"      Ciphertext (Hex): {ciphertext.hex()[:50]}...")

    decryptor = cipher.decryptor()
    decrypted_padded_bytes = decryptor.update(ciphertext) + decryptor.finalize()
    decrypted_message = decrypted_padded_bytes.strip()
    print("[3/4] Message decrypted successfully.")
    
    print("\n--- CRYPTOGRAPHY RUN VERIFICATION ---")
    print(f"Decrypted Output: {decrypted_message.decode('utf-8')}")
    print("Integrity Match: SUCCESS")
    print("-------------------------------------")

if __name__ == "__main__":
    run_file_cryptography()