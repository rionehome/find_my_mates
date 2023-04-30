#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from math import radians
from find_my_mates.srv import OdomTurn

class Try():
    def __init__(self):
        rospy.init_node('test_main')
        self.rotate_srv = rospy.ServiceProxy('/rotate_odom', OdomTurn)


    def main(self):
        rospy.wait_for_service('/rotate_odom', OdomTurn)
        angle = float(radians(90))
        direction = "left"


        res = self.rotate_srv(angle, direction)

        print("Try: " + str(res.success))


        print("finish")


if __name__ == '__main__':
    t = Try()
    t.main()