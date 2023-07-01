#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from math import radians
from find_my_mates.srv import OdomMove

class Try():
    def __init__(self):
        rospy.init_node('test_main')
        self.rotate_srv = rospy.ServiceProxy('/move_odom', OdomMove)
        self.main()
        
    def main(self):
        rospy.wait_for_service('/move_odom')
        forward_back = "forwoard"
        distance = 1.0
        direction = "left"
        angle = float(radians(90))

        print("try")
        
        # forward_back方向にdistance(m)だけ進んだところで、direction方向にangle(度)だけ回転を行う
        # forward_back: string  = "forward" or "back"
        # distance:     float64 = 0 〜 x
        # direction:　  string  = "left" or "right"
        # angle:        float64 = 0 〜 360

        # res = self.rotate_srv(forward_back, 0.0, "right", 270.0)
        distance = 0.1

        res = self.rotate_srv(forward_back, distance, direction, angle)

        print("Result: " + str(res.res))

        print("finish")


if __name__ == '__main__':
##### test program #####
# roslaunch find_my_mates try_srv_odom.launch
# Turtlebotは起動しません。
    t = Try()