#!/usr/bin/env python

from geometry_msgs.msg import Twist
from find_my_mates.msg import LidarData
import rospy
import time

twist = Twist()

class ControlSystem():
    def __init__(self):
        self.twist_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)

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