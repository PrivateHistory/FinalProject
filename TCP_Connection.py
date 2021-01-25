from socket import *
from math import sin,cos
import gopigo3
#import easygopigo3
import time
#global variables
THRESHOLD=2.5
#everybody can connect
HOST='' 
PORT=21555
BUFFSIZE=2048
ADDR=(HOST,PORT)
TCPServer_Socket=socket(AF_INET,SOCK_STREAM)
TCPServer_Socket.bind(ADDR)
TCPServer_Socket.listen()

robot = gopigo3.GoPiGo3()
#Previous values
check=True

#PID
ks=30
ka=20

def get_strength(y,z):
	strength=round(z,2)
	angle=round(y*90/9.8,0)
	return [strength*cos(angle),strength*sin(angle)]

def move(strength,angle):
	global check,ks,ka
	check=False
	left_motor_speed=int(ks*strength+ka*angle)
	right_motor_speed=int(ks*strength-ka*angle)
	robot.set_motor_dps(robot.MOTOR_LEFT, dps=left_motor_speed)
	robot.set_motor_dps(robot.MOTOR_RIGHT, dps=right_motor_speed)
	time.sleep(0.01)
	check=True

print("Opened a connection on port "+ str(PORT))

try:
	while True:
		#print("Waiting for connection ...")
		conn,addr=TCPServer_Socket.accept()
		#print("Connection established to "+str(addr))
		
		while True:
			data=''
			data=conn.recv(BUFFSIZE).decode('ascii')
			if not data:
				break
			elif check:
				#do something with the data received
				list_data=data.split(",")
				if (len(list_data) == 3 and len(list_data[1]) > 2 and len(list_data[2]) > 2):
					strength, angle = float(list_data[2]), float(list_data[1])
					print("Strenght: %.4f\t\tAngle: %.4f" % (strength, angle))
					move(strength,angle)

except KeyboardInterrupt:
	print("\n\n=====\nConnection closed")
finally:
	TCPServer_Socket.close()
	robot.reset_all()
