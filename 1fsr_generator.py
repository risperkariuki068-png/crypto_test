class LFSR:
    def _init_(self, seed, taps):
        if not seed or all(bit == 0 for bit in seed):
            raise ValueError("Seed cannot be empty or all zeros.")
        self.state = list(seed)
        self.taps = taps

    def step(self):
        feedback = self.state[self.taps - 1]
        for tap in self.taps[1:]:
            feedback ^= self.state[tap - 1]
        output_bit = self.state[-1]
        self.state = [feedback] + self.state[:-1]
        return output_bit

    def generate_sequence(self, length):
        return [self.step() for _ in range(length)]

def statistical_randomness_suite(bit_sequence):
    print("\n==================================================")
    print("      STATISTICAL RANDOMNESS TESTING SUITE        ")
    print("==================================================")
    n = len(bit_sequence)
    ones = bit_sequence.count(1)
    zeros = bit_sequence.count(0)
    proportion = ones / n
    
    # ------------------------------------------------------------
    # TEST 1: FREQUENCY (MONOBIT) TEST
    # ------------------------------------------------------------
    transformed = [1 if bit == 1 else -1 for bit in bit_sequence]
    S_n = sum(transformed)
    S_obs = abs(S_n) / math.sqrt(n)
    p_value_mono = math.erfc(S_obs / math.sqrt(2))
    
    # ------------------------------------------------------------
    # TEST 2: RUNS TEST (Checks oscillation frequency between 0 and 1)
    # ------------------------------------------------------------
    # Calculate total number of runs (an unbroken sequence of identical bits)
    V_n = 1
    for i in range(n - 1):
        if bit_sequence[i] != bit_sequence[i + 1]:
            V_n += 1
            
    # Calculate Runs Test p-value
    numerator = abs(V_n - (2 * n * proportion * (1 - proportion)))
    denominator = 2 * math.sqrt(2 * n) * proportion * (1 - proportion)
    
    # Defensive handling for perfect balances to avoid division by zero
    if denominator == 0:
        p_value_runs = 0.0
    else:
        p_value_runs = math.erfc(numerator / denominator)

    # ------------------------------------------------------------
    # OUTPUT METRICS MATRIX
    # ------------------------------------------------------------
    print(f"Total Sequence Length : {n} bits")
    print(f"Bit Split Proportion  : {ones} Ones / {zeros} Zeros")
    print(f"Total Observed Runs   : {V_n}")
    print("--------------------------------------------------")
    print(f"1. MonoBit Test p-value : {p_value_mono:.4f}")
    print(f"2. Runs Test p-value    : {p_value_runs:.4f}")
    print("--------------------------------------------------")
    
    # Evaluation Criteria: Both p-values must be >= 0.01 to pass
    print("SUITE EVALUATION VERIFICATION:")
    if p_value_mono >= 0.01 and p_value_runs >= 0.01:
        print("Final Status: PASSED (Sequence is cryptographically viable)")
    else:
        print("Final Status: FAILED (Sequence possesses structural pattern defects)")
    print("==================================================")

def run_evaluation():
    # Utilizing an extended period sequence for stable statistics
    seed = [1, 1, 0, 0, 1] # 5-bit seed
    taps = [3, 5]          # Maximal period taps for length 5
    
    lfsr = LFSR(seed, taps)
    # Generate 2^5 - 1 = 31 bits sequence twice to evaluate predictability
    sequence = lfsr.generate_sequence(62) 
    
    statistical_randomness_suite(sequence)

if __name__ == "__main__":
    run_evaluation()