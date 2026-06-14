# Week 7/structure_evaluation.py

# Standard 4-bit S-Box for consistency
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def spn_round_simulation(data_byte, key_byte):
    """Simulates a standard uniform SPN round: Key Mix -> Substitution -> Identity."""
    # 1. Key Mixing
    mixed = data_byte ^ key_byte
    
    # 2. Substitution (Splitting 8-bit into two 4-bit nibbles)
    high_nibble = (mixed >> 4) & 0x0F
    low_nibble = mixed & 0x0F
    
    sub_high = S_BOX[high_nibble]
    sub_low = S_BOX[low_nibble]
    
    # Combine back to an 8-bit output block
    return (sub_high << 4) | sub_low

def feistel_round_simulation(data_byte, key_byte):
    """Simulates a Feistel round: Splits block in half, processes only the right side."""
    # Split 8-bit block into Left (4 bits) and Right (4 bits)
    left = (data_byte >> 4) & 0x0F
    right = data_byte & 0x0F
    
    # Feistel Round Function F: S-Box mapping of (Right XOR Key)
    round_function_input = right ^ (key_byte & 0x0F)
    f_output = S_BOX[round_function_input]
    
    # New Left becomes old Right. New Right becomes old Left XOR F(Right)
    new_left = right
    new_right = left ^ f_output
    
    return (new_left << 4) | new_right

if __name__ == "__main__":
    print("=" * 60)
    print("        PRACTICAL TASK 3: ARCHITECTURE RUNTIME LOG       ")
    print("=" * 60)
    
    # Sample test data: Input Byte 0x4A with Round Key 0xF5
    input_val = 0x4A
    round_key = 0xF5
    
    print(f"Initial State Input : Hex: {hex(input_val).upper()}   | Binary: {bin(input_val)[2:].zfill(8)}")
    print(f"Round Key Token     : Hex: {hex(round_key).upper()}   | Binary: {bin(round_key)[2:].zfill(8)}")
    print("-" * 60)
    
    # Execute SPN Execution Path
    spn_out = spn_round_simulation(input_val, round_key)
    print(f"[SPN Round Output]    : Hex: {hex(spn_out).upper()}   | Binary: {bin(spn_out)[2:].zfill(8)}")
    print(" -> Observation: The entire 8-bit block changed uniformly.")
    print("-" * 60)
    
    # Execute Feistel Execution Path
    feistel_out = feistel_round_simulation(input_val, round_key)
    print(f"[Feistel Round Output]: Hex: {hex(feistel_out).upper()}   | Binary: {bin(feistel_out)[2:].zfill(8)}")
    print(" -> Observation: Left half mirrors old Right; only Right half was scrambled.")
    print("=" * 60)