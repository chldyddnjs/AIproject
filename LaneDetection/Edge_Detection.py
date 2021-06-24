import cv2
import numpy as np
import math

file_name = 'car3.jpeg'
frame = cv2.imread(file_name)

height,width,channels = frame.shape
print(height,width,channels)

#Convert the image to grayscale
gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

#Gaussianblur for refucing noise
blur =cv2.GaussianBlur(gray,(5,5),0)

canny = cv2.Canny(blur,40,140)

mask  = np.zeros((height,width),dtype = 'uint8')
poly_height = int(0.60 * height)
poly_left = int(0.47 * width)
poly_right = int(0.53 * width)
polygons= np.array([[(0,height),(poly_left,poly_height),(poly_right,poly_height),(width,height)]])
cv2.fillPoly(mask,polygons,255)

#Mask와 canny 공통부분 합치기
masked = cv2.bitwise_and(canny,mask)

cv2.imshow('mask',masked)
cv2.waitKey(0)
cv2.destroyAllWindows()


