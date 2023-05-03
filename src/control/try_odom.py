#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from find_my_mates.srv import OdomMove
from tf.transformations import euler_from_quaternion
from math import pi

LINEAR_MAX_SPEED = 0.2
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
        self.current_angle = msg.pose.pose.orientation.z

    def rotate(self, msg):
        # 前進に関する設定
        distance = msg.distance
        start_linear = self.current_linear
        target_point = start_linear + distance
        if start_linear < 0:
            target_point = start_linear - distance
        
        # 回転に関する設定
        start_angle = self.current_angle + pi
        target_angle = start_angle + msg.angle
        if target_angle >= 2 * pi:
            target_angle = target_angle - 2 * pi
        direction = msg.direction
        if direction == "right":
            target_angle = start_angle - msg.angle
        if target_angle <= 0:
            target_angle = target_angle + 2 * pi
        target_angle = target_angle - pi
        
        print(target_point)
        print(target_angle)
        
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            # 残差を計算
            lin_error = abs(target_point - self.current_linear)
            if abs(lin_error) < 0.02:  # 0.02 radian未満になったら回転終了
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            twist = Twist()
            if lin_error > LINEAR_MAX_SPEED:
                lin_error = LINEAR_MAX_SPEED
            twist.linear.x = Kp * lin_error
            twist.angular.z = 0
            self.turtle_pub.publish(twist)
            rate.sleep()
        
        while not rospy.is_shutdown():
            # 残差を計算
            ang_error = abs(target_angle - self.current_angle)
            if abs(ang_error) < 0.02:  # 0.02 radian未満になったら回転終了
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            twist = Twist()
            if ang_error > ANGULAR_MAX_SPEED:
                ang_error = ANGULAR_MAX_SPEED
            if direction == "right":
                ang_error = -ang_error
            twist.linear.x = 0
            twist.angular.z = Kp * ang_error
            self.turtle_pub.publish(twist)
            rate.sleep()
        return True

if __name__ == '__main__':
    rospy.init_node('test_odom')
    r = RotateBot()

    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()