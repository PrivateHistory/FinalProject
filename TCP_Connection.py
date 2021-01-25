from socket import *
from math import sin,cos
#import gopigo3
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
check=True

#PID
ks=20
ka=0.5
def get_strength(y,z):
  strength=round(z,2)
  angle=round(y*90/9.8,0)
  return [strength,strenght]
def move(strength,angle):
                global check,ks,ka
                left_motor_speed=int(ks*strength+ka*angle)
                right_motor_speed=int(ks*strength-ka*angle)
                gopigo3.set_motor_dps(gopigo3.MOTOR_LEFT, dps=left_motor_speed)
                gopigo3.set_motor_dps(gopigo3.MOTOR_RIGHT, dps=right_motor_speed)
                time.sleep(0.01)
                check=True                
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
                    [strength,angle]=get_strength(float(list_data[1]),float(list_data[2]))
                    if(check):
                      move(strength,angle)
                  
                  #do something with data from get_strenth firts one is the power and second is the angle
    except KeyboardInterrupt:
        print("Closed")
TCPServer_Socket.close()
