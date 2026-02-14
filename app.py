import os
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, Response, jsonify, request
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import preprocess_input

app = Flask(__name__)

# --- CONFIGURATION ---
MODEL_PATH = 'core_modules/xception_deepfake.h5'
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
IMG_SIZE = (224, 224) # Match the size used in your 'Turbo' training
SECURITY_THRESHOLD = 0.85 # Strictness: 0-1 (higher = more secure)

# 1. Load the Model at startup (not in the route!)
print("[INFO] Loading Xception Model...")
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    print(f"[ERROR] Model not found at {MODEL_PATH}. Run training first.")
    model = None

# Load Face Detector
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

def get_deepfake_prediction(frame):
    """Processes a frame and returns the Liveness score."""
    if model is None: return "Error", 0.0

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "No Face Detected", 0.0

    # Process the first face found
    (x, y, w, h) = faces[0]
    face_roi = frame[y:y+h, x:x+w]
    
    # Preprocess for Xception
    face_input = cv2.resize(face_roi, IMG_SIZE)
    face_input = np.expand_dims(face_input, axis=0)
    face_input = preprocess_input(face_input) # Scales to -1 to 1

    # Predict
    score = model.predict(face_input, verbose=0)[0][0]
    label = "REAL" if score >= SECURITY_THRESHOLD else "FAKE"
    
    return label, float(score)

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html') # Ensure you have this file in /templates

@app.route('/verify', methods=['POST'])
def verify():
    """Triggered by the 'Initiate Verification' button."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"success": False, "error": "Could not access camera"})

    label, confidence = get_deepfake_prediction(frame)
    
    # 2. Integrate Blockchain logic if verification passes
    blockchain_tx = None
    if label == "REAL":
        blockchain_tx = mint_proof_token(confidence)

    return jsonify({
        "label": label,
        "confidence": f"{confidence:.2f}",
        "blockchain_tx": blockchain_tx,
        "success": True
    })

def mint_proof_token(score):
    """Placeholder for your blockchain minting logic."""
    # Here you would call your Solidity contract via Web3.py
    return f"0x{os.urandom(16).hex()}... (MINTED)"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
