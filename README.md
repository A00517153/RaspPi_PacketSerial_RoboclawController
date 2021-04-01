# RaspPi_PacketSerial_RoboclawController
Modified Packet Serial Controller for Roboclaw drivers, for Raspberry Pi with python3.


Model: 
https://www.basicmicro.com/Roboclaw-Solo-30A-34VDC-Motor-Controller_p_44.html

Original: 
https://resources.basicmicro.com/packet-serial-with-the-raspberry-pi-3/

Original GIT:
https://github.com/basicmicro/raspberry_pi_packet_serial


Required Python Libraries:
- serial (pyserial)
- ros
- os
- time
- numpy

Required ROS Packages:
- rospy
- sensor_msgs
- joy

In case of testing or using, run *motors_node.py*, for testing, please modify the lines 121 - 156 acording to the new configuration you are going to use.

This version doesn't require to have running any other topic for comunication, with the exception of 'Joy/joy', which will let us get directly the values without the need of other program running.

This is still a alpha version, test and developments are still being made. In this version is reintegrated an old code with the purpose of not needing to give the permits to the port, it may be unestable, because it hasn't been tested again, nor have any documentation on how it worked.

Connection Circuit Master-Slave Diagram and Info:
![alt text](https://github.com/A00517153/RaspPi_PacketSerial_RoboclawController/blob/main/image.jpg?raw=true)
