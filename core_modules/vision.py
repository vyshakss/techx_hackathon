import cv2
import numpy as np
import time

def get_color_mask(hsv_frame, target_color):
    """Creates a binary mask for the requested color."""
    color = target_color.lower()
    if "red" in color:
        lower1, upper1 = np.array([0, 100, 100]), np.array([10, 255, 255])
        lower2, upper2 = np.array([160, 100, 100]), np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv_frame, lower1, upper1)
        mask2 = cv2.inRange(hsv_frame, lower2, upper2)
        return cv2.bitwise_or(mask1, mask2)
    elif "blue" in color:
        lower, upper = np.array([100, 150, 0]), np.array([140, 255, 255])
    elif "green" in color:
        lower, upper = np.array([40, 80, 50]), np.array([90, 255, 255])
    elif "yellow" in color:
        lower, upper = np.array([20, 100, 100]), np.array([30, 255, 255])
    else:
        # Default fallback
        lower, upper = np.array([0, 50, 50]), np.array([180, 255, 255])
    return cv2.inRange(hsv_frame, lower, upper)

def verify_physical_liveness(target_color, required_seconds=2):
    """
    Verifies the user holds the color.
    RETURNS: (True/False, The_Image_Frame)
    """
    # Try indices 0, 1, and -1 to find the camera
    cap = None
    for i in [0, 1, -1]:
        temp_cap = cv2.VideoCapture(i)
        if temp_cap.isOpened():
            cap = temp_cap
            break
            
    if cap is None:
        print("[ERROR] No camera found.")
        return False, None
    
    start_time = None
    print(f"[VISION] Looking for a {target_color} object...")

    success = False
    final_frame = None

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1) # Mirror view
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = get_color_mask(hsv, target_color)
        
        # Check for the color
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected = False
        
        for cnt in contours:
            if cv2.contourArea(cnt) > 5000: # Filter small noise
                detected = True
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                break
        
        if detected:
            if start_time is None: start_time = time.time()
            elapsed = time.time() - start_time
            cv2.putText(frame, f"HOLD STEADY: {int(elapsed)}s", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if elapsed >= required_seconds:
                print("[SUCCESS] Physical challenge passed!")
                final_frame = frame.copy() # <--- CRITICAL: SAVE THE FRAME
                success = True
                break
        else:
            start_time = None
            cv2.putText(frame, f"SHOW ME {target_color.upper()}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Proof of Life Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    return success, final_frame
