import sys

def vigenere_cipher(text, key, mode='encrypt'):
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            if mode == 'decrypt':
                shift = -shift
                
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) + shift - 97) % 26 + 97)
            key_index += 1
        else:
            result += char
    return result

def get_validated_input():
    print("\n=========================================")
    print("      VIGENÈRE CRYPTOGRAPHY INTERFACE     ")
    print("=========================================")
    
    # 1. Validate Mode Selection
    while True:
        mode = input("Select Mode (1: Encrypt, 2: Decrypt, Q: Quit): ").strip().lower()
        if mode in ['1', 'encrypt']:
            mode = 'encrypt'
            break
        elif mode in ['2', 'decrypt']:
            mode = 'decrypt'
            break
        elif mode in ['q', 'quit']:
            print("Exiting interface. Goodbye!")
            sys.exit()
        else:
            print("[VALIDATION ERROR] Invalid choice. Please enter 1, 2, or Q.")

    # 2. Validate Plaintext / Ciphertext Message
    while True:
        text = input(f"Enter the message to {mode}: ").strip()
        if not text:
            print("[VALIDATION ERROR] Message cannot be empty. Try again.")
        else:
            break

    # 3. Validate Secret Keyword (Strictly Alphabetical Only)
    while True:
        key = input("Enter secret keyword (Letters only): ").strip()
        if not key:
            print("[VALIDATION ERROR] Secret keyword cannot be empty.")
        elif not key.isalpha():
            print("[VALIDATION ERROR] Keyword must contain LETTERS ONLY (No numbers/symbols).")
        else:
            break
            
    return text, key, mode

def run_interface():
    while True:
        try:
            text, key, mode = get_validated_input()
            output = vigenere_cipher(text, key, mode)
            
            print("\n-----------------------------------------")
            print(f"OUTPUT ({mode.upper()} SUCCESS)")
            print(f"Result: {output}")
            print("-----------------------------------------")
            
            # Ask to loop or end
            again = input("\nProcess another message? (y/n): ").strip().lower()
            if again != 'y':
                print("Exiting interface. Goodbye!")
                break
        except KeyboardInterrupt:
            print("\nProgram interrupted. Goodbye!")
            break

if __name__ == "__main__":
    run_interface()