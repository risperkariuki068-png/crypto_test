import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

def transmit_secure_message(plaintext_message, public_key_path):
    print("[1/2] TRANSMITTER SIDE: Preparing secure transmission package...")
    
    # 1. Generate a temporary, single-use symmetric AES-256 key and IV
    aes_key = os.urandom(32)
    iv = os.urandom(16)
    
    # 2. Encrypt the actual large message payload using AES-CBC
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext_message) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_payload = encryptor.update(padded_data) + encryptor.finalize()
    
    # 3. Encrypt the temporary AES key using the recipient's RSA Public Key
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
        
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    print("      -> Message payload encrypted via fast AES-256.")
    print("      -> Shared symmetric key safely locked inside RSA envelope.")
    
    # The transmission package contains: the encrypted key, the IV, and the encrypted message
    return encrypted_aes_key, iv, encrypted_payload

def receive_secure_message(encrypted_aes_key, iv, encrypted_payload, private_key_path):
    print("\n[2/2] RECEIVER SIDE: Opening secure transmission package...")
    
    # 1. Load the private key to unlock the transmission envelope
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
        
    # 2. Decrypt the symmetric AES key using RSA Private Key
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    # 3. Use the recovered AES key to decrypt the large payload data
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(encrypted_payload) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    print("      -> Symmetric AES envelope key recovered using RSA math.")
    print("      -> Ciphertext payload smoothly decrypted.")
    return plaintext

def run_hybrid_simulation():
    print("==================================================")
    print("      SECURE TRANSMISSION: HYBRID CRYPTOSYSTEM    ")
    print("==================================================")
    
    transmitted_payload = b"Top Secret Transmission: Hybrid Cryptography is Operational!"
    print(f"Plaintext to Send: {transmitted_payload.decode('utf-8')}\n")
    
    # Simulate transmission over unsecured channel
    enc_key, iv, enc_payload = transmit_secure_message(transmitted_payload, "rsa_public.pem")
    
    # Simulate receiving the packet at destination
    recovered_payload = receive_secure_message(enc_key, iv, enc_payload, "rsa_private.pem")
    
    print("\n--- HYBRID SYSTEM PIPELINE VERIFICATION ---")
    print(f"Received Message: {recovered_payload.decode('utf-8')}")
    if transmitted_payload == recovered_payload:
        print("Transmission Link Status: SECURE & FULLY VERIFIED")
    else:
        print("Transmission Link Status: CORRUPTED/TAMPERED")
    print("==================================================")

if __name__ == "__main__":
    run_hybrid_simulation()