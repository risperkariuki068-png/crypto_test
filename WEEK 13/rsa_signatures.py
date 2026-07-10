from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

def run_digital_signature_system():
    print("=== Week 13: 2048-bit RSA Digital Signature System ===\n")
    
    # Requirement 1: Generate a robust 2048-bit RSA public/private key pair
    print("[1/6] Generating secure 2048-bit RSA key pair... (This might take a moment)")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    print("[✓] Keys successfully generated!\n")
    
    # Requirement 2: Prompt the user to enter a message
    user_message = input("[2/6] Enter a text message to digitally sign: ")
    message_bytes = user_message.encode('utf-8')
    
    # Requirement 3: Hash and sign the message using the RSA private key
    # This automatically computes the SHA-256 hash and applies PKCS#1 v1.5 padding
    signature = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print(f"\n[3/6] Signature generated successfully!")
    print(f"Signature Hex (Truncated): {signature.hex()[:60]}...\n")
    
    # Requirement 4: Verify the signature using the RSA public key
    print("[4/6] Verifying original signature against original message...")
    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("[✓] Verification Result: SUCCESS! The signature is valid and authentic.")
    except InvalidSignature:
        print("[X] Verification Result: FAILED! Invalid signature detected.")
        
    # Requirement 5 & 6: Modify one character in the message and verify again
    print("\n[5/6] Simulating an unauthorized alteration attack...")
    # Let's slightly tweak the last character of the message to simulate tampering
    tampered_message = user_message[:-1] + ("?" if user_message[-1] != "?" else "!")
    print(f"Original Message: '{user_message}'")
    print(f"Tampered Message: '{tampered_message}'")
    
    print("\n[6/6] Verifying original signature against the tampered payload...")
    try:
        public_key.verify(
            signature,
            tampered_message.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("[✓] Verification Result: SUCCESS! (This should not happen if secure)")
    except InvalidSignature:
        print("[X] Verification Result: FAILED! Integrity check blocked the transaction.")
        print("\nExplanation: Because the message hash changed by even one bit, the decrypted")
        print("signature no longer matches the calculated digest, successfully catching the modification.")

if __name__ == "__main__":
    run_digital_signature_system()