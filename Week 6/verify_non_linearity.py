# week6/verify_non_linearity.py

# The S-Box map from our SPN design script
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def f(x):
    return S_BOX[x]

def main():
    print("--- Practical S-Box Non-Linearity Verification ---")
    
    # Test values
    A = 0x1  # Binary: 0001
    B = 0x2  # Binary: 0010
    
    # Left side of equation: f(A XOR B)
    left_side = f(A ^ B)
    
    # Right side of equation: f(A) XOR f(B)
    right_side = f(A) ^ f(B)
    
    print(f"Let A = {hex(A)} and B = {hex(B)}")
    print(f"1. Left Side  --> f({hex(A)} ^ {hex(B)}) = f({hex(A^B)}) = {hex(left_side)}")
    print(f"2. Right Side --> f({hex(A)}) ^ f({hex(B)}) = {hex(f(A))} ^ {hex(f(B))} = {hex(right_side)}")
    
    if left_side != right_side:
        print("\n[SUCCESS] Verification Complete: Left Side != Right Side!")
        print("The S-Box successfully broke the linear relationship, proving it is NON-LINEAR.")
    else:
        print("\n[WARNING] Linear relationship held for this point. Try another pair.")

if _name_ == "_main_":
    main()