from os import getcwd
import cv2
from matplotlib.patches import Rectangle
import numpy as np
from numpy.core.defchararray import count

print("OpenCV version:", cv2.__version__)

img = cv2.imread('carl1.jpg',cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

import matplotlib.pyplot as plt

# plt.imshow(img)
# plt.show()
# plt.imshow(gray)
# plt.show()

print(img.shape[1]) #width
print(img.shape[0]) #height
print(img.shape[2]) #chanel

(width ,height) = img.shape[:2]
center = (width // 2,height // 2)

X = 0 #@param {type:"slider",min:0,max:1204,step:1}
Y = 0 #@param {type:"slider",min:0,max:615,step:1}
SIZE = 100 #@param {type:"slider",min:0,max:0,step:1}

(b,g,r) = img[X,Y]
print("Pixel at ({},{}) - Red:{}, Green:{},Blue:{}".format(X,Y,r,g,b))

#Crop cordination = image[y:y+h,x:x+w]
croped = img[Y:Y+SIZE,X:X+SIZE]
# plt.imshow(croped)
# plt.show()

img[Y:Y+SIZE,X:X+SIZE] = (0,0,255)
cv2.rectangle(img,(X+SIZE*2, Y),(X+SIZE*3,Y+SIZE),(0,255,0),5)
# print(test)
# 원을 그릴때는 반지름이 중요하다.
radius = int(SIZE/2)
cv2.circle(img,(X+SIZE*4, Y+radius),radius,(255,255,0),-1)
cv2.line(img,(X+SIZE*5,Y),(X+SIZE*6,Y+SIZE),(0,255,255),5)
cv2.putText(img,'creApple',(X+SIZE*7,Y+SIZE),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))
# plt.imshow(img)
# plt.show()

# cv2.imwrite('car_copy.jpg',img)

# def download(path):
#     try:
#         from google.colab import files
#         files.download(path)
#     except:
#         import os
#         print('ERRor download:', os.path.join(os,getcwd(),path))

#moved down:+,up:- and right:+,left -
move = np.float32([[1,0,100],[0,1,100]])
moved = cv2.warpAffine(img,move,(width,height))
# plt.imshow(moved)
# plt.show()

rotate = cv2.getRotationMatrix2D(center,90,1.0)
rotated = cv2.warpAffine(img,rotate,(width,height))
# plt.imshow(rotated)
# plt.show()

ratio = SIZE /width
dimention = (SIZE,int(height*ratio))
resized = cv2.resize(img,dimention,interpolation=cv2.INTER_AREA)

# plt.imshow(resized)
# plt.show()

fliped = cv2.flip(img,1)

# plt.imshow(fliped)
# plt.show()

#width,height,chanel
background = np.full((width,height,3),255,np.uint8)
# plt.imshow(background)
# plt.show()
img[Y:Y+SIZE,X:X+SIZE] = (0,0,255)
background[Y:Y+SIZE,X:X+SIZE] = (0,0,255)
cv2.rectangle(background,(X+SIZE*2,Y),(X+SIZE*3,Y+SIZE),(0,255,0),5)
cv2.circle(background,(X+SIZE*4,Y+radius),radius,(255,255,0),-1)
cv2.line(background,(X+SIZE*5,Y),(X+SIZE*6,Y+SIZE),(0,255,255),5)
cv2.putText(background,'creApple',(X+SIZE*7,Y+SIZE),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))
# plt.figure(figsize=(15,15))
# plt.imshow(background)
# plt.show()

cv2.imwrite('plt_copy.jpg',background)

# Mask
mask = np.zeros(img.shape[:2],dtype='uint8')
cv2.circle(mask,center,int(height/2),(255,255,255),-1)
masked = cv2.bitwise_and(img,img,mask=mask)
# cv2.imshow('masked',masked)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#Fliter
zeros = np.zeros(img.shape[:2],np.uint8)
# cv2.imshow('zeros',zeros)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#이미지를 3가지 필터로 구분하기
(Blue,Green,Red) = cv2.split(img)
#다른채널을 까맣게 만든다.
# cv2.imshow('Glab',cv2.merge([Red,Green,Blue]))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow('Glab',gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#컴퓨터가 이해하기 편함
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# cv2.imshow('hsv',hsv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#영상처리를 쉽게하기위해 ex 노이즈를 없애기위해
lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
# cv2.imshow('lab',lab)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#색상의 차이를 띄워주는게 threshold 윤곽선을 찾는다.
ret, thresh = cv2.threshold(gray,127,255,0) # 0 대신 cv2.THRESH_BINARY 사용가능
cv2.imshow('Gray',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
#대상의 외형을 파악하는데 유용함
contours,hierachy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours,key=cv2.contourArea,reverse= True)[:10]

#윤곽선 검출
back = np.zeros((width,height,3),np.uint8)
for i in range(len(contours)):
    cv2.drawContours(back, contours,i,(0,255,255))
cv2.imshow('back',back)
cv2.waitKey(0)
cv2.destroyAllWindows()
