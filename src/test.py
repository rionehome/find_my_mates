#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
# from find_my_mates.msg import Place
from std_msgs.msg import Float32
from find_my_mates.msg import Cp, Gngt, Ksntl, Mng, Mtfsl, Rp, Rsp
from control_system import ControlSystem
import time



class Test():
    def __init__(self):
        rospy.init_node("test")
        time.sleep(3)
        self.control = ControlSystem()

    def main(self):
        next_to_location = 2
        self.control.move_to_first_search_location(next_to_location)

if __name__=="__main__":
    test = Test()
    test.main()