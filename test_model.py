import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

import cv2
import mediapipe as mp
import pickle
import numpy as np
import sys
import subprocess
import time
import threading

MODEL_PATH = "rf_model.pickle"   
expected_len = 42                # number of features model was trained on (2 coords * 21 landmarks = 42)
labels_dict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}

# Cross-platform TTS helper function
def speak_digit(digit):
    """Speak the digit using platform-appropriate TTS (non-blocking)"""
    def _speak():
        try:
            if sys.platform == "darwin":
                # macOS: use say command
                subprocess.run(["say", f"The number is {digit}"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL,
                             check=False)
            elif sys.platform == "win32":
                # Windows: use pyttsx3
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.say(f"The number is {digit}")
                    engine.runAndWait()
                except ImportError:
                    print("pyttsx3 not installed. Install with: pip install pyttsx3")
                except Exception as e:
                    print(f"Windows TTS Error: {e}")
            else:
                # Linux: try espeak
                subprocess.run(["espeak", f"The number is {digit}"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL,
                             check=False)
        except Exception as e:
            print(f"TTS Error: {e}")
    
    # Run in separate thread to avoid blocking
    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()


model = pickle.load(open(MODEL_PATH, "rb")) 

#Setup MediaPipe + webcam
# Try camera index 1 first (common for external/Continuity cameras on Mac), fallback to 0
# On Windows, typically use index 0
if sys.platform == "win32":
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Camera 1 not available, trying camera 0...")
        cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,        
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Variables for TTS debouncing
last_spoken_digit = None
last_speech_time = 0
speech_cooldown = 2.0  # Wait 2 seconds before speaking the same digit again
stable_digit = None
stable_count = 0
stability_threshold = 10  # Require 10 consecutive frames of the same digit before speaking

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from webcam. Exiting.")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

            data_aux = []
            for i in range(len(mp_hands.HandLandmark)):
                lm = hand_landmarks.landmark[i]
                data_aux.extend([lm.x, lm.y])

            if len(data_aux) == expected_len:
                # Ensure shape is (1, n_features)
                X = np.asarray(data_aux, dtype=np.float32).reshape(1, -1)

                try:
                    prediction = model.predict(X)
                    predicted_label = labels_dict[int(prediction[0])]
                    
                    # Display prediction on frame
                    cv2.putText(frame, f'Prediction: {predicted_label}', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    
                    # Stability check: only speak if the same digit appears consistently
                    if predicted_label == stable_digit:
                        stable_count += 1
                    else:
                        stable_digit = predicted_label
                        stable_count = 1
                    
                    # Speak if stable and enough time has passed
                    current_time = time.time()
                    if (stable_count >= stability_threshold and 
                        (predicted_label != last_spoken_digit or 
                         current_time - last_speech_time > speech_cooldown)):
                        
                        speak_digit(predicted_label)
                        last_spoken_digit = predicted_label
                        last_speech_time = current_time
                        print(f"🔊 Speaking: {predicted_label}")
                        
                        # Show visual feedback
                        cv2.putText(frame, f'Speaking: {predicted_label}', (10, 70),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2, cv2.LINE_AA)
                    else:
                        print("Predicted digit:", predicted_label)
                        
                except Exception as e:
                    # If the model fails
                    print("Model prediction error:", e)
                    stable_digit = None
                    stable_count = 0
            else:
                # Skip prediction if feature vector length doesn't match
                cv2.putText(frame, f'Feat len: {len(data_aux)} (expected {expected_len})', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2, cv2.LINE_AA)
                stable_digit = None
                stable_count = 0
        else:
            # No hand detected
            cv2.putText(frame, 'No hand detected', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 255), 2, cv2.LINE_AA)
            stable_digit = None
            stable_count = 0

        cv2.imshow('Webcam - Sign Digit Recognition', frame)

        # ESC to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
