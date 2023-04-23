#!/usr/bin/env python

from geometry_msgs.msg import Twist
import rospy
import time
import turn

LINEAR_SPEED = 0.20
TIME12 = 2.0
TIME23 = 2.0
TIME34 = 2.0
TIME24 = TIME23 + TIME34

turn = turn.Turn()


twist = Twist()
turtle_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)

def move_12():
    twist.linear.x = LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME12
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_21():
    twist.linear.x = -1 * LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME12
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_23():
    turn.turn_90("right")
    twist.linear.x = LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME23
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_32():
    twist.linear.x = -1 * LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME23
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_34():
    twist.linear.x = LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME34
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_43():
    twist.linear.x =  -1 * LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME34
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_24():
    twist.linear.x = LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME24
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

def move_42():
    twist.linear.x = -1 * LINEAR_SPEED
    twist.angular.z = 0

    move_time = TIME24
    start_time = time.time()

    while time.time() - start_time < move_time:
        turtle_pub.publish(twist)

