#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class RotateBot:
    def __init__(self, target_angle):
        rospy.init_node('/rotate_turtlebot')
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
    rospy.init_node('rotate_turtlebot')
    rotate = RotateBot()


# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import rospy
# from geometry_msgs.msg import Twist
# from nav_msgs.msg import Odometry
# from tf.transformations import euler_from_quaternion
# from math import radians
# import math

# class RotateBot:
#     def __init__(self, target_angle):
#         rospy.init_node('rotate_turtlebot')
#         self.turtle_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
#         self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
#         self.target_angle = target_angle
#         self.current_angle = 0.0

#     def odom_callback(self, msg):
#         orientation = msg.pose.pose.orientation
#         (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
#         self.current_angle = yaw

    # def rotate(self, target_angle=0, direction="left"):
    #     # self.target_angle = radians(target_angle)
    #     rate = rospy.Rate(10) # 10Hz
    #     # error = self.target_angle - self.current_angle
    #     if direction == "left":
    #         error = self.target_angle - self.current_angle
    #     else:
    #         error = self.current_angle - self.target_angle

    #     while abs(error) < 0.01:#abs()は絶対値を求める関数
    #         # 残差を計算
    #         if direction == "left":
    #             error = self.target_angle - self.current_angle
    #         else:
    #             error = self.current_angle - self.target_angle
    #         # if abs(error) < 0.01:  # 0.01 radian未満になったら回転終了
    #         #     break
    #         # PID制御
    #         Kp = 1.0  # 比例制御ゲイン
    #         # Ki = 0.0  # 積分制御ゲイン
    #         # Kd = 0.0  # 微分制御ゲイン
    #         twist = Twist()
    #         twist.angular.z = Kp * error
    #         self.turtle_pub.publish(twist)
    #         rate.sleep()

#     def euler_from_quaternion(self, quaternion):
#         x = quaternion[0]
#         y = quaternion[1]
#         z = quaternion[2]
#         w = quaternion[3]
        
#         sinr_cosp = 2.0 * (w * x + y * z)
#         cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
#         roll = math.atan2(sinr_cosp, cosr_cosp)
        
#         sinp = 2.0 * (w * y - z * x)
#         if abs(sinp) >= 1:
#             pitch = math.copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
#         else:
#             pitch = math.asin(sinp)
        
#         siny_cosp = 2.0 * (w * z + x * y)
#         cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
#         yaw = math.atan2(siny_cosp, cosy_cosp)
        
#         return roll, pitch, yaw

# if __name__ == '__main__':
#     try:
#         rotate_bot = RotateBot(target_angle=1.57)  # 目標角度は90度（1.57ラジアン）
#         rotate_bot.rotate()
#         rotate_bot = RotateBot(target_angle=1.57)  # 目標角度は90度（1.57ラジアン）
#         rotate_bot.rotate()
#     except rospy.ROSInterruptException:
#         print("pass")
#         pass





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