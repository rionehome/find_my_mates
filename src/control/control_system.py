#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geographic_msgs.msg import Twist
import rospy

class ControlSystem():
    def __init__(self):
        self.twist_pub = rospy.Publisher("")

    def move_to_guest_room(self):
        
        

if __name__=="__main__":
    controlsystem = ControlSystem()
    controlsystem.main()