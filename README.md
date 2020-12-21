# RaspPi_PacketSerial_RoboclawController
Modified Packet Serial Controller for Roboclaw drivers, for Raspberry Pi with python3.


Model: 
https://www.basicmicro.com/Roboclaw-Solo-30A-34VDC-Motor-Controller_p_44.html

Original: 
https://resources.basicmicro.com/packet-serial-with-the-raspberry-pi-3/

Original GIT:
https://github.com/basicmicro/raspberry_pi_packet_serial


Required Python Libraries:

-> serial (pyserial)

-> ros

Required ROS Packages:

-> rospy

-> sensor_msgs

-> std_msgs

-> geometry_msgs

-> joy

Run tank_node.py or motors_node.py for testing purposes.

Needs to be running control.py for topic comunication, or some script that sends a Float32 value to the '/Motors/left_vel' and '/Motors/right_vel' in ROS.

This is only a First and Second Test version, changes or elimination of the proyect may happen. Has yet to be tested.

Connection Circuit Master-Slave Diagram and Info:

