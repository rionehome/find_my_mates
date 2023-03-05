#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import time
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist

class MoveTest():
    def __init__(self):
        self.movebase_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
        #self.movebase_sub = rospy.Subscriber('/moveturn', Int16, call_back)


    #def call_back():


    def pub_angular_z(self):     #rotational movement
        theta = 360.0 * 1.3   #angle   1.3 is correction
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
    rospy.init_node('move360')

    sample = MoveTest()

    #The following is the operation related to movement

    sample.pub_angular_z()
    