#!/usr/bin/env python
# -*- coding: utf-8 -*-

from find_my_mates.msg import PersonDetect, MoveAction, LidarData
import rospy
import time
from std_msgs.msg import String

ANGULAR_SPEED = 0.75
LINEAR_SPEED = 0.05
keep_distance = 0.5
keep_first_direction = "right"

m = MoveAction()

def init(self):
    self.move_pub = rospy.Publisher("/move", MoveAction, queue_size=1)
    self.switch_pub = rospy.Publisher("/switch_camera", String, queue_size=1)

def main(self):
#マスターの前
    #180度回転する
    m.direction = "right"
    m.angle_speed = ANGULAR_SPEED
    m.linear_speed = 0.0
    m.time = 9.5
    self.move_pub.publish(m)

#隣の部屋に移動する
    start_time = time.time()
    target_time = 3.5 #調整アリーナの幅によって実行時間を調整したい
    while time.time() - start_time < target_time:
        lidarData = rospy.wait_for_message('/lidar', LidarData)
        distance = lidarData.distance
        mn = min(distance)
        mn_index = distance.index(mn)
        mx = max(distance)
        mx_index = distance.index(mx)
        print("min:", mn, mn_index)
        print("max", mx, mx_index)
        front_back = lidarData.front_back
        left_right = lidarData.left_right
        
        while mn < 0.6 and front_back == "front": #調整Turtlebotがギリギリぶつからない位置に設定したい#調整これ系高性能PCで書いたやつを参考にする
            lidarData = rospy.wait_for_message('/lidar', LidarData)
            target_time += 0.1 #進む距離が変わらないように
            if left_right == "Right":
                m.direction = "left"
            else:
                m.direction = "right"
            m.angle_speed = 0.4
            m.linear_speed = 0.0
            m.time = 0.1
            self.move_pub.publish(m)

        else:
            m.direction = "left"
            m.angle_speed = 0.0
            m.linear_speed = LINEAR_SPEED
            m.time = 0.1
            self.move_pub.publish(m)

#隣の部屋の中心あたりまで移動した時に止まって、人間が居る方向に向く
    m.direction = "right"
    m.angle_speed = ANGULAR_SPEED
    m.linear_speed = 0.0
    m.time = 4.7 #調整90度回転したい
    self.move_pub.publish(m)

#人間との距離が近くなった時にperson_detectを実行して、人間から決まった距離を取って止まる
    switch = String()
    switch.data = "person"
    self.switch_pub.publish(switch)
    detectData = rospy.wait_for_message('/person', PersonDetect)
    p_direction = detectData.robo_p_drct
    p_distance = detectData.robo_p_dis
        
    while p_distance == 0:#調整どの人間に近づいた時にするのかを書く#調整person_detect.py内の遠い判定を調整する
        lidarData = rospy.wait_for_message('/lidar', LidarData)
        detectData = rospy.wait_for_message('/person', PersonDetect)
        distance = lidarData.distance
        mn = min(distance)
        mn_index = distance.index(mn)
        mx = max(distance)
        mx_index = distance.index(mx)
        print("min:", mn, mn_index)
        print("max", mx, mx_index)
        front_back = lidarData.front_back
        left_right = lidarData.left_right
        # while mn < 0.6 and front_back == "front": #調整Turtlebotがギリギリぶつからない位置に設定したい#調整これ系高性能PCで書いたやつを参考にする
        #     lidarData = rospy.wait_for_message('/lidar', LidarData)
        #     if left_right == "Right":
        #         m.direction = "left"
        #     else:
        #         m.direction = "right"
        #     m.angle_speed = 0.4
        #     m.linear_speed = 0.0
        #     m.time = 0.1
        #     self.move_pub.publish(m)
        if mn < 0.6:
            keep_distance = distance[11]
            break
        m.direction = "right"
        m.angle_speed = 0.0
        m.linear_speed = LINEAR_SPEED #調整人を探すからゆっくりでいい
        m.time = 0.1
        self.move_pub.publish(m)
        
    keep_first_direction = p_direction#戻る時に利用する
    
    detectData = rospy.wait_for_message('/person', PersonDetect)
    p_direction = detectData.robo_p_drct
    p_distance = detectData.robo_p_dis
    while p_direction != 1:
        detectData = rospy.wait_for_message('/person', PersonDetect)
        if p_direction == 2:
            m.direction = "right"
        elif p_direction == 0:
            m.direction = "left"
        m.angle_speed = ANGULAR_SPEED
        m.linear_speed = 0.0
        m.time = 9.5
        self.move_pub.publish(m)
        
    while mn > 1.3:#調整ゲストとの最終的な距離
        lidarData = rospy.wait_for_message('/lidar', LidarData)
        distance = lidarData.distance
        mn = min(distance)
        mn_index = distance.index(mn)
        mx = max(distance)
        mx_index = distance.index(mx)
        print("min:", mn, mn_index)
        print("max", mx, mx_index)
        front_back = lidarData.front_back
        left_right = lidarData.left_right
        
        m.direction = "right"
        m.angle_spee = 0.0
        m.linear_speed = LINEAR_SPEED
        m.time = 0.1
        self.move_pub.publish(m)
        
#人間の特徴量を取る関数を実行する
    #調整@人間の特徴量を取る関数を実行する

#最初に人間に向けて方向転換しておいた方向を記録しておき、そっち方向に４５度ぐらい回転して、そのままアリーナの壁まで直線運動する
    m.direction = keep_first_direction
    m.angle_speed = ANGULAR_SPEED
    m.linear_speed = 0.0
    m.time = 5.2#調整とにかく45度は回転するようにする！
    self.move_pub.publish(m)
    
    i = 0.1
    while i * LINEAR_SPEED < keep_distance:
        lidarData = rospy.wait_for_message('/lidar', LidarData)
        distance = lidarData.distance
        mn = min(distance)
        mn_index = distance.index(mn)
        mx = max(distance)
        mx_index = distance.index(mx)
        print("min:", mn, mn_index)
        print("max", mx, mx_index)
        front_back = lidarData.front_back
        left_right = lidarData.left_right
        
        while mn < 0.6 and front_back == "front": #調整Turtlebotがギリギリぶつからない位置に設定したい#調整これ系高性能PCで書いたやつを参考にする
            lidarData = rospy.wait_for_message('/lidar', LidarData)
            if left_right == "Right":
                m.direction = "left"
            else:
                m.direction = "right"
            m.angle_speed = 0.4
            m.linear_speed = 0.0
            m.time = 0.1
            self.move_pub.publish(m)

        else:
            i += 0.1
            m.direction = "left"
            m.angle_speed = 0.0
            m.linear_speed = LINEAR_SPEED
            m.time = 0.1
            self.move_pub.publish(m)
            
    while mn < 0.6:#調整Turtlebotがギリギリぶつからない位置に設定したい#調整これ系高性能PCで書いたやつを参考にする
        m.direction = "right"
        m.angle_speed = 0.0
        m.linear_speed = LINEAR_SPEED #調整人を探すからゆっくりでいい
        m.time = 0.1
        self.move_pub.publish(m)
#壁に着いたら左に回転して、そのまま右の壁に物から内容にマスターの元へ移動する
    while p_distance == 0:#調整どの人間に近づいた時にするのかを書く#調整person_detect.py内の遠い判定を調整する
        lidarData = rospy.wait_for_message('/lidar', LidarData)
        detectData = rospy.wait_for_message('/person', PersonDetect)
        distance = lidarData.distance
        mn = min(distance)
        mn_index = distance.index(mn)
        mx = max(distance)
        mx_index = distance.index(mx)
        print("min:", mn, mn_index)
        print("max", mx, mx_index)
        front_back = lidarData.front_back
        left_right = lidarData.left_right
        while mn < 0.6 and front_back == "front": #調整Turtlebotがギリギリぶつからない位置に設定したい#調整これ系高性能PCで書いたやつを参考にする
            lidarData = rospy.wait_for_message('/lidar', LidarData)
            if left_right == "Right":
                m.direction = "left"
            else:
                m.direction = "right"
            m.angle_speed = 0.4
            m.linear_speed = 0.0
            m.time = 0.1
            self.move_pub.publish(m)
        m.direction = "right"
        m.angle_speed = 0.0
        m.linear_speed = LINEAR_SPEED #調整人を探すからゆっくりでいい
        m.time = 0.1
        self.move_pub.publish(m)