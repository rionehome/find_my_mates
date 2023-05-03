#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
<<<<<<< HEAD:src/control/try_odom.py
=======
from tf.transformations import euler_from_quaternion
from math import pi, sqrt
>>>>>>> dabc9f33d5e0faefe5914e739089b89d8d504e2a:src/control/move_odom.py
from find_my_mates.srv import OdomMove
from tf.transformations import euler_from_quaternion
from math import pi

LINEAR_MAX_SPEED = 0.2
ANGULAR_MAX_SPEED = 0.5
# 閾値
THRESHOLD_LINEAR = 0.03
THRESHOLD_ANGULAR = 0.05

class RotateBot:
    def __init__(self):
        self.turtle_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.speechToTextSrv = rospy.Service("/move_odom", OdomMove, self.move_odom)
        self.current_point = [0.0, 0.0]
        self.current_angle = 0.0

    def odom_callback(self, msg):
<<<<<<< HEAD:src/control/try_odom.py
        self.current_linear = msg.pose.pose.position.y
        self.current_angle = msg.pose.pose.orientation.z
=======
        self.current_point = [msg.pose.pose.position.x, msg.pose.pose.position.y]
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_angle = yaw
>>>>>>> dabc9f33d5e0faefe5914e739089b89d8d504e2a:src/control/move_odom.py

    def move_odom(self, msg):
        # 前進に関する設定
        forward_back = msg.forward_back
        distance = msg.distance
        start_point = self.current_point
        
        # 回転に関する設定
        start_angle = self.current_angle + pi   # -pi〜pi -> 0〜2*pi
        target_angle = start_angle + msg.angle
        if target_angle >= 2 * pi:
            target_angle = target_angle - 2 * pi
        left_right = msg.left_right
        if left_right == "right":
            target_angle = start_angle - msg.angle
        if target_angle <= 0:
            target_angle = target_angle + 2 * pi
<<<<<<< HEAD:src/control/try_odom.py
        target_angle = target_angle - pi
        
        print(target_point)
        print(target_angle)
=======
        target_angle = target_angle - pi        # 0〜2*pi -> -pi〜pi
>>>>>>> dabc9f33d5e0faefe5914e739089b89d8d504e2a:src/control/move_odom.py
        
        rate = rospy.Rate(10) # 10Hz
        while not rospy.is_shutdown():
            # 残差を計算
<<<<<<< HEAD:src/control/try_odom.py
            lin_error = abs(target_point - self.current_linear)
            if abs(lin_error) < 0.02:  # 0.02 radian未満になったら回転終了
=======
            x = self.current_point[0] - start_point[0]
            y = self.current_point[1] - start_point[1]
            lin_error = distance - sqrt(x**2 + y**2)
            if abs(lin_error) < THRESHOLD_LINEAR:  # (閾値) (m) 未満になったら回転終了
>>>>>>> dabc9f33d5e0faefe5914e739089b89d8d504e2a:src/control/move_odom.py
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            twist = Twist()
            if lin_error > LINEAR_MAX_SPEED:
                lin_error = LINEAR_MAX_SPEED
            if forward_back == "back":
                lin_error = -lin_error
            twist.linear.x = Kp * lin_error
            twist.angular.z = 0
            self.turtle_pub.publish(twist)
            rate.sleep()
        
        while not rospy.is_shutdown():
            # 残差を計算
            ang_error = abs(target_angle - self.current_angle)
            if abs(ang_error) < THRESHOLD_ANGULAR:  # (閾値) (radian) 未満になったら回転終了
                break
            # PID制御
            Kp = 1.0  # 比例制御ゲイン
            twist = Twist()
            if ang_error > ANGULAR_MAX_SPEED:
                ang_error = ANGULAR_MAX_SPEED
            if left_right == "right":
                ang_error = -ang_error
            twist.linear.x = 0
            twist.angular.z = Kp * ang_error
            self.turtle_pub.publish(twist)
            rate.sleep()
        return True

if __name__ == '__main__':
    rospy.init_node("move_odom")
    r = RotateBot()

    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()