import hashlib
import os

def pad_message(message, block_size=4):
    """Pads the message with spaces so its length is divisible by block_size."""
    remainder = len(message) % block_size
    if remainder != 0:
        padding_needed = block_size - remainder
        message += " " * padding_needed
    return message

def split_into_blocks(message, block_size=4):
    """Splits a padded message into fixed-size chunks."""
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]

def merkle_damgard_hash(message, block_size=4):
    """Computes a custom hash using the iterative Merkle-Damgard approach."""
    iv = "INITIAL_VALUE_VECTOR_STATE_W11__".encode('utf-8')
    current_state = iv
    
    padded_msg = pad_message(message, block_size)
    blocks = split_into_blocks(padded_msg, block_size)
    
    for block in blocks:
        combination = current_state + block.encode('utf-8')
        current_state = hashlib.sha256(combination).digest()
    
    return current_state.hex()

# --- NEW EXTENDED FILE HANDLING FEATURES ---
HASH_FILE = "stored_hashes.txt"

def save_hash_to_file(message, file_path=HASH_FILE):
    """Generates the hash and stores both the message and hash in a text file."""
    digest = merkle_damgard_hash(message)
    with open(file_path, "w") as f:
        f.write(f"{message}\n{digest}")
    print(f"\n[✓] Successfully saved to '{file_path}'!")
    print(f"Generated Hash: {digest}")

def verify_message_integrity(new_message, file_path=HASH_FILE):
    """Compares the hash of a new message against the stored hash."""
    if not os.path.exists(file_path):
        print("\n[!] Error: No stored hash file found. Run Option 1 first.")
        return

    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        if len(lines) < 2:
            print("[!] Error: Stored hash file is corrupted.")
            return
        stored_message = lines[0]
        stored_hash = lines[1]

    # Hash the incoming message to verify against the baseline
    new_hash = merkle_damgard_hash(new_message)
    
    print("\n--- Integrity Verification ---")
    print(f"Original Stored Message: '{stored_message}'")
    print(f"Incoming Test Message:   '{new_message}'")
    print(f"Stored Baseline Hash:    {stored_hash}")
    print(f"New Computed Hash:       {new_hash}")
    
    if new_hash == stored_hash:
        print("\n[✓] SUCCESS: The hashes match perfectly. Data integrity intact!")
    else:
        print("\n[X] WARNING: Hashes do not match! The message has been MODIFIED.")

# --- Interactive Main Menu ---
def main():
    print("=== Enhanced Merkle-Damgård Hashing Application ===")
    print("1. Hash a new message and store to file")
    print("2. Verify a message against the stored file hash")
    choice = input("Select an option (1 or 2): ")

    if choice == "1":
        msg = input("Enter the original text message to secure: ")
        save_hash_to_file(msg)
    elif choice == "2":
        msg = input("Enter the message to test for alterations: ")
        verify_message_integrity(msg)
    else:
        print("[!] Invalid option selected.")

if __name__ == "__main__":
    main()