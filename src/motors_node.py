#!/usr/bin/env python

#   ROS Libraries.
import roslib
import rospy

#   ROS Modules.
from sensor_msgs.msg import Joy

#   Operation Libraries.
from roboclaw import Roboclaw
import tank_steeering as tank
from os import system
from time import sleep


#   Joystick information from Joy type to float variables.
class joysticks_data:
    #   Initializes the object and it's variables.
    def __init__(self):
        self.x_left = self.x_right = float()
        self.y_left = self.y_right = float()

    #   Function that allows to update the value of the variables.
    def update_values(self, data):
        self.x_left, self.x_right = float(data[0]), float(data[3])
        self.y_left, self.y_right = float(data[1]), float(data[4])

    #   Function that allows to get the value in float array type.
    def get_values(self, dual):
        if dual == True:
            return [self.y_left, self.y_right]
        return [self.x_left, self.y_left]

#   Object node that allows to comunicate and connect all the information.
#   Reads the Joysticks data, stores it, translates it to a tank steering configuration,
#   and send that values to the driver of each motor for the movements.
class motors_node:
    #   Constructor function that defines the mode of control (solo or dual joystick),
    #   the port of comunication with the dirvers, the addresses and the max speed 
    #   value of the motors.
    def __init__(self, DUAL, PORT, RATE=38400, ADDRESSES=[128, 129], MAX_SPEED=127, NODE_NAME = 'Motors'):
        #   Definition of constants. 
        self.ADDRESSES = ADDRESSES
        self.DUAL = DUAL
        self.PORT = PORT

        #   Definition of useful tool objects.
        self.tank = tank.tank_steering(MAX_SPEED)
        self.joysticks = joysticks_data()

        #   Opening port for communication.
        self.open()

        #   Opening comunication between drivers and program.
        self.drivers = Roboclaw('/dev/'+self.PORT, RATE)
        self.drivers.Open()

        #   Enable Ros Comunication and it's suscribe frequency.
        rospy.init_node(NODE_NAME)
        rospy.Subscriber('joy', Joy, self.ros_suscribe)
        r = rospy.Rate(200)

        #   Control loop for comunication with the drivers.
        while not rospy.is_shutdown():
            self.tank_drive()
            r.sleep()

    #   OLD CODE, ENABLES COMMUNIATION WITH PORT, AND ENABLES ALL ACCESS, BUT AT THE MOMENT THERE IS NOT DOCUMENTATION.
    def open(self):
        for i in range(1):
            rospy.loginfo("waiting port: %s. %i sec." %(self.PORT,10-i))
            sleep(1)
        else:
            rospy.loginfo("open port: %s" %self.PORT)
            system("sudo chmod 777 /dev/" + self.PORT)
            rospy.loginfo("port: %s opened" %self.PORT)
        if self.rccm.Open():
            print(self.rccm._port)
        else: 
            exit("Error: cannot open port: " + self.PORT)


    #   Function that reads the Joy information and saves the Joysticks values.
    def ros_suscribe(self, data):
        self.joysticks.update_values(data.axes)


    #   Function in charge of managing the data, translate it to tank steering,
    #   define the direction of the motors, and sending the command to the drivers.  
    def tank_drive(self):
        #   Updating the values of the tank steering with the new data.
        if self.DUAL == True:
            self.tank.dual = self.joysticks.get_values(DUAL)
        else:
            self.tank.solo = self.joysticks.get_values(DUAL)

        #   Getting the direction and value of the new speed of the motors.
        motors = self.tank.get_speed(False)
        left_forward = motors[0] > 0
        right_forward = motors[1] > 0

        #   Getting the absolute value of the speed of the motors for the command.
        motors = [abs(motors[0]),abs(motors[1])]

        #   Sending the value of the speed to each address respectively.
        #   (All the par addresses are left, and non adresses are right).
        for i in self.addresses:
            if (i % 2 == 0):
                if left_forward == True:
                    self.roboclaw.ForwardM1(i, motors[0])
                else:
                    self.roboclaw.BackwardM1(i, motors[0])
            else:
                if right_forward:
                    self.roboclaw.ForwardM1(i, motors[1])
                else:
                    self.roboclaw.BackwardM1(i, motors[1])


#   Running program configuration. Change the values for the needed ones.
if __name__ == "__main__":
    try:
        #   Select the tank steering control mode:
        #   True is for each joystick controls each side.
        #   False is both sides are controled by only one joystick.
        dual = False

        #   Define the port which will be used to comunicate with the
        #   Roboclaw Solo Drivers.
        port = "ttyACM0"

        #   Define the baudrate at which the driver will communicate.
        rate = 115200

        #   Define the addreses for the program (par for left, non for right).
        addresses = [0x80, 0x81, 0x82, 0x83, 0x84, 0x85]

        #   Define the max speed of the motors (for roboclaw solo the max is 127,
        #   but the normal values have been 102).
        max_speed = 102

        #   Define the name for the ROS node.
        node_name = "motors_node_ALV"

        #   Initializating program.
        print("Running motors node on ",end="")
        if dual == True:
            print("dual mode.")
        elif dual   == False:
            print("solo mode.")
        print()
        motors_node(dual,port,rate,addresses,max_speed,node_name)
    except:
        pass
