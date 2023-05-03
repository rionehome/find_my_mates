#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import radians

class RotateBot:
    def __init__(self, target_angle):
        rospy.init_node('rota_sam')
        self.cmd_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.target_angle = target_angle
        self.current_angle = 0.0

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_angle = yaw

    def rotate(self):
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            # 残差を計算
            error = self.target_angle - self.current_angle
            if abs(error) < 0.01:  # 0.01 radian未満になったら回転終了
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            Ki = 0.0  # 積分制御ゲイン
            Kd = 0.0  # 微分制御ゲイン
            cmd = Twist()
            cmd.angular.z = Kp * error
            self.cmd_pub.publish(cmd)
            rate.sleep()

if __name__ == '__main__':
    try:
        target_angle = radians(180)
        rotate_bot = RotateBot(target_angle)  # 目標角度は90度（1.57ラジアン）
        rotate_bot.rotate()
    except rospy.ROSInterruptException:
        pass
