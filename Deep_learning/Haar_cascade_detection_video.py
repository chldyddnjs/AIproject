import cv2
import numpy as np
import IPython

file_name = 'obama_01.mp4'
face_cascade_name = 'haarcascade_frontalface_alt.xml'
eyes_cascade_name = 'haarcascade_eye_tree_eyeglasses.xml'

face_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()

if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)


def detectAndDisplay(frame):
    IPython.display.clear_output(wait = True)
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    #Detect face
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        faceROI = frame_gray[y:y+h, x:x+w]
        #Detect Eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x+x2+w2//2,y+y2+h2//2)
            radius = int(round((w2+h2)*0.25))
            frame = cv2.circle(frame,eye_center,radius,(255,0,0),3)
    cv2.imshow('Obama',frame)
    
    

cap = cv2.VideoCapture(file_name)
if not cap.isOpened:
    print('--(!)Error loading eyes cascade')
    exit(0)
    
while(cap.isOpened()):
    ret, frame = cap.read()
    detectAndDisplay(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()