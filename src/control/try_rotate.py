#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import radians
from find_my_mates.srv import OdomTurn

class RotateBot:
    def __init__(self, target_angle):
        self.turtle_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.speechToTextSrv = rospy.Service("/rotate_odom", OdomTurn, self.rotate)
        self.target_angle = target_angle
        self.current_angle = 0.0

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_angle = yaw

    def rotate(self, msg):
        target_angle = msg.angle
        direction = msg.direction
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            # 残差を計算
            error = target_angle - self.current_angle
            if abs(error) < 0.01:  # 0.01 radian未満になったら回転終了
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            twist = Twist()
            twist.angular.z = Kp * error
            self.turtle_pub.publish(twist)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('rota_sam')
    r = RotateBot()

    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()