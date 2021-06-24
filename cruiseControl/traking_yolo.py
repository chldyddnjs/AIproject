import cv2
import numpy as np
import IPython
import time

min_confidence = 0.5
weight_file = 'yolov3.weights'
name_file = 'coco.names'
cfg_file = 'yolov3.cfg'

file_name = 'cabc30fc-e7726578.mp4'

net = cv2.dnn.readNet(weight_file,cfg_file)

classes = []
with open(name_file,'r') as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]


def writerFrame(img):
    global writer
    height,width = img.shape[:2]
    if writer is None and output_name is not None:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(output_name,fourcc,24,(width,height),True)
    if writer is not None:
        writer.write(img)

frame_count = 0
writer = None
output_name = 'output_tracking.avi'

detected = False
frame_mode = 'Tracking'
elapsed_time = 0

tracker = cv2.TrackerKCF_create()
trackers = cv2.legacy.MultiTracker_create()

vs = cv2.VideoCapture(file_name)


while True:
    ret,frame = vs.read()
    if frame is None:
        break
    if detected:
        frame_mode = 'Tracking'
        (success,boxes) = trackers.update(frame)
        for box in boxes:
            (x,y,w,h) = [int(v) for v in box]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    else:
        frame_mode = 'Detection'
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
        roi_left = int(0.3 * width)
        roi_right = int(0.6 * width)
            
        
        indexes = cv2.dnn.NMSBoxes(boxes,confidences,min_confidence,0.4)
        font = cv2.FONT_HERSHEY_COMPLEX

        for i in range(len(boxes)):
            if i in indexes:
                x,y,w,h = boxes[i]
                #Eliminate car
                if w > 50 and x > roi_left and x < roi_right:
                    print(class_ids[i],w)
                    selected = boxes[i]
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
        trackers.add(tracker,frame,tuple(selected))
        detected = True
    cv2.imshow('test',frame)
    writerFrame(frame)
vs.release()
cv2.destroyAllWindows()


