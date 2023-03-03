#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import time

from geometry_msgs.msg import Twist

class Sample():
    def __init__(self):
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)


    

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
            self.pub.publish(t)
            end_time = time.time()  #get the current time
            
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('move360')

    sample = Sample()

    #The following is the operation related to movement

    sample.pub_angular_z()
    