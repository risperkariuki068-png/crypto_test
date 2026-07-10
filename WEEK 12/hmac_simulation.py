import hmac
import hashlib

# --- Core Cryptographic Engine ---

def generate_hmac(secret_key, message):
    """Generates an HMAC-SHA256 signature for a message using a shared key."""
    key_bytes = secret_key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    
    # Compute the HMAC token using SHA-256
    digest = hmac.new(key_bytes, message_bytes, hashlib.sha256).hexdigest()
    return digest

def verify_hmac(secret_key, message, received_hmac):
    """Recomputes and verifies the HMAC token against the received variant."""
    computed_hmac = generate_hmac(secret_key, message)
    
    # hmac.compare_digest avoids timing attacks during verification loops
    if hmac.compare_digest(computed_hmac, received_hmac):
        return "Integrity Verified"
    else:
        return "Message Modified!"

# --- Automated Lab Test Scenarios ---

def run_lab_tests():
    print("=== Week 12 HMAC Verification Tests ===\n")
    
    # Setup baseline configuration parameters
    shared_key = "SuperSecretSharedKey123"
    original_message = "Transfer $500 to account 987654"
    
    print(f"Shared Secret Key:   {shared_key}")
    print(f"Original Payload:    '{original_message}'")
    
    # Client creates signature
    client_hmac = generate_hmac(shared_key, original_message)
    print(f"Client Generated HMAC: {client_hmac}\n")
    
    # Test Scenario A: Unchanged Message (Success Route)
    print("--- Test 1: Sending Unchanged Message ---")
    result_1 = verify_hmac(shared_key, original_message, client_hmac)
    print(f"Server Verification Result: {result_1}\n")
    
    # Test Scenario B: Modifying the Message (Tamper Detection)
    print("--- Test 2: Modifying Message Content During Transmission ---")
    tampered_message = "Transfer $5000 to account 987654" # Added extra zero
    print(f"Interception Message payload altered to: '{tampered_message}'")
    result_2 = verify_hmac(shared_key, tampered_message, client_hmac)
    print(f"Server Verification Result: {result_2}\n")
    
    # Test Scenario C: Changing the Secret Key (Authentication Failure)
    print("--- Test 3: Changing Secret Key on Server Side ---")
    wrong_server_key = "WrongSecretSharedKey999"
    print(f"Server checks using incorrect key parameter: {wrong_server_key}")
    result_3 = verify_hmac(wrong_server_key, original_message, client_hmac)
    print(f"Server Verification Result: {result_3}\n")

if __name__ == "__main__":
    run_lab_tests()