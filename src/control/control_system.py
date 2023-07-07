#!/usr/bin/env python

from geometry_msgs.msg import Twist, PoseStamped
from find_my_mates.msg import LidarData
import rospy
import time
import numpy as np
import move_odom from RotateBot

#Odometryで移動する部分の長さを決める
DISTANCE = 0

#/click_positionノードで位置情報を取得する
OP_POS_X = 0
OP_POS_Y = 0
OP_POS_YAW = 0

OP_DOOR_POS_X = 0
OP_DOOR_POS_Y = 0
OP_DOOR_POS_YAW = 0

GUEST_DOOR_POS_X = 0
GUEST_DOOR_POS_Y = 0
GUEST_POS_YAW = 0

FIRST_POS_X = 0
FIRST_POS_Y = 0
FIRST_POS_YAW = 0

SECOND_POS_X = 0
SECOND_POS_Y = 0
SECOND_POS_YAW = 0

THIRD_POS_X = 0
THIRD_POS_Y = 0
THIRD_POS_YAW = 0

FOURTH_POS_X = 0
FOURTH_POS_Y = 0
FOURTH_POS_YAW = 0


twist = Twist()

class ControlSystem():
    def __init__(self):
        self.twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)

    def send_goal(self, next_location, current_position):
        yaw = 0
        if(next_location == 1):
            self.send_goal(6)
            self.move_door()
            x = OP_POS_X
            y = OP_POS_Y
            yaw = OP_POS_YAW
        elif(next_location == 2):
            if(current_position == 1):
                self.move_door()
                self.send_goal(5)
            x = FIRST_POS_X
            y = FIRST_POS_Y
            yaw = FIRST_POS_YAW
        elif(next_location == 3):
            if(current_position == 1):
                self.move_door()
                self.send_goal(5)
            x = SECOND_POS_X
            y = SECOND_POS_Y
            yaw = SECOND_POS_YAW
        elif(next_location == 4):
            if(current_position == 1):
                self.move_door()
                self.send_goal(5)
            x = THIRD_POS_X
            y = THIRD_POS_Y
            yaw = THIRD_POS_YAW
        elif(next_location == 5):# OPからドアまでの移動
            if(current_position == 1):
                self.move_door()
                self.send_goal(5)
            x = OP_DOOR_POS_X
            y = OP_DOOR_POS_Y
            yaw = OP_DOOR_POS_YAW
        elif(next_location == 6):
            if(current_position == 1):
                self.move_door()
                self.send_goal(5)
            x = GUEST_DOOR_POS_X
            y = GUEST_DOOR_POS_Y
            yaw = GUEST_POS_YAW

        msg = PoseStamped()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "map"
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = 0
        # send orientation with quaternion
        msg.pose.orientation.x = 0
        msg.pose.orientation.y = 0
        msg.pose.orientation.z = np.sin(yaw / 2)
        msg.pose.orientation.w = np.cos(yaw / 2)

        self.control_goal_pub.publish(msg)

    def move_door(self):#自己位置位低で動けない部分をOdometryで直線移動して通り過ぎる関数を作る
        r = RotateBot()
        r(DISTANCE)

    def move_to_next_room(self,to_or_):
        twist.linear.x = 0.20
        twist.angular.z = 0

        move_time = 2.0
        start_time = time.time()

        while time.time() - start_time < move_time:
            self.twist_pub.publish(twist)

    def move_to_position(self, serching_place):
        if serching_place == 0:
            
        elif serching_place == 1:

        elif serching_place == 2:

        elif serching_place == 3:

        elif serching_place == 4:


        
        serching_place = serching_place + 1

        return serching_place
    

    def move_near_guest(self):
        while True:
            lidarData = rospy.wait_for_message("/lidar", LidarData)
            min_distance = min(lidarData.distance)
            print("min_distance : " + min_distance)
            
            if min_distance < 0.9: #adj
                return
            
            twist.linear.x = 0.05
            twist.angular.z = 0
            move_time = 0.1
            start_time = time.time()
            
            while time.time() - start_time < move_time:
                self.twist_pub.publish(twist)
                
        

if __name__=="__main__":
    controlsystem = ControlSystem()
    controlsystem.main()