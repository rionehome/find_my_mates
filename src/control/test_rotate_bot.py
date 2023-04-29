#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from my_pkg.srv import OdomTurn

if __name__ == '__main__':
    rospy.init_node('rotate_bot')
    rospy.wait_for_service('/odom_turn')
    try:
        odom_turn = rospy.ServiceProxy('/odom_turn', OdomTurn)
        res = odom_turn(1.57, "right")  # 90度 = 1.57ラジアン
        print("Result: success={}, message={}".format(res.success, res.message))
    except rospy.ServiceException as e:
        print("Service call failed: {}".format(e))

