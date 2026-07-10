from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import os

# File paths config
DOCUMENT_FILE = "signed_document.txt"
SIGNATURE_FILE = "document_signature.sig"

def generate_and_save_keys():
    """Generates standard 2048-bit RSA keys."""
    print("[✓] Generating 2048-bit RSA key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_and_save_document(private_key, text_content):
    """Saves the document text and its RSA signature to separate files on disk."""
    # Step 2: Convert message string to bytes
    doc_bytes = text_content.encode('utf-8')
    
    # Step 3 & 4: Compute SHA-256 hash internally and sign with private key
    signature = private_key.sign(
        doc_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    # Step 5: Save the document content and signature to separate files
    with open(DOCUMENT_FILE, "w", encoding="utf-8") as doc_f:
        doc_f.write(text_content)
        
    with open(SIGNATURE_FILE, "wb") as sig_f:
        sig_f.write(signature)
        
    print(f"[✓] Content saved successfully to '{DOCUMENT_FILE}'")
    print(f"[✓] Cryptographic signature saved to '{SIGNATURE_FILE}'")
    print(f"    Signature token: {signature.hex()[:50]}...")

def verify_document_signature(public_key):
    """Reads the files from disk and checks the signature against the text content."""
    if not os.path.exists(DOCUMENT_FILE) or not os.path.exists(SIGNATURE_FILE):
        print("[X] Error: Files are missing. Please sign a document first.")
        return

    # Read both items back from disk
    with open(DOCUMENT_FILE, "r", encoding="utf-8") as doc_f:
        current_content = doc_f.read()
        
    with open(SIGNATURE_FILE, "rb") as sig_f:
        stored_signature = sig_f.read()

    print("\n--- Initializing Disk Verification Check ---")
    print(f"Reading content from file: '{current_content}'")
    
    # Step 6: Verify the signature using the RSA public key
    try:
        public_key.verify(
            stored_signature,
            current_content.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("[✓] VERIFICATION RESULT: SUCCESS! The document is authentic and unmodified.")
    except InvalidSignature:
        print("[X] VERIFICATION RESULT: FAILED! Unauthorized modification detected.")

# --- Interactive Application Execution Loop ---
def main():
    print("=== Secure Digital Document Signing System ===")
    private_key, public_key = generate_and_save_keys()
    print()

    while True:
        print("\nManagement Options:")
        print("1. Write, Sign, and Save a New Document")
        print("2. Verify Current Saved Document Integrity")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            user_text = input("Enter the document text or system instruction: ")
            sign_and_save_document(private_key, user_text)
        elif choice == "2":
            verify_document_signature(public_key)
        elif choice == "3":
            print("System closing.")
            break
        else:
            print("[!] Invalid input choice. Try again.")

if __name__ == "__main__":
    main()