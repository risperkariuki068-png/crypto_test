import hmac
import hashlib
import os

# --- Configuration Constants ---
SHARED_KEY = "SecureSystemSharedSecretKey789!"
LOG_FILE = "integrity_log.txt"
TARGET_FILE = "document.txt"

def calculate_file_hmac(file_path, secret_key):
    """Reads a file from disk and computes its HMAC-SHA256 signature."""
    key_bytes = secret_key.encode('utf-8')
    hasher = hmac.new(key_bytes, digestmod=hashlib.sha256)
    
    # Read the file in binary mode to handle any encoding or line endings safely
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
            
    return hasher.hexdigest()

def initialize_baseline_file():
    """Step 1, 2, & 3: Creates a sample text file and logs its initial baseline HMAC."""
    # Create a dummy file if it doesn't exist yet
    if not os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "w") as f:
            f.write("System Configuration Payload: Access Authorized.")
        print(f"[✓] Created standard test file: '{TARGET_FILE}'")
        
    # Calculate the authentic signature
    baseline_hmac = calculate_file_hmac(TARGET_FILE, SHARED_KEY)
    
    # Store the filename and the HMAC together in the log file
    with open(LOG_FILE, "w") as log:
        log.write(f"{TARGET_FILE}\n{baseline_hmac}")
        
    print(f"[✓] Baseline signature logged inside '{LOG_FILE}'")
    print(f"    HMAC: {baseline_hmac}\n")

def run_verification_check(secret_key_to_use):
    """Step 4 & 5: Compares current file state against the saved log file."""
    if not os.path.exists(LOG_FILE) or not os.path.exists(TARGET_FILE):
        print("[!] Error: Initialization required. Please run option 1 first.")
        return

    # Read baseline parameters from disk log
    with open(LOG_FILE, "r") as log:
        lines = log.read().splitlines()
        stored_filename = lines[0]
        stored_hmac = lines[1]

    # Recompute the HMAC based on current state of the target file
    try:
        current_hmac = calculate_file_hmac(TARGET_FILE, secret_key_to_use)
    except Exception as e:
        print("[X] Status: VERIFICATION FAILED (Cannot read target file)")
        return

    print("--- Running Disk Integrity Verification ---")
    print(f"Target File:         {TARGET_FILE}")
    print(f"Logged Baseline:     {stored_hmac}")
    print(f"Current Evaluation:  {current_hmac}")

    # Check for unauthorized tampering or key failures
    if not hmac.compare_digest(secret_key_to_use.encode(), SHARED_KEY.encode()):
        print("\n[X] Status: VERIFICATION FAILED (Invalid Secret Key Provided)")
    elif hmac.compare_digest(current_hmac, stored_hmac):
        print("\n[✓] Status: AUTHENTIC (The file has not been modified)")
    else:
        print("\n[!] Status: MODIFIED (Unauthorized changes detected inside the file!)")

def main():
    while True:
        print("=== File Integrity Verification System ===")
        print("1. Initialize Baseline (Create file and log secure signature)")
        print("2. Run Verification Check (Using correct shared key)")
        print("3. Run Verification Check (Simulate key failure with wrong key)")
        print("4. Exit")
        choice = input("Select an option (1-4): ")
        print()

        if choice == "1":
            initialize_baseline_file()
        elif choice == "2":
            run_verification_check(SHARED_KEY)
        elif choice == "3":
            run_verification_check("WrongMaliciousKey111")
        elif choice == "4":
            print("System shutting down.")
            break
        else:
            print("[!] Invalid option. Please pick a choice between 1 and 4.\n")

if __name__ == "__main__":
    main()