#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import time
from geometry_msgs.msg import Twist
from control.move_only_between_position import Position
from control.turn import Turn
from find_my_mates.msg import LidarData
from math import radians
from find_my_mates.srv import OdomTurn

#環境に合わせて変更する
APPROACH_SPEED = 0.08
APPROACH_DIS = 0.8

class ControlSystem():
    def __init__(self):
        self.turtle_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.rotate_srv = rospy.ServiceProxy("/rotate_odom", OdomTurn)
        self.twist = Twist()
        self.pos = Position()
        self.turn = Turn()
        pass

    def first_destination(self, next_location):
        rospy.wait_for_service("/rotate_odom")
        angle = float(radians(90))

        if next_location == 1:
            self.pos.pos_12()
            current_position = 2

        elif next_location == 2:
            self.pos.pos_12()

            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            self.pos.pos_23()

            direction = "left"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("left")
            current_position = 3

        elif next_location == 3:
            self.pos.pos_12()

            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            self.pos.pos_23()

            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            current_position = 3

        elif next_location == 4:
            self.pos.pos_12()

            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            self.pos.pos_24()

            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            current_position = 4

        elif next_location == 5:
            self.pos.pos_12()

            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            self.pos.pos_24()

            direction = "left"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("left")

            current_position = 4

        return current_position, next_location + 1

    def move_to_destination(self, current_position, next_location): #2~4の間のポジションを移動するとき（１つ前のlocationに人が居なかった場合）に、次のpositionに移動してlocationの方向を向く関数
        rospy.wait_for_service("/rotate_odom")
        
        if current_position == 2:

            angle = float(radians(90))
            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            time.sleep(0.5)
            self.pos.pos_23()
            time.sleep(0.5)

            angle = float(radians(90))
            direction = "left"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("left")

            time.sleep(0.5)
            current_position = 3

        elif current_position == 3 and next_location == 3:
            angle = float(radians(180))
            direction = "left"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_180("left")

            time.sleep(0.5)

        elif current_position == 3 and next_location == 4:
            angle = float(radians(90))
            direction = "left"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("left")

            time.sleep(0.5)
            self.pos.pos_34()
            time.sleep(0.5)

            direction = "right"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_90("right")

            time.sleep(0.5)
            current_position = 4

        elif current_position == 4:
            angle = float(radians(180))
            direction = "left"
            res = self.rotate_srv(angle, direction)

            # self.turn.turn_180("left")
            
            time.sleep(0.5)

        return current_position, next_location + 1

    def approach_guest(self):
        print(1)
        apr_guest_time = 0.0
        apr_start_time = time.time()
        while True:
            print(2)
            lidarData = rospy.wait_for_message("/lidar", LidarData)
            min_distance = min(lidarData.distance)
            front_back = lidarData.front_back
            print(min_distance)
            print(3)
            
            if min_distance < APPROACH_DIS and front_back == "front": #adj
                print("近づく")
                apr_guest_time = time.time() - apr_start_time
                print(apr_guest_time)
                # return apr_guest_time
                break
            
            self.twist.linear.x = APPROACH_SPEED
            self.twist.angular.z = 0
            move_time = 0.1

            

            print(4)

            start_time = time.time()
            while time.time() - start_time < move_time:
                self.turtle_pub.publish(self.twist)
                # apr_guest_time += move_time
        return apr_guest_time

    def return_position_from_guest(self, apr_guest_time):
        self.twist.linear.x = APPROACH_SPEED * -1
        self.twist.angular.z = 0

        start_time = time.time()
        while time.time() - start_time < apr_guest_time:
            self.turtle_pub.publish(self.twist)
        time.sleep(2)

    def return_start_position(self, current_position, next_location):
        if current_position == 2:
            self.pos.pos_21()

        elif current_position == 3 and next_location == 3:
            self.turn.turn_90("right")
            self.pos.pos_32()
            self.turn.turn_90("left")
            self.pos.pos_21()

        elif current_position == 3 and next_location == 4:
            self.turn.turn_90("left")
            self.pos.pos_32()
            self.turn.turn_90("left")
            self.pos.pos_21()

        elif current_position == 4 and next_location == 5:
            self.turn.turn_90("left")
            self.pos.pos_42()
            self.turn.turn_90("left")
            self.pos.pos_21()

        elif current_position == 4 and next_location == 6:
            self.turn.turn_90("right")
            self.pos.pos_42()
            self.turn.turn_90("left")
            self.pos.pos_21()

        current_position = 1
        
        return current_position
                
        

if __name__=="__main__":
    #rospy.init_node("control")
    controlsystem = ControlSystem()