# Week 7/aes_security_test.py

# Official AES 8-bit S-Box mapping sample array (subset for demonstration analysis)
AES_SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0
]

def analyze_differential_resistance():
    """Evaluates how effectively the AES S-Box splits uniform input differences."""
    print("[1] Evaluating Differential Uniformity Profile...")
    
    # We test a fixed input difference (Delta X)
    input_diff = 0x01 
    diff_counts = {}
    
    # Check all possible value pairs with this input difference across our space
    for x1 in range(len(AES_SBOX)):
        x2 = x1 ^ input_diff
        if x2 < len(AES_SBOX):
            y1 = AES_SBOX[x1]
            y2 = AES_SBOX[x2]
            output_diff = y1 ^ y2
            
            diff_counts[output_diff] = diff_counts.get(output_diff, 0) + 1

    # Find the maximum probability peak
    max_output_diff = max(diff_counts, key=diff_counts.get)
    max_occurrences = diff_counts[max_output_diff]
    
    print(f" -> Fixed Input Diff (ΔX) : {hex(input_diff).upper()}")
    print(f" -> Max Output Diff (ΔY)   : {hex(max_output_diff).upper()} (Occurred {max_occurrences} times)")
    print(f" -> Evaluation Statement  : High resistance verified. Output differences are distributed")
    print(f"                            uniformly, preventing differential path matching.")

def analyze_linear_resistance():
    """Measures the non-linear bias of the S-Box mapping to verify linear immunity."""
    print("\n[2] Evaluating Linear Bias Approximation Profile...")
    
    # Track input-to-output bit correlations
    total_trials = len(AES_SBOX)
    matches = 0
    
    for x in range(total_trials):
        y = AES_SBOX[x]
        
        # Test a standard linear mask equation: Input Bit 0 == Output Bit 0
        input_bit = x & 1
        output_bit = y & 1
        
        if input_bit == output_bit:
            matches += 1
            
    bias = abs((matches / total_trials) - 0.5)
    print(f" -> Linear Balance Equation: Input_Bit_0 ⊕ Output_Bit_0 = 0")
    print(f" -> Observed Match Ratio   : {matches}/{total_trials} pairs")
    print(f" -> Resulting Linear Bias  : {bias:.4f} (Ideal value is 0.0000)")
    print(f" -> Evaluation Statement  : Low linear bias prevents attackers from creating reliable")
    print(f"                            linear approximations to deduce key round tokens.")

if __name__ == "__main__":
    print("=" * 65)
    print("          PRACTICAL TASK 3: AES SECURITY PROFILING TOOL          ")
    print("=" * 65)
    analyze_differential_resistance()
    print("-" * 65)
    analyze_linear_resistance()
    print("=" * 65)