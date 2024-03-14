import time
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
stage = None
last_high = 0
highest = 0
lowest = 0
pTime = 0
up = False
down = False

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            high = (landmarks[22].y+landmarks[23].y)*100
            # cv2.putText(image, str(high > highest), (300,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            # cv2.putText(image, str(high-last_high>10), (300,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            if high-last_high<-7:
                up = True
                highest = high
                stage = "up"
            elif high-last_high>9:
                down = True
                if up and down and lowest-highest>15:
                    counter = counter + 1
                    highest = lowest+200
                lowest = high
                stage = "down"
            elif (up and down) or (not(up) and not(down)):
                stage = "ground"
                up = False
                down = False
            cv2.putText(image, str((up)), (0,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(image, str((down)), (0,350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(image, str(int(highest)), (0,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            # print(stage)
            last_high = high

        except:
            pass

        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (640,73), (245,117,16), -1)

        # Rep data
        cv2.putText(image, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),(10,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(image, 'STAGE', (170,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage,
                    (130,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)


        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image, f"FPS : {int(fps)}", (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()