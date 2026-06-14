from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def run_rsa_key_generation():
    print("==================================================")
    print("         RSA ASYMMETRIC KEY PAIR GENERATION       ")
    print("==================================================")
    
    # 1. Generate the private key using secure primes
    # 2048 bits is the standard cryptographic industry minimum length
    # 65537 is the standard Fermat prime public exponent (e)
    print("[1/3] Generating 2048-bit RSA private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # 2. Extract the mathematically paired public key
    print("[2/3] Extracting the corresponding public key...")
    public_key = private_key.public_key()
    
    # 3. Serialize the private key into a readable PEM format
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 4. Serialize the public key into a readable PEM format
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Display the structured text blocks on screen
    print("\n--- PRIVATE KEY SNAPSHOT (PEM) ---")
    print(pem_private.decode('utf-8')[:120] + "\n...[TRUNCATED BY SYSTEM]...\n-----END RSA PRIVATE KEY-----")
    
    print("\n--- PUBLIC KEY BLOCK (PEM) ---")
    print(pem_public.decode('utf-8').strip())
    print("--------------------------------------------------")
    
    # 5. Export key files directly to local persistent disk storage
    print("[3/3] Saving key tokens to local storage directory...")
    with open("rsa_private.pem", "wb") as f:
        f.write(pem_private)
    with open("rsa_public.pem", "wb") as f:
        f.write(pem_public)
        
    print("      Success: 'rsa_private.pem' and 'rsa_public.pem' saved.")
    print("==================================================")

if __name__ == "__main__":
    run_rsa_key_generation()