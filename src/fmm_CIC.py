#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
import time
from std_msgs.msg import Bool
import threading
from find_my_mates.msg import LidarData, OdomData
from geometry_msgs.msg import Twist
from math import sqrt

#image
from img_tasks.mediapipe_main.FMM_person_detect_dd_ftr import Person
from find_my_mates.msg import ImgData

#sound
from speech_and_NLP.src.textToSpeech import textToSpeech #発話
from speech_and_NLP.src.speechToText import recognize_speech #音声認識
from speech_and_NLP.src.tools.speech_to_text.findNearestWord import find_nearest_word #文章の中に単語を検索する

APPROACH_SPEED = 0.08
APPROACH_DIS = 0.8

Function = ["Bin", "Long Table", "White Table", "Tall Table", "Drawer"]
Guest = ["Amelia", "Angel", "Ava", "Charlie", "Charlotte" "Hunter", "Max", "Mia", "Olivia", "Parker", "Sam", "Jack", "Noah", "Thomas", "William"]


class CIC():
    def __init__(self):
        #control
        rospy.init_node("cic")
        self.control = ControlSystem()
        #self.audio = textToSpeech()
        # self.thread_approach_guest = threading.Thread(target=self.approach_guest)
        self.twist = Twist()
        self.turtle_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)

        #image
        self.img_str_pub = rospy.Publisher("/person", Bool, queue_size=1)
        # self.thread_img_pic = threading.Thread(target=person_detect)
        self.apr_guest_time = 0.0
        self.person = Person

        #sound
        
        
    def main(self):
        # function_list = ["Bin", "Long Table", "White Table", "Tall Table", "Drawer"]
        # position:移動するする場所の中継地
        # location:人がいる可能性のある場所
        current_position = 1#現在position
        next_location = 1#次に人がいるかもしれないlocation
        apr_guest_time = 0.0#人間に近づく為にかかった時間
        textToSpeech("I start program.", gTTS_lang="en")

        a = ["age", "gender", "glasses", "up_color", "down_color", "height"]
        b = []

        for i in range(3):
            thread_approach_guest = threading.Thread(target=self.approach_guest)
            thread_img_pic = threading.Thread(target=self.person.person_detect)
            current_position, next_location = self.control.first_destination(next_location)

            #画像認識で人間が要るかを検知
            discover_person = rospy.wait_for_message("/person", Bool)
            
            time.sleep(5)

            while discover_person.data:
                current_position, next_location = self.control.move_to_destination(current_position, next_location)

                #画像認識で人間が要るかを検知
                # if True:#人間がいる
                    # discover_person = False#人がいる場合Falseにしてループを抜ける
                    
                discover_person = rospy.wait_for_message("/person", Bool)

                time.sleep(5)

                if next_location == 6:#後で使うから要る
                    break

            time.sleep(2)

            textToSpeech(text="Hello!", gTTS_lang="en")

            odom_start_data = rospy.wait_for_message("/odom_data", OdomData)

            print("approachsuruhazu")
            self.approach_guest()

            #人間に近づく処理と写真を撮る処理を同時に行う必要があるため、threadingしている
            thread_approach_guest.start()
            print("apr:" + str(self.apr_guest_time))
            take_pic = thread_img_pic.start()
            
            print(take_pic)

            print("近づき終了")

            odom_finish_data = rospy.wait_for_message("/odom_data", OdomData)

            textToSpeech(text="Can I listen your name?", gTTS_lang="en")
            #(音声)音声（名前）を取得する
            res = recognize_speech(print_partial=True, use_break=3, lang='en-us')

            guest_name = find_nearest_word(res, Guest)
            print(guest_name)
            # guest_name = "mark"
            #(音声)名前を組み込んだ文章を作成する
            #(音声)今日は○○さん、みたいなことを言う
            textToSpeech(text="Hello " + guest_name + "I'm happy to see you", gTTS_lang="en")
            img_data = rospy.wait_for_message("/imgdata", ImgData)

            if i == 0:
                function = "age"
            

            #画像で特徴量を取得する
            time.sleep(3)

            x = odom_finish_data.x - odom_start_data.x
            y = odom_finish_data.y - odom_start_data.y
            distance = sqrt(x**2 + y**2)
            self.control.return_position_from_guest(distance)

            time.sleep(1)

            current_position = self.control.return_start_position(current_position, next_location)

            textToSpeech(text="Hi, operator", gTTS_lang="en")

            # a = ["age", "gender", "glasses", "up_color", "down_color", "height"]
            # b = []
            for j in range(3):
                k = a[0]
                l = a[1]

                a.remove(k)
                a.remove(l)

                b.append(k)
                b.append(l)

            #(音声)"○○"さんは、"家具名"の場所に居て、"特徴量" で、"特徴量"でした（特徴は二つのみ）
            textToSpeech(text=guest_name + "is near by" + Function[next_location - 2] + "and guest is" + "特徴量の変数" + "and" + "特徴量の変数", gTTS_lang="en")
            #(音声)I will search next guest!と喋る
            textToSpeech(text="I will search next guest!", gTTS_lang="en")
            

            print("finish")
            time.sleep(2)

        #(音声)以上で終了します。と喋る

    def approach_guest(self):
        print(1)
        apr_guest_time = 0.0
        apr_start_time = time.time()
        while True:
            print(2)
            lidarData = rospy.wait_for_message("/lidar", LidarData)
            min_DISTANCE = min(lidarData.distance)
            front_back = lidarData.front_back
            print(min_DISTANCE)
            print(3)
            
            if min_DISTANCE < APPROACH_DIS and front_back == "front": #adj
                print("近づく")
                self.apr_guest_time = time.time() - apr_start_time
                print(self.apr_guest_time)
                # return apr_guest_time
                break
            
            self.twist.linear.x = APPROACH_SPEED
            self.twist.angular.z = 0
            move_time = 0.1

            print(4)

            start_time = time.time()
            while time.time() - start_time < move_time:
                self.turtle_pub.publish(self.twist)
                # apr_guest_time += move_time
        # return apr_guest_time

    # def return_position_from_guest(self, distance):
    #     print("近づき時間" + str(self.apr_guest_time))
    #     self.twist.linear.x = APPROACH_SPEED * -1
    #     self.twist.angular.z = 0

    #     start_time = time.time()
    #     while time.time() - start_time < self.apr_guest_time:
    #         self.turtle_pub.publish(self.twist)
    #     time.sleep(2)

if __name__=="__main__":
    rospy.init_node('cic')
    try:
        cic = CIC()
        cic.main()
    except rospy.ROSInterruptException:
        print("pass")
        pass