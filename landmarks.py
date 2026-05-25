import os

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True,min_detection_confidence=0.3)
data_dir = r'C:\Users\kriti\Documents\TIET\TIET\SEMESTER-V\MACHINE LEARNING\SignLanguage\ASL Digits\asl_dataset_digits'
data = []
labels =  []
for dir_ in os.listdir(data_dir):
    for img_path in os.listdir(os.path.join(data_dir, dir_))[:1]:
        data_aux = []
        image = cv2.imread(os.path.join(data_dir, dir_, img_path))
        imagergb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imagergb)
        for hand_landmarks in results.multi_hand_landmarks:        
            mp_drawing.draw_landmarks(
                imagergb,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        plt.figure()
        plt.imshow(imagergb)
plt.show()
