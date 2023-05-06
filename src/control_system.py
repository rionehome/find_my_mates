#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
# from geometry_msgs.msg import Twist
# from find_my_mates.msg import LidarData
from find_my_mates.srv import OdomMove
from math import radians
import time

#環境に合わせて変更する
# APPROACH_SPEED = 0.08
# APPROACH_DIS = 0.8

#12=2.8
#23=1.45
#34=1.318

DISTANCE_01 = 2.40
DISTANCE_12 = 2.8
DISTANCE_23 = 1.45
DISTANCE_34 = 1.318

DISTANCE_10 = DISTANCE_01
DISTANCE_21 = DISTANCE_12
DISTANCE_32 = DISTANCE_23
DISTANCE_43 = DISTANCE_34
DISTANCE_24 = DISTANCE_23 + DISTANCE_34
DISTANCE_42 = DISTANCE_24
#
# position(1〜4) and location(①〜⑤)
# 
# 1----0.5(m)----2      ①
#                |
#               0.5(m)
#                |
#         ③     3      ②
#                |
#               0.5(m)
#                |
#         ④     4      ⑤

class ControlSystem():
    def __init__(self):
        # self.turtle_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.move_odom_srv = rospy.ServiceProxy("/move_odom", OdomMove)
        # self.twist = Twist()

    def move_position(self, current_position, next_position):
        if current_position == 0:
            self.move_odom_srv("None", 0, "right", -180)
            self.move_odom_srv("forward", DISTANCE_01, "None", 0)
        elif current_position == 1:
            if next_position == 0:
                self.move_odom_srv("forward", DISTANCE_10, "None", 0)
            else:
                self.move_odom_srv("forward", DISTANCE_12, "None", 0)
        elif current_position == 2:
            if next_position == 1:
                self.move_odom_srv("forward", DISTANCE_21, "None", 0)
            else:
                self.move_odom_srv("forward", DISTANCE_23, "None", 0)
        elif current_position == 3:
            if next_position == 2:
                self.move_odom_srv("forward", DISTANCE_32, "None", 0)
            else:
                self.move_odom_srv("forward", DISTANCE_34, "None", 0)
        elif current_position == 4:
            self.move_odom_srv("None", 0, "right", 180)
            self.move_odom_srv("forward", DISTANCE_43, "None", 0)
    def straight(self, direction, distance):
        rospy.wait_for_service("/move_odom")
        self.move_odom_srv(direction, distance, "None", 0)
        return 0


    def turn(self, direction, degree):
        rospy.wait_for_service("/move_odom")
        angle = float(radians(degree))
        self.move_odom_srv("None", 0, direction, angle)
        return 0

    def first_destination(self, next_location):
        rospy.wait_for_service("/move_odom")
        angle = float(radians(90))

        if next_location == 1:
            # move 1->2
            self.move_odom_srv("forward", DISTANCE_12, "None", 0)
            
            current_position = 2

        elif next_location == 2:
            # move 1->2, and turn right
            self.move_odom_srv("forward", DISTANCE_12, "right", angle)
            # move 2->3, and turn left
            self.move_odom_srv("forward", DISTANCE_23, "left", angle)

            current_position = 3

        elif next_location == 3:
            # move 1->2, and turn right
            self.move_odom_srv("forward", DISTANCE_12, "right", angle)
            # move 2->3, and turn right
            self.move_odom_srv("forward", DISTANCE_23, "right", angle)

            current_position = 3

        elif next_location == 4:
            # move 1->2, and turn right
            self.move_odom_srv("forward", DISTANCE_12, "right", angle)
            # move 2->4, and turn right
            self.move_odom_srv("forward", DISTANCE_24, "right", angle)

            current_position = 4

        elif next_location == 5:
            # move 1->2, and turn right
            self.move_odom_srv("forward", DISTANCE_12, "right", angle)
            # move 2->4, and turn left
            self.move_odom_srv("forward", DISTANCE_24, "left", angle)

            current_position = 4

        return current_position, next_location + 1

    def move_to_destination(self, current_position, next_location): #2~4の間のポジションを移動するとき（１つ前のlocationに人が居なかった場合）に、次のpositionに移動してlocationの方向を向く関数
        rospy.wait_for_service("/move_odom")
        
        if current_position == 2:
            # turn right
            angle = float(radians(90))
            self.move_odom_srv("None", 0, "right", angle)
            # move 2->3, and turn left
            self.move_odom_srv("forward", DISTANCE_23, "left", angle)

            current_position = 3

        elif current_position == 3 and next_location == 3:
            # turn back
            angle = float(radians(180))
            self.move_odom_srv("None", 0, "left", angle)
            
            current_position = 3  # as it is

        elif current_position == 3 and next_location == 4:
            # turn left
            angle = float(radians(90))
            self.move_odom_srv("None", 0, "left", angle)
            # move 3->4, and turn right
            self.move_odom_srv("forward", DISTANCE_34, "right", angle)

            current_position = 4

        elif current_position == 4:
            # turn back
            angle = float(radians(180))
            self.move_odom_srv("None", 0, "right", angle)

            current_position = 4  # as it is
        
        return current_position, next_location + 1

########## この間は、いじってないです。


    # def approach_guest(self):
    #     print(1)
    #     apr_guest_time = 0.0
    #     apr_start_time = time.time()
    #     while True:
    #         print(2)
    #         lidarData = rospy.wait_for_message("/lidar", LidarData)
    #         min_DISTANCE = min(lidarData.distance)
    #         front_back = lidarData.front_back
    #         print(min_DISTANCE)
    #         print(3)
            
    #         if min_DISTANCE < APPROACH_DIS and front_back == "front": #adj
    #             print("近づく")
    #             apr_guest_time = time.time() - apr_start_time
    #             print(apr_guest_time)
    #             # return apr_guest_time
    #             break
            
    #         self.twist.linear.x = APPROACH_SPEED
    #         self.twist.angular.z = 0
    #         move_time = 0.1

    #         print(4)

    #         start_time = time.time()
    #         while time.time() - start_time < move_time:
    #             self.turtle_pub.publish(self.twist)
    #             # apr_guest_time += move_time
    #     return apr_guest_time

    def return_position_from_guest(self, distance):
        self.move_odom_srv("back", distance, "None", 0)
        # print("近づき時間" + str(apr_guest_time))
        # self.twist.linear.x = APPROACH_SPEED * -1
        # self.twist.angular.z = 0

        # start_time = time.time()
        # while time.time() - start_time < apr_guest_time:
        #     self.turtle_pub.publish(self.twist)
        # time.sleep(2)

##########

    def return_start_position(self, current_position, next_location):
        rospy.wait_for_service("/move_odom")
        angle = float(radians(90))

        if current_position == 2:
            pass

        elif current_position == 3 and next_location == 3:
            # turn right
            self.move_odom_srv("None", 0, "right", angle)
            # move 3->2, and turn left
            self.move_odom_srv("back", DISTANCE_32, "left", angle)

        elif current_position == 3 and next_location == 4:
            # turn left
            self.move_odom_srv("None", 0, "left", angle)
            # move 3->2, and turn left
            self.move_odom_srv("back", DISTANCE_32, "left", angle)

        elif current_position == 4 and next_location == 5:
            # turn left
            self.move_odom_srv("None", 0, "left", angle)
            # move 4->2, and turn left
            self.move_odom_srv("back", DISTANCE_42, "left", angle)

        elif current_position == 4 and next_location == 6:
            # turn right
            self.move_odom_srv("None", 0, "right", angle)
            # move 3->2, and turn left
            self.move_odom_srv("back", DISTANCE_42, "left", angle)
        
        # move 2->1
        self.move_odom_srv("back", DISTANCE_21, "None", 0)
        
        current_position = 1
        
        return current_position 
        

if __name__=="__main__":

##### test program #####
# roslaunch find_my_mates control_test.launch
# Turtlebotも起動します。

    rospy.init_node("control_system")
    c = ControlSystem()
    
    # 全体を通してテスト
    def overall():
        current_position = 1
        next_location = 1
        
        print("start")
        while next_location < 6:
            current_position, next_location = c.first_destination(next_location)
            current_position = c.return_start_position(current_position, next_location)
        print("finish")
    
    # 初期位置からnext_locationの場所に行って帰ってくる
    def round_trip(next_location):
        current_position = 1
        
        print("start")
        current_position, next_location = c.first_destination(next_location)
        current_position = c.return_start_position(current_position, next_location)
        print("finish")
    
#   test
    next_location = 1
    round_trip(next_location)
    # overall()