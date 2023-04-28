#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class RotateBot:
    def __init__(self, target_angle):
        rospy.init_node('rotate_turtlebot')
        self.cmd_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.target_angle = target_angle
        self.current_angle = 0.0

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_angle = yaw

    def rotate(self):
        print("aaa")
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
            print("bbbbb")

if __name__ == '__main__':
    try:
        rotate_bot = RotateBot(target_angle=1.57)  # 目標角度は90度（1.57ラジアン）
        rotate_bot.rotate()
        rotate_bot = RotateBot(target_angle=1.57)  # 目標角度は90度（1.57ラジアン）
        rotate_bot.rotate()
    except rospy.ROSInterruptException:
        print("pass")
        pass





# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import rospy
# from geometry_msgs.msg import Twist
# from math import radians, pi

# # 初期化
# rospy.init_node('rotate_turtlebot', anonymous=False)

# # Twistメッセージのインスタンスを作成
# cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

# # 角度と速度を指定
# angular_speed = 45 * 2 * 3.14 / 360  # 45度毎秒
# relative_angle = radians(90)  # 回転する角度（ラジアン）

# # Twistメッセージのインスタンスを作成し、角速度を設定
# rotate_cmd = Twist()
# rotate_cmd.angular.z = angular_speed * -1

# # 90度回転
# t0 = rospy.Time.now().to_sec()
# current_angle = 0
# while(current_angle < relative_angle):
#     cmd_vel.publish(rotate_cmd)
#     t1 = rospy.Time.now().to_sec()
#     current_angle = angular_speed * (t1 - t0)

# # 停止
# rotate_cmd = Twist()
# cmd_vel.publish(rotate_cmd)

# # 終了
# rospy.spin()