# Week 7/differential_analysis.py

# A standard 4-bit S-Box mapping table (similar to our SPN implementations)
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def compute_xor_difference(val1, val2):
    """Computes the bitwise XOR difference between two values."""
    return val1 ^ val2

def run_differential_analysis(pt1, pt2):
    """Simulates how an input difference propagates through the substitution layer."""
    # 1. Calculate input difference
    input_diff = compute_xor_difference(pt1, pt2)
    
    # 2. Pass both plaintexts through the non-linear S-Box layer
    ct1 = S_BOX[pt1 & 0x0F]  # Ensure we stay within 4-bit boundaries
    ct2 = S_BOX[pt2 & 0x0F]
    
    # 3. Calculate output difference
    output_diff = compute_xor_difference(ct1, ct2)
    
    # Print the formatted analysis report terminal log
    print("=" * 55)
    print("        DIFFERENTIAL CRYPTANALYSIS SIMULATION TRAIL    ")
    print("=" * 55)
    print(f"Plaintext 1 (P1)     : Hex: {hex(pt1).upper()}   | Binary: {bin(pt1)[2:].zfill(4)}")
    print(f"Plaintext 2 (P2)     : Hex: {hex(pt2).upper()}   | Binary: {bin(pt2)[2:].zfill(4)}")
    print(f"Input Difference (ΔX): Hex: {hex(input_diff).upper()}   | Binary: {bin(input_diff)[2:].zfill(4)}")
    print("-" * 55)
    print(f"S-Box Output 1 (C1)  : Hex: {hex(ct1).upper()}   | Binary: {bin(ct1)[2:].zfill(4)}")
    print(f"S-Box Output 2 (C2)  : Hex: {hex(ct2).upper()}   | Binary: {bin(ct2)[2:].zfill(4)}")
    print(f"Output Diff (ΔY)     : Hex: {hex(output_diff).upper()}   | Binary: {bin(output_diff)[2:].zfill(4)}")
    print("=" * 55)
    
    # Observation summary
    print("\n[Observation]:")
    print(f"An input difference of {hex(input_diff).upper()} mutated into an output difference of {hex(output_diff).upper()}.")
    if input_diff == output_diff:
        print("⚠️ Warning: Linear property detected for this specific pair!")
    else:
        print("✔️ Success: Non-linear diffusion behavior observed. The difference mutated!")
    print("=" * 55)

if __name__ == "__main__":
    print("--- Practical Task 1: Differential Cryptanalysis ---")
    # Prompt the user to enter two 4-bit plaintext inputs (0 to 15 in decimal or hex)
    try:
        p1 = int(input("Enter Plaintext 1 (Hex character, e.g., 4): "), 16)
        p2 = int(input("Enter Plaintext 2 (Hex character, e.g., 5): "), 16)
        run_differential_analysis(p1, p2)
    except ValueError:
        print("[Error] Please enter valid hex inputs (0-F).")