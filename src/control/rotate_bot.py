#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from find_my_mates.srv import OdomTurn
from math import radians

class RotateBot:
    def __init__(self):
        rospy.init_node('rotate_turtlebot')
        self.turtle_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.current_angle = 0.0

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_angle = yaw
        print(orientation)

    def rotate(self, angle, direction):
        
        if direction == "left":
            error = angle - self.current_angle
        elif direction == "right":
            error = self.current_angle - angle
            if error < 0:
                error += radians(360)  # errorが負の場合に360度を加算する
        else:
            rospy.logerr("Invalid direction: %s" % direction)
            return False

        # if direction == "left":
        #     error = angle - self.current_angle
        # elif direction == "right":
        #     error = angle + radians(360) - self.current_angle # 右回転するための処理
        # else:
        #     rospy.logerr("Invalid direction: %s" % direction)
        #     return False

        while abs(error) >= 0.01:
            print("whileのなか")
            if direction == "left":
                error = angle - self.current_angle
            elif direction == "right":
                error = self.current_angle - angle
                if error < 0:
                    error += radians(360)  # errorが負の場合に360度を加算する
            else:
                rospy.logerr("Invalid direction: %s" % direction)
                return False

            # if direction == "left":
            #     error = angle - self.current_angle
            # elif direction == "right":
            #     error = angle + radians(360) - self.current_angle # 右回転するための処理
            
            Kp = 1.0
            twist = Twist()
            twist.angular.z = Kp * error
            self.turtle_pub.publish(twist)

            rospy.sleep(1)
        return True

def handle_odom_turn(msg):
    rb = RotateBot()
    return rb.rotate(msg.angle, msg.direction)

if __name__ == '__main__':
    rospy.init_node('rotate_turtlebot')
    rospy.Service('/odom_turn', OdomTurn, handle_odom_turn)
    rospy.spin()




# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import rospy
# from geometry_msgs.msg import Twist
# from nav_msgs.msg import Odometry
# from tf.transformations import euler_from_quaternion
# from my_pkg.srv import OdomTurn
# from math import radians

# class RotateBot:
#     def __init__(self):
#         # rospy.init_node('rotate_turtlebot')
#         self.turtle_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
#         self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
#         self.current_angle = 0.0

#     def odom_callback(self, msg):
#         orientation = msg.pose.pose.orientation
#         (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
#         self.current_angle = yaw
#         print(orientation)

#     def rotate(self, angle, direction):
        
#         if direction == "left":
#             error = angle - self.current_angle
#         elif direction == "right":
#             error = radians(360) - angle
#         else:
#             rospy.logerr("Invalid direction: %s" % direction)
#             return False

#         while abs(error) >= 0.01:#abs()は絶対値を求める関数
#             print("whileのなか")
#             if direction == "left":
#                 error = angle - self.current_angle
#             elif direction == "right":
#                 error = self.current_angle - angle
            
#             # if abs(error) < 0.01:  # 0.01 radian未満になったら回転終了
#             #     break
#             # PID制御
#             Kp = 1.0  # 比例制御ゲイン
#             # Ki = 0.0  # 積分制御ゲイン
#             # Kd = 0.0  # 微分制御ゲイン
#             twist = Twist()
#             twist.angular.z = Kp * error
#             self.turtle_pub.publish(twist)

#             # 残差を計算
#             if direction == "left":
#                 pass
#                 # error = angle - self.current_angle
#             elif direction == "right":
#                 error = radians(360) - angle
#             else:
#                 rospy.logerr("Invalid direction: %s" % direction)
#                 return False

#             rospy.sleep(1)
#         return True

# def handle_odom_turn(msg):
#     rb = RotateBot()
#     # success = rb.rotate(msg.angle, msg.direction)
#     return rb.rotate(msg.angle, msg.direction)

# if __name__ == '__main__':
#     rospy.init_node('rotate_turtlebot')
#     rospy.Service('/odom_turn', OdomTurn, handle_odom_turn)
#     rospy.spin()
