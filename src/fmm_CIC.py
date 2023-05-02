#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
import time
from std_msgs.msg import Bool
import threading

#image
from img_tasks.mediapipe_main.FMM_person_detect_dd_ftr import person_pic
from find_my_mates.msg import ImgData


#sound
from speech_and_NLP.src.textToSpeech import textToSpeech #発話
from speech_and_NLP.src.speechToText import recognize_speech #音声認識
from speech_and_NLP.src.tools.speech_to_text.findNearestWord import find_nearest_word #文章の中に単語を検索する

Function = ["Bin", "Long Table", "White Table", "Tall Table", "Drawer"]
Guest = ["Amelia", "Angel", "Ava", "Charlie", "Hunter", "Max", "Mia", "Olivia", "Parker", "Sam", "Jack", "Noah", "Thomas", "William"]

class CIC():
    def __init__(self):
        #control
        rospy.init_node("cic")
        self.control = ControlSystem()
        #self.audio = textToSpeech()
        self.thread_approach_guest = threading.Thread(target=self.control.approach_guest)

        #image
        self.img_str_pub = rospy.Publisher("/person", Bool, queue_size=1)
        self.thread_img_pic = threading.Thread(target=person_pic)

        #sound
        
        
    def main(self):
        # function_list = ["Bin", "Long Table", "White Table", "Tall Table", "Drawer"]
        # position:移動するする場所の中継地
        # location:人がいる可能性のある場所
        current_position = 1#現在position
        next_location = 1#次に人がいるかもしれないlocation
        apr_guest_time = 0#人間に近づく為にかかった時間
        textToSpeech("I start program.", gTTS_lang="en")

        for i in range(3):
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

                if next_location == 6:#仮
                    break

            time.sleep(2)

            textToSpeech(text="Hello!", gTTS_lang="en")

            print("approachsuruhazu")
            # apr_guest_time = self.control.approach_guest()

            #人間に近づく処理と写真を撮る処理を同時に行う必要があるため、threadingしている
            apr_guest_time = self.thread_approach_guest.start()
            take_pic = self.thread_img_pic.start()
            
            print(take_pic)

            print("近づき終了")

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
            

            #画像で特徴量を取得する
            time.sleep(3)

            self.control.return_position_from_guest(apr_guest_time)

            time.sleep(1)

            current_position = self.control.return_start_position(current_position, next_location)

            textToSpeech(text="Hi, operator", gTTS_lang="en")

            #(音声)"○○"さんは、"家具名"の場所に居て、"特徴量" で、"特徴量"でした（特徴は二つのみ）
            textToSpeech(text=guest_name + "is near by" + Function[next_location - 2] + "and guest is" + "特徴量の変数" + "and" + "特徴量の変数", gTTS_lang="en")
            #(音声)I will search next guest!と喋る
            textToSpeech(text="I will search next guest!", gTTS_lang="en")
            

            print("finish")
            time.sleep(2)

        #(音声)以上で終了します。と喋る

if __name__=="__main__":
    rospy.init_node('cic')
    try:
        cic = CIC()
        cic.main()
    except rospy.ROSInterruptException:
        print("pass")
        pass