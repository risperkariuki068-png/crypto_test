import random
import math

# --- ElGamal Cryptosystem: 5-Message Batch Evaluation ---

# 1. Setup Fixed Keys
p = 29              # Shared prime modulus
g = 2               # Shared base generator
private_key_d = 7   # Private key

# Public key e1 = (g^d) % p
e1 = pow(g, private_key_d, p)

print("--- ElGamal Batch System Initialized ---")
print(f"Public Key (p, g, e1): ({p}, {g}, {e1})\n")

# We will collect exactly 5 messages from the terminal
messages = []
print("Please enter 5 plaintext integers to test:")
for i in range(1, 6):
    msg = int(input(f"Enter message {i} (must be < {p}): "))
    messages.append(msg)

print("\n=== Processing Encrypt/Decrypt Cycle ===\n")

# 2 & 3. Encrypt and Decrypt each message
for index, message in enumerate(messages, 1):
    # Choose a random k that is coprime to p-1 (28)
    # Valid choices for k mod 28 include 3, 5, 9, 11, 13, 15...
    k = random.choice([3, 5, 9, 11, 13, 15])
    
    # Encryption
    c1 = pow(g, k, p)
    c2 = (message * pow(e1, k, p)) % p
    
    # Decryption
    blind_factor_inv = pow(pow(c1, private_key_d, p), -1, p)
    decrypted_message = (c2 * blind_factor_inv) % p
    
    # Output metrics
    print(f"Result {index} | Plaintext: {message} | k: {k} -> Ciphertext: ({c1}, {c2}) -> Decrypted: {decrypted_message}")

print("\n========================================")
print("--- Theoretical Requirement 4 Answer ---")
print("Why a fresh random value (k) is essential:")
print("If the same value of k is reused to encrypt two different messages (M1 and M2),")
print("the ciphertexts will share the exact same C1 component. An eavesdropper can divide")
print("the two C2 components to reveal the exact plaintext ratio: C2_1 / C2_2 = M1 / M2.")
print("This completely breaks the security of the encryption, making k-reuse fatal.")
print("========================================")