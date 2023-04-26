#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#control
import rospy
from control_system import ControlSystem
import time

#image


#sound
# from speech_and_NLP.src.speechToText import recognize_speech #音声認識
# from speech_and_NLP.src.tools.speech_to_text.isMeaning import is_meaning #文章の中に単語を検索する
# from speech_and_NLP.src.textToSpeech import textToSpeech #発話
# from speech_and_NLP.src.tools.speech_to_text.extractPersonName import extractPersonName #人名取得

class CIC():
    def __init__(self):
        #control
        rospy.init_node("cic")
        self.control = ControlSystem()

        #image

        #sound

        
    def main(self):
        time.sleep(3)

        # position:移動するする場所の中継地
        # location:人がいる可能性のある場所
        
        current_position = 1#現在position
        next_position = 2#次のposition
        next_location = 1#次に人がいるかもしれないlocation

        for i in range(3):
            mtfsl.next_to_location = next_to_location
            self.mtfsl_pub.publish(mtfsl)
            time.sleep(3)

            #画像認識で人間が要るかを検知
            discover_person = True#仮
            
            while discover_person:
                next_to_location += 1
                print(next_to_location)
                ksntl.current_position = current_position
                ksntl.next_to_location = next_to_location
                self.ksntl_pub.publish(ksntl)

                cp_sub = rospy.wait_for_message("/cp", Cp)
                current_position = cp_sub.current_position

                print("current_positionを出力")
                print(current_position)

                #画像認識で人間が要るかを検知
                # if True:#人間がいる
                    # discover_person = False#人がいる場合Falseにしてループを抜ける
                time.sleep(1)
                if current_position == 5:
                    break

            mng.tekitou = 1
            self.mng_pub.publish(mng)

            gngt_sub = rospy.wait_for_message("/gngt", Gngt)
            go_near_guest_time = gngt_sub.go_near_guest_time

            #画像で特徴量を取得する

            rp.go_near_guest_time = go_near_guest_time
            self.rp_pub.publish(rp)

            rsp.current_position =  current_position
            self.rsp_pub.publish(rsp)

if __name__=="__main__":
    cic = CIC()
    cic.main()