#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from find_my_mates.srv import OdomTurn
import time
from math import radians

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('rotate_bot')
    rospy.wait_for_service('/odom_turn')
    try:
        odom_turn = rospy.ServiceProxy('/odom_turn', OdomTurn)
        # res = odom_turn(angle=radians(90), direction="right")  # 90度 = 1.57ラジアン
        # print("Result: success={}".format(res.success))
        # time.sleep(2)

        angle = radians(180)
        print(angle)

        
        res = odom_turn(angle, "left")  # 90度 = 1.57ラジアン
        print("Result: success={}".format(res.success))

        # time.sleep(2)

        # res = odom_turn(angle=radians(180), direction="right")  # 90度 = 1.57ラジアン
        # print("Result: success={}".format(res.success))

        # time.sleep(2)
        
        # res = odom_turn(angle=radians(180), direction="left")  # 90度 = 1.57ラジアン
        # print("Result: success={}".format(res.success))


    except rospy.ServiceException as e:
        print("Service call failed: {}".format(e))

