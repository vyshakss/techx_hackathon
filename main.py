import cv2
import sys
import time
from core_modules.orchestrator import generate_challenge, generate_blockchain_narrative
from core_modules.vision import verify_physical_liveness
from core_modules.emotion import analyze_emotion
from core_modules.blockchain import mint_proof_token # Ensure this function exists in blockchain.py

def run_security_gate():
    # --- DEBUG BANNER ---
    print("\n" + "="*60)
    print("      [SYSTEM] PROOF OF LIFE: LOCAL AI MODE ACTIVE      ")
    print("="*60 + "\n")
    
    # 1. BRAIN: Generate Challenge using Local LLM
    challenge = generate_challenge()
    if not challenge: return
    
    # 2. INSTRUCTIONS
    print(f"\n--- CHALLENGE ISSUED ---")
    print(f"1. QUESTION: {challenge.cognitive_question}")
    print(f"2. ACTION: Hold a {challenge.target_color.upper()} object.")
    print(f"3. EMOTION: You must look {challenge.target_emotion.upper()}!")

    # 3. EYES: Vision Loop (Checks for Color Object)
    # Returns: (True/False, The_Captured_Image)
    verified, proof_frame = verify_physical_liveness(challenge.target_color)

    if verified and proof_frame is not None:
        print("\n[STEP 1 SUCCESS] Color object verified.")
        
        # 4. FACE: Emotion Analysis
        print("[STEP 2] Analyzing facial expression from the captured frame...")
        
        # We pass the captured frame to DeepFace
        detected_emotion = analyze_emotion(proof_frame)
        
        print(f" > AI Detected: {detected_emotion}")
        print(f" > Challenge Required: {challenge.target_emotion}")

        # Fuzzy matching (e.g. 'happy' matches 'happiness')
        required = challenge.target_emotion.lower()
        detected = detected_emotion.lower()

        if required in detected or detected in required:
            print("\n[ACCESS GRANTED] Identity, Liveness, and Emotion confirmed.")
            
            # --- 5. AI NOTARY: Generate Unique Log ---
            current_time = time.ctime()
            narrative = generate_blockchain_narrative(
                challenge.target_color, 
                detected_emotion, 
                current_time
            )
            print(f"\n[AI NOTARY LOG]: {narrative}")
            
            # --- 6. BLOCKCHAIN: Mint the Token ---
            # We pass the AI narrative to be "stored" (printed) by the blockchain module
            mint_proof_token() 
            
        else:
            print(f"\n[ACCESS DENIED] Emotion mismatch. Expected {required}, got {detected}")
            
    else:
        print("\n[ACCESS DENIED] Liveness verification failed (Color check).")

if __name__ == "__main__":
    run_security_gate()
