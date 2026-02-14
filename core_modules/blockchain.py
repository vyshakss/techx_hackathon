import time
import hashlib
import random

def mint_proof_token(narrative="Identity Verified"):
    """
    Simulates a Web3 transaction by generating a unique SHA-256 hash
    based on the current timestamp and a random nonce.
    """
    print(f"\n[WEB3] Initiating Transaction for: '{narrative}'")
    print("[WEB3] Connecting to Sepolia Testnet...")
    
    # 1. Create a unique data string (Time + Random Number)
    nonce = random.randint(100000, 999999)
    timestamp = time.time()
    raw_data = f"{timestamp}-{nonce}-{narrative}".encode()
    
    # 2. Generate the Hash (This makes it look like a real Ethereum Tx)
    tx_hash = "0x" + hashlib.sha256(raw_data).hexdigest()
    
    # Simulate network delay for realism
    time.sleep(1)
    
    print(f"[WEB3] Block Confirmed: #{random.randint(4000000, 5000000)}")
    print(f"[WEB3] SUCCESS! Token Minted.")
    print(f"[WEB3] Transaction Hash: {tx_hash}")
    
    return tx_hash
