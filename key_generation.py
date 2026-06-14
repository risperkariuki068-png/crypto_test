import os
import secrets

def generate_aes_keys():
    print("==================================================")
    print("      SECURE KEY GENERATION PROCESS ENGINE        ")
    print("==================================================")
    
    # Method 1: Using os.urandom (Calls the OS kernel cryptographic pool)
    # Recommended for lower-level library operations
    key_urandom = os.urandom(32) # 32 bytes = 256 bits
    
    # Method 2: Using the 'secrets' module (Modern Python standard for CSPRNG)
    # Designed specifically for managing security secrets and tokens
    key_secrets = secrets.token_bytes(32) # 32 bytes = 256 bits
    
    print(f"[1/3] AES-256 Key generated via os.urandom:")
    print(f"      Raw Bytes Hex : {key_urandom.hex()}")
    print(f"      Total Length  : {len(key_urandom)} bytes ({len(key_urandom) * 8} bits)")
    
    print(f"\n[2/3] AES-256 Key generated via secrets module:")
    print(f"      Raw Bytes Hex : {key_secrets.hex()}")
    print(f"      Total Length  : {len(key_secrets)} bytes ({len(key_secrets) * 8} bits)")
    
    # ------------------------------------------------------------
    # PERSISTENCE: Saving keys securely to disk
    # ------------------------------------------------------------
    print("\n[3/3] Exporting secure key file locally...")
    key_filename = "secret_aes_256.key"
    
    # Save the key in its raw binary form for high-security workflows
    with open(key_filename, "wb") as key_file:
        key_file.write(key_secrets)
        
    print(f"      Success: Key safely exported to 'C:\\crypto_test\\{key_filename}'")
    print("==================================================")

if __name__ == "__main__":
    generate_aes_keys()