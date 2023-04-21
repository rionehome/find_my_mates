#!/usr/bin/env python
# -*- coding: utf-8 -*-

from speech_and_NLP.src.tools.speech_to_text.speechToText import recognize_speech #音声認識
from speech_and_NLP.src.tools.speech_to_text.isMeaning import is_meaning #文章の中に単語を検索する
from speech_and_NLP.src.tools.text_to_speech.textToSpeech import textToSpeech #発話
from speech_and_NLP.src.tools.speech_to_text.extractPersonName import extractPersonName #人名取得
class CIC():
    def __init__(self):
        

    def main(self):
        

if __name__=="__main__":
    cic = CIC()
    cic.main()