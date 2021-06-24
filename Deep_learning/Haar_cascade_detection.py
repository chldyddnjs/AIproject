import cv2
import numpy as np

file_name = 'obama_03.jpg'
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

img = cv2.imread(file_name)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
# cv2.imshow('Obama',gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#얼굴들을 찾는다.
faces = face_cascade.detectMultiScale(gray)
#얼굴들을 찾으면 좌표와 가로와 세로를 리턴
for (x,y,w,h) in faces:
    center = (x+w//2,y+h//2)
    img = cv2.rectangle(img, (x,y),(x+w,y+h),(0, 255 , 0),3)
    faceROI = gray[y:y+h,x:x+w]
    eyes = eyes_cascade.detectMultiScale(faceROI)
    for (x2,y2,w2,h2) in eyes:
        eye_center = (x+x2+w2//2,y+y2+h2//2)
        radius = int(round((w2+h2)*0.25))
        img = cv2.circle(img,eye_center,radius,(0,255,255),3)

# cv2.imshow('face',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

