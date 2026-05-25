import threading
import queue
import time
import pyttsx3
import cv2

tts_queue = queue.Queue()

def tts_worker(q: queue.Queue):
    engine = pyttsx3.init()
    # Optional: tune voice rate/volume
    engine.setProperty('rate', 150)  # speaking rate
    engine.setProperty('volume', 1.0)  # 0.0-1.0
    while True:
        text = q.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)
        q.task_done()

# start worker thread (daemon so it won't block exit)
worker_thread = threading.Thread(target=tts_worker, args=(tts_queue,), daemon=True)
worker_thread.start()

# ---------- Simple debounce/stability logic ----------
STABILITY_THRESHOLD = 5  # number of consecutive frames required to accept a digit
last_pred = None
stable_count = 0
last_announced = None
announced_cooldown = 1.0  # seconds to wait before re-announcing same digit

last_announce_time = 0

# map digits to words (optional)
digit_words = ["zero","one","two","three","four","five","six","seven","eight","nine"]

# ---------- Example OpenCV loop ----------
# Replace the body of get_prediction_from_frame with your model/landmark pipeline
def get_prediction_from_frame(frame):
    """
    Stub: replace with your landmark-based model's prediction call.
    Should return an integer 0-9 or None if no confident prediction.
    """
    # ----- YOUR CODE HERE -----
    # e.g. return model.predict(landmark_features)
    return None

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        predicted = get_prediction_from_frame(frame)  # integer 0-9 or None

        # Stability/debounce logic
        if predicted is None:
            last_pred = None
            stable_count = 0
        else:
            if predicted == last_pred:
                stable_count += 1
            else:
                last_pred = predicted
                stable_count = 1

        if stable_count >= STABILITY_THRESHOLD:
            # Only announce if new or cooldown passed
            now = time.time()
            if last_announced != predicted or (now - last_announce_time) > announced_cooldown:
                text_to_say = f"{digit_words[predicted]}"  # "three"
                # Add any context: f"Detected digit {digit_words[predicted]}"
                tts_queue.put(text_to_say)
                last_announced = predicted
                last_announce_time = now

            # optionally reset stable_count so it doesn't keep re-announcing
            stable_count = 0

        # show frame (optional)
        cv2.imshow('Sign Digit', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    # stop worker cleanly
    tts_queue.put(None)
    worker_thread.join(timeout=1)
