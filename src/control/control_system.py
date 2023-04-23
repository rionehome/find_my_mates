#!/usr/bin/env python

from geometry_msgs.msg import Twist
from find_my_mates.msg import LidarData
import move_to_only_position as mtop
import rospy
import time

NEAR_GEST_SPEED = 0.02

twist = Twist()

class ControlSystem():
    def __init__(self):
        self.twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)

    def return_start_position(self, current_position):
        if current_position == 1:
            mtop.move_21()

        elif current_position == 2:
            turn.turn_90("right")
            mtop.move_32()
            turn.turn_90("left")
            mtop.move_21()

        elif current_position == 3:
            turn.turn_90("left")
            mtop.move_32()
            turn.turn_90("left")
            mtop.move_21()

        elif current_position == 4:
            turn.turn_90("left")
            mtop.move_42()
            turn.turn_90("left")
            mtop.move_21()

        elif current_position == 5:
            turn.turn_90("right")
            mtop.move_42()
            turn.turn_90("left")
            mtop.move_21()

    def keep_serch_next_to_location(self, current_position, next_to_location):
        if current_position == 2 and next_to_location == 2:
            turn.turn_90("right")
            mtop.move_23()
            turn.turn_90("left")
            current_position = 3

        elif current_position == 3 and next_to_location == 3:
            turn.turn_180("left")

        elif current_position == 3 and next_to_location == 4:
            turn_90("left")
            mtop.move_34()
            turn.turn_90("right")
            current_position = 4

        elif current_position == 4 and next_to_location == 5:
            turn_180("left")

        return current_position

    def move_to_first_serch_location(self, next_to_location):
        if next_to_location == 1:
            mtop.move_12()

        elif next_to_location == 2:
            mtop.move_12()
            mtop.move_23()
            turn.turn_90("left")

        elif next_to_location == 3:
            mtop.move_12()
            mtop.move_23()
            turn.turn_90("right")

        elif next_to_location == 4:
            mtop.move_12()
            mtop.move_24()
            turn.turn_90("right")

        elif next_to_location == 5:
            mtop.move_12()
            mtop.move_24()
            turn.turn_90("left")

    def move_to_position(self, now_place, serching_place):
        discover_person = False

        move_function_num = 10 * now_place + serching_place

        if move_function_num = 12:
            mtop.move_12()
        elif move_function_num = 21:
            mtop.move_21()
        elif move_function_num = 23:
            mtop.move_23()
        elif move_function_num = 32:
            mtop.move_32()
        elif move_function_num = 34:
            mtop.move_34()
        elif move_function_num = 43:
            mtop.move_43()
        elif move_function_num = 24:
            mtop.move_24()
        elif move_function_num = 42:
            mtop.move_42()


        serching_place = serching_place + 1

        return now_place, serching_place, discover_person
    

    def move_near_guest(self):
        go_near_gest_time = 0
        while True:
            lidarData = rospy.wait_for_message("/lidar", LidarData)
            min_distance = min(lidarData.distance)
            print("min_distance : " + min_distance)
            
            if min_distance < 0.9: #adj
                return
            
            twist.linear.x = NEAR_GEST_SPEED
            twist.angular.z = 0
            move_time = 0.1
            start_time = time.time()
            
            while time.time() - start_time < move_time:
                self.twist_pub.publish(twist)
                go_near_guest_time += move_time

        return go_near_guest_time

    def return_position(self, go_near_gest_time):
        twist.linear.x = NEAR_GEST_SPEED
        twist.angular.z = 0
        start_time = time.time()
        while time.time() - start_time < go_near_gest_time:
            self.twist_pub.publish(twist)
                
        

if __name__=="__main__":
    controlsystem = ControlSystem()
    controlsystem.main()