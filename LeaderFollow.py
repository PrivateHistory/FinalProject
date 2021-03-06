import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#P controller after P works  ID will be added
#Proportional controller to adjust for velocity ,should be tuned practically
kvelocity=20
#Proportional controller to adjust for angle 
kangle=20
# allow the camera to set
time.sleep(0.1)
check=True
ratio_to_speed = interpolate.interp1d(x=[1, 30], y=[100, 350], fill_value=(0, 350), bounds_error=False)
#accounts for minimum distance=10cm
base_velocity=0.1
def move(velocity,correction):
	#global variables
	global check,kvelocity,kangle,base_velocity
	check=False
	#velocity component is derived from traingular similarity so if the apparent area occupied by image increases that means that you are close to image 
	#if apparent area(as seen when taken the picture) of the object decreases you know you are far appart so u can use this to adjust the strength of velocity of wheels
	#now if the image get distorted or move in some directions u know that the image rotated so u have to rotate the car two that corresponds with complementary correction of wheels
	#Also it has to be pointed out that all of these have to have bounderies tested practically like cant approch biggern than 10cm and dont try to move the car when rotation is two small
	left_motor_speed=int(kvelocity*(velocity-base_velocity)+kangle*correction)
	right_motor_speed=int(kvelocity*(velocity-base_velocity)-kangle*correction)
	robot.set_motor_dps(robot.MOTOR_LEFT, dps=left_motor_speed)
	robot.set_motor_dps(robot.MOTOR_RIGHT, dps=right_motor_speed)
	
	time.sleep(0.01)
	check=True

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)::
    cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    image_taken= frame.array
    # conduct color threshold
    if image_taken:
        (h_frame, w_frame) = image_taken.shape[:2]
        mask=cv2.cvtColor(image_taken, cv2.COLOR_BGR2HSV)
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
	    #triangle similarity this will give a distance to the object 
	    #h_frame * w_frame is the total area camera sees and h * w is the area occupied by the object
            ratio_image= h_frame * w_frame / (h * w)
	    #this is filter to adjust for some distortion
            velocity=ratio_to_speed(ratio_image)
        
	    correction=0.9*deviation_translation+0.1*deviation_rotation
            #dont forget to put some limit of distance like actual velocity should be velocity -limit (that limit should be related to 10 cm)
	    if(check):
                move(velocity,correction)
            #put deviations in PID as a sume of deviations
            print("Deviation translation "+str(deviation_translation)+ " Deviation in rotation "+str(deviation_rotation))
            cv2.rectangle(image_taken, (x, y), (x + w, y + h), (0, 0, 255), 2) 
        cv2.imshow("Final",image_taken)
        rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break




