import random

# --- 1. MATH FOUNDATIONS & PRIMALITY TESTING ---

def gcd(a, b):
    """Euclidean algorithm to find the greatest common divisor."""
    while b:
        a, b = b, a % b
    return a

def is_prime_miller_rabin(n, k=5):
    """Tests if a number is prime using the Miller-Rabin algorithm."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False

    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def pollards_rho(n):
    """Pollard's rho algorithm to factor a small composite number n."""
    if n % 2 == 0: return 2
    x = random.randint(2, n - 2)
    y = x
    c = random.randint(1, n - 1)
    g = 1
    while g == 1:
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        g = gcd(abs(x - y), n)
    return g

# --- 2. CORE RSA OPERATIONS ---

def generate_keys():
    print("--- Step 1: RSA Key Generation ---")
    # Choosing two small primes for educational demonstration
    p, q = 61, 53
    
    # Verify using Miller-Rabin requirement
    print(f"Testing primality of p={p}: {is_prime_miller_rabin(p)}")
    print(f"Testing primality of q={q}: {is_prime_miller_rabin(q)}")
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose standard public exponent e
    e = 17
    while gcd(e, phi) != 1:
        e += 2
        
    # Calculate private exponent d using modular inverse
    d = pow(e, -1, phi)
    
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})\n")
    return (e, n), (d, n), p, q

# --- 3. MAIN EXECUTION FLOW ---

# Run Key Generation
public_key, private_key, p, q = generate_keys()
e, n = public_key
d, _ = private_key

# Accept plaintext message integer
message = int(input(f"Enter a plaintext integer message to encrypt (must be < {n}): "))

# Encrypt & Decrypt
ciphertext = pow(message, e, n)
decrypted_message = pow(ciphertext, d, n)

print("\n--- Encryption / Decryption ---")
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted Message: {decrypted_message}")

# Digital Signature Mechanics
signature = pow(message, d, n)
verified_message = pow(signature, e, n)

print("\n--- Digital Signature ---")
print(f"Generated Digital Signature: {signature}")
print(f"Verification Check: Signature recovers original message -> {verified_message == message}")

# Demonstrate Security Risk of Small Primes
print("\n--- Security Risk Demonstration (Pollard's Rho Crack) ---")
print(f"An eavesdropper intercepts the public modulus n = {n}")
print("Attempting to factor n using Pollard's rho algorithm...")
factored_p = pollards_rho(n)
factored_q = n // factored_p
print(f"CRACKED! Found prime factors: p = {factored_p}, q = {factored_q}")