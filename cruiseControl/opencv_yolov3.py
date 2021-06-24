weight_file = 'yolov3.weights'
cfg_file = 'yolov3.cfg'
name_file = 'coco.names'

min_confidence = 0.5
import cv2
import numpy as np
import IPython
import time

#Load yolo
net = cv2.dnn.readNet(weight_file,cfg_file)

classes = []
with open(name_file) as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)

#cfg 안에는 127개의 레이어가 있다. 모든 레이어를 가져온다.
layer_names = net.getLayerNames()
#이중에서 언커넥트된 3개의 아웃풋레이어를 가져온다.
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0,255,size=(len(classes),3))

frame_count = 0
#initialize the video writer
writer = None
output_name = 'output_video.avi'

def writeFrame(img):
    #use global variable, writer
    global writer
    height,width = img.shape[:2]
    if writer is None and output_name is not None:
        #비디오 코덱 설정 Mjpg
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(output_name,fourcc,24,(width,height),True)
    if writer is not None:
        writer.write(img)
    
def detectAndDisplay(frame):
    IPython.display.clear_output(wait=True)
    height,width,channels = frame.shape
    #이미지에서 4차원 blob을 만들고 선택적으로 크기 조정
    #dnn이 분석하기 쉽게 단순화해주는 작업
    blob = cv2.dnn.blobFromImage(frame,0.0392,(416,416),(0,0,0),True,crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            #only car
            if (confidence > min_confidence) and (class_id == 2):
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    #Region of Interest
    mask = np.zeros((height,width),dtype='uint8')
    poly_top = int(0.65 * height)
    poly_bottom = int(0.85 * height)
    poly_left = int(0.47 * width)
    roi_left = int(0.3 * width)
    roi_right = int(0.6 * width)
    poly_right = int(0.53 * width)
    poly_margin = 50
    polygons = np.array([[(0+poly_margin,poly_bottom),(poly_left,poly_top),(poly_right,poly_top),(width-poly_margin,poly_bottom)]])
    
    cv2.fillPoly(mask,polygons,255)
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,min_confidence,0.4)
    font = cv2.FONT_HERSHEY_COMPLEX
    margin =5
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            #Eliminate car
            if w > 50 and x > roi_left and x < roi_right:
                label = str(classes[class_ids[i]])
                print(i,label)
                # color = colors[i]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,label,(x,y+30),font,0.5,(0,255,0),1)
                box = np.array([[(x-margin,y+h+margin),(x-margin,y-margin),(x+w+margin,y),(x+w+margin,y+h+margin)]])
                cv2.fillPoly(mask,box,0)
    #Lane Detection
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur,40,130)
    #Bitwise operation
    masked = cv2.bitwise_and(canny,mask)
    
    lines = cv2.HoughLinesP(masked,2,np.pi/180,20,np.array([]),20,10)
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,255),5)

    cv2.imshow('test',frame)
    writeFrame(frame)
    
file_name = 'cabc30fc-e7726578.mp4'

cap = cv2.VideoCapture(file_name)

if not cap.isOpened:
    print('--(!)Erorr opening video capture')
    exit(0)
num =0
while(cap.isOpened()):
    ret, frame = cap.read()
    if num == 10:
        break
    detectAndDisplay(frame)
    num +=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()