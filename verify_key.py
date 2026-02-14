from core_modules.blockchain import mint_proof_token

print("--- TESTING RANDOM KEY GENERATION ---\n")

# Run 1
print("Run #1:")
key1 = mint_proof_token("User Test 1")
print("-" * 30)

# Run 2
print("Run #2:")
key2 = mint_proof_token("User Test 2")
print("-" * 30)

# Run 3
print("Run #3:")
key3 = mint_proof_token("User Test 3")
print("-" * 30)

if key1 != key2 and key2 != key3:
    print("\n[TEST PASSED] All keys are unique and random!")
else:
    print("\n[TEST FAILED] Keys are identical (Static).")
