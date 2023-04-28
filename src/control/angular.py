#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from math import radians, pi

# 初期化
rospy.init_node('rotate_turtlebot', anonymous=False)

# Twistメッセージのインスタンスを作成
cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

# 角度と速度を指定
angular_speed = 45 * 2 * pi / 360  # 45度毎秒
relative_angle = radians(90)  # 回転する角度（ラジアン）

# Twistメッセージのインスタンスを作成し、角速度を設定
rotate_cmd = Twist()
rotate_cmd.angular.z = angular_speed

# 90度回転
t0 = rospy.Time.now().to_sec()
current_angle = 0
while(current_angle < relative_angle):
    cmd_vel.publish(rotate_cmd)
    t1 = rospy.Time.now().to_sec()
    current_angle = angular_speed * (t1 - t0)

# 停止
rotate_cmd = Twist()
cmd_vel.publish(rotate_cmd)

# 終了
rospy.spin()