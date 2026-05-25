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
    for img_path in os.listdir(os.path.join(data_dir, dir_)):
        data_aux = []
        image = cv2.imread(os.path.join(data_dir, dir_, img_path))
        imagergb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imagergb)
        if results.multi_hand_landmarks:        
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(mp_hands.HandLandmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
            data.append(data_aux)
            labels.append(dir_)
import pickle
f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels' : labels}, f)
f.close()