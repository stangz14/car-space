from turtle import color
import cv2
import pickle
from cv2 import COLOR_BGR2GRAY
import cvzone
import numpy as np

import pyfirmata
from time import sleep


redLed = 8
yellowled = 9
greenled = 10

on = 1 
off = 0

try: 
    board = pyfirmata.Arduino('COM3')
    print("Connected Successfuly")
except:
    print("Falied To Conncet")

    # board.digital[redLed].write(on)
    # board.digital[9].write(1)
    # sleep(0.5)
    # board.digital[redLed].write(off)


cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
      posList = pickle.load(f)  

width, height = 107, 48

def checkParkingSpace(imgpro):
    for pos in posList:
        x,y = pos

        imgCrop = imgpro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-5), scale = 1.5 , thickness = 2, offset=0)

        if count < 800:
            color = (0,255,0)
            tickness = 5
        else:
            color = (0,0,255)
            tickness = 2
        cv2.rectangle(img, pos, (pos[0]+width,pos[1]+height),color, tickness) 
        c = "F"
        n = 0
        while c == "F":
            if pos == posList[n]:
                c = "T"
                m = n + 8
                if color == (0,255,0):
                    board.digital[m].write(1)
                else:
                    board.digital[m].write(0)
            else:
                n = n + 1
         


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img  = cap.read()   
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imDilate = cv2.dilate(imgMedian,kernel, iterations=1)
    
    checkParkingSpace(imDilate)  
    # for pos in posList:
    cv2.imshow("Image",img)
    # cv2.imshow("ImageBlur",imgBlur)
    # cv2.imshow("ImageThreshold",imgThreshold)
    cv2.waitKey(1)

    

    