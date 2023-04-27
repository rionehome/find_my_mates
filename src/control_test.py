#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
from control.turn import Turn
from control.move_only_between_position import Position
import time



class Test():
    def __init__(self):
        rospy.init_node("test")
        time.sleep(3)
        self.control = ControlSystem()
        self.turn = Turn()
        self.pos = Position()

    def main(self):
        next_to_location = 2
        # self.control.move_to_destination(next_to_location)
        self.turn.turn_90("right")
        time.sleep(3)
        self.turn.turn_180("right")
        time.sleep(3)
        # self.turn.turn_90("left")
        # time.sleep(3)
        # self.turn.turn_180("left")
        # time.sleep(3)

        

if __name__=="__main__":
    test = Test()
    test.main()