import cv2
import numpy as np
import time
from time import sleep

#RUN CAMERA CAPTURE VIDEO
cap = cv2.VideoCapture('video.mp4')

count_line_position = 550
delay = 150 #VIDEO FPS

min_width_rectangle = 80    #MINIMUM WIDTH OF RECTANGLE
min_height_rectangle = 80   #MINIMUM HEIGHT OF RECTANGLE

#INITIALIZE SUBSTRACTOR ALGORITHM FOR DETECT
algorithm = cv2.bgsegm.createBackgroundSubtractorMOG()

def center_point(x,y,w,h):  #IT IS A FUNTION OF CENTER PNT OF RECTANG
    x1 = int(x/2)
    y1 = int(h/2)
    cx = x+x1 #C IS CHANNEL
    cy = y+y1
    return cx,cy

detect = []  #LIST OF VEHICLES COUNTED
offset = 6   #ALLOWABLE ERROR BTW PIXEL
counter= 0

while True:
    ret,frame1=cap.read()
    time = float(1/delay) #FPS
    sleep(time)
    gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),5)
    #APPLYING ON EACH FRAME
    img_sub = algorithm.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilatada = cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
    counterShape,h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),4) #CROSSING LINE
    
    #TO DRAW RECTANGLE WITH LOOP FOR BCZ OF VARIOUS VEHICLES
    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>= min_width_rectangle) and (h>= min_height_rectangle)
        if not validate_counter:
            continue
        
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1,"Vehicle:"+str(counter),(x, y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)
        center = center_point(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)
        
   
        for (x,y) in detect:
             if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
                cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
                detect.remove((x,y))
                print("Vehicle Counter: "+str(counter))


    cv2.putText(frame1,"VEHICLE COUNTER:"+str(counter),(550,100),cv2.FONT_HERSHEY_TRIPLEX,2,(0,0,280),3)            
        
   
        
    
    
    cv2.imshow('Video Original',frame1)
    cv2.imshow('Detector',dilatada)
    if cv2.waitKey(1) == 13:
        break
    
    cv2.destroyAllWindows
    cap.release


