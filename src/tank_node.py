#!/usr/bin/env python
import roslib
import rospy
from roboclaw import Roboclaw
from time import sleep

from std_msgs.msg import Float32

class speed:
    def __init__(self):
        self.left = Float32()
        self.right = Float32()

class tank:
    def __int__(self,port="ttyACM0",rate=38400,adresses=[128,129,130],max_speed=102):
        self.port = port
        self.rate = rate
        self.adresses = adresses
        self.max_speed=max_speed

        self.roboclaw=Roboclaw(port, rate)
        self.roboclaw.Open()
        
    def fixPwm(self,percentage): #"""CONVIERTE EL VALOR DE PORCENTAJE A PWM (ESCALA DE 0-1 A 0-102) CON REDONDEO A 2 DECIMALES"""
        return int(abs(percentage)*self.max_speed)

    def tankDrive(self,joy):
        for i in self.adresses:
            if(i%2==0):
                if(joy.left>0):
                    self.roboclaw.ForwardM1(i,self.fixPwm(joy.left))
                elif(joy.left<0):
                    self.roboclaw.BackwardM1(i,self.fixPwm(joy.left))
                else:
                    self.roboclaw.ForwardM1(i,0)
            else:
                if(joy.right>0):
                    self.roboclaw.ForwardM1(i,self.fixPwm(joy.right))
                elif(joy.right<0):
                    self.roboclaw.BackwardM1(i,self.fixPwm(joy.right))
                else:
                    self.roboclaw.ForwardM1(i,0)
                

class tank_node:
    def __init__(self, port, rate, adresses):
        self.port = port
        self.rate = rate
        self.adresses = adresses
        self.mvec = speed()
        self.max_speed = int(102)
        self.rover=tank(port=self.port, rate=self.rate,adresses=self.adresses,max_speed=self.max_speed)
        rospy.Subscriber('/Motors/left_vel',Float32,self.left_callback)
        rospy.Subscriber('/Motors/right_vel',Float32,self.right_callback)

        r = rospy.Rate(20)

        while not rospy.is_shutdown():
            self.rover.tankDrive(self.mvec)

            r.sleep()

    def left_callback(self, data):
        self.mvec.left=data.data

    def right_callback(self, data):
        self.mvec.right=data.data

 

if __name__=="__main__":
    rospy.init_node('MotorsAlv')
    try:
        port = "ttyACM0"
        bRate = 115200
        adresses = [0x80, 0x81, 0x82, 0x83, 0x84, 0x85]
        tank_node(port=port, rate=bRate, adresses=adresses)
    except:
        pass