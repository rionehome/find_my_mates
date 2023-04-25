#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geometry_msgs.msg import Twist
from find_my_mates.msg import LidarData, Cp, Gngt, Mtfsl, Ksntl, Mng, Rp, Rsp
import move_to_only_position as mtop
import turn
import rospy
import time

NEAR_GEST_SPEED = 0.02

twist = Twist()
cp = Cp()
gngt = Gngt()
turn = turn.Turn()

class ControlSystem():
    def __init__(self):
        #rospy.init_node("control")
        #self.twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.cp_pub = rospy.Publisher("/cp", Cp, queue_size=1)
        self.gngt_pub = rospy.Publisher("/gngt", Gngt, queue_size=1)
        self.mtfsl_sub = rospy.Subscriber("/mtfsl", Mtfsl, self.move_to_first_serch_location)
        self.ksntl_sub = rospy.Subscriber("/ksntl", Ksntl, self.keep_serch_next_to_location)
        self.mng_sub = rospy.Subscriber("/mng", Mng, self.move_near_guest)
        self.rp_sub = rospy.Subscriber("/rp", Rp, self.return_position)
        self.rsp_sub = rospy.Subscriber("/rsp", Rsp, self.return_start_position)

    def move_to_first_serch_location(self, msg):
        print("uketottayo")
        next_to_location = msg.next_to_location
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

    def keep_serch_next_to_location(self, msg):
        current_position = msg.current_position
        next_to_location = msg.next_to_location
        if current_position == 1 and next_to_location == 2:
            turn.turn_90("right")
            time.sleep(0.5)
            mtop.move_23()
            time.sleep(0.5)
            turn.turn_90("left")
            time.sleep(0.5)
            current_position = 2
            print("いち")

        elif current_position == 2 and next_to_location == 3:
            turn.turn_180("left")
            time.sleep(0.5)
            print("に")

        elif current_position == 3 and next_to_location == 4:
            turn.turn_90("left")
            time.sleep(0.5)
            mtop.move_34()
            time.sleep(0.5)
            turn.turn_90("right")
            time.sleep(0.5)
            current_position = 4
            print("さん")

        elif current_position == 4 and next_to_location == 5:
            turn.turn_180("left")
            time.sleep(0.5)
            print("よん")

        cp.current_position = current_position
        self.cp_pub.publish(cp)

    def move_near_guest(self, msg):
        go_near_gest_time = 0
        while True:
            lidarData = rospy.wait_for_message("/lidar", LidarData)
            min_distance = min(lidarData.distance)
            print("min_distance : " + min_distance)
            
            if min_distance < 0.9: #adj
                gngt.go_near_guest_time = go_near_guest_time
                self.gngt_pub.publish(gngt)
                return
            
            twist.linear.x = NEAR_GEST_SPEED
            twist.angular.z = 0
            move_time = 0.1
            start_time = time.time()
            
            while time.time() - start_time < move_time:
                self.twist_pub.publish(twist)
                go_near_guest_time += move_time

    def return_position(self, msg):
        go_near_guest_time = msg.go_near_guest_time
        twist.linear.x = NEAR_GEST_SPEED
        twist.angular.z = 0
        start_time = time.time()
        while time.time() - start_time < go_near_guest_time:
            self.twist_pub.publish(twist)

    def return_start_position(self, msg):
        current_position = msg.current_position
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
                
        

if __name__=="__main__":
    rospy.init_node("control")
    controlsystem = ControlSystem()
    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()