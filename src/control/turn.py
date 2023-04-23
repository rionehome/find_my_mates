#!/usr/bin/env python

from geometry_msgs.msg import Twist
import rospy
import time

twist = Twist()

ANGULAR_SPEED = 0.20

TIME90 = 2.0
TIME180 = 4.0

class Turn():
    def __init__(self):
        self.turn_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)

    def turn_90(self, direction="right"):
        print("askr")
        twist.linear.x = 0
        twist.angular.z = ANGULAR_SPEED

        if direction == "left":
            twist.angular.z *= - 1

        move_time = TIME90
        
        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turn_pub.publish(twist)
            rospy.Rate(30).sleep()

    def turn_180(self, direction="left"):
        twist.linear.x = 0
        twist.angular.z = ANGULAR_SPEED

        if direction == "left":
            twist.angular.z *= - 1

        move_time = TIME180
        
        start_time = time.time()
        while time.time() - start_time < move_time:
            self.turn_pub.publish(twist)
            rospy.Rate(30).sleep()

if __name__=="__main__":
    turn = Turn()