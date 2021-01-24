import time
import cv2
import numpy as np
cap = cv2.VideoCapture('http://192.168.2.106:21555/video')
while(True):
    cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    ret, frame = cap.read()
    # conduct color threshold
    if ret:
        (h_frame, w_frame) = frame.shape[:2]
        mask=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_range=np.array([110,50,50])
        upper_range=np.array([130,255,255])
        image= cv2.inRange(mask,lower_range,upper_range)
        # show the images
        (cnts, _) = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
          # loop over the contours
        for c in cnts:
       # if the contour is too small, ignore it
            if cv2.contourArea(c) < 300:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            deviation_translation=(w_frame/2-(x+w/2))*100/w_frame
            deviation_rotation=(h_frame-w_frame)*100/h_frame
            #put deviations in PID as a sume of deviations
            print("Deviation translation "+str(deviation_translation)+ " Deviation in rotation "+str(deviation_rotation))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) 
        cv2.imshow("Final",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break




