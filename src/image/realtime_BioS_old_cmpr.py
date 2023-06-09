#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


#ジコログ, 【Python】OpenCVを超えたInsightFaceによる顔認識,
#https://self-development.info/%E3%80%90python%E3%80%91opencv%E3%82%92%E8%B6%85%E3%81%88%E3%81%9Finsightface%E3%81%AB%E3%82%88%E3%82%8B%E9%A1%94%E8%AA%8D%E8%AD%98/
#2023年2月28日.

import numpy as np
import cv2
from insightface.app import FaceAnalysis
import torch
import detect_color_realtime as detect_color_realtime
from scipy import stats
import rospy
from std_msgs.msg import String, Bool
from find_my_mates.msg import Info
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class RtBioSOldComp():


    def __init__(self):
        """
        (追加)------------------------------------------------
        音声への出版者を作成する   名前、年齢、性別、服の色を報告するため  名前:文字列、年齢:(0~10)程度の整数、 性別:(0, 1)の整数、 服の色:(文字列)色の名前
        音声からの購読者を作成する 報告済かどうかを確かめるため  報告済であるかどうか True:報告済、False未報告 
        -------------------------------------------------------
        中心部からの購読者を作成する (ターゲットの名前を取得するため)
        現在、画面中央に写っている人の名前を音声認識で取得し、探すべき名前と同じならばその顔から特徴を抽出する
        音声からの購読者を作成する (ターゲット未発見時の状態で 現在中央に写っている顔がターゲットかを知るため)
        音声への出版者を作成する (ターゲットが未発見の状態 誰かの顔が見つかったときに静止し、名前を聞くため)
        制御への出版者を作成する (ターゲットが未発見、発見、または報告状態において、その人に接近し距離を調節するため)
        """
        rospy.init_node("raltimebio")
        self.per_pub = rospy.Publisher("/person", Bool, queue_size=1)
        self.bool = bool
        self.feature_pub = rospy.Publisher("/information", Info, queue_size=1)
    
    def make_ftr_sentence(gst_vlu, s_vlu, name, year_field, cloth_clr):

            S = ""

            #1のときに男性
            if s_vlu:
                S = "man"
            #0のときに女性
            else:
                S = "woman"


            if year_field == 0:
                year_fld_str = "under teens"

            elif year_field >= 10:
                year_fld_str = str(year_field) + "years old"

            sentence = str(gst_vlu) + "番目のゲストである" + name + "は、" + year_fld_str + "の" + S + "性で" +"服の色は" + cloth_clr + "色です"

            i = Info()
            i.age = year_fld_str
            i.gender = S
            i.up_color = cloth_clr
            self.feature_pub.publish(i)

            return sentence

    def main(self, front_person):
        rtbioscmp = RtBioSOldComp()
        time.sleep(10)

        #ゲストの特徴を報告する文章を作る関数
        #引数 ゲストの番号(int)、ゲストの性別番号(int)、ゲストの名前(str)、ゲストの年齢(int)、ゲストの服の色(str)
        def make_ftr_sentence(gst_vlu, s_vlu, name, year_field, cloth_clr):

            S = ""

            #1のときに男性
            if s_vlu:
                S = "man"
            #0のときに女性
            else:
                S = "woman"


            if year_field == 0:
                year_fld_str = "under teens"

            elif year_field >= 10:
                year_fld_str = str(year_field) + "years old"

            sentence = str(gst_vlu) + "番目のゲストである" + name + "は、" + year_fld_str + "の" + S + "性で" +"服の色は" + cloth_clr + "色です"

            # i = Info()
            # i.age = year_fld_str
            # i.gender = S
            # i.up_color = cloth_clr
            # self.feature_pub.publish(i)

            return sentence

        

        """
        # 音声を喋るにはここに文字列を渡す
        self.audio_pub.publish("あなたの名前は何ですか。")#名前を聞く。

        # 音声を聞き取るには下の二行で取得する。
        # self.speechToText(中間テキスト表示非表示を設定(bool), 最低文字数, 名前のみ抽出するか(bool), 空白取り除くか(bool), voskLogLevel(-1でいいです))

        rospy.wait_for_service("/speechToText")
        voice_res = self.speechToText(True, 3, True, True, -1)
        name = voice_res.res
        print(name) 

        # rospy.wait_for_service("/isMeaning")
        # res = self.isMeaning("検出したい文章",["検出","したい","単語","をかく"])
        # res.res に booleanが返される

        res = self.isMeaning("ためす文字列", ["a","a"])
        response = res.res
        """

        #上記の関数化
        question = "あなたの名前は何ですか。"
        #speech_test(question)

        #0:未発見、1発見抽出済、2報告完了
        state = 0

        get_name = "ゲスト1" #音声から取得した名前を保持する

        #マスターとゲストの特徴を保持する
        names = ["マスター", "チャーリー", "パーカー", "トーマス"]

        MSTftrs = [20, 1, "黒"] #マスターの特徴を保持 (マスターのみ抽出を3とする)

        ftr_list = [{"名前":names[0],"年齢":MSTftrs[0], "性別":MSTftrs[1], "服の色":MSTftrs[2], "抽出":3},
                    {"名前":names[1],"年齢":0, "性別":0, "服の色":"", "抽出":0},
                    {"名前":names[2],"年齢":0, "性別":0, "服の色":"", "抽出":0},
                    {"名前":names[3],"年齢":0, "性別":0, "服の色":"", "抽出":0}]

        

        print(ftr_list)

        app = FaceAnalysis() #実体化 app = FaceAnalysis(name="antelopev2")でモデルを変更できる
        app.prepare(ctx_id=0, det_size=(640, 640))

        #カメラの設定　デバイスIDは0
        cap = cv2.VideoCapture(0)

        cam_count = 0 #1回だけカメラの画像から高さと幅を取得するための変数
        frame_w = 0 #カメラの画像の幅を保持する 
        frame_h = 0 #カメラの画像の高さを保持する

        gender = ["女", "男"]

        robo_face_dis = 0  #(ロボットから見た)人の顔とロボットとの距離  0:遠い 1:中距離 2:近い
        robo_face_drct = 0 #(ロボットから見た)人の顔が存在する方向      0:左   1:中央   2:右
        thrd_min = 640/32 #距離の遠近の閾値の最小値 (これを下回ると距離は遠いと判断される)
        thrd_max = 640/8 #距離の遠近の閾値の最大値 (これを上回ると距離は近いと判断される)
        #閾値をこのカメラで取得した幅の値で設定したが、他のカメラでも同様のことができるようにするため数値で指定した。

        #len(color_list) = 12色 (9彩色、3無彩色)
        color_list = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"] #色の名前のリスト
        color_dic = {} #色名と割合を辞書で対応つける 色の画素の数を保持する

        #目標ゲストを保持する変数
        target = 1  #1:ゲスト1、2:ゲスト2、3:ゲスト3 

        #10回の中で最も多く出た値を特徴として使用するためのリスト
        Ymemo = []
        Smemo = []
        Cmemo = []

        clt_left = 0
        clt_top = 0
        clt_right = 0
        clt_bottom = 0
        
        #front_person = True #顔の前に来たときはTrue

        for i in range(len(color_list)):  
            color_dic[color_list[i]] = 0



        #繰り返しのためのwhile文
        while True:
            #カメラからの画像取得
            ret, frame = cap.read()


            if cam_count == 0:
                frame_h, frame_w, _ = frame.shape
                print("カメラの画像の形状: 幅:" + str(frame_w) + "、高さ:" + str(frame_h))
                #カメラの画像の形状: 幅:640、高さ:480
                cam_count = 1

            faces = app.get(np.asarray(frame))
            print("faces:" + str(len(faces)))

             #人の顔から遠ざかったら終了する
            if front_person == False:
                print("キャプチャの終了")
                break

          
            #カメラの起動中は顔を検出し、特徴抽出する
            if len(faces) == 0:
                print("この位置の方向に人はいない")
                self.bool = True
                self.per_pub.publish(self.bool)
                # break#仮

            else: #顔が写っていたとき
                self.bool = False
                self.per_pub.publish(self.bool)
                        
                #0番目のみ対象が画面に映る顔の添字 

                top = faces[0]['bbox'][1]
                bottom = faces[0]['bbox'][3]
                left = faces[0]['bbox'][0]
                right = faces[0]['bbox'][2]

                w = int(right - bottom)
                h = int(bottom - top)
                c_x = int((right + left)/2)
                c_y = int((bottom + top)/2)
        
            
                #距離を仕分ける 
                if w < thrd_min:
                    #print(str(i) + "番目の人が遠い")
                    robo_face_dis = 0 #ロボットは人が中央に来るまで前に進む

                elif w >= thrd_min and w <= thrd_max:
                    #print(str(i) + "番目の人が中央の距離")
                    robo_face_dis = 1 #ロボットはそのまま

                elif w > thrd_max:
                    #print(str(i) + "番目の人が近い")
                    robo_face_dis = 2 #ロボットは人が中央に来るまで後ろに下がる


                #方向を仕分ける
                if c_x < frame_w / 3:
                    #print(str(i) + "番目の人が左にいる")
                    robo_face_drct = 0 #ロボットは人が中央に来るまで左回りする

                elif c_x > frame_w/3 and c_x < frame_w * 2/3:
                    #print(str(i) + "番目の人が中央の方向")
                    robo_face_drct = 1 #ロボットはそのまま

                elif c_x > frame_w * 2/3:
                    #print(str(i) + "番目の人が右にいる")
                    robo_face_drct = 2 #ロボットは人が中央に来るまで右回りする
                    

                print("顔の距離:" + str(robo_face_dis) + "、方向:" + str(robo_face_drct))
                #print("\n")

                #中央で中距離のときのみ特徴抽出する
                if robo_face_dis == 1 and robo_face_drct == 1:

                    #10回のさいひんち
                    for k in range(10):
                        clt_top = int(bottom+h/2)
                        clt_bottom = int(bottom+h*(5/2))
                        clt_left = int(left-w/2)
                        clt_right = int(right+w/2)

                        #服のtopを画像内に収める
                        if clt_top < 0:
                            clt_top = 0
                        elif clt_top >= frame_h:
                            clt_top = frame_h-1

                        #服のbottomを画像内に収める
                        if clt_bottom < 0:
                            clt_bottom = 0
                        elif clt_bottom >= frame_h:
                            clt_bottom = frame_h-1

                        #服のleftを画像内に収める
                        if clt_left < 0:
                            clt_left = 0
                        elif clt_left >= frame_w:
                            clt_left = frame_w-1

                        #服のrightを画像内に収める
                        if clt_right < 0:
                            clt_right = 0
                        elif clt_right >= frame_w:
                            clt_right = frame_w-1


                        if clt_bottom > clt_top and clt_right > clt_left: 
                            color_dic = detect_color_realtime.get_colors(frame[clt_top:clt_bottom, clt_left:clt_right], color_dic, color_list)

                            #print(color_dic)
                            #辞書の値が最大・最小となるキーを取得
                            #最大値が0でないとき

                            #年代を保持する 年齢を10で割ったときの商かける10 
                            year_field = (faces[0]['age'] // 10) * 10

                            if (max(color_dic.values())):
                                max_k = max(color_dic, key=color_dic.get)
                                print(color_dic)

                                Ymemo.append(year_field)
                                Smemo.append(faces[0]['gender'])
                                Cmemo.append(max_k)


                    #配列が空のときに最頻値を求めるとエラーが出る
                    if len(Ymemo) != 0 and len(Smemo) != 0 and len(Cmemo) != 0:
                        mode_Ymemo = int(stats.mode(Ymemo).mode)
                        mode_Smemo = int(stats.mode(Smemo).mode)
                        mode_Cmemo = str(stats.mode(Cmemo).mode).strip("['").strip("']")

                            #print(mode_Ymemo)s
                            #print(mode_Smemo)
                            #print(mode_Cmemo)

                        #{"名前":names[0],"年齢":2, "性別":1, "服の色":"黒", "抽出":1}
                        ftr_list[target]["名前"] == get_name

                        #それぞれの特徴に10回の標本の最頻値を渡す
                        ftr_list[target]["年齢"] = mode_Ymemo #年代を抽出 0:10代未満 以降 ~代
                        ftr_list[target]["性別"] = mode_Smemo #性別を取得する 0:女、1:男
                        ftr_list[target]["服の色"] = mode_Cmemo #服の色を取得する
                        ftr_list[target]["抽出"] = 2 #目標ゲストを抽出した印として2を代入する


                                    
                        if Ymemo == 0:
                            print("年齢:10代未満")
                        else:
                            print("年齢:" + str(ftr_list[target]["年齢"]) + "代")



                        print("幅:" + str(w) + "、高さ:" + str(h))
                        print("中心: x=" + str(c_x) + ", y=" + str(c_y)) 
                        print("性別:" + str(gender[ftr_list[target]["性別"]]))
                        print(ftr_list[target]["服の色"] + "色の服を着ている")


                        gst_vlu = target
                        s_vlu = ftr_list[target]["性別"]
                        name = ftr_list[target]["名前"]
                        yearold = ftr_list[target]["年齢"]
                        cloth_clr = ftr_list[target]["服の色"]

                        rpt_sentence = make_ftr_sentence(gst_vlu, s_vlu, name, yearold, cloth_clr)
                        print(rpt_sentence)
                        



                cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0))

                if top < bottom and left < right:
                    cv2.rectangle(frame, (clt_left, clt_top), (clt_right, clt_bottom), (0, 255, 0))             

                """
                音声へ、距離、方向を出版する (音声側で購読したとき:ターゲット未発見状態かつ中央と中距離のときに名前を聞く または 報告状態かつ中央と中距離のときに名前や特徴を報告する)
                制御へ、距離、方向を出版する (制御側で購読したとき:人に近づく必要性のある未発見、報告状態で位置を調整するために使う)
                """

                cv2.imshow("capture", frame)


                clt_left = 0
                clt_top = 0
                clt_right = 0
                clt_bottom = 0

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

#デバッグ用の関数
def func_test():

    def make_ftr_sentence(gst_vlu, s_vlu, name, year_field, cloth_clr):

        S = ""

        #1のときに男性
        if s_vlu:
            S = "男"
        #0のときに女性
        else:
            S = "女"


        if year_field == 0:
            year_fld_str = "10代未満"

        elif year_field >= 10:
            year_fld_str = str(year_field) + "代"

        sentence = str(gst_vlu) + "番目のゲストである" + name + "は、" + year_fld_str + "の" + S + "性で" +"服の色は" + cloth_clr + "色です"

        return sentence


    #マスターとゲストの特徴を保持する
    names = ["マスター", "ゲスト1", "ゲスト2", "ゲスト3"]

    MSTftrs = [0, 1, "黒"] #マスターの特徴を保持 (マスターのみ抽出を3とする)

    ftr_list = [{"名前":names[0],"年齢":MSTftrs[0], "性別":MSTftrs[1], "服の色":MSTftrs[2], "抽出":3},
                {"名前":names[1],"年齢":0, "性別":0, "服の色":"", "抽出":0},
                {"名前":names[2],"年齢":0, "性別":0, "服の色":"", "抽出":0},
                {"名前":names[3],"年齢":0, "性別":0, "服の色":"", "抽出":0}]
    
    target = 0


    gst_vlu = target
    s_vlu = ftr_list[target]["性別"]
    name = ftr_list[target]["名前"]
    yearold = ftr_list[target]["年齢"]
    cloth_clr = ftr_list[target]["服の色"]

    name_like = make_ftr_sentence(gst_vlu, s_vlu, name, yearold, cloth_clr)
    print(name_like)

if __name__ == '__main__':


    rtbioscmp = RtBioSOldComp()
    #k = rospy.wait_for_message("/real", Bool)
    rtbioscmp.main(True)
    


     #ゲストの特徴を報告する文章を作る関数
    #引数 ゲストの番号(int)、ゲストの性別番号(int)、ゲストの名前(str)、ゲストの年齢(int)、ゲストの服の色(str)
    #func_test()
