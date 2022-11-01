import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self,mode=False,maxNumHands = 2,detectionCon = 0.5,trackCon = 0.5, modelComplexity=1,):
        self.mode = mode
        self.maxNumHands = maxNumHands
        self.detectionCon =detectionCon
        self.trackCon = trackCon
        self.modelComplex = modelComplexity

        self.mpHands = mp.solutions.hands
        self. hands = self.mpHands.Hands( self.mode,self.maxNumHands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def FindHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if(self.results.multi_hand_landmarks):
            for handLms in self.results.multi_hand_landmarks:
                if(draw):
                     self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    def FindPos(self,img,handNum=0,draw = True):

        lmList = []
        if(self.results.multi_hand_landmarks):
            myHand = self.results.multi_hand_landmarks[handNum]
            for id,lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append((id,cx,cy))
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        return lmList
    def FingersUp(self,lmList):#returns an array, where 1 means finger up(open) and 0 means finger down(closed)
        tipId = [4,8,12,16,20]
        fingers = [0,0, 0,0,0]
        #For thumb
        if lmList[2][1]<lmList[0][1]: #if right hand
            if lmList[tipId[0]][1]<lmList[tipId[0]-1][1]:
                fingers[0] = 1
            else:
                fingers[0] = 0
        
        else:
            if lmList[tipId[0]][1]>lmList[tipId[0]-1][1]:#if left hend
                fingers[0] = 1
            else:
                fingers[0] = 0
        for Id in range(1,5):#other firgers
            if(lmList[tipId[Id]][2]<lmList[tipId[Id]-2][2]):
                fingers[Id] = 1
            else:
                fingers[Id] = 0
        return fingers
def main():
    pTime =0
    cTime =0
    cap = cv2.VideoCapture(0)
    
    detector = HandDetector(detectionCon = 0.7,maxNumHands = 6)
    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)
        img = detector.FindHands(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

        cv2.imshow("Cam",img)
        cv2.waitKey(1)
        if cv2.getWindowProperty("Cam",0) == -1:
            break




if __name__ == "__main__":
    main()
