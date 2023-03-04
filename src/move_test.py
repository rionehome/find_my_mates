#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import time
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from find_my_mates.msg import MoveAction

class MoveTest():
    def __init__(self):
        self.movebase_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        start_rotation = rospy.Subscriber("/moveturn", Int16)
        #self.movebase_sub = rospy.Subscriber('/moveturn', Int16, call_back)


    def start_rotation():



        def pub_angular_z(self):     #rotational movement
    
            theta = 360.0 * 1.3   #1.3 is correction
            speed = 40.0    #speed
            target_time = theta / speed     #calculation of the time required for movement

            t = Twist()
            t.linear.x = 0

            ###### Negative value are clockwise #####
            t.angular.z = (-1) * speed * 3.1415 / 180.0    #conversion from degree to radians
            
            start_time = time.time()    #get the current time
            end_time = time.time()      #get the current time

            rate = rospy.Rate(30)
            while end_time - start_time <= target_time:  #repeat for as long as needed

                self.movebase_pub.publish(t)
                end_time = time.time()  #get the current time
            
                rate.sleep()

if __name__ == '__main__':
    rospy.init_node('moveturn')

    move_test = MoveTest()

    #The following is the operation related to movement

    move_test.pub_angular_z()
    