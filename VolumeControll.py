from multiprocessing.sharedctypes import Value
import cv2
import time
import numpy as np
import HandTrackerModule as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
wCam,hCam = 640,480
MinValue = 0
MaxValue = 0
try:
    with open("config","r") as f:
        MinValue = float(f.readline())
        MaxValue = float(f.readline())
except FileNotFoundError:
    print("You have to run calibration.py at first!")
    sys.exit()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
MinVolume, MaxVolume, _ = volume.GetVolumeRange()


cap = cv2.VideoCapture(0)

pTime =0
cTime =0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4,hCam)

detector = hm.HandDetector(detectionCon = 0.7)
VolumeLocked = True
StartTime = 0

PrevValue = -7
PrevValActive = False
LockTime = 2
TimeLeft = LockTime
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.FindHands(img,draw=True)
    LmList = detector.FindPos(img,draw=False)
    if(len(LmList)!=0):
        x1,y1 = LmList[4][1],LmList[4][2]
        x2,y2 = LmList[8][1],LmList[8][2]

        cx = (x1+x2)//2
        cy = (y1+y2)//2
        length = math.hypot(x2-x1,y2-y1)
        if VolumeLocked:
            cv2.putText(img,"Edit locked!",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(img,f"Don't move your fingers for {round(TimeLeft,1)} sec",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(img,"To unlock edit mode",(10,120),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.circle(img,(x1,y1),7,(255,0,255),1)
            cv2.circle(img,(x2,y2),7,(255,0,255),1)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            
            
            if TimeLeft<0.1:
                VolumeLocked = False
                StartTime = 0
                PrevValue = -7
                TimeLeft = LockTime
            elif PrevValue < 0:
                PrevValue = length
                StartTime = time.time()
                TimeLeft = LockTime
            elif length>PrevValue*0.8 and length<PrevValue*1.2:
                TimeLeft = LockTime-(time.time() - StartTime)
            else:
                VolumeLocked = True
                StartTime = 0
                PrevValue = -7
                TimeLeft = LockTime
        else:
            cv2.putText(img,"Edit unlocked!",(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            cv2.putText(img,f"Don't move your fingers for {round(TimeLeft,1)} sec",(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            cv2.putText(img,"To lock edit mode",(10,120),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            length = math.hypot(x2-x1,y2-y1)
            Vol = np.interp(length,[MinValue*1.25,MaxValue*0.75],[MinVolume,MaxVolume])
            volume.SetMasterVolumeLevel(Vol, None)
            Vol_percent = np.interp(Vol,[MinVolume, MaxVolume],[0,100])
            cv2.putText(img,f"{int(Vol_percent)}%",(x1-40,y1-20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            if TimeLeft<0.1:
                VolumeLocked = True
                StartTime = 0
                PrevValue = -7
                TimeLeft = LockTime
            elif PrevValue < 0:
                PrevValue = length
                StartTime = time.time()
                TimeLeft = LockTime
            elif length>PrevValue*0.8 and length<PrevValue*1.2:
                TimeLeft = LockTime-(time.time() - StartTime)
            else:
                VolumeLocked = False
                StartTime = 0
                PrevValue = -7
                TimeLeft = LockTime
    cv2.imshow("Cam",img)
    cv2.waitKey(1)
    if cv2.getWindowProperty("Cam",0) == -1:
        break
    
