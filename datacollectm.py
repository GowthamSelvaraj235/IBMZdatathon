import cv2
import mediapipe as mp
import numpy as np
import csv
import os

# Initialize MediaPipe hands and drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Create/Open a CSV file to store the landmarks and labels
csv_filename = 'gesture_data2.csv'

# Check if CSV file exists; if not, create it and write the header
if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write the header (21 landmarks * 3D coordinates * 2 hands + label)
        header = [f"x{i}" for i in range(42)] + [f"y{i}" for i in range(42)] + [f"z{i}" for i in range(42)] + ["label", "num_hands"]
        writer.writerow(header)

# Setup webcam capture
cap = cv2.VideoCapture(0)

# Ask for gesture label before collecting data
gesture_label = input("Enter gesture label (type 'exit' to quit): ")

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=2) as hands:
    while cap.isOpened() and gesture_label != "exit":
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the frame to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Process the frame for hand landmarks
        results = hands.process(image)
        
        # Convert the image color back to BGR for display
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract and draw hand landmarks
        if results.multi_hand_landmarks:
            num_hands_detected = len(results.multi_hand_landmarks)
            landmarks = []
            
            # Collect landmarks for both hands
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Save landmarks (21 landmarks * 3D coordinates)
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])

            # If less than 2 hands, pad the landmarks
            if num_hands_detected == 1:
                landmarks.extend([[0, 0, 0]] * 21)

            # Flatten the landmarks array
            np_landmarks = np.array(landmarks).flatten()

            # Save the landmarks, number of hands detected, and the label to the CSV file
            with open(csv_filename, 'a', newline='') as f:
                writer = csv.writer(f)
                row = np.append(np_landmarks, [gesture_label, num_hands_detected])
                writer.writerow(row)
                print(f"Collected data for gesture: {gesture_label}, Num Hands: {num_hands_detected}")
        
        # Display the image with the hand landmarks drawn
        cv2.imshow('Hand Gesture Detection', image)

        # Press 'q' to stop the current gesture collection and prompt for a new label
        if cv2.waitKey(10) & 0xFF == ord('q'):
            gesture_label = input("Enter gesture label (type 'exit' to quit): ")

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
