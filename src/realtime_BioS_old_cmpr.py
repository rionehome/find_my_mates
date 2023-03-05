#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#ジコログ, 【Python】OpenCVを超えたInsightFaceによる顔認識,
#https://self-development.info/%E3%80%90python%E3%80%91opencv%E3%82%92%E8%B6%85%E3%81%88%E3%81%9Finsightface%E3%81%AB%E3%82%88%E3%82%8B%E9%A1%94%E8%AA%8D%E8%AD%98/
#2023年2月28日.

import numpy as np
import cv2
#from insightface.app import FaceAnalysis
import torch
import detect_color_realtime
from scipy import stats
import rospy
#from std_msgs.msg import String
from std_msgs.msg import String
from find_my_mates.msg import MoveAction, Feature, RealTime
from carry_my_luggage.srv import SpeechToText, isMeaning


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

        #self.realtime_sub = rospy.wait_for_message('/realtime', RealTime)
        self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)
        self.main_pub = rospy.Publisher("/realtime", RealTime, queue_size=1)

        # for audio
        self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)

        # for speechToText

        self.speechToText = rospy.ServiceProxy("/speechToText", SpeechToText )

        self.isMeaning = rospy.ServiceProxy("/isMeaning", isMeaning )

        print("初期化")




    def main(self):
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
        #0:未発見、1発見抽出済、2報告完了
        state = 0

        get_name = "ゲスト1" #音声から取得した名前を保持する

        #マスターとゲストの特徴を保持する
        names = ["マスター", "ゲスト1", "ゲスト2", "ゲスト3"]

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



            #なんか人が写ってるとき
            if len(faces) != 0:

                #iが画面に映る顔の添字 
                for i in range(len(faces)):

                    #0番目の添字のみ対象とする
                    if i == 0:

                        top = faces[i]['bbox'][1]
                        bottom = faces[i]['bbox'][3]
                        left = faces[i]['bbox'][0]
                        right = faces[i]['bbox'][2]

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
                            
        
                        print(str(i+1) + "番目の顔の距離:" + str(robo_face_dis) + "、方向:" + str(robo_face_drct))
                        #print("\n")





                    #回転し続けている間に視界に入った場合
                    if robo_face_dis == 0 and robo_face_drct == 1:
                        #m = MoveAction()
                        #m.angular_speed = 0
                        #m.linear_speed = 0

                        acsess_count = 0 #接近したか判定するために使用する

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
                            year_field = (faces[i]['age'] // 10) * 10

                            if (max(color_dic.values())):
                                max_k = max(color_dic, key=color_dic.get)
                                print(color_dic)

                                Ymemo.append(year_field)
                                Smemo.append(faces[i]['gender'])
                                Cmemo.append(max_k)


                        #配列が空のときに最頻値を求めるとエラーが出る
                        if len(Ymemo) != 0 and len(Smemo) != 0 and len(Cmemo) != 0:
                            mode_Ymemo = int(stats.mode(Ymemo).mode)
                            mode_Smemo = int(stats.mode(Smemo).mode)
                            mode_Cmemo = str(stats.mode(Cmemo).mode).strip("['").strip("']")

                            #print(mode_Ymemo)
                            #print(mode_Smemo)
                            #print(mode_Cmemo)


                            #ここで見た特徴が、今までに見たことがないものか確かめる
                            for j in range(1, len(ftr_list)):

                                #それぞれの特徴を10回の標本の最頻値で比較する　
                                if ftr_list[j]["年齢"] == mode_Ymemo and ftr_list[j]["性別"] == mode_Smemo and ftr_list[j]["服の色"] == mode_Cmemo:
                                    acsess_count += 1 #接近したことがある印
                                    break

                            #未発見状態のとき、目標のゲストを見つけるために
                            if state == 0:
                                #接近するための条件は 未発見 or 目的でないゲストを発見したときの特徴があった
                                if (acsess_count == 0) or ((acsess_count == 1) and (ftr_list[j]["抽出"] == 1)):
                                    #m = MoveAction()
                                    #m.linear_speed = 1.0
                                    #m.angular_speed = 0.5
                                    #m.direction = "normal"                                  
                                    """
                                    制御では、現在写っている顔に接近する操作を行う (現在の位置を出版するためそのまま)
                                    
                                    """
                                    #self.main_pub.publish(m)
                                else:
                                    """
                                    制御では、別の顔を探す操作を行う (距離と方向の両方を3にする)
                                    
                                    """
                                    robo_face_dis = 3 
                                    robo_face_drct = 3
                                    self.main_pub.publish(m)


                            #発見特徴抽出完了状態のとき、マスタに報告するために見つける
                            elif state == 1:
                                #マスタの特徴を全て満たすときに現在画面中央に写っている人物はマスタだと考える
                                if (MSTftrs[0] == mode_Ymemo) and (MSTftrs[1] == mode_Smemo) and (MSTftrs[2] == mode_Cmemo):
                                    """
                                    制御では、現在写っている顔に接近する操作を行う (現在の位置を出版するためそのまま)
                                    
                                    """

                                else:
                                    """
                                    制御では、別の顔を探す操作を行う (距離と方向の両方を3にする)
                                    
                                    """
                                    robo_face_dis = 3 
                                    robo_face_drct = 3
                                    self.main_pub.publish(m)



                        #リストを空にする
                        Ymemo = []
                        Smemo = []
                        Cmemo = []





                    #名前を知らないというような理由で近づいた場合
                    #距離と角度がちょうど良いときに、特徴抽出を行う。
                    #ifで分岐することで、近づいたとき(精度の良い特徴で識別できる)
                    elif (robo_face_dis == 1 or robo_face_dis == 2) and robo_face_drct == 1:

                        print(color_dic)

                        mode_Ymemo = 0
                        mode_Smemo = 0
                        mode_Cmemo = ""

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
                            year_field = (faces[i]['age'] // 10) * 10

                            #色の面積の最大値が0でないとき
                            if (max(color_dic.values())):
                                max_k = max(color_dic, key=color_dic.get)

                                Ymemo.append(year_field)
                                Smemo.append(faces[i]['gender'])
                                Cmemo.append(max_k)

                        #配列が空のときに最頻値を求めるとエラーが出る
                        if len(Ymemo) != 0 and len(Smemo) != 0 and len(Cmemo) != 0:
                            mode_Ymemo = int(stats.mode(Ymemo).mode)
                            mode_Smemo = int(stats.mode(Smemo).mode)
                            mode_Cmemo = str(stats.mode(Cmemo).mode).strip("['").strip("']")

        
                            #特徴のリストへの追加は未発見状態のときのみ
                            if state == 0:

                                """
                                
                                """

                                #現在中央に映るゲストがターゲットのゲストであるときに、目標ゲストのための特徴抽出する
                                if ftr_list[target]["名前"] == get_name:
                                    #{"名前":names[0],"年齢":2, "性別":1, "服の色":"黒", "抽出":1}

                                    #それぞれの特徴に10回の標本の最頻値を渡す
                                    ftr_list[target]["年齢"] = mode_Ymemo #年代を抽出 0:10代未満 以降 ~代
                                    ftr_list[target]["性別"] = mode_Smemo #性別を取得する 0:女、1:男
                                    ftr_list[target]["服の色"] = mode_Cmemo #服の色を取得する
                                    ftr_list[target]["抽出"] = 2 #目標ゲストを抽出した印として2を代入する

                                    #print(int(stats.mode(Ymemo).mode))
                                    #print((np.array(Ymemo)))
                                    #print(ftr_list[target]["年齢"])


                                    if year_field == 0:
                                        print("年齢:10代未満")
                                    else:
                                        print("年齢:" + str(ftr_list[target]["年齢"]) + "代")



                                    print("幅:" + str(w) + "、高さ:" + str(h))
                                    print("中心: x=" + str(c_x) + ", y=" + str(c_y)) 
                                    print("性別:" + str(gender[ftr_list[target]["性別"]]))
                                    print(ftr_list[target]["服の色"] + "色の服を着ている")


                                    #現在のゲストの特徴を抽出したあとに
                                    state = 1  #発見特徴抽出完了になる



                                #ターゲットではない場合でも、識別のため特徴を抽出する
                                else:
                                    #特徴のリストから現在中央に写っているゲストの名前を見つけ比較用に特徴を追加する
                                    #jはゲストの添字
                                    for j in range(1, len(ftr_list)):
                                        #それぞれの特徴に10回の標本の最頻値を渡す
                                        #見たことがなく、音声から取得した名前と等しいゲストに特徴を追加
                                        if ftr_list[j]["名前"] == get_name and ftr_list[j]["抽出"] == 0: 
                                            ftr_list[j]["年齢"] = mode_Ymemo #年代を抽出 0:10代未満 以降 ~代
                                            ftr_list[j]["性別"] = mode_Smemo #性別を取得する 0:女、1:男
                                            ftr_list[j]["服の色"] = mode_Cmemo #服の色を取得する
                                            ftr_list[j]["抽出"] = 1 #目標ではない人の特徴を抽出した印として1を代入する



                            #発見特徴抽出完了状態のときオペレータのもとへ戻る必要性がある
                            #オペレータを特徴で認識する
                            elif state == 1:
                                print(mode_Ymemo)
                                print(mode_Smemo)
                                print(mode_Cmemo)

                                #マスタの特徴を全て満たすときに現在画面中央に写っている人物はマスタだと考える
                                if (MSTftrs[0] == mode_Ymemo) and (MSTftrs[1] == mode_Smemo) and (MSTftrs[2] == mode_Cmemo):


                                    """
                                    
                                    ここで報告する流れを作る
                                    
                                    音声へ出版する 名前:文字列、年齢:(0~10)程度の整数、 性別:(0, 1)の整数、 服の色:(文字列)色の名前
                                    音声から購読する 報告済であるかどうか True:報告済、False未報告
                                    """
                                    
                                
                                    S = ""

                                    #1のときに男性
                                    if ftr_list[target]["性別"]:
                                        S = "男"

                                    #0のときに女性
                                    else:
                                        S = "女"

                                    # Str = String()

                                    sentence = str(target) + "番目のゲストである" + ftr_list[target]["名前"] + "は、" + str(ftr_list[target]["年齢"]) + "代の" + S + "性で" +"服の色は" + ftr_list[target]["服の色"] + "色です"
                                    print(sentence)
                                    ftr_list[target][""]                       
                                    #Str.data = sentence
                                    self.audio_pub.publish(sentence)
                                    

                                    state = 2

                                    #報告完了状態のときに以下を実行する
                                    if state == 2:
            
                                        target += 1 #ターゲットを更新する
                                        state = 0 #未発見状態へ遷移する

                                #マスタの特徴を全て満たさないときはマスタでないと考え回転
                                else:
                                    robo_face_dis = 3
                                    robo_face_dis = 3


                        #リストを空にする
                        Ymemo = []
                        Smemo = []
                        Cmemo = []

                cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0))

                if top < bottom and left < right:
                    cv2.rectangle(frame, (clt_left, clt_top), (clt_right, clt_bottom), (0, 255, 0))             

                """
                音声へ、距離、方向を出版する (音声側で購読したとき:ターゲット未発見状態かつ中央と中距離のときに名前を聞く または 報告状態かつ中央と中距離のときに名前や特徴を報告する)
                制御へ、距離、方向を出版する (制御側で購読したとき:人に近づく必要性のある未発見、報告状態で位置を調整するために使う)
                """


                clt_left = 0
                clt_top = 0
                clt_right = 0
                clt_bottom = 0

            #人すら見つかっていないとき
            else:

                #2つの値が3のとき
                robo_face_dis = 3 
                robo_face_drct = 3



                print("\n\n")


            #距離と方向をPublishしてほしい。
            p = RealTime()
            print(type(p))
            p.robo_p_dis = robo_face_dis
            print(type(p.robo_p_dis))
            p.robo_p_drct = robo_face_drct #改良してから変更する
            self.main_pub.publish(p)
            print(robo_face_drct, robo_face_dis)


            #self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)
            #self.audio_sub = rospy.Subscriber("/audio", String, queue_size=1)
            #self.move_pub = rospy.Publisher("/move", MoveAction, queue_size=1)


            print("ターゲット=" + str(target))
            print("状態=" + str(state))
            print("\n")
            print("マスターの特徴")
            print(ftr_list[0])
            print("ゲストの特徴リスト")
            for l in range(1, target+1):
                print(ftr_list[l])
                

            cv2.imshow('camera' , frame)

            #繰り返し文から抜けるためのif文
            key =cv2.waitKey(10)
            if key == 27:
                break


        #メモリを解放して終了するためのコマンド
        cap.release()
        cv2.destroyAllWindows()

    def speech_test(self):
        # 音声を喋るにはここに文字列を渡す
        self.audio_pub.publish("あなたの名前は何ですか。")#名前を聞く。

        # 音声を聞き取るには下の二行で取得する。
        # self.speechToText(中間テキスト表示非表示を設定(bool), 最低文字数, 名前のみ抽出するか(bool), 空白取り除くか(bool), voskLogLevel(-1でいいです))

        rospy.wait_for_service("/speechToText")
        voice_res = self.speechToText(True, 3, True, True, -1)
        name = voice_res.res
        print(name) 

if __name__ == '__main__':
    rtbioscmp = RtBioSOldComp()
    #tbioscmp.main()
    
    rtbioscmp.speech_test()
