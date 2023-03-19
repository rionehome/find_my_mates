#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String, Float32

# from find_my_mates.msg import ArmAction, MoveAction, LidarData, RealTime
from find_my_mates.msg import MoveAction, RealTime
from geometry_msgs.msg import Twist
import time
import sys
from math import pi
import os
import numpy as np

# from hand_detect.finger_direction import get_direction


STOP_DISTANCE = 1.0 + 0.15  # m
LINEAR_SPEED = 0.20  # m/s
ANGULAR_SPEED = 0.75  # m/s

# recognize_speech()


class FindMyMates:
    def __init__(self):
        rospy.init_node("main")
        # for robot movement
        self.move_pub = rospy.Publisher("/move", MoveAction, queue_size=1)

        # 回転用
        self.moveturn_pub = rospy.Publisher("/moveturn", MoveAction, queue_size=1)
        # for audio
        self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)
        # for realtime_Bios
        self.realtime_pub = rospy.Publisher("/realtime", RealTime, queue_size=1)

        # for speechToText

        self.speechToText = rospy.ServiceProxy("/speechToText", SpeechToText)

        # for isMeaning

        self.isMeaning = rospy.ServiceProxy("/isMeaning", isMeaning)

    def main(self):
        # wait for nodes
        time.sleep(3)

        # self.move360_sub = rospy.wait_for_message(/move360, MoveTest)

        global_direction = "forward"
        global_linear_speed = LINEAR_SPEED  # 対象に合わせて、速度を変える
        # global_angle_speed = ANGULAR_SPEED #これは使いみち無いかも
        global_distance = "normal"

        while True:
            """
            lidar information
            lidarData = rospy.wait_for_message('/lidar', LidarData) #lidar.pyから一つのデータが送られてくるまで待つ
            distance = lidarData.distance
            print(distance)
            mn = min(distance)
            mn_index = distance.index(mn)
            mx = max(distance)
            mx_index = distance.index(mx)
            print("min:", mn, mn_index)
            print("max", mx, mx_index)
            self.audio_pub.publish("おはよ") #audio.pyを動かす時に、引数として発言させたいものを入れる
            """

            mn = 0.4
            # Face information
            detectData = rospy.wait_for_message("/realtime", RealTime)
            p_direction = detectData.robo_p_drct
            p_distance = detectData.robo_p_dis

            # command select^
            c = MoveAction()
            c.distance = "forward"
            c.direction = "stop"
            c.distance = "normal"
            c.time = 0.1
            c.linear_speed = 0.0
            c.angle_speed = 0.0
            c.direction = "normal"

            # 回転指示が画像側から送られたら
            if p_direction == 3 and p_distance == 3:
                """
                move_test.pyにより回転動作を行う
                """

            else:
                if mn < 0.35:  # 止まる（Turtlebotからの距離が近い）
                    if global_direction != "stop":
                        print("I can get close here")
                        self.audio_pub.publish("これ以上近づけません")
                        global_direction = "stop"
                    c.direction = "stop"
                    c.angle_speed = 0.0

                    pass
                    # 止まることを最優先するため、初期値で設定している

                # 左にいるとき
                elif p_direction == 0:
                    if global_direction != "left":
                        print("you are left side so I turn left")
                        self.audio_pub.publish("たーんれふと")
                        global_direction = "left"
                    c.direction = "left"
                    c.angle_speed = ANGULAR_SPEED

                # 中央にいるとき
                elif p_direction == 1:
                    if global_direction != "forward":
                        print("you are good")
                        self.audio_pub.publish("いいね")
                        global_direction = "forward"
                    c.direction = "forward"

                # 右にいるとき
                elif p_direction == 2:
                    if global_direction != "right":
                        print("you are right side so I turn right")
                        self.audio_pub.publish("たーんらいと")
                        global_direction = "right"
                    c.direction = "right"
                    c.angle_speed = ANGULAR_SPEED

                if mn < 0.35:
                    c.linear_speed = 0.0

                # 遠いとき
                elif p_distance == 0:
                    if global_distance != "long":
                        self.audio_pub.publish("かくどはいいが、きょりがとおい")
                        print("angle but you have long distance.")
                        global_distance = "long"
                    c.distance = "long"
                    global_linear_speed = global_linear_speed * 1.25
                    c.linear_speed = global_linear_speed

                # 中距離のとき
                elif p_distance == 1:
                    if global_distance != "normal":
                        self.audio_pub.publish("かくどもきょりもいいかんじ")
                        print("angle and distance.")
                        global_distance = "normal"
                    c.distance = "normal"
                    c.linear_speed = global_linear_speed

                # 近いのとき
                elif p_distance == 2:
                    if global_distance != "short":
                        self.audio_pub.publish("かくどはいいが、きょりがちかい")
                        print("angle but you have short distance.")
                        global_distance = "short"
                    c.distance = "short"
                    global_linear_speed = global_linear_speed * 1.25
                    c.linear_speed = global_linear_speed

                self.move_pub.publish(c)  # 通常の顔への位置調整

            # 聞こえた名前を文字列に
            # recognize_speech(return_extract_person_name=True)

        exit(0)
        while True:
            distance = rospy.wait_for_message("/lidar", Float32)

            if distance.data > STOP_DISTANCE and distance.data < STOP_DISTANCE * 1.5:
                m = MoveAction()
                m.direction = "forward"
                m.speed = LINEAR_SPEED / 2
                m.time = 0.1
                self.move_pub.publish(m)
            elif distance.data > STOP_DISTANCE:
                m = MoveAction()
                m.direction = "forward"
                m.speed = LINEAR_SPEED
                m.time = 0.1
                self.move_pub.publish(m)
            else:
                break

        exit(0)

        # audio test
        self.audio_pub.publish("テスト")

        # robot arm test
        armAction = ArmAction()
        armAction.joint = [0, pi / 4, 0, 0]
        armAction.gripper = "open"
        # armAction.time = 6 # オプショナル。大きな角度を移動する場合に指定
        self.arm_pub.publish(armAction)

        time.sleep(3)
        sys.exit(0)


if __name__ == "__main__":
    findmymates = FindMyMates()
    findmymates.main()

# 左右の方向が与えられるので、それに対応して、回転するような動きをするもの
"""

"""
