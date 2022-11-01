import cv2
import numpy as np
import HandTrackerModule as hm
import win32api, win32con
from win32api import GetSystemMetrics
wCam,hCam = 640,480
frameR = 100
k = 3
pTime =0
cTime =0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4,hCam)
detector = hm.HandDetector(detectionCon = 0.9,trackCon = 0.8)
ScreenW = GetSystemMetrics(0)
ScreenH = GetSystemMetrics(1)
print(ScreenW, ScreenH)
n = 0
PrevX,PrevY = 0,0
CurX,CurY = 0,0
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.FindHands(img,draw=True)
    LmList = detector.FindPos(img,draw=False)
    if(len(LmList)!=0):
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        x1,y1 = LmList[8][1],LmList[8][2]
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        x2 = int(np.interp(x1,(frameR,wCam-frameR),(0,ScreenW)))
        y2 = int(np.interp(y1,(frameR,hCam-frameR),(0,ScreenH)))
        CurX = int(PrevX+(x2-PrevX)/k)
        CurY = int(PrevY+(y2-PrevY)/k)
        win32api.SetCursorPos((CurX,CurY))
        if(detector.FingersUp(LmList)[2] == 0):
             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,CurX,CurY,0,0)
             cv2.circle(img,(x1,y1),17,(255,0,0),cv2.FILLED)
        else:
             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,CurX,CurY,0,0)
        PrevX,PrevY = CurX,CurY
    cv2.imshow("Cam",img)
    cv2.waitKey(1)
    if cv2.getWindowProperty("Cam",0) == -1:
        break
    
