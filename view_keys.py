from core_modules.blockchain import mint_proof_token
import time

print("\n--- 🔐 GENERATING 5 UNIQUE KEYS ---")

for i in range(1, 6):
    # We pass a dummy narrative just to trigger the hash generation
    narrative = f"Test Run #{i}"
    
    # This calls your function which returns the random hash
    key = mint_proof_token(narrative)
    
    print(f"Key #{i}: {key}")
    print("-" * 40)
    time.sleep(0.5) # Small pause to ensure timestamps differ
