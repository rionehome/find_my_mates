#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from math import radians
from find_my_mates.srv import OdomMove

class Try():
    def __init__(self):
        rospy.init_node('test_main')
        self.rotate_srv = rospy.ServiceProxy('/move_odom', OdomMove)
        
    def main(self):
        rospy.wait_for_service('/move_odom')
        angle = float(radians(90))
        distance = 0.5
        direction = "left"

        print("try")
        
        # distance(m)前進したところで、direction方向にangle(度)だけ回転を行う
        res = self.rotate_srv(angle, distance, direction)

        print("Result: " + str(res.success))

        print("finish")


if __name__ == '__main__':
    t = Try()
    t.main()