#!/usr/bin/env python
# -*- coding: utf-8 -*-

#control
import rospy
from find_my_mates.msg import Cp, Gngt, Ksntl, Mng, Mtfsl, Rp, Rsp
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
        self.mtfsl_pub = rospy.Publisher("/mtfsl", Mtfsl, queue_size=1)
        self.ksntl_pub = rospy.Publisher("/ksntl", Ksntl, queue_size=1)
        self.mng_pub = rospy.Publisher("/mng", Mng, queue_size=1)
        self.rp_pub = rospy.Publisher("/rp", Rp, queue_size=1)
        self.rsp_pub = rospy.Publisher("/rsp", Rsp, queue_size=1)

        #image

        #sound

        
    def main(self):
        time.sleep(3)

        current_position = 1#現在地点
        next_to_location = 1#次に人がいるかもしれない場所
        start_position = 1#スタート地点
        ksntl = Ksntl()
        mng = Mng()
        mtfsl = Mtfsl()
        rp = Rp()
        rsp = Rsp()

        print("hi")
        mtfsl.next_to_location = next_to_location
        self.mtfsl_pub.publish(mtfsl)
        print("good bye")

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