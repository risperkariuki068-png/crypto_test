# Week 7/cryptanalysis_toolkit.py
import collections

# A standard 4-bit S-Box mapping table for our test suite
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def analyze_sbox_distribution():
    """Automates input difference tracking, frequency analysis, and bias measurements."""
    print("=" * 65)
    print("         CORE LOGISTIC RUN: AUTOMATED CRYPTANALYSIS TOOLKIT     ")
    print("=" * 65)
    
    # 1. & 2. Calculate Input Differences & Perform Output Frequency Analysis
    # We test a fixed structural input difference of 0x01
    target_input_diff = 0x01
    differential_distribution = []
    
    for pt1 in range(16):
        pt2 = pt1 ^ target_input_diff
        ct1 = S_BOX[pt1]
        ct2 = S_BOX[pt2]
        output_diff = ct1 ^ ct2
        differential_distribution.append(output_diff)
        
    # Count frequencies of each output difference
    frequency_map = collections.Counter(differential_distribution)
    
    print(f"[✔️] Target Input XOR Difference Evaluated: {hex(target_input_diff).upper()}")
    print("\n--- Output Difference Frequency Distribution Analysis ---")
    print(f" {'Output Diff (Hex)':<20} | {'Occurrence Count':<18} | {'Probability':<10}")
    print("-" * 65)
    
    for out_diff, count in sorted(frequency_map.items()):
        probability = count / 16.0
        print(f"  {hex(out_diff).upper():<19} | {count:<18} | {probability:<10.2%}")
        
    # 3. Measure Statistical Bias
    # Let's measure the bit-bias for Output Bit 0 relative to Input Bit 0
    linear_matches = 0
    for x in range(16):
        y = S_BOX[x]
        if (x & 1) == (y & 1):  # Checking correlation between lowest bits
            linear_matches += 1
            
    bias = abs((linear_matches / 16.0) - 0.5)
    
    # 4. Display Results Automatically
    print("-" * 65)
    print("--- Statistical Bias & Metric Profiles ---")
    print(f" -> Linear Correlation Match Count : {linear_matches}/16 states")
    print(f" -> Computed Linear Selection Bias : {bias:.4f}")
    
    max_diff_count = max(frequency_map.values())
    max_diff_prob = max_diff_count / 16.0
    print(f" -> Max Differential Probability   : {max_diff_prob:.2%}")
    print("=" * 65)

if __name__ == "__main__":
    analyze_sbox_distribution()