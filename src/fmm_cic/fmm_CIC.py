#!/usr/bin/env python
# -*- coding: utf-8 -*-

#control
import rospy

#image


#sound
from speech_and_NLP.src.speechToText import recognize_speech #音声認識
from speech_and_NLP.src.tools.speech_to_text.isMeaning import is_meaning #文章の中に単語を検索する
from speech_and_NLP.src.textToSpeech import textToSpeech #発話
from speech_and_NLP.src.tools.speech_to_text.extractPersonName import extractPersonName #人名取得

class CIC():
    def __init__(self):
        #control
        rospy.init_node("cic")
        self.control_

        #image

        #sound

        
    def main(self):
        current_position = 1#現在地点
        next_to_location = 1#次に人がいるかもしれない場所
        start_position = 1#スタート地点

        for i in range(3):
            control_system.move_to_first_serch_location(next_to_location)

            #画像認識で人間が要るかを検知
            discover_person = True#仮
            while discover_person:
                current_position = control_system.keep_serch_next_to_location(current_position, next_to_location)
                next_to_location += 1
                #画像認識で人間が要るかを検知
                if True:#人間がいる
                    discover_person = False#人がいる場合Falseにしてループを抜ける

            go_near_guest_time = control_system.move_near_guest()

            #画像で特徴量を取得する

            control_system.return_position(go_near_guest_time)

            control_system.return_start_position(current_position)

if __name__=="__main__":
    cic = CIC()
    cic.main()