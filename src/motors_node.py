#!/usr/bin/env python
import roslib
import rospy
from roboclaw import Roboclaw
from time import sleep

from std_msgs.msg import Float32

#Data Structure for storage of the value of the Left and Right Joysticks. 
class vec_speed:
    def __init__(self):
        self.left = Float32()
        self.right = Float32()

#Class for the motors, requires the port, and have default values that can be changed when calling it.
class motors_node:
    def __init__(self, port, rate=38400, adresses=[0x80,0x81], max_speed=127):
        self.speed = vec_speed() #Value of the information of the joysticks.
        self.adresses = adresses #Addreses of the drivers.
        self.max_speed = round((max_speed<=0x7F)*max_speed or 0x7F*(max_speed>0x7F)) #Speed of the motors (range: 0-127).
        self.roboclaw = Roboclaw(port, rate) #Define driver control with port and rate defined.
        self.roboclaw.Open() #Open serial comunication with the driver.

        rospy.Subscriber('/Motors/left_vel',Float32,self.left_callback) #Suscriber function to left joystick Topic.
        rospy.Subscriber('/Motors/right_vel',Float32,self.right_callback) #Suscriber funcion to right joystick Topic.

        r = rospy.Rate(1000)

        while not rospy.is_shutdown():
            self.tankDrive(self.speed)
            r.sleep()

    #Callback function for left topic.
    def left_callback(self, data):
        self.speed.left=data.data

    #Callback function for right topic.
    def right_callback(self, data):
        self.speed.right=data.data

    #Conversion from joy info to a valid speed value.
    def fixPwm(self, joy):
        if(joy>=0):
            return int(abs(joy)*self.max_speed), True
        else:
            return int(abs(joy)*self.max_speed), False

    #Function in charge of sending the Serial Packages to the drivers from the collected values.
    def tankDrive(self, joy):
        left_speed,left_forward=self.fixPwm(joy.left)
        right_speed,right_forward=self.fixPwm(joy.right)
        for i in self.adresses:
            if(i%2==0):
                if(left_forward):    
                    self.roboclaw.ForwardM1(i,left_speed)
                else:   
                    self.roboclaw.BackwardM1(i,left_speed)
            else:
                if(right_forward):   
                    self.roboclaw.ForwardM1(i,right_speed)
                else:   
                    self.roboclaw.BackwardM1(i,right_speed)

#Only run if the module is running as main program.
if __name__=="__main__":
    rospy.init_node('MotorsAlv')
    try:
        port = "ttyACM0"
        rate = 115200
        adresses = [0x80, 0x81, 0x82, 0x83, 0x84, 0x85]
        motors_node(port=port, rate=rate, adresses=adresses, max_speed=102)
    except:
        pass
    