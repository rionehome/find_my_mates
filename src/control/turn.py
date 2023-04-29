#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import 




class Turn():
    def __init__(self):
        self.turn_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.


# import rospy
# import time
# from geometry_msgs.msg import Twist
# from control.angular import RotateBot

# #環境に合わせて変更する
# ANGULAR_SPEED = 0.8 #速すぎず遅すぎず
# L_TIME90 = 4.25 #90度回転できる時間にする
# L_TIME180 = 6.95 #180度回転できる時間にする
# R_TIME90 = 3.8
# R_TIME180 = 6.7


#turn_~~の~~の部分は回転角度を表す
# class Turn():
#     def __init__(self):
#         self.turn_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
#         self.twist = Twist()
#         self.twist.linear.x = 0
#         self.rotate = RotateBot()

#     def turn_90(self, direction="right"):
#         self.twist.angular.z = ANGULAR_SPEED
#         move_time = L_TIME90

#         if direction == "right":
#             self.twist.angular.z *= - 1
#             move_time = R_TIME90

#         start_time = time.time()
#         while time.time() - start_time < move_time:
#             self.turn_pub.publish(self.twist)
#             rospy.Rate(30).sleep()

#     def turn_180(self, direction="left"):
#         self.twist.angular.z = ANGULAR_SPEED
#         move_time = L_TIME180

#         if direction == "right":
#             self.twist.angular.z *= - 1
#             move_time = R_TIME180

#         start_time = time.time()
#         while time.time() - start_time < move_time:
#             self.turn_pub.publish(self.twist)
#             rospy.Rate(30).sleep()