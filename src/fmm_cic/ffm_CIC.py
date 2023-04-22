#!/usr/bin/env python
# -*- coding: utf-8 -*-


#control
from control import control_system

#image


#sound
from speech_and_NLP.src.speechToText import recognize_speech #音声認識
from speech_and_NLP.src.tools.speech_to_text.isMeaning import is_meaning #文章の中に単語を検索する
from speech_and_NLP.src.textToSpeech import textToSpeech #発話
from speech_and_NLP.src.tools.speech_to_text.extractPersonName import extractPersonName #人名取得

class CIC():
    def __init__(self):
        self
        
    def main(self):
        control_system.move_to_next_room()
        control_system.move_near_guest()

if __name__=="__main__":
    cic = CIC()
    cic.main()