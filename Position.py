Last_left=0
Last_Right=0
x=0
y=0
def position():
    #Get encoder values
    Left=robot.get_motor_encoder(robot.MOTOR_LEFT)-Last_Left
    Right=robot.get_motor_encoder(robot.MOTOR_RIGHT)-Last_Right
    #Get distance from encoer 
    distance=min(Left,Right)*WHEEL_CIRCUMFERENCE/360
    Last_Left=robot.get_motor_encoder(robot.MOTOR_LEFT)
    Last_Right=robot.get_motor_encoder(robot.MOTOR_RIGHT)
    #Save last values
    
    #Get angle
    angle=(Right-Left)%360
    #Get distances
    x=x+distance*math.cos(angle)
    y=y+distance*math.sin(angle)
    return [x,y]
    
    
