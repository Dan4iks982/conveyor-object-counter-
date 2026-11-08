#activate virtual enviroment:   source .venv/bin/activate     
import numpy as np

import sys

import cv2

cv2.setNumThreads(4)
cap = cv2.VideoCapture(0)
if(cap.isOpened()) : print("Camera connected!")
else: 
    print("Camera is not working")
    sys.exit()
colors = {
    "Blue": {
        "lower": np.array([100, 100, 50]),
        "upper": np.array([130, 255, 255]),
        "bgr": (255, 0, 0)
    },
    "Green": {
        "lower": np.array([40, 100, 50]),
        "upper": np.array([80, 255, 255]),
        "bgr": (0, 255, 0)
    },
    "Yellow": {
        "lower": np.array([20, 100, 100]),
        "upper": np.array([35, 255, 255]),
        "bgr": (0, 255, 255)
    },
    "Red": {
        "lower": np.array([170, 100, 50]),
        "upper": np.array([180, 255, 255]),
        "bgr": (0, 0, 255)
    }
}

counts = {"Blue": 0, "Green": 0, "Yellow": 0, "Red": 0}
inside_zone = {"Blue": False, "Green": False, "Yellow": False, "Red": False}
cooldown = {"Blue": 0, "Green": 0, "Yellow": 0, "Red": 0}

while(True):
    ret,frame = cap.read()
    if(ret==False): break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for color_name, data in colors.items():
        if cooldown[color_name] > 0: cooldown[color_name] -= 1
        mask = cv2.inRange(hsv, data["lower"], data["upper"])
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(frame,(320,0),(320,480),(0,255,255),2)
        for c in contours:
            if cv2.contourArea(c)>2000:
                x,y,w,h = cv2.boundingRect(c)
                offset = 6
                
                cx = int(x + w / 2)
                cy = int(y + h / 2)
                cv2.circle(frame, (cx,cy),4,(255, 255, 255),-1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),data["bgr"], 2)
                cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, data["bgr"], 2)
                if (320 - offset) < cx < (320 + offset) and inside_zone[color_name] == False:
                    
                    inside_zone[color_name] = True
                    if cooldown[color_name] == 0: 
                        counts[color_name] +=1
                        cooldown[color_name] = 30
                    cv2.line(frame,(320,0),(320,480),(0, 128, 0),2)
                else: inside_zone[color_name] = False
                print("Printed:", counts)
                
                    
                
                
                
    
    cv2.imshow("Camera output", frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break 
    

cap.release()
cv2.destroyAllWindows()