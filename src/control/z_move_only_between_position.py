#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geometry_msgs.msg import Twist
import rospy
import time

#環境に合わせて変更する
LINEAR_SPEED = 0.20 #速すぎず遅すぎず
TIME12 = 6.0 #1~2の間を進む時間にする
TIME23 = 4.0 #2~3の間を進む時間にする
TIME34 = 4.0 #3~4の間を進む時間にする
TIME24 = 8.0 #2~4の間を進む時間にする

#pos_~~の~~の部分はmemo.txtのpositionを参照
class Position():
    def __init__(self):
        self.turtle_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.twist = Twist()
        self.twist.angular.z = 0

    def pos_12(self):
        self.twist.linear.x = LINEAR_SPEED
        move_time = TIME12

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_21(self):
        self.twist.linear.x = -1 * LINEAR_SPEED
        move_time = TIME12

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_23(self):
        self.twist.linear.x = LINEAR_SPEED
        move_time = TIME23

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_32(self):
        self.twist.linear.x = -1 * LINEAR_SPEED
        move_time = TIME23

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_34(self):
        self.twist.linear.x = LINEAR_SPEED
        move_time = TIME34

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_43(self):
        self.twist.linear.x =  -1 * LINEAR_SPEED
        move_time = TIME34

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_24(self):
        self.twist.linear.x = LINEAR_SPEED
        move_time = TIME24

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

    def pos_42(self):
        self.twist.linear.x = -1 * LINEAR_SPEED
        move_time = TIME24

        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turtle_pub.publish(self.twist)
            rospy.Rate(30).sleep()

