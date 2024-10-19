import cv2
import mediapipe as mp
import numpy as np
import csv
import os


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


csv_filename = 'gesture_dat7.csv'


if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        header = [f"x{i}" for i in range(42)] + [f"y{i}" for i in range(42)] + [f"z{i}" for i in range(42)] + ["label", "num_hands"]
        writer.writerow(header)


cap = cv2.VideoCapture(0)


cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 


gesture_label = input("Enter gesture label (type 'exit' to quit): ")

with mp_hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.8, max_num_hands=2) as hands:
    while cap.isOpened() and gesture_label.lower() != "exit":
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        
        frame = cv2.flip(frame, 1)
        
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        
        results = hands.process(image)
        
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        
        if results.multi_hand_landmarks:
            num_hands_detected = len(results.multi_hand_landmarks)
            landmarks = []
            
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
               
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])

            
            if num_hands_detected == 1:
                landmarks.extend([[0, 0, 0]] * 21)

          
            np_landmarks = np.array(landmarks).flatten()

            
            with open(csv_filename, 'a', newline='') as f:
                writer = csv.writer(f)
                row = np.append(np_landmarks, [gesture_label, num_hands_detected])
                writer.writerow(row)
                print(f"Collected data for gesture: {gesture_label}, Num Hands: {num_hands_detected}")
        
        
        cv2.imshow('Hand Gesture Detection', image)

       
        print("Press 'q' to stop current gesture collection and prompt for a new label, or continue for more frames.")

        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            gesture_label = input("Enter new gesture label (type 'exit' to quit): ")


cap.release()
cv2.destroyAllWindows()
