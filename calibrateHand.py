from ast import Call
from sqlite3 import Time
import cv2
import time
import HandTrackerModule as htm
import math
cap = cv2.VideoCapture(0)
wCam,hCam = 640,480

cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.HandDetector(detectionCon = 0.7)
MinValue = -1
ValueArr = []
MaxValue = -1
CalibrationNum = -1
Start_Time = 0
TimeLeft = 3


while True:
    s,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.FindHands(img)
    lmList = detector.FindPos(img,draw = False)
    
    if(len(lmList)!=0):
        if(CalibrationNum == -1):
            fingers = detector.FingersUp(lmList)
            cv2.putText(img,f"To start calibration,",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(img,f"show five a hold it for {round(TimeLeft,1)} sec",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            if TimeLeft<0.1:
                CalibrationNum = 0
                Start_Time = 0
            if fingers == [1,1,1,1,1]:
                if Start_Time == 0:
                    Start_Time = time.time()
                else:
                    TimeLeft = 3 - (time.time() - Start_Time)
            else:
                Start_Time = 0
                TimeLeft = 3
        elif(CalibrationNum == 0):
            TimeLeft = 3
            if(Start_Time == 0):
                Start_Time = time.time()
            else:
                TimeLeft = 3 - (time.time() - Start_Time) 
            cv2.putText(img,f"The calibration will start in {round(TimeLeft,1)} sec",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(img,"Connect your thumb and forefinger",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            if TimeLeft<0.1:
                CalibrationNum = 1
                Start_Time = 0
        elif(CalibrationNum == 1):
            TimeLeft = 5
            if(Start_Time == 0):
                Start_Time = time.time()
            else:
                TimeLeft = 5 - (time.time() - Start_Time) 
            cv2.putText(img,"Calibration process started",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(img,f"Hold Fingers together for {round(TimeLeft,1)} sec",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            x1,y1 = lmList[4][1],lmList[4][2]
            x2,y2 = lmList[8][1],lmList[8][2]
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            length = math.hypot(x2-x1,y2-y1)
            ValueArr.append(length)
            if(TimeLeft<0.1):
                MinValue = sum(ValueArr)/len(ValueArr)
                CalibrationNum = 2
                Start_Time = 0
                ValueArr = []
                print(MinValue)
        elif(CalibrationNum == 2):
            TimeLeft = 3
            if(Start_Time == 0):
                Start_Time = time.time()
            else:
                TimeLeft = 3 - (time.time() - Start_Time) 
            cv2.putText(img,f"The calibration will continue in {round(TimeLeft,1)} sec",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(img,"Extend your thumb and index finger",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            if TimeLeft<0.1:
                CalibrationNum = 3
                Start_Time = 0
        elif(CalibrationNum == 3):
            TimeLeft = 5
            if(Start_Time == 0):
                Start_Time = time.time()
            else:
                TimeLeft = 5 - (time.time() - Start_Time) 
            cv2.putText(img,"Calibration process started",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(img,f"Keep your fingers spread for {round(TimeLeft,1)} sec",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            x1,y1 = lmList[4][1],lmList[4][2]
            x2,y2 = lmList[8][1],lmList[8][2]
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            length = math.hypot(x2-x1,y2-y1)
            ValueArr.append(length)
            if(TimeLeft<0.1):
                MaxValue = sum(ValueArr)/len(ValueArr)
                CalibrationNum = 4
                Start_Time = 0
                ValueArr = []
                print(MaxValue)
        else:
            cv2.putText(img,"Calibration process finished",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.putText(img,f"Hide your hands to close the window",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    else:
        if(CalibrationNum == 4):
            break
        cv2.putText(img,"Show your hand to run the calibration",(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        Start_Time = 0
        TimeLeft = 3
        ValueArr = []
        if CalibrationNum ==1: CalibrationNum = 0
        elif CalibrationNum == 3: CalibrationNum = 2
    cv2.imshow("Cam",img)
    cv2.waitKey(1)
    if cv2.getWindowProperty("Cam",0) == -1:
        break
if MinValue!=-1 and MaxValue!=-1:
    with open("config","w") as f:
        f.write(str(MinValue) + "\n")
        f.write(str(MaxValue) + "\n")