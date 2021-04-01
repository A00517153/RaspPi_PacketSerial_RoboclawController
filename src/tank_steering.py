#!/usr/bin/env python

#   Operation Libraries.
from numpy import angle, pi, sin, cos, linalg


#   Control from 2 joystick configuration.
class dual_joystick:
    #   Set function for object -> owner value.
    def __set__(self, instance, value):
        instance.mult = value

#   Control from 1 joystick configuration.
class solo_joystick:
    #   Set function for object->owner value.
    def __set__(self, instance, value):
        instance.mult = self.multiplierLR(
            value[0], value[1])

    #   Function in charge of rotating the values by pi/4.
    def multiplierLR(self, x, y):
        joysitck = x + (y * 1j)
        mag = linalg.norm(joysitck)
        alpha = angle(joysitck) - pi/4
        R = sin(alpha) * mag
        L = cos(alpha)*mag
        return L, R

#   Object that defines the values of the tank steering configuration.
class tank_steering:
    #   Link objects variables as instances.
    dual = dual_joystick()
    solo = solo_joystick()

    #   Constructor function defining max values and variables to use.
    def __init__(self, MAX_SPEED=0):
        self.MAX_SPEED = MAX_SPEED
        self. mult = [float(), float()]

    #   Function that allows to get the values of the speed of each motor
    def get_speed(self, return_float=False):
        a = self.mult[0]*self.MAX_SPEED
        b = self.mult[1]*self.MAX_SPEED
        if return_float == True:
            return [float(a), float(b)]
        return [int(a), int(b)]

#   Function for testing the code and it's output.
#   Expected Output should be:
#   [0,0]\n[160,0]\n[0,160]\n
if __name__ == '__main__':
    max_speed_value = 160
    test = tank_steering(MAX_SPEED=max_speed_value)
    print(test.get_speed())
    test.solo = [(.5)**.5, (.5)**.5]
    print(test.get_speed())
    test.dual = [0, 1]
    print(test.get_speed())
