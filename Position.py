import math
from time import sleep
import gopigo3
robot = gopigo3.GoPiGo3()
from Firebase import add,retreive


#Comment one out when u are on that 
MAC_ADRESS_LEADER="leaderraspber123a"
MAC_ADRESS_FOLLOWER=["follower2468","follower13579"]
Last_Left=0
Last_Right=0
x=0
y=0
WHEEL_CIRCUMFERENCE = 0.20892 # wheel circumference in meter

def position():
    	#Get encoder values
	Left=robot.get_motor_encoder(robot.MOTOR_LEFT)-Last_Left
	Right=robot.get_motor_encoder(robot.MOTOR_RIGHT)-Last_Right
	#Get distance from encoer 
	distance=min(Left,Right)*WHEEL_CIRCUMFERENCE
	Last_Left=robot.get_motor_encoder(robot.MOTOR_LEFT)
	Last_Right=robot.get_motor_encoder(robot.MOTOR_RIGHT)
	#Save last values
	
	#Get angle
	angle=(Right-Left)%360
	#Get distances
	x=x+distance*math.cos(angle)
	y=y+distance*math.sin(angle)

	print("x: %.3f, y: %.3f" % (x, y)          
while True:
    position()
    data={"x":str(x),"y":str(y)}
    add("Put here the right macadress",data)
    print(retreive())
	sleep(0.2)
    
