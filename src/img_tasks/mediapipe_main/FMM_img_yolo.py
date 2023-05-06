#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

#FMMの特徴量抽出mainルーチン
#1番目に起動させておき、img_mdppからの送信を待つ

import os
import cv2
import time
from statistics import mean, mode

from img_tasks.mediapipe_main.img_glasses_detect import get_glasses_tf_set, get_glasses_tf

from img_tasks.mediapipe_main.UDP_module import UDP_send, UDP_recv

import rospy



def img_yolo_main(sock, sock2):
    #sock = UDP_send("始まり")
    #sock = UDP_recv("始まり")
    #sock2 = UDP_send("始まり", HOST_NAME='127.0.0.4')

    #count = 0 #繰り返し回数を数える
    age_push, sex_push, up_color_push, down_color_push, glasstf_push = img_analysis_sub(sock=sock, sock2=sock2)

    #UDP_recv("終了", sock=sock)
    #UDP_send("終了", sock=sock2)

    return age_push, sex_push, up_color_push, down_color_push, glasstf_push

    """
    #ディレクトリのパスを指定
    DIR = '/home/ri-one/catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/memory'
    DIR = '/home/ri-one/fksg_catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/memory'
    
    #print(file_num)

    MAX_FILE_NUM = 20 #personとface合わせて20枚

    while (True):

        #ファイル数を出力
        file_num = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
        

        #写真が揃ってからまだ一回も実行していないときに、特徴を抽出する
        if file_num == MAX_FILE_NUM and count == 0:
            time.sleep(1.5)
            #age_push, sex_push, up_color_push, down_color_push, glasstf_push img_analysis_sub(sock=sock, sock2=sock2)
            count = 1

        #写真が揃っていないときに、カウントを0に戻す
        elif file_num < MAX_FILE_NUM:
            count = 0

    #UDP_send("終了", sock=sock)
    UDP_recv("終了", sock=sock)
    UDP_send("終了", sock=sock2)
    """


def img_analysis_sub(sock, sock2):


    model = get_glasses_tf_set()
    img_c = 1 

    age_push = "不明"
    sex_push = "不明"
    up_color_push = "不明"
    down_color_push = "不明"
    glasstf_push = "不明"

    age_list = []
    sex_list = []
    up_color_list = []
    down_color_list = []
    glasstf_list = []

    DIR = '/home/ri-one/catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/memory'
    # DIR = '/home/ri-one/fksg_catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/memory' #個人用PC

    while(True):
        # 画像を読み込む #####################################################
        read_path = DIR + "/face" + str(img_c) + ".png"#眼鏡は顔画像から読み取る


        #ファイルが存在するとき読み込み
        if os.path.exists(read_path):
            print("img_yolo:if os.path.exists(read_path) OK")
        
            image = cv2.imread(read_path)

            if image is not None:
                print("img_yolo:img_OK")

                print(str(img_c) + ":")

                sock2 = UDP_send("繰り返し", sock=sock2, send_data="OK", HOST_NAME='127.0.0.4') 
                rcv_data, sock = UDP_recv("繰り返し", sock=sock) #他の特徴がimg_mdppから届くのを待つ

                rcv_ftr_list = rcv_data.split(",")

                if rcv_ftr_list[0] != "なし":
                    age = int(rcv_ftr_list[0]) #年齢を取得
                else:
                    age = "なし"
                
                sex = rcv_ftr_list[1] #性別を取得
                up_color = rcv_ftr_list[2] #上の服の色を取得
                down_color = rcv_ftr_list[3] #下の服の色を取得
                glstf = get_glasses_tf(model, image) #眼鏡の有無を取得


                if age != "なし":
                    age_list.append(age) #年齢を追加

                if sex != "なし":
                    sex_list.append(sex) #性別を追加

                if up_color != "なし":  
                    up_color_list.append(up_color) #上の服の色を追加

                if down_color != "なし":
                    down_color_list.append(down_color) #下の服の色を追加

                if glstf != "なし":
                    glasstf_list.append(glstf) #眼鏡の有無を追加

                print("glstf=" + glstf)
                print("rcv_ftr_list=" + str(rcv_ftr_list))

                print("\n")

                img_c += 1

                #sock = UDP_send("繰り返し", sock=sock, send_data=glstf)

        #存在しなければ終了
        else:
            break

    
    print("age_list=" + str(age_list))
    print("sex_list=" + str(sex_list))
    print("up_color_list=" + str(up_color_list))
    print("down_color_list=" + str(down_color_list))
    print("glasstf_list=" + str(glasstf_list))

    if len(age_list) != 0:
        age_push = str(int(mean(age_list))) + "歳"

    if len(sex_list) != 0:
        sex_push = mode(sex_list)

    if len(up_color_list) != 0:
        up_color_push = mode(up_color_list)

    if len(down_color_list) != 0:
        down_color_push = mode(down_color_list)

    if len(glasstf_list) != 0:
        glasstf_push = mode(glasstf_list)


    print("age_push=" + age_push)
    print("sex_push=" + str(sex_push))
    print("up_color_push=" + str(up_color_push))
    print("down_color_push=" + str(down_color_push))
    print("glasstf_push=" + str(glasstf_push))

    return age_push, sex_push, up_color_push, down_color_push, glasstf_push



if __name__ == "__main__":
    rospy.init_node("img_yolo")
    #img_analysis_sub()
    img_yolo_main()
    
    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()