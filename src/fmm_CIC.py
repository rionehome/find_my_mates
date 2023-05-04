#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
import time
from std_msgs.msg import Bool, String
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
APPROACH_DIS = 0.9

Function = ["Bin", "Long Table", "White Table", "Tall Table", "Drawer"]
Guest = ["Amelia", "Angel", "Ava", "Charlie", "Charlotte", "Hunter", "Max", "Mia", "Olivia", "Parker", "Sam", "Jack", "Noah","Oliver", "Thomas", "William"]

def is_features_usable(feature, used_feature_list, used_feature_n):
    if feature != "不明" and not feature in used_feature_list and used_feature_n < 2:
        return True
    return False

class CIC():
    def __init__(self):
        #control
        rospy.init_node("cic")
        self.control = ControlSystem()
        self.twist = Twist()
        self.turtle_pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.first_feature1_num = 0
        self.first_feature2_num = 1
        self.second_feature1_num = 2
        self.second_feature2_num = 3
        self.pic_pub = rospy.Publisher("/state", String, queue_size=1)

        #image
        # self.img_str_pub = rospy.Publisher("/person", Bool, queue_size=1)
        # self.apr_guest_time = 0.0
        self.person = Person

        #sound
        
        
    def main(self):
        state = String()
        state.data = "到着"#この情報をpublishすることで、写真を撮る関数を実行する
        self.pic_pub.publish(state)

        # position:移動するする場所の中継地
        # location:人がいる可能性のある場所
        current_position = 1#現在position
        next_location = 1#次に人がいるかもしれないlocation
        # apr_guest_time = 0.0#人間に近づく為にかかった時間
        textToSpeech("I start program.", gTTS_lang="en")

        feature_list = ["age", "gender", "glasses", "up_color", "down_color", "height"]
        used_feature_list = []

        print("start")

        for i in range(3):
            current_position, next_location = self.control.first_destination(next_location)

            #画像認識で人間が要るかを検知
            print("aaa")
            discover_person.data = rospy.wait_for_message("/person", Bool)
            print("bbb")

            while not discover_person.data:
                print("No person")
                current_position, next_location = self.control.move_to_destination(current_position, next_location)

                time.sleep(1)

                discover_person = rospy.wait_for_message("/person", Bool)

                if next_location == 6:#後で使うから要る
                    break

            print("There is person.")

            textToSpeech(text="Hello!", gTTS_lang="en")

            odom_start_data = rospy.wait_for_message("/odom_data", OdomData)

            self.pic_pub.publish(state)
            self.approach_guest()

            # print("apr:" + str(self.apr_guest_time))
            

            print("I finish to approach guest.")
            time.sleep(1)

            odom_finish_data = rospy.wait_for_message("/odom_data", OdomData)

            textToSpeech(text="Can I listen your name?", gTTS_lang="en")

            #(音声)音声（名前）を取得する
            res = recognize_speech(print_partial=True, use_break=3, lang='en-us')

            guest_name = find_nearest_word(res, Guest)
            print(guest_name)

            #(音声)名前を組み込んだ文章を作成する
            #(音声)今日は○○さん、みたいなことを言う
            textToSpeech(text="Hello " + guest_name + "I'm happy to see you", gTTS_lang="en")

            #画像で特徴量を取得する
            img_data = rospy.wait_for_message("/imgdata", ImgData)

            x = odom_finish_data.x - odom_start_data.x
            y = odom_finish_data.y - odom_start_data.y
            distance = sqrt(x**2 + y**2)
            self.control.return_position_from_guest(distance)

            time.sleep(1)

            current_position = self.control.return_start_position(current_position, next_location)
            
            age = img_data.age_push
            sex = img_data.sex_push
            up_color = img_data.up_color_push
            down_color = img_data.down_color_push
            glasstf = img_data.glasstf_pushglasstf

            used_feature_n = 0

            if is_features_usable(age, used_feature_list, used_feature_n):
                used_feature_list.push("age")
                used_feature_n += 1
            
            if is_features_usable(age, used_feature_list, used_feature_n):
                used_feature_list.push("sex")
                used_feature_n += 1
            
            if is_features_usable(up_color, used_feature_list, used_feature_n):
                used_feature_list.push("up_color")
                used_feature_n += 1
            
            if is_features_usable(down_color, used_feature_list, used_feature_n):
                used_feature_list.push("down_color")
                used_feature_n += 1
            
            if is_features_usable(glasstf, used_feature_list, used_feature_n):
                used_feature_list.push("glasses")
                used_feature_n += 1
            
            first_feature = used_feature_list[-1]
            second_feature = used_feature_list[-2]


            i = first_feature
            j = second_feature

            if i == "age":
                first_feature = age
            elif i == "sex":
                first_feature = sex
            elif i == "up_color":
                first_feature = up_color
            elif i == "down_color":
                first_feature = down_color
            elif i == "glasses":
                first_feature = glasstf
            
            if j == "age":
                second_feature = age
            elif j == "sex":
                second_feature = sex
            elif j == "up_color":
                second_feature = up_color
            elif j == "down_color":
                second_feature = down_color
            elif j == "glasses":
                second_feature = glasstf

            # first_feature １つめの特徴量
            # second_feature ２つめの特徴量
            # ここで煮るなり焼くなり二宮和也

            if len(used_feature_n) < 2:
                print("Not enough features")

            self.control.turn("right", 90)

            textToSpeech(text="Hi, operator", gTTS_lang="en")

            #(音声)"○○"さんは、"家具名"の場所に居て、"特徴量" で、"特徴量"でした（特徴は二つのみ）
            textToSpeech(text=guest_name + "is near by" + Function[next_location - 2] + "and guest is" + "特徴量の変数" + "and" + "特徴量の変数", gTTS_lang="en")
            #(音声)I will search next guest!と喋る
            
            textToSpeech(text="I will search next guest!", gTTS_lang="en")

            time.sleep(1)

            self.control.turn("left", 90)
            

            print(str(i) + "person" + "finish")

        #(音声)以上で終了します。と喋る
        textToSpeech("I'll finish serch guest. Thank you", gTTS_lang="en")

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