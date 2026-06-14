# week6/spn_cipher.py

# 1. Define our Lookup Matrices (Mapping dictionaries)
# S-Box (Substitution): Swaps hex keys to break clear linear patterns
S_BOX = {
    '0': 'E', '1': '4', '2': 'D', '3': '1',
    '4': '2', '5': 'F', '6': 'B', '7': '8',
    '8': '3', '9': 'A', 'A': '6', 'B': 'C',
    'C': '5', 'D': '9', 'E': '0', 'F': '7'
}

# P-Box (Permutation): Shifts specific bit positions to diffuse patterns
# Maps index positions: 0->2, 1->0, 2->3, 3->1
P_BOX = [2, 0, 3, 1]


def substitute(hex_char):
    """Replaces a hexadecimal character using our S-Box definition."""
    char_upper = hex_char.upper()
    return S_BOX.get(char_upper, char_upper)


def permute(hex_char):
    """Converts hex to 4-bit binary, shifts positions via P-Box, returns hex."""
    # Convert hex to 4-bit padded binary string
    bin_str = bin(int(hex_char, 16))[2:].zfill(4)
    
    # Scramble bit arrays using our P-Box positions
    permuted_bits = [''] * 4
    for original_idx, target_idx in enumerate(P_BOX):
        permuted_bits[target_idx] = bin_str[original_idx]
        
    permuted_str = "".join(permuted_bits)
    # Convert back to upper case hex character string
    return hex(int(permuted_str, 2))[2:].upper()


def main():
    print("--- Basic Substitution-Permutation Network (SPN) Engine ---")
    
    # Requirement 1: User enters a single hex character string (e.g., A, 5, F)
    user_input = input("Enter a single hexadecimal character plaintext (0-F): ").strip()
    
    if len(user_input) != 1 or user_input.upper() not in S_BOX:
        print("[!] Error: Please enter exactly one valid hexadecimal character (0-F).")
        return

    print(f"\n[+] Input Plaintext:  {user_input.upper()}")

    # Requirement 2: Apply substitution layer step
    sub_result = substitute(user_input)
    print(f"[->] After Substitution (S-Box):  {sub_result}")

    # Requirement 3: Apply permutation layer step
    cipher_result = permute(sub_result)
    
    # Requirement 4: Display final output ciphertext code
    print(f"[==] Final Ciphertext Output (P-Box): {cipher_result}")


if __name__ == "__main__":
    main()
