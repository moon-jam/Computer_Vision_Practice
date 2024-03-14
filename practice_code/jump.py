import time
from cvzone.PoseModule import PoseDetector
import cv2

counter = 0
stage = None
last_high = 0
highest = 0
lowest = 0
pTime = 0
up = False
down = False
err = 0

detector = PoseDetector()

cap = cv2.VideoCapture(0)     #webcam

while True:
    ret, frame = cap.read()
    if ret:
        frame = detector.findPose(frame)
        lmList, bboxInfo = detector.findPosition(frame)

        high = 0
        try:
            high = bboxInfo['center'][1]

            if high-last_high<-5:
                up = True
                down = False
                highest = high
                stage = "up"
                err = 0
            elif high-last_high>5:
                down = True
                if up and down and lowest-highest>15:
                    counter = counter + 1
                    highest = lowest+600
                up = False
                lowest = high
                stage = "down"
                err = 0
            # elif (up and down) or (not(up) and not(down)) and abs(high-last_high)<2 and err>10:
            #     stage = "ground"
            #     up = False
            #     down = False
            #     err = 0
            # else:
            #     err = err+1

            # cv2.putText(frame, str(high-last_high), (0,2500), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            # cv2.putText(frame, str(high), (0,300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            # cv2.putText(frame, str(up), (0,350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            # cv2.putText(frame, str(down), (0,400), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            # cv2.putText(frame, str(err), (0,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

            last_high = high
        except:
            pass

        # Render curl counter
        # Setup status box
        cv2.rectangle(frame, (0,0), (640,73), (245,117,16), -1)

        # Rep data
        cv2.putText(frame, 'REPS', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(counter),(10,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(frame, 'STAGE', (170,12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame, stage,(130,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(frame, f"FPS : {int(fps)}", (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

        cv2.imshow('video', frame)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        break