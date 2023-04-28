#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from carry_my_luggage.srv import SpeechToText, isMeaning

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# 音声認識の関数 (vosk)
from speech_and_NLP.src.speechToText import recognize_speech 
from speech_and_NLP.src.tools.speech_to_text.isMeaning import is_meaning
from speech_and_NLP.src.textToSpeech import textToSpeech

class AudioSystem():
    def __init__(self):
        self.sub = rospy.Subscriber("/audio", String, self.callback)
        self.speechToTextSrv = rospy.Service("/speechToText", SpeechToText, self.calbkSTT)
        self.isMeaningSrv = rospy.Service("/isMeaning", isMeaning, self.calbkIsMeaning)

    def calbkIsMeaning(self, msg):
        return is_meaning(msg.text, msg.word_list)

    def calbkSTT(self, msg):
        return recognize_speech(msg.print_partial, msg.use_break, msg.return_extract_person_name, msg.remove_space, msg.voskLogLevel)
    
    def callback(self, msg):
        textToSpeech(msg.data, verbose=True)

if __name__ == '__main__':
    rospy.init_node("audio")
    audio = AudioSystem()
    
    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()