#!/usr/bin/env python

from geometry_msgs.msg import Twist
import rospy
import time

twist = Twist()

ANGULAR_SPEED = 0.05

TIME90 = 2.0
TIME180 = 4.0

def turn_90(direction="right"):
    twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
    twist.linear.x = 0
    twist.angular.z = ANGULAR_SPEED

    if direction == "left":
        twist.angular.z *= - 1

    move_time = TIME90
    
    start_time = time.time()
    while time.time() - start_time < move_time:
        twist_pub.publish(twist)

def turn_180(direction="left"):
    twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
    twist.linear.x = 0
    twist.angular.z = ANGULAR_SPEED

    if direction == "left":
        twist.angular.z *= - 1

    move_time = TIME180
    
    start_time = time.time()
    while time.time() - start_time < move_time:
        twist_pub.publish(twist)