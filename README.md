# find_my_mates


# speech_and_NLP

## 使い方

+ isMeaning
```python
rospy.wait_for_service("/isMeaning")
res = self.isMeaning("検出したい文章",["検出","したい","単語","をかく"])
res.res に booleanが返される
```
+ textToSpeech
```python
self.audio_pub.publish("発話させたい音声")
```
+ recognize_speech
```python
rospy.wait_for_service("/speechToText")
res = self.speechToText(中間テキスト表示非表示を設定(bool), 最低文字数, 名前のみ抽出するか(bool), 空白取り除くか(bool), voskLogLevel(-1でいいです))
res.resにテキストが入る
```
