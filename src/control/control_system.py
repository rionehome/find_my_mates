#!/usr/bin/env python

from geometry_msgs.msg import Twist
from find_my_mates.msg import LidarData, cp, gngt, Mtfsl, Ksntl, mng, rp, rsp
import move_to_only_position as mtop
import turn
import rospy
import time

NEAR_GEST_SPEED = 0.02

twist = Twist()
cp = cp()
gngt = gngt()

class ControlSystem():
    def __init__(self):
        self.twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.cp_pub = rospy.Publisher("/cp", cp, queue_size=1)
        self.gngt_pub = rospy.Publisher("/gngt", gngt, queue_size=1)
        self.mtfsl_sub = rospy.Subscriber("/mtfsl", Mtfsl, self.move_to_first_serch_location)
        self.ksntl_sub = rospy.Subscriber("/ksntl", Ksntl, self.keep_serch_next_to_location)
        self.mng_sub = rospy.Subscriber("/mng", mng, self.move_near_guest)
        self.rp_sub = rospy.Subscriber("/rp", rp, self.return_position)
        self.rsp_sub = rospy.Subscriber("/rsp", rsp, self.return_start_position)

    def move_to_first_serch_location(self, msg):
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
        if current_position == 2 and next_to_location == 2:
            turn.turn_90("right")
            mtop.move_23()
            turn.turn_90("left")
            current_position = 3

        elif current_position == 3 and next_to_location == 3:
            turn.turn_180("left")

        elif current_position == 3 and next_to_location == 4:
            turn.turn_90("left")
            mtop.move_34()
            turn.turn_90("right")
            current_position = 4

        elif current_position == 4 and next_to_location == 5:
            turn.turn_180("left")

        cp.current_position = current_position
        self.cp_pub(cp)

    def move_near_guest(self, msg):
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

        gngt.go_near_guest_time = go_near_guest_time
        self.gngt_pub(gngt)

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
    controlsystem = ControlSystem()
    controlsystem.main()