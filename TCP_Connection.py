from socket import *
from math import sin,cos
import gopigo3
import time
#global variables
THRESHOLD=0.7
#everybody can connect
HOST='' 
PORT=21555
BUFFSIZE=2048
ADDR=(HOST,PORT)
TCPServer_Socket=socket(AF_INET,SOCK_STREAM)
TCPServer_Socket.bind(ADDR)
TCPServer_Socket.listen()
#Previous values
x_axis_prev=0
y_axis_prev=0
def get_strength(y,z):
  strength=round(z,2)
  angle=round(y*90/9.8,0)
  return [strength*cos(angle),strenght*sin(angle)]
def move(x_axis,y_axis):
                # then move the robot to the left
                if x_axis < -THRESHOLD:
                    robot.left()
                # if the mouse is moved to the right
                # then move the robot to the right
                elif x_axis >THRESHOLD:
                    robot.right()
                # if the mouse is moved backward
                # then move the robot backward
                elif y_axis < -MOUSE_THRESHOLD:
                    robot.backward()
                # if the mouse is moved forward
                # then move the robot forward
                elif y_axis > MOUSE_THRESHOLD:
                    robot.forward()
                # if the mouse is not moving in any direction
                # then stop the robot from moving
                else:
                    robot.stop()
                time.sleep(0.1)    
while True:
    print("Waiting for connection ...")
    conn,addr=TCPServer_Socket.accept()
    print("Connection established to "+str(addr))
    try:
        while True:
           data=''
           data=conn.recv(BUFFSIZE).decode('ascii')
           if not data:
                break
           else:
                #do something with the data received
                list_data=data.split(",")
                if(len(list_data)==3):
                  print(get_strength(float(list_data[1]),float(list_data[2]))
                  try:      
                    [x_axis,y_axis]=get_strength(float(list_data[1]),float(list_data[2]))
                    move(x_axis-x_axis_prev,y_axis-y_axis_prev)
                    x_axis_prev=x_axis
                    y_axis_prev=y_axis    
                  except:
                     print("It cant do that")
                  #do something with data from get_strenth firts one is the power and second is the angle
    except KeyboardInterrupt:
        print("Closed")
TCPServer_Socket.close()
