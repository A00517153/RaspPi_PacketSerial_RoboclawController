#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy

izq=Float32(0.0)
der=Float32(0.0)

def principal():
    rospy.init_node('control',anonymous=True)
    rospy.Subscriber('joy',Joy,reader)


    pub = rospy.Publisher('/Motors/left_vel',Float32,queue_size=10)
    pub2 = rospy.Publisher('/Motors/right_vel',Float32,queue_size=10)
    rate=rospy.Rate(10) #10hz
    while not rospy.is_shutdown():
        print(izq,der)
        pub.publish(izq)
        pub2.publish(der)

        rate.sleep()

    rospy.spin()


def reader(data):
    global izq
    global der
    izq = data.axes[1]
    der = data.axes[4]
    #print(izq,der)
    
if __name__ == '__main__':
    print("INICIO")
    principal()
