import ollama
import json
import random
import time
from pydantic import BaseModel, Field

# --- 1. DATA STRUCTURE ---
class ProofOfLifeChallenge(BaseModel):
    cognitive_question: str = Field(description="A short riddle.")
    target_color: str = Field(description="One of: red, blue, green, yellow.")
    target_emotion: str = Field(description="One of: happy, surprise, fear, sad, neutral.")

# --- 2. FALLBACK (Safety Net) ---
def get_fallback_challenge():
    fallbacks = [
        ("What has keys but can't open locks?", "green", "surprise"),
        ("What comes down but never goes up?", "red", "happy"),
        ("What has a face but no eyes?", "blue", "fear"),
        ("I'm tall when young, short when old.", "yellow", "sad")
    ]
    q, c, e = random.choice(fallbacks)
    return ProofOfLifeChallenge(
        cognitive_question=f"[FALLBACK] {q}",
        target_color=c,
        target_emotion=e
    )

# --- 3. THE BRAIN (Ollama) ---
def generate_challenge():
    print("[ORCHESTRATOR] Connecting to Local Llama 3.2...")
    
    # --- THIS WAS MISSING IN YOUR FILE ---
    prompt = """
    Generate a JSON object for a security challenge.
    1. cognitive_question: A simple riddle (max 10 words).
    2. target_color: red, blue, green, or yellow.
    3. target_emotion: happy, surprise, fear, sad, or neutral.
    Output ONLY JSON.
    """
    # -------------------------------------

    try:
        # Now 'prompt' exists, so this line will work
        response = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'user', 'content': prompt}
        ], format=ProofOfLifeChallenge.model_json_schema())

        # DEBUG PRINTS (To prove it's local)
        print(f"[DEBUG] 🧠 Model Used: {response['model']}")
        print(f"[DEBUG] ⏱️  Time: {response['total_duration'] / 1e9:.2f}s")

        data = json.loads(response['message']['content'])
        return ProofOfLifeChallenge(**data)

    except Exception as e:
        print(f"[ERROR] Ollama connection failed: {e}")
        return get_fallback_challenge()

# --- 4. THE NOTARY (Blockchain Log) ---
def generate_blockchain_narrative(color, emotion, timestamp):
    print("\n[ORCHESTRATOR] Generating unique Blockchain Narrative via LLM...")
    
    prompt = f"""
    You are a digital notary. Write a ONE-sentence log entry.
    Details: {color} object, {emotion} face, Time: {timestamp}.
    Style: Cyberpunk.
    """

    try:
        response = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']
        
    except Exception as e:
        return f"Standard Verification Log: {color} object / {emotion} face confirmed."
