# week6/compare_structures.py

def mock_spn_round(block):
    """SPN: Processes the entire block simultaneously."""
    # Simulating a simple substitution + permutation on the whole block
    s_box_layer = (block + 3) % 16
    p_box_layer = ((s_box_layer & 1) << 3) | (s_box_layer >> 1)
    return p_box_layer

def mock_feistel_round(left, right, round_key):
    """Feistel: Splits block in half. Only modifies ONE half per round."""
    # Round function f(R, K) = (Right + Key) % 16
    round_function = (right + round_key) % 16
    
    # New Right becomes old Left XORed with the round function output
    new_right = left ^ round_function
    # New Left is just the unmodified old Right
    new_left = right
    
    return new_left, new_right

def main():
    print("--- Practical Architectural Evaluation: SPN vs Feistel ---")
    
    original_hex = 0xAB  # 8-bit block split into Left (A) and Right (B)
    left_half = 0xA
    right_half = 0xB
    
    print(f"Initial Input Block: {hex(original_hex)} (Left: {hex(left_half)}, Right: {hex(right_half)})")
    print("-" * 50)
    
    # Execution 1: SPN execution path
    spn_out_l = mock_spn_round(left_half)
    spn_out_r = mock_spn_round(right_half)
    print(f"[SPN Path] Complete Block Transformed: Left -> {hex(spn_out_l)}, Right -> {hex(spn_out_r)}")
    
    # Execution 2: Feistel execution path
    feistel_l, feistel_r = mock_feistel_round(left_half, right_half, round_key=5)
    print(f"[Feistel Path] Half-Block Transformed:  Left -> {hex(feistel_l)} (Unmodified Right), Right -> {hex(feistel_r)} (XORed Result)")

if __name__ == "__main__":
    main()