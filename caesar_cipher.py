def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    # Adjust shift direction based on encryption or decryption mode
    if mode == 'decrypt':
        shift = -shift
        
    for char in text:
        # Process uppercase letters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Process lowercase letters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        # Leave punctuation, numbers, and spaces unchanged
        else:
            result += char
            
    return result

def run_classical_evaluation():
    print("--- Classical Cryptography: Caesar Cipher Evaluation ---")
    
    # Define our payload and secret shift key
    plaintext = "Classic Cryptography Evaluation 2026!"
    secret_shift = 4
    print(f"Original Plaintext: {plaintext}")
    print(f"Secret Shift Key:   {secret_shift}\n")
    
    # 1. Evaluate Encryption
    ciphertext = caesar_cipher(plaintext, secret_shift, mode='encrypt')
    print(f"[1/2] Encrypted Ciphertext: {ciphertext}")
    
    # 2. Evaluate Decryption
    decrypted_text = caesar_cipher(ciphertext, secret_shift, mode='decrypt')
    print(f"[2/2] Decrypted Plaintext:  {decrypted_text}")
    
    # 3. Verify Integrity
    print("\n--- CIPHER RUN VERIFICATION ---")
    if plaintext == decrypted_text:
        print("Integrity Match: SUCCESS")
    else:
        print("Integrity Match: FAILED")
    print("--------------------------------")

if __name__ == "__main__":
    run_classical_evaluation()