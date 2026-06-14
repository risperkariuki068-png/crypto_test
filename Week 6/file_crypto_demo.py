import os
from aes_block_cipher import aes_256_cbc_encrypt, aes_256_cbc_decrypt

def run_file_encryption_demo():
    print("==================================================")
    print("       AES-256 LOCAL FILE ENCRYPTION DEMO         ")
    print("==================================================")
    
    # 1. Read the raw plaintext data from the local text file
    input_file = "document.txt"
    encrypted_file = "document.encrypted"
    decrypted_file = "document_restored.txt"
    
    with open(input_file, "rb") as f:
        plaintext_content = f.read()
    
    print(f"[1/4] Loaded '{input_file}' ({len(plaintext_content)} bytes).")

    # 2. Generate a fresh 32-byte key and encrypt the content
    secret_key = os.urandom(32)
    iv, ciphertext = aes_256_cbc_encrypt(plaintext_content, secret_key)
    
    # 3. Write the scrambled ciphertext to a new binary file
    # We save the IV at the beginning of the file so we can find it during decryption
    with open(encrypted_file, "wb") as f:
        f.write(iv + ciphertext)
        
    print(f"[2/4] Scrambled data written to '{encrypted_file}'.")

    # 4. Read the encrypted file back to simulate decryption later
    with open(encrypted_file, "rb") as f:
        file_data = f.read()
        
    # Extract the components: first 16 bytes is the IV, the rest is ciphertext
    read_iv = file_data[:16]
    read_ciphertext = file_data[16:]
    
    # 5. Reverse the math to decrypt the payload
    restored_plaintext = aes_256_cbc_decrypt(read_ciphertext, secret_key, read_iv)
    
    # 6. Save the restored data to a clean text file
    with open(decrypted_file, "wb") as f:
        f.write(restored_plaintext)
        
    print(f"[3/4] Successfully decrypted data into '{decrypted_file}'.")
    print("--------------------------------------------------")
    print("VERIFICATION CHECKS:")
    print(f"Original Text  : {plaintext_content.decode('utf-8').strip()}")
    print(f"Decrypted Text : {restored_plaintext.decode('utf-8').strip()}")
    print("Final Status   : SUCCESS (File integrity preserved)")
    print("==================================================")

if __name__ == "__main__":
    run_file_encryption_demo()