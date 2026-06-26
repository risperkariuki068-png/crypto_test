# 1. Accept public values p and g
print("--- Diffie-Hellman Key Exchange Setup ---")
p = int(input("Enter the shared prime modulus (p): "))
g = int(input("Enter the shared base/generator (g): "))
# 2. Allow two users to choose private keys
print("\n--- Private Key Selection ---")
private_key_a = int(input("Alice, enter your private key (a): "))
private_key_b = int(input("Bob, enter your private key (b): "))

# 3. Generate public keys
public_key_a = pow(g, private_key_a, p)
public_key_b = pow(g, private_key_b, p)

print("\n--- Exchanging Public Keys ---")
print(f"Alice's Public Key sent to Bob: {public_key_a}")
print(f"Bob's Public Key sent to Alice: {public_key_b}")
# 4. Compute the shared secret
shared_secret_alice = pow(public_key_b, private_key_a, p)
shared_secret_bob = pow(public_key_a, private_key_b, p)

print("\n--- Calculating Shared Secrets ---")
print(f"Alice's calculated secret: {shared_secret_alice}")
print(f"Bob's calculated secret: {shared_secret_bob}")

# 5. Verify that both users obtain the same secret key
print("\n--- Verification ---")
if shared_secret_alice == shared_secret_bob:
    print(f"SUCCESS: Both secrets match! The shared secret key is: {shared_secret_alice}")
else:
    print("FAILURE: Secrets do not match. Check your mathematical logic.")