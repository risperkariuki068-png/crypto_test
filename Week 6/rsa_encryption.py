from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def rsa_encrypt(plaintext, public_key_path):
    # 1. Load the public key file from disk
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
        
    # 2. Encrypt using secure OAEP padding with SHA-256 hash function
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt(ciphertext, private_key_path):
    # 1. Load the private key file from disk
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
        
    # 2. Decrypt using matching OAEP padding parameters
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

def run_asymmetric_demo():
    print("==================================================")
    print("        RSA PUBLIC KEY ENCRYPTION ENGINE          ")
    print("==================================================")
    
    secret_message = b"Asymmetric Encryption Verification 2026"
    print(f"Original Plaintext: {secret_message.decode('utf-8')}")
    print(f"Message Length    : {len(secret_message)} bytes")

    # 1. Run Asymmetric Encryption
    print("\n[1/2] Loading public key and encrypting...")
    try:
        ciphertext = rsa_encrypt(secret_message, "rsa_public.pem")
        print(f"      Success! Encrypted Ciphertext (Hex Snapshot):")
        print(f"      {ciphertext.hex()[:60]}...")
        print(f"      Ciphertext Output Length: {len(ciphertext)} bytes")
    except FileNotFoundError:
        print("[ERROR] 'rsa_public.pem' not found! Run rsa_key_pair.py first.")
        return

    # 2. Run Asymmetric Decryption
    print("\n[2/2] Loading private key and decrypting...")
    restored_message = rsa_decrypt(ciphertext, "rsa_private.pem")
    print(f"      Success! Restored Plaintext: {restored_message.decode('utf-8')}")
    
    # 3. Verify Integrity
    print("\n--- ASYMMETRIC RUN VERIFICATION ---")
    if secret_message == restored_message:
        print("Integrity Check: SUCCESS (Key pair math fully valid)")
    else:
        print("Integrity Check: FAILED")
    print("==================================================")

if __name__ == "__main__":
    run_asymmetric_demo()