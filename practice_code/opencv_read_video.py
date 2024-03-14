import cv2

cap = cv2.VideoCapture('thumb.mp4')     #video
cap = cv2.VideoCapture(0)     #webcam

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (0,0), fx = 1.4, fy = 1.4)
        frame = cv2.Canny(frame, 100, 200)
        cv2.imshow('video', frame)
    else:
        break
    if cv2.waitKey(10) == ord('q'):
        break