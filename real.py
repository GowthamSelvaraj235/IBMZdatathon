import cv2
import mediapipe as mp
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import subprocess
from gpt import gptvoice


model = joblib.load('gesture_model1.pkl')


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.9, min_tracking_confidence=0.8)


gesture_buffer = []
buffer_size = 5


def preprocess_landmarks(landmarks, num_hands):
    
    flat_landmarks = np.array(landmarks).flatten()

    
    if num_hands == 1 and len(flat_landmarks) == 63:
        flat_landmarks = np.pad(flat_landmarks, (0, 63), mode='constant')

    
    elif len(flat_landmarks) > 126:
        flat_landmarks = flat_landmarks[:126]

    return flat_landmarks

def play_movie():
    
    movie_path = r"D:\Future Man - 01x01 - Pilot.mkv"
    
    subprocess.Popen(['start', '', movie_path], shell=True)


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.flip(frame, 1)

    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
    results = hands.process(rgb_frame)

    
    landmarks = []
    num_hands = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            num_hands += 1

           
            hand_landmark_data = []
            for landmark in hand_landmarks.landmark:
                hand_landmark_data.append([landmark.x, landmark.y, landmark.z])

            
            landmarks.extend(hand_landmark_data)

        
        processed_landmarks = preprocess_landmarks(landmarks, num_hands)

        
        if len(processed_landmarks) == 126:
            
            processed_landmarks = np.array(processed_landmarks).reshape(1, -1)
            gesture = model.predict(processed_landmarks)[0]

          
            gesture_buffer.append(gesture)

           
            if len(gesture_buffer) > buffer_size:
                gesture_buffer.pop(0)

            
            most_common_gesture = max(set(gesture_buffer), key=gesture_buffer.count)

            
            print(f'Gesture: {most_common_gesture}')

            
            if most_common_gesture == 'movie':
                play_movie()
            elif most_common_gesture == 'story':
                gptvoice("generate random story")

    else:
        
        print('No Gesture Detected')

    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
hands.close()
