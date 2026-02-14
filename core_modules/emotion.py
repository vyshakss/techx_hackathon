from deepface import DeepFace
import cv2

def analyze_emotion(frame):
    """
    Uses DeepFace to analyze facial expressions in a single frame.
    Returns the dominant emotion as a string.
    """
    try:
        # We use enforce_detection=False so the script doesn't crash 
        # if the user moves slightly out of frame.
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        # results is a list of detected faces; we take the primary one.
        dominant_emotion = results[0]['dominant_emotion']
        return dominant_emotion
        
    except Exception as e:
        # Common on Linux if the backend isn't ready or face is obscured.
        return "undetected"

def verify_human_reaction(expected_list, detected_emotion):
    """
    Checks if the user's emotion matches the context of the AI's challenge.
    Example: If the AI tells a joke, we expect ['happy', 'surprise'].
    """
    if detected_emotion.lower() in expected_list:
        print(f"[EMOTION] Authenticity Confirmed: {detected_emotion}")
        return True
    else:
        print(f"[EMOTION] Suspicious Reaction: {detected_emotion}")
        return False
