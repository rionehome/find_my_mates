#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String, Float32
#from find_my_mates.msg import ArmAction, MoveAction, LidarData, RealTime
from find_my_mates.msg import MoveAction, RealTime, LidarData
from geometry_msgs.msg import Twist
import time
import sys
from math import pi
import os
import numpy as np
from carry_my_luggage.msg import MoveAction, LidarData, PersonDetect
from carry_my_luggage.srv import Camera_msg, MoveArm, SpeechToText, isMeaning

STOP_DISTANCE = 1.0 + 0.15 # m
LINEAR_SPEED = 0.20 # m/s
ANGULAR_SPEED = 0.75 # m/s


class FindMyMates():
    def __init__(self):
        rospy.init_node("main")
        # for robot movement
        self.move_pub = rospy.Publisher("/move", MoveAction, queue_size=1)

        # for audio
        self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)
        #for realtime_Bios
        self.realtime_pub = rospy.Publisher("/realtime", RealTime, queue_size=1)
        # for camera
        self.camera_ser = rospy.ServiceProxy("/camera", Camera_msg)
        # for speechToText

        self.speechToText = rospy.ServiceProxy("/speechToText", SpeechToText )

        # for isMeaning

        self.isMeaning = rospy.ServiceProxy("/isMeaning", isMeaning )
    
    def go_near(self, move_mode="front", approach_distance=1.0):
        global_direction = "forward"
        global_linear_speed = LINEAR_SPEED #対象に合わせて、速度を変える
        # global_angle_speed = ANGULAR_SPEED #これは使いみち無いかも
        global_distance = "normal"
        #self.audio_pub.publish("おはよ") #audio.pyを動かす時に、引数として発言させたいものを入れる
        
        #Yolo information
        while True:
            print("go_near Function is runnning")
            
            
            #lidar information
            lidarData = rospy.wait_for_message('/lidar', LidarData) #lidar.pyから一つのデータが送られてくるまで待つ
            distance = lidarData.distance
            print(lidarData)
            print(distance)
            mn = min(distance)
            mn_index = distance.index(mn)
            mx = max(distance)

            mx_index = distance.index(mx)
            print("min:", mn, mn_index)
            print("max", mx, mx_index)
            detectData = rospy.wait_for_message('/realtime', RealTime)
            p_direction = detectData.robo_p_drct
            p_distance = detectData.robo_p_dis
            
            #command select^
            c = MoveAction()
            c.distance = "forward"
            c.direction = "stop"
            c.distance = "normal"
            c.time = 0.1
            c.linear_speed = 0.0
            c.angle_speed = 0.0
            c.direction = "normal"
            if mn < approach_distance: #止まる（Turtlebotからの距離が近い）
                if global_direction != "stop":
                    print("I can get close here")
                    self.audio_pub.publish("これ以上近づけません")
                    time.sleep(2)
                    global_direction = "stop" 
                    break
                c.direction = "stop"
                c.angle_speed = 0.0
                c.linear_speed = 0.0
                c.distance = "long"
                
                
                #止まることを最優先するため、初期値で設定している
            elif p_direction == 0:
                if global_direction != "left":
                    print("you are left side so I turn left")
                    self.audio_pub.publish("たーんれふと")
                    global_direction = "left"
                c.direction = "left"
                c.angle_speed = ANGULAR_SPEED + global_linear_speed * 2 
            elif p_direction == 2:
                if global_direction != "right":
                    print("you are right side so I turn right")
                    self.audio_pub.publish("たーんらいと")
                    global_direction = "right"
                c.direction = "right"
                c.angle_speed = ANGULAR_SPEED + global_linear_speed * 2 
            elif p_direction== 1:
                if global_direction != "forward":
                    print("you are good")
                    self.audio_pub.publish("かくどいいね")
                    global_direction = "forward"
                c.direction = "forward"

            if mn < approach_distance:
                c.linear_speed = 0.0

            elif p_distance == 0:
                if global_distance != "long":
                    self.audio_pub.publish("かくどはいいが、きょりがとおい")
                    print("angle but you have long distance.")
                    global_distance = "long"
                c.distance = "long"
                if global_linear_speed < 0.5:
                    global_linear_speed += 0.07
                if global_linear_speed < 1:
                    global_linear_speed += 0.02
                c.linear_speed = global_linear_speed
                print(c.linear_speed)

            elif p_distance == 2:
                if global_distance != "short":
                    self.audio_pub.publish("かくどはいいが、きょりがちかい")
                    print("angle but you have short distance.")
                    global_distance = "short"
                c.distance = "short"
                global_linear_speed = 0.1
                # if global_linear_speed >= 0.1:
                    # global_linear_speed -= 0.7
                c.linear_speed = 0.05
                print(c.linear_speed)
                self.audio_pub.publish("あああああああ")

            elif p_distance == 1:
                if global_distance != "normal":
                    self.audio_pub.publish("かくどもきょりもいいかんじ")
                    print("angle and distance.")
                    global_distance = "normal"
                c.distance = "normal"
                if global_linear_speed >= LINEAR_SPEED:
                    global_linear_speed -= 0.05
                c.linear_speed = global_linear_speed
                print(c.linear_speed)

            print("GLOBAL LINEAR : " + str(global_linear_speed))
            
            if move_mode == "back":
                c.linear_speed *= -1
                c.angle_speed *= -1
            self.move_pub.publish(c)

            
            
    def main(self):
        time.sleep(3)
        self.audio_pub.publish("")
        
                

                

            
        exit(0)
        while True:
            distance = rospy.wait_for_message('/lidar', Float32)

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

# 回転して、ゲストを見つける
    #@(制御)だいきが作った回転する部分を実装する
    #@(画像)ゲストを認識したときに、何か値をmain.pyに送る


# ゲストの前まで移動する
    #@(制御)person_detect.pyをOP以外の人間に対して動くようにする必要がある
    
    
# ゲストの特徴を取得する
    #@(制御)ゲストに名前を聞き、情報として取得する
    
    
# 回転して、OPの位置まで移動する
    #@(制御)だいきが作った回転する部分を実装する


# OPに、ゲストの名前、特徴を知らせる

    #forループ終了


#プログラムを終了する
    m = MoveAction()
    m.time = 0.1
    m.angle_speed = 0.0
    m.angle_speed = 0.0
    m.direction = "forward"
    m.distance = "normal"
    self.move_pub.publish(m)
    self.audio_pub.publish("実行終了しました")

            




if __name__ == '__main__':
    findmymates = FindMyMates()
    findmymates.main()

#左右の方向が与えられるので、それに対応して、回転するような動きをするもの
'''

'''