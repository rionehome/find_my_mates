#!/usr/bin/env python
# -*- coding: utf-8 -*-

#control
import rospy
from find_my_mates.msg import cp, gngt, Ksntl, mng, Mtfsl, rp, rsp

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
        self.mtfsl_pub = rospy.Publisher("/Mtfsl", Mtfsl, queue_size=1)
        self.ksntl_pub = rospy.Publisher("/Ksntl", Ksntl, queue_size=1)
        self.mng_pub = rospy.Publisher("/mng", mng, queue_size=1)
        self.rp_pub = rospy.Publisher("/rp", rp, queue_size=1)
        self.rsp_pub = rospy.Publisher("/rsp", rsp, queue_size=1)

        #image

        #sound

        
    def main(self):
        current_position = 1#現在地点
        next_to_location = 1#次に人がいるかもしれない場所
        start_position = 1#スタート地点
        ksntl = Ksntl()
        mng = mng()
        mtfsl = Mtfsl()
        rp = rp()
        rsp = rsp()


        for i in range(3):
            mtfsl.next_to_location = next_to_location
            self.mtfsl_pub(mtfsl)

            #画像認識で人間が要るかを検知
            discover_person = True#仮
            while discover_person:
                ksntl.current_position = current_position
                ksntl.next_to_location = next_to_location
                self.ksntl_pub(ksntl)

                current_position = rospy.wait_for_message("/cp", cp)

                next_to_location += 1
                #画像認識で人間が要るかを検知
                if True:#人間がいる
                    discover_person = False#人がいる場合Falseにしてループを抜ける

            mng.tekitou = 1
            self.mng_pub(mng)

            go_near_guest_time = rospy.wait_for_message("/gngt", gngt)

            #画像で特徴量を取得する

            rp.go_near_guest_time = go_near_guest_time
            self.rp_pub(rp)

            rsp.current_position =  current_position
            self.rsp_pub(rsp)

if __name__=="__main__":
    cic = CIC()
    cic.main()