# week6/advanced_spn.py

# 1. Expand the S-Box to support larger 4-bit boundaries (0-F matrix mapping)
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

# Static P-Box permutation array mapping (Bit-shuffling index)
P_BOX = [2, 0, 3, 1]


def substitute(state_byte):
    """S-Box Layer: Splits an 8-bit state byte into two 4-bit nibbles and substitutes."""
    left_nibble = (state_byte >> 4) & 0x0F
    right_nibble = state_byte & 0x0F
    
    sub_left = S_BOX[left_nibble]
    sub_right = S_BOX[right_nibble]
    
    return (sub_left << 4) | sub_right


def permute_nibble(nibble):
    """Permutes a single 4-bit nibble using our P-Box mapping index rules."""
    bin_str = bin(nibble)[2:].zfill(4)
    permuted_bits = [''] * 4
    for orig_idx, target_idx in enumerate(P_BOX):
        permuted_bits[target_idx] = bin_str[orig_idx]
    return int("".join(permuted_bits), 2)


def permute(state_byte):
    """P-Box Layer: Separates state byte into nibbles, permutes, recombines."""
    left_nibble = (state_byte >> 4) & 0x0F
    right_nibble = state_byte & 0x0F
    
    perm_left = permute_nibble(left_nibble)
    perm_right = permute_nibble(right_nibble)
    
    return (perm_left << 4) | perm_right


def encrypt_spn(plaintext_byte, round_keys, num_rounds):
    """Executes a full multi-round SPN encryption sequence."""
    state = plaintext_byte
    
    for r in range(num_rounds):
        # 1. Key Mixing Layer (XOR state with that round's specific subkey)
        state = state ^ round_keys[r]
        
        # 2. Substitution Layer
        state = substitute(state)
        
        # 3. Permutation Layer (skipped on the final round for standard SPN protocol)
        if r < num_rounds - 1:
            state = permute(state)
            
    # Final Key Mixing layer step
    state = state ^ round_keys[-1]
    return state


def count_differing_bits(byte1, byte2):
    """Calculates the Hamming Distance (how many bits differ) between two bytes."""
    xor_result = byte1 ^ byte2
    # Count the number of active 1s in the binary string
    return bin(xor_result).count('1')


def main():
    print("=== Advanced Multi-Round SPN Crypto Engine ===")
    
    # Requirement 1 & 2: Define Multiple Rounds and Custom Round Keys
    ROUNDS = 3
    # 4 Subkeys needed for a 3-round network setup (Key 0, 1, 2, and Final Key)
    custom_keys = [0x3C, 0xA5, 0x5A, 0xF0]
    
    # Test Data Set: Base Plaintext and a variant altered by exactly 1 bit
    pt1 = 0x41  # Character 'A' -> Binary: 0100 0001
    pt2 = 0x42  # Character 'B' -> Binary: 0100 0010 (Altered by exactly 1 bit)
    
    print(f"[+] Plaintext 1 (P1):  {hex(pt1)} ({bin(pt1)[2:].zfill(8)})")
    print(f"[+] Plaintext 2 (P2):  {hex(pt2)} ({bin(pt2)[2:].zfill(8)})")
    print(f"[*] Initial Input Bit Difference: {count_differing_bits(pt1, pt2)} bit(s)\n")
    
    # Execute Multi-round cipher pipelines
    ct1 = encrypt_spn(pt1, custom_keys, ROUNDS)
    ct2 = encrypt_spn(pt2, custom_keys, ROUNDS)
    
    print("-" * 50)
    print(f"[==] Ciphertext 1 (C1): {hex(ct1)} ({bin(ct1)[2:].zfill(8)})")
    print(f"[==] Ciphertext 2 (C2): {hex(ct2)} ({bin(ct2)[2:].zfill(8)})")
    
    # Requirement 4: Calculate and Demonstrate the Avalanche Effect
    avalanche_bits = count_differing_bits(ct1, ct2)
    avalanche_percentage = (avalanche_bits / 8) * 100
    
    print("-" * 50)
    print(f"[RESULT] Avalanche Effect Analysis:")
    print(f" -> Changing a single input bit caused {avalanche_bits} bits to flip in the final cipher text output.")
    print(f" -> Cascade Mutation Rate: {avalanche_percentage:.1f}%")


if __name__ == "__main__":
    main()