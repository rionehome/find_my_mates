#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

#FMMの特徴量抽出mainルーチン

import os
import cv2
import time

from statistics import mean, mode

from img_BioS_old_cmpr import get_sex_age_set, get_sex_age
from img_clothes_color import get_clothes_color_set, get_clothes_color

from UDP_module import UDP_recv

import rospy
from find_my_mates.msg import ImgData


#UDP通信の受信側の繰り返し
#データを待ち受け

def main():
    sock = UDP_recv("始まり")

    count = 0 #繰り返し回数を数える

    #ディレクトリのパスを指定
    DIR = '/home/ri-one/catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/memory'
    
    #print(file_num)

    MAX_FILE_NUM = 20

    while (True):

        #ファイル数を出力
        file_num = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
        
        #写真が揃ってからまだ一回も実行していないときに、特徴を抽出する
        if file_num == MAX_FILE_NUM and count == 0:
            time.sleep(1)
            img_analysis_main(sock=sock)
            count = 1

        #写真が揃っていないときに、カウントを0に戻す
        elif file_num < MAX_FILE_NUM:
            count = 0

    UDP_recv("終了", sock=sock)


def img_analysis_main(sock):

    data_pub = rospy.Publisher("/imgdata", ImgData, queue_size=1)
    imgdata = ImgData()

    app = get_sex_age_set()
    pose, enable_segmentation, segmentation_score_th, use_brect, plot_world_landmark, ax, display_fps = get_clothes_color_set()

    img_c = 1

    age_list = []
    sex_list = []
    up_color_list = []
    down_color_list = []
    glasstf_list = []

    while(True):        

        # 画像を読み込む #####################################################
        read_path = "memory/person" + str(img_c) + ".png"#多くの特徴は人画像から読み取る


        #ファイルが存在するとき読み込み
        if os.path.exists(read_path):
        
            image = cv2.imread(read_path)


            print(str(img_c) + ":")

            age, sex = get_sex_age(app, image)
            print(":age=" + str(age) + "、sex=" + str(sex))

            if age != "なし":
                age_list.append(age)
            if age != "なし":
                sex_list.append(sex)

            color_dic_down, color_dic_up = get_clothes_color(pose, image, enable_segmentation, segmentation_score_th, use_brect, plot_world_landmark, ax, display_fps)
            print("上の服の色:" + str(color_dic_up))
            print("下の服の色:" + str(color_dic_down))

            #辞書が空のときは追加しない
            print("color_dic_up=" + str(color_dic_up))
            if bool(color_dic_up) == True:
                #print(max(color_dic_up, key=color_dic_up.get()))
                up_color_list.append(max(color_dic_up, key=color_dic_up.get))

            if bool(color_dic_down) == True:
                down_color_list.append(max(color_dic_down, key=color_dic_down.get))


            #glstf = get_glasses_tf(model, image)
            #print(":glstf=" + glstf)

            rcv_data, sock = UDP_recv("繰り返し", sock=sock) #眼鏡が届くまで待っている
            print("眼鏡=" + str(rcv_data))
            glasstf_list.append(rcv_data)

            print("\n")

            img_c += 1

        #存在しなければ終了
        else:
            break

    print("age_list=" + str(age_list))
    print("sex_list=" + str(sex_list))
    print("up_color_list=" + str(up_color_list))
    print("down_color_list=" + str(down_color_list))
    print("glasstf_list=" + str(glasstf_list))


    print("\n")

    #年齢の処理
    if len(age_list) == 0:
        age_push = "不明"

    else:
        age_lvl = int((mean(age_list) // 10) * 10) #平均値 --> 代
        age_push = str(age_lvl) + "代"

        if age_lvl < 10:
            age_push = "10代未満"

    
    #性別の処理
    if len(sex_list) == 0:
        sex_list = "不明"
    
    else:
        sex_push = mode(sex_list)



    #上の服の色の処理
    if len(up_color_list) == 0:
        up_color_push = "不明"

    else:
        up_color_push = mode(up_color_list)



    #下の服の色の処理
    if len(down_color_list) == 0:
        down_color_push = "不明"

    else:
        down_color_push = mode(down_color_list)


    #眼鏡の有無の処理
    glasstf_push = "眼鏡なし"

    if "眼鏡をかけている" in glasstf_list:
        glasstf_push = "眼鏡をかけている"

    print("最終出力")
    print("age_push=" + age_push)
    print("sex_push=" + sex_push)
    print("up_color_push=" + up_color_push)
    print("down_color_push=" + down_color_push)
    print("glasstf_push=" + glasstf_push)

    imgdata.age_push = age_push
    imgdata.sex_push = sex_push
    imgdata.up_color_push = up_color_push
    imgdata.down_color_push = down_color_push
    imgdata.glasstf_push = glasstf_push

    data_pub.publish(imgdata)

    

        #del get_clothes_color_set(), get_clothes_color()
 
#time.sleep(10)
#del get_clothes_color_set, get_clothes_color
#from img_glasses_detect import get_glasses_tf_set, get_glasses_tf


if __name__ == "__main__":
    rospy.init_node("img_mdpp")
    #img_analysis_main()
    main()

    while not rospy.is_shutdown():
        rospy.Rate(10).sleep()
    
    