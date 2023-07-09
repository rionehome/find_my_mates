#32!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
import time
from std_msgs.msg import Bool, String
from find_my_mates.msg import LidarData, OdomData #, Info
from geometry_msgs.msg import Twist
from math import sqrt

#image
from img_tasks.mediapipe_main.FMM_person_detect_dd_ftr import Person
from img_tasks.mediapipe_main.UDP_module import UDP_recv, UDP_send

from find_my_mates.msg import ImgData

#sound
from speech_and_NLP.src.textToSpeech import textToSpeech #発話
from speech_and_NLP.src.speechToText import recognize_speech #音声認識
from speech_and_NLP.src.tools.speech_to_text.findNearestWord import find_nearest_word #文章の中に単語を検索する

import speech_recognition as sr

#navigation
from point_to_point import PointToPoint
import numpy as np

APPROACH_SPEED = 0.08
APPROACH_DIS = 0.9

Function = ["Bin", "Long Table", "White Table", "Tall Table", "Drawer"]
Guest = ["amelia", "angel", "ava", "charlie", "charlotte", "hunter", "max", "mia", "olivia", "parker", "sam", "jack", "noah","oliver", "thomas", "william"]

def is_features_usable(feature, used_feature_list, used_feature_n):
    if feature != "unknown" and not feature in used_feature_list and used_feature_n < 2:
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
        self.state = "移動中"

        self.sock = UDP_recv("始まり", HOST_NAME='127.0.0.10')
        self.sock2 = UDP_send("始まり", HOST_NAME='127.0.0.11')

        #image
        # self.img_str_pub = rospy.Publisher("/person", Bool, queue_size=1)
        # self.apr_guest_time = 0.0
        self.person = Person() #FMM_person_detect_dd_ftrのクラスの実体化

        #sound
        
        #navigation
        self.point_moving = PointToPoint()
    

    def info_data(self, msg):
        self.age = msg.age
        self.gender = msg.gender
        self.up_color = msg.up_color
        
     #時間制御の関数
    def time_control(self, move_time, linear_x=0, angular_z=0):
        start_time = time.time() #開始時刻
        
        twist = Twist()
        
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        
        while True:
            
            end_time = time.time() #終了時刻
            #print(end_time - start_time)
            
            self.velocity_pub.publish(twist)
            
            if end_time - start_time > move_time:
                break
        
        
    def main(self):
        print("final")
        textToSpeech("Hello, Family.", gTTS_lang="en")
        # textToSpeech("Hello, Family. Would you start detect suspicious person system? Please tell me Yes? or No?", gTTS_lang="en")
        # time.sleep(1)
        # response = ["yes", "no"]
        # res = recognize_speech(print_partial=True, use_break=1, lang='en-us')
        # audio_response = find_nearest_word(res, response)

        # if audio_response == "no":
        #     textToSpeech("I finish program.", gTTS_lang="en")
        #     return

        # # response = ["yes", "no"]
        # # res = recognize_speech(print_partial=True, use_break=1, lang='en-us')
        # audio_response = find_nearest_word(res, response)

        # if audio_response == "yes":
        #     textToSpeech("I finish program.", gTTS_lang="en")
        #     return
        
        textToSpeech("I start program.", gTTS_lang="en")
        textToSpeech("Please come closer", gTTS_lang="en")

        age, sex, up_color, down_color, glasstf = self.person.main(state="到着", sock=self.sock, sock2=self.sock2) #特徴を抽出するための写真を10枚撮影する
        color_jp = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"]
        color_en = ["orange", "yellow", "light green", "green","aqua", "blue", "purple", "pink", "red", "black","gray", "white"]
        for i in range(len(color_jp)):
            if up_color == color_jp[i]:
                up_color = color_en[i]

        for i in range(len(color_jp)):
            if down_color == color_jp[i]:
                down_color = color_en[i] 

        current_position = 1#現在地
        route = "down"#positionを時計回りを"up"、反時計回りを"down"としている
        
        textToSpeech("I can get your feature. Thank you. I'll see you later.", gTTS_lang="en")
        time.sleep(3)

        while True:
            textToSpeech("I start serching.", gTTS_lang="en")


            # person_count = self.person_count

            i = 1
            next_position = 1

            print("I start serching")
            while True:#人の有無を調べる
                print("current_position"  + str(current_position))
                
                if(next_position % 4 == 0){ / 最初のスタート位置
                    self.point_moving.send_goal([2.32376, -1.56895, np.pi/2])
                }
                elif(current_position % 4 == 1){ / ２つ目の位置
                    self.point_moving.send_goal([2.32376, -1.56895, np.pi/2])
                }
                elif(){ / ３つ目の位置
                    self.point_moving.send_goal([2.32376, -1.56895, np.pi/2])
                }
                elif(){ / ４つ目の位置
                    self.point_moving.send_goal([2.32376, -1.56895, np.pi/2])
                }
                
                next_position += 1
                
                discover_person = self.person.main(state="移動中", sock=self.sock, sock2=self.sock2)
                if discover_person == True and current_position == 3 and i == 4:
                    break
                

                # if route == "down":
                #     self.control.move_position(current_position, current_position - 1)
                #     current_position -= 1
                #     print("down")
                #     if current_position == 0:
                #         route = "up"

                # else:
                #     self.control.move_position(current_position, current_position + 1)
                #     current_position += 1
                #     print("up")
                #     if current_position == 4:
                #         route = "down"

                # if current_position == 3:
                #     i += 1
                
                # discover_person = self.person.main(state="移動中", sock=self.sock, sock2=self.sock2)
                # if discover_person == True and current_position == 3 and i == 4:
                #     break




                # self.control.turn("left", 90)
                # discover_person = self.person.main(state="移動中", sock=self.sock, sock2=self.sock2)
                # if discover_person == True:#人間を見つけたら
                #     textToSpeech("Welcome home!")
                #     break
                # self.control.turn("left", 90)
                # discover_person = self.person.main(state="移動中", sock=self.sock, sock2=self.sock2)
                # if discover_person == True:#人間を見つけたら
                #     textToSpeech("Welcome home!")
                #     break
                # self.control.turn("left", 90)
                # discover_person = self.person.main(state="移動中", sock=self.sock, sock2=self.sock2)
                # if discover_person == True:#人間を見つけたら
                #     textToSpeech("Welcome home!")
                #     break
                # self.control.turn("left", 90)
                # discover_person = self.person.main(state="移動中", sock=self.sock, sock2=self.sock2)

            a_age, a_sex, a_up_color, a_down_color, a_glasstf = self.person.main(state="到着", sock=self.sock, sock2=self.sock2) #特徴を抽出するための写真を10枚撮影する
            color_jp = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"]
            color_en = ["orange", "yellow", "light green", "green","aqua", "blue", "purple", "pink", "red", "black","gray", "white"]
            for i in range(len(color_jp)):
                if a_up_color == color_jp[i]:
                    a_up_color = color_en[i]

            for i in range(len(color_jp)):
                if a_down_color == color_jp[i]:
                    a_down_color = color_en[i] 

        
            # if age == a_age or sex == a_sex or a_up_color == up_color or a_down_color == down_color or a_glasstf == glasstf:
            if a_up_color == up_color or a_down_color == down_color:
                textToSpeech("Welcome home!", gTTS_lang="en")
                textToSpeech("Can I stop the program? Please tell me Yes? or No?", gTTS_lang="en")
                response = ["yes", "no"]
                res = recognize_speech(print_partial=True, use_break=1, lang='en-us')
                audio_response = find_nearest_word(res, response)

                if audio_response == "yes":
                    print("response : " + audio_response)
                    textToSpeech("I finish program.", gTTS_lang="en")
                    return
                print("response : " + audio_response)
            else:
                textToSpeech("Oh, no you are stranger I will call the police", gTTS_lang="en")
                print("Oh, no! You are stranger I will call the police")
                textToSpeech("I finish program.", gTTS_lang="en")
                return
                        



        time.sleep(20)   
        
    
    def listing_recognition(self):

        # Define the microphone as the audio source
        microphone = sr.Microphone()

        # Create a recognizer object
        recognizer = sr.Recognizer()

        # Set the language for speech recognition
        language = 'en-US'  # Update with the desired language code

        spoken_text = []

        # Function to process the audio data
        def process_audio():
            text = ""

            with microphone as source:
                print("Listening...")
                audio = recognizer.listen(source)

            try:
                # Perform speech recognition
                text = recognizer.recognize_google(audio, language=language)
                print("Recognized:", text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error:", str(e))

            return text

        # Continuously listen for audio input and process it
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        try:
            text = process_audio()
            spoken_text.append(text)
        except KeyboardInterrupt:
            print("Interrupted")
            
        
        return spoken_text



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