# Sign Language Digit Recognition with TTS

Real-time sign language digit recognition (0-9) using MediaPipe hand landmarks and Random Forest classifier, with text-to-speech announcements.

## Features

- ✅ Real-time hand landmark detection using MediaPipe
- ✅ Sign language digit recognition (0-9)
- ✅ Cross-platform text-to-speech support (macOS, Windows, Linux)
- ✅ Stability detection to prevent false announcements
- ✅ Visual feedback with hand landmarks overlay
- ✅ Non-blocking TTS for smooth video performance

## Requirements

### All Platforms
```bash
pip install opencv-python mediapipe numpy scikit-learn
```

### Windows Only
For text-to-speech on Windows, also install:
```bash
pip install pyttsx3
```

### macOS
No additional TTS dependencies needed (uses built-in `say` command)

### Linux
Install espeak for TTS:
```bash
sudo apt-get install espeak
```

## Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. For Windows users, also install:
```bash
pip install pyttsx3
```

## Usage

Run the main recognition script:
```bash
python test_model.py
```

### Controls
- **ESC**: Exit the application
- Show hand signs to the camera for digit recognition
- The system will announce detected digits via TTS

### How It Works

1. **Hand Detection**: MediaPipe detects hand landmarks (21 points)
2. **Feature Extraction**: X,Y coordinates of landmarks are extracted (42 features)
3. **Classification**: Random Forest model predicts the digit (0-9)
4. **Stability Check**: Requires 10 consecutive frames of the same digit before announcing
5. **TTS Announcement**: Speaks "The number is [digit]" using platform-appropriate TTS
6. **Cooldown**: Waits 2 seconds before re-announcing the same digit

## Configuration

You can adjust these parameters in `test_model.py`:

```python
speech_cooldown = 2.0           # Seconds between re-announcing same digit
stability_threshold = 10        # Consecutive frames required before speaking
min_detection_confidence = 0.5  # Hand detection confidence threshold
min_tracking_confidence = 0.5   # Hand tracking confidence threshold
```

## Camera Selection

- **macOS**: Tries camera index 1 first (external/Continuity camera), falls back to 0
- **Windows**: Uses camera index 0 by default
- **Linux**: Uses camera index 0 by default

To change camera index, edit the `cv2.VideoCapture()` line in `test_model.py`.

## Files

- `test_model.py` - Main recognition script with TTS
- `train_model.py` - Script to train the Random Forest model
- `data_preprocessing.py` - Data collection and preprocessing
- `rf_model.pickle` - Trained Random Forest model
- `test_tts.py` - TTS testing utility
- `test_camera.py` - Camera diagnostic utility

## Troubleshooting

### Windows
- If TTS doesn't work: `pip install pyttsx3`
- If camera doesn't open: Check Windows privacy settings for camera permissions

### macOS
- If camera doesn't work: Check System Settings → Privacy & Security → Camera
- Grant Terminal/Python camera permissions

### Linux
- If TTS doesn't work: `sudo apt-get install espeak`
- If camera doesn't work: Check `/dev/video*` permissions

### All Platforms
- **No hand detected**: Ensure good lighting and hand is clearly visible
- **Wrong predictions**: Retrain the model with more/better training data
- **Laggy video**: Lower the webcam resolution or reduce stability_threshold

## Performance

- **Stability Detection**: Prevents false announcements from hand movements
- **Non-blocking TTS**: Speech runs in background thread, doesn't freeze video
- **Frame Rate**: ~30 FPS on modern hardware

## Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 42 (X,Y coordinates of 21 hand landmarks)
- **Classes**: 10 (digits 0-9)
- **Accuracy**: Depends on training data quality

## Credits

- MediaPipe by Google for hand landmark detection
- scikit-learn for Random Forest classifier
- pyttsx3 for cross-platform TTS (Windows)

## License

MIT License - Feel free to use and modify!
