#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import radians, pi
from find_my_mates.srv import OdomMove

ANGULAR_MAX_SPEED = 0.5

class RotateBot:
    def __init__(self):
        self.turtle_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.speechToTextSrv = rospy.Service("/move_odom", OdomMove, self.rotate)
        self.current_linear = 0.0
        self.current_angle = 0.0

    def odom_callback(self, msg):
        self.current_linear = msg.pose.pose.position.y
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_angle = yaw

    def rotate(self, msg):
        start_angle = self.current_angle + pi
        target_angle = start_angle + msg.angle
        if target_angle >= 2 * pi:
            target_angle = target_angle - 2 * pi
        distance = self.current_linear + msg.distance
        direction = msg.direction
        if direction == "right":
            target_angle = start_angle - msg.angle
        if target_angle <= 0:
            target_angle = target_angle + 2 * pi
        target_angle = target_angle - pi
        print(target_angle)
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            # 残差を計算
            error = abs(target_angle - self.current_angle)
            if abs(error) < 0.02:  # 0.02 radian未満になったら回転終了
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            twist = Twist()
            if error > ANGULAR_MAX_SPEED:
                error = ANGULAR_MAX_SPEED
            if direction == "right":
                error = -error
            twist.angular.z = Kp * error
            self.turtle_pub.publish(twist)
            rate.sleep()
        return True

if __name__ == '__main__':
    rospy.init_node('test_rotate')
    r = RotateBot()

    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()