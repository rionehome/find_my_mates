#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
import time
from std_msgs.msg import Bool

#image


#sound
# from audio_system import AudioSystem
from speech_and_NLP.src.textToSpeech import textToSpeech #発話
# from audio.speech_and_NLP.src.speechToText import recognize_speech #音声認識
# from speech_and_NLP.src.tools.speech_to_text.isMeaning import is_meaning #文章の中に単語を検索する
# from speech_and_NLP.src.tools.speech_to_text.extractPersonName import extractPersonName #人名取得

class CIC():
    def __init__(self):
        #control
        rospy.init_node("cic")
        time.sleep(3)
        self.control = ControlSystem()
        # self.audio = textToSpeech()

        #image

        #sound

        
    def main(self):
        # position:移動するする場所の中継地
        # location:人がいる可能性のある場所
        current_position = 1#現在position
        next_location = 1#次に人がいるかもしれないlocation
        apr_guest_time = 0#人間に近づく為にかかった時間
        textToSpeech(text="I start program.", gTTS_lang="en")

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

            apr_guest_time = self.control.approach_guest()

            textToSpeech(text="Can I listen your name?", gTTS_lang="en")

            #画像で特徴量を取得する
            time.sleep(3)

            self.control.return_position_from_guest(apr_guest_time)

            time.sleep(1)

            current_position = self.control.return_start_position(current_position, next_location)
            print("finish")
            
            #特徴量の情報をOPに対して喋る
            time.sleep(2)

if __name__=="__main__":
    cic = CIC()
    cic.main()