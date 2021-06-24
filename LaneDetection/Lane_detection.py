import cv2
import numpy as np
import math
import IPython

file_name = 'test_video.mp4'
def detectAndDisplay(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    height,width = gray.shape
    blur = cv2.GaussianBlur(gray,(5,5),0)

    #min,max threshold(문턱치값)
    canny = cv2.Canny(blur,40,130)

    mask  = np.zeros((height,width),dtype = 'uint8')
    poly_height = int(0.60 * height)
    poly_left = int(0.47 * width)
    poly_right = int(0.53 * width)
    polygons= np.array([[(0,height),(poly_left,poly_height),(poly_right,poly_height),(width,height)]])
    cv2.fillPoly(mask,polygons,255)

    masked = cv2.bitwise_and(canny,mask)

    #Lane Detection
    #Hough transform 이미지에서 모양을 찾는 가장 유명한 방법이며 이미지의 형태를 찾거나 누락되거나 깨진 영역을 복원할 수 있다.
    #기본적으로 직선의 방정식을 이용합니다.
    #무수한 직선의 방정식은 y=mx+c로 표현할 수 있습니다. 삼각함수를 이용하면 r = xcos + ysin로 표현할수 있다.
    #허프변환은 너무 계산이 복잡하기때문에 확률 허프변환으로 최적화를 시켰다.

    #parameter scr,r값의 범위(0~1),세타 값의 범위(0~180),threshold(만나는 점의 기준 숫자가작으면 많은 선이 검출되지만 정확도가 떨어지고 숫자가 크면 정확도가 올라감)
    lines = cv2.HoughLinesP(masked,2,np.pi / 180,20,np.array([]),20,10)

    image_rgb = cv2.cvtColor(canny,cv2.COLOR_GRAY2RGB)

    if lines is not None:
        for line in lines:
            print(line)
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),5)
        cv2.imshow('test',frame)
    


cap = cv2.VideoCapture(file_name)

while(cap.isOpened()):
    ret, frame = cap.read()
    detectAndDisplay(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()