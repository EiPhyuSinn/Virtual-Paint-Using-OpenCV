import cv2 as cv 
import numpy as np 

capture = cv.VideoCapture(0)
capture.set(3,140)
capture.set(4,180)
capture.set(10,130)

myColors = [
    [101, 100, 100, 130, 255, 255], # Blue

]
myColorValues = [[255,0,0]]
myPoints = []

def findColor(img,myColors,myColorValues):
    imgHsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHsv,lower,upper)
        x,y = getContours(mask)
        cv.circle(image,(x,y),10,(255,0,0),cv.FILLED)
        if x!= 0 and y!= 0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints
        # cv.imshow(str(color[0]),mask)

def getContours(img):
    x,y,w= 0,0,0
    contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        
        cv.drawContours(image,cnt,-1,(0,255,0),3)
        peri = cv.arcLength(cnt,True)
        approx = cv.approxPolyDP(cnt,0.02*peri,True)
        x,y,w,h = cv.boundingRect(approx) 
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv.circle(image,(point[0],point[1]),10,myColorValues[point[2]],cv.FILLED)

while True:
    success,frame = capture.read()
    image = frame.copy()
    newPoints = findColor(frame,myColors,myColorValues)
    if len(newPoints) != 0:
        for point in newPoints:
            myPoints.append(point)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv.imshow("video",image)
    frame = cv.flip(frame, 0)
    if cv.waitKey(1) & 0xFF == 27:
        break


