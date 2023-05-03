#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse

import cv2 
import numpy as np
import mediapipe as mp

import matplotlib.pyplot as plt

from utils import CvFpsCalc

from detect_color_realtime import get_colors

import os




def remove_shade(img):
    s_mag = 2
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # 色空間をBGRからHSVに変換
    img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*s_mag # 彩度の計算
    img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR) # 色空間をHSVからBGRに変換
    return img_bgr


def get_clothes_color_set():
    # 引数解析 ################################################################

    #yoloと合体させるときに、煩雑なので引数解析の関数を取り払う
    cap_device = 0
    cap_width = 960
    cap_height = 540

    # upper_body_only = args.upper_body_only
    model_complexity = 1
    min_detection_confidence = 0.5
    min_tracking_confidence = 0.5
    enable_segmentation = 0.5 #繰り返し部分へ返り値として渡すことが必要
    segmentation_score_th = 0.5 #繰り返し部分へ返り値として渡すことが必要

    use_brect = False #繰り返し部分へ返り値として渡すことが必要
    plot_world_landmark = False #繰り返し部分へ返り値として渡すことが必要
    


    # カメラ準備 ###############################################################
    cap = cv2.VideoCapture(cap_device) #繰り返し部分へ返り値として渡すことが必要
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    mp_pose = mp.solutions.pose 
    pose = mp_pose.Pose( #繰り返し部分へ返り値として渡すことが必要
        # upper_body_only=upper_body_only,
        model_complexity=model_complexity,
        #enable_segmentation=enable_segmentation,   ###
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10) #繰り返し部分へ返り値として渡すことが必要

    # World座標プロット ########################################################
    #if plot_world_landmark:
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d") #繰り返し部分へ返り値として渡すことが必要
    fig.subplots_adjust(left=0.0, right=1, bottom=0, top=1)

    
    display_fps = cvFpsCalc.get() #繰り返し部分へ返り値として渡すことが必要

    return pose, enable_segmentation, segmentation_score_th, use_brect, plot_world_landmark, ax, display_fps




def get_clothes_color(pose, image, enable_segmentation, segmentation_score_th, use_brect, plot_world_landmark, ax, display_fps):

    color_dic_up = {} #上の服の色の割合を表す辞書を初期化 
    color_dic_down = {} #下の服の色の割合を表す辞書を初期化


    image = cv2.flip(image, 1)  # ミラー表示しないと、左と右を逆に検出してしまう。
    debug_image = copy.deepcopy(image)

    # 検出実施 #############################################################
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # 描画 ################################################################
    if enable_segmentation and results.segmentation_mask is not None:
        # セグメンテーション
        mask = np.stack((results.segmentation_mask, ) * 3,
                        axis=-1) > segmentation_score_th
        bg_resize_image = np.zeros(image.shape, dtype=np.uint8)
        bg_resize_image[:] = (0, 255, 0)
        debug_image = np.where(mask, debug_image, bg_resize_image)
    if results.pose_landmarks is not None:
        # 外接矩形の計算
        brect = calc_bounding_rect(debug_image, results.pose_landmarks)
        # 描画
        debug_image, color_dic_up, color_dic_down = draw_landmarks(
            debug_image,
            results.pose_landmarks,
            # upper_body_only,
        )
        debug_image = draw_bounding_rect(use_brect, debug_image, brect)

    # World座標プロット ###################################################
    if plot_world_landmark:
        if results.pose_world_landmarks is not None:
            plot_world_landmarks(
                plt,
                ax,
                results.pose_world_landmarks,
            )

    # FPS表示
    if enable_segmentation and results.segmentation_mask is not None:
        fps_color = (255, 255, 255)
    else:
        fps_color = (0, 255, 0)
    #cv2.putText(debug_image, "FPS:" + str(display_fps), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0, fps_color, 2, cv2.LINE_AA)

    # 画像を書き込む #######################################################
    #write_path = "memory_change/person_chg" + str(img_c) + ".png"
    #cv2.imwrite(write_path, debug_image)

    return color_dic_down, color_dic_up

def main_use():
    pose, enable_segmentation, segmentation_score_th, use_brect, plot_world_landmark, ax, display_fps = get_clothes_color_set()

    img_c = 1

    while(True):
        # 画像を読み込む #####################################################
        read_path = "memory/person" + str(img_c) + ".png"

        #ファイルが存在するとき読み込み
        if os.path.exists(read_path):
            #print("OK")
            image = cv2.imread(read_path)
            color_dic_down, color_dic_up = get_clothes_color(pose, image, enable_segmentation, segmentation_score_th, use_brect, plot_world_landmark, ax, display_fps)

            print(str(img_c) + ":")
            print("上の服の色:" + str(color_dic_up))
            print("下の服の色:" + str(color_dic_down))
            print("\n")

            img_c += 1

        #存在しなければ終了
        else:
            break




def main():
    # 引数解析 ################################################################

    #yoloと合体させるときに、煩雑なので引数解析の関数を取り払う
    cap_device = 0
    cap_width = 960
    cap_height = 540

    # upper_body_only = args.upper_body_only
    model_complexity = 1
    min_detection_confidence = 0.5
    min_tracking_confidence = 0.5
    enable_segmentation = 0.5 #繰り返し部分へ返り値として渡すことが必要
    segmentation_score_th = 0.5 #繰り返し部分へ返り値として渡すことが必要

    use_brect = False #繰り返し部分へ返り値として渡すことが必要
    plot_world_landmark = False #繰り返し部分へ返り値として渡すことが必要
    


    # カメラ準備 ###############################################################
    cap = cv2.VideoCapture(cap_device) #繰り返し部分へ返り値として渡すことが必要
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    mp_pose = mp.solutions.pose 
    pose = mp_pose.Pose( #繰り返し部分へ返り値として渡すことが必要
        # upper_body_only=upper_body_only,
        model_complexity=model_complexity,
        #enable_segmentation=enable_segmentation,   ###
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10) #繰り返し部分へ返り値として渡すことが必要

    # World座標プロット ########################################################
    if plot_world_landmark:
        import matplotlib.pyplot as plt
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d") #繰り返し部分へ返り値として渡すことが必要
        fig.subplots_adjust(left=0.0, right=1, bottom=0, top=1)

    
    display_fps = cvFpsCalc.get() #繰り返し部分へ返り値として渡すことが必要

    img_c = 1 #画像が何枚目か
    while (True):
        # 画像を読み込む #####################################################
        read_path = "memory/person" + str(img_c) + ".png"

        #ファイルが存在するとき読み込み
        if os.path.exists(read_path):
            print("OK")
            image = cv2.imread(read_path)
        #存在しなければ終了
        else:
            break


        image = cv2.flip(image, 1)  # ミラー表示しないと、左と右を逆に検出してしまう。
        debug_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 描画 ################################################################
        if enable_segmentation and results.segmentation_mask is not None:
            # セグメンテーション
            mask = np.stack((results.segmentation_mask, ) * 3,
                            axis=-1) > segmentation_score_th
            bg_resize_image = np.zeros(image.shape, dtype=np.uint8)
            bg_resize_image[:] = (0, 255, 0)
            debug_image = np.where(mask, debug_image, bg_resize_image)
        if results.pose_landmarks is not None:
            # 外接矩形の計算
            brect = calc_bounding_rect(debug_image, results.pose_landmarks)
            # 描画
            debug_image, _, _ = draw_landmarks(
                debug_image,
                results.pose_landmarks,
                # upper_body_only,
            )
            debug_image = draw_bounding_rect(use_brect, debug_image, brect)

        # World座標プロット ###################################################
        if plot_world_landmark:
            if results.pose_world_landmarks is not None:
                plot_world_landmarks(
                    plt,
                    ax,
                    results.pose_world_landmarks,
                )

        # FPS表示
        if enable_segmentation and results.segmentation_mask is not None:
            fps_color = (255, 255, 255)
        else:
            fps_color = (0, 255, 0)
        cv2.putText(debug_image, "FPS:" + str(display_fps), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, fps_color, 2, cv2.LINE_AA)

        # 画像を書き込む #######################################################
        write_path = "memory_change/person_chg" + str(img_c) + ".png"
        cv2.imwrite(write_path, debug_image)

        img_c += 1

        # 画面反映 #############################################################
        #cv2.imshow('MediaPipe Pose Demo', debug_image)

        #cap.release()
        #cv2.destroyAllWindows()


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def draw_landmarks(
    image,
    landmarks,
    # upper_body_only,
    visibility_th=0.5,
):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    #x, yは正規化されているため、もとに戻す必要性あり。
    #print("landmarks.landmark[11].x=" + str(landmarks.landmark[11].x))
    #print("landmarks.landmark[11].y=" + str(landmarks.landmark[11].y))
    #print("landmarks.landmark[11].z=" + str(landmarks.landmark[11].z))

    color_list = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"] #色の名前のリスト
    color_dic_up = {} #色名と割合を辞書で対応つける 色の画素の数を保持する
    color_dic_down = {} #色名と割合を辞書で対応つける 色の画素の数を保持する

    #-------------------服の部分を画像として切り取る---------------------

    #右肩、左肩、腰(右側)、腰(左側)
    up_idx_list = [11, 12, 23, 24]
    up_list = [] 
    for i in up_idx_list:
        mark = landmarks.landmark[i]
        landmark_x = min(int(mark.x * image_width), image_width - 1)
        landmark_y = min(int(mark.y * image_height), image_height - 1)
        landmark_z = mark.z
        landmark_vis = mark.visibility

        data = [i, landmark_x, landmark_y, landmark_z, landmark_vis] #検出座標と可能性をデータとしてまとめる
        up_list.append(data)

        #print("[" + str(i) + "] (x, y, z, vis)=" + str(landmark_x) + ", " + str(landmark_y) + ", " + str(landmark_z) + ", " + str(landmark_vis))

    #右のx座標 > 左のx座標
    #矩形の範囲 = 右側は肩と腰のx座標の最小値 or 平均値
    #             左側は肩と腰のx座標の最大値
    #             上側は左右の最大値 or 平均値
    #　　　　　　 下側は左右の最小値 or 平均

    #0で初期化(何が来ても大丈夫なようにそれ以外の場合は全て0)
    rect_right = 0
    rect_left = 0
    rect_up = 0
    rect_down = 0

    #左右の肩と腰の4点が視界に入っているときに
    if all([up_list[0][4]>visibility_th, up_list[1][4]>visibility_th, up_list[2][4]>visibility_th, up_list[3][4]>visibility_th]):

        rect_right = int((up_list[0][1] + up_list[2][1])/2) #右肩のx座標と、右腰のx座標との平均
        rect_left = int((up_list[1][1] + up_list[3][1])/2)  #左肩のx座標と、左腰のx座標との平均
        rect_up = int((up_list[0][2] + up_list[1][2])/2)    #右肩のy座標と、左肩のy座標との平均
        rect_down = int((up_list[1][2] + up_list[3][2])/2)  #右腰のy座標と、左腰のy座標との平均

    #左右の肩が視界に入っているときに
    elif all([up_list[0][4]>visibility_th, up_list[1][4]>visibility_th]):
        rect_right = up_list[0][1] #右肩のx座標
        rect_left = up_list[1][1] #右肩のx座標
        rect_up = int((up_list[0][2] + up_list[1][2])/2)    #右肩のy座標と、左肩のy座標との平均
        rect_down = image_height - 1

    

    #画像として存在できるとき (高さと幅があるとき)に切り取る
    if rect_up != rect_down and rect_left != rect_right:
         #image[top : bottom, left : right]
        rect_img = image[rect_up:rect_down, rect_left:rect_right]

        #配列の大きさが0でないとき 書き出す
        if rect_img.size != 0:
            #rect_img = rect_img * 1.2
            #c_bright = 1.5
            #rect_img=np.where(rect_img>255/c_bright,255,rect_img*c_bright)
            #rect_img = remove_shade(rect_img)

            cv2.imwrite("up_colthes.jpg", rect_img) #上の服の画像

            color_list = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"] #色の名前のリスト
            color_dic_up = {} #色名と割合を辞書で対応つける 色の画素の数を保持する

            

            color_dic_up = get_colors(rect_img, color_dic_up, color_list)

            #print("上の服の色")
            #print(color_dic_up)
            #print(str(max(color_dic, key=color_dic.get)) + "色、" + "量:" + str(max(color_dic.values)))
            #print(str(max(color_dic_up, key=color_dic_up.get)) + "色")
            #print("\n")

    #------------------------------------------------------------------------



    #-------------------ズボンの部分を画像として切り取る---------------------

    #腰(右側)、腰(左側)、右膝、左膝
    down_idx_list = [23, 24, 25, 26]
    down_list = [] 
    for i in down_idx_list:
        mark = landmarks.landmark[i]
        landmark_x = min(int(mark.x * image_width), image_width - 1)
        landmark_y = min(int(mark.y * image_height), image_height - 1)
        landmark_z = mark.z
        landmark_vis = mark.visibility

        data = [i, landmark_x, landmark_y, landmark_z, landmark_vis] #検出座標と可能性をデータとしてまとめる
        down_list.append(data)

        #print("[" + str(i) + "] (x, y, z, vis)=" + str(landmark_x) + ", " + str(landmark_y) + ", " + str(landmark_z) + ", " + str(landmark_vis))

    #右肩、左肩、腰(右側)、腰(左側)
    #右のx座標 > 左のx座標
    #x座標の大小関係
    #右肩、腰(右側)、腰(左側)、左肩        
    #念のため絶対値を取る
    #right_knees_width = np.abs(down_list[0][1] - down_list[2][1]) 
    #left_knee_width = np.abs(down_list[3][1] - down_list[1][1])

    knee_width = np.abs(down_list[0][1] - down_list[1][1])/2 #腰のマーカーの差の半分を膝の幅として利用する。
    #print("knee_width=" + str(knee_width))

    #print("right_knees_width=" + str(right_knees_width))
    #print("left_knee_width=" + str(left_knee_width))

    #矩形の範囲 = 右側は肩と腰のx座標の最小値 or 平均値
    #             左側は肩と腰のx座標の最大値
    #             上側は左右の最大値 or 平均値
    #　　　　　　 下側は左右の最小値 or 平均


    #0で初期化 (何が来ても大丈夫なようにそれ以外の場合は全て0)
    r_rect_right = 0 #右腿の右
    r_rect_left = 0  #右腿の左
    l_rect_right = 0 #左腿の右
    l_rect_left = 0  #左腿の左
    rl_rect_up = 0   #両腿の上
    rl_rect_down = 0 #両腿の下


    #左右の腰と膝の4点が視界に入っているときに
    if all([down_list[0][4]>visibility_th, down_list[1][4]>visibility_th, down_list[2][4]>visibility_th, down_list[3][4]>visibility_th]):
        #print("down_clothes_all_OK")

        #左右の膝の矩形の上下の平均　
        rl_rect_up = int((down_list[0][2] + down_list[1][2])/2) #左右の腰のy座標の平均
        rl_rect_down = int((down_list[2][2] + down_list[3][2])/2) #左右の膝のy座標の平均

        #右膝の矩形の左右
        r_rl_mid = (down_list[0][1] + down_list[2][1])/2
        r_rect_right = int(r_rl_mid + knee_width/2) #右の腰と膝のx座標の平均に、膝の幅の半分を足した座標
        r_rect_left = int(r_rl_mid - knee_width/2) #右の腰と膝のx座標の平均に、膝の幅の半分を足した座標

        #左膝の矩形の左右
        l_rl_mid = (down_list[1][1] + down_list[3][1])/2
        l_rect_right = int(l_rl_mid + knee_width/2) #右の腰と膝のx座標の平均に、膝の幅の半分を足した座標
        l_rect_left = int(l_rl_mid - knee_width/2) #右の腰と膝のx座標の平均に、膝の幅の半分を足した座標


    #膝が写っていないが左右の腰が視界に入っているときに
    elif all([down_list[0][4]>visibility_th, down_list[1][4]>visibility_th]):
        #print("down_clothes_half_OK")

        #左右の膝の矩形の上下の平均　
        rl_rect_up = int((down_list[0][2] + down_list[1][2])/2) #左右の腰のy座標の平均
        rl_rect_down = image_height - 1 #画像の高さから1を引いたもの

        #右膝の矩形の左右
        r_rect_right = int(down_list[0][1] + knee_width/2) #右の腰のx座標に、膝の幅の半分を足した座標
        r_rect_left = int(down_list[0][1] - knee_width/2) #右の腰のx座標に、膝の幅の半分を足した座標

        #左膝の矩形の左右
        l_rect_right = int(down_list[1][1] + knee_width/2) #左の腰のx座標に、膝の幅の半分を足した座標
        l_rect_left = int(down_list[1][1] - knee_width/2) #左の腰のx座標に、膝の幅の半分を足した座標

    
    #print("right")

    #画像として存在できるとき (高さと幅があるとき)に切り取る
    if rl_rect_up != rl_rect_down and r_rect_left != r_rect_right and l_rect_left != l_rect_right:
        #image[top : bottom, left : right]
        #rect_img = image[rect_up:rect_down, rect_left:rect_right]
        r_rect_img = image[rl_rect_up:rl_rect_down, r_rect_left:r_rect_right] #右膝の矩形
        l_rect_img = image[rl_rect_up:rl_rect_down, l_rect_left:l_rect_right] #左膝の矩形


        #配列の大きさが0でないとき 書き出す
        if r_rect_img.size != 0 and l_rect_img.size != 0:
            rl_con_rect_img = cv2.hconcat([r_rect_img, l_rect_img]) #高さが等しい画像を横に連結

            cv2.imwrite("down_con_colthes.jpg", rl_con_rect_img) 
            #cv.imwrite("down_right_colthes.jpg", r_rect_img) #右下のズボンの画像
            #v.imwrite("down_left_colthes.jpg", l_rect_img) #右下のズボンの画像

            color_list = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"] #色の名前のリスト
            color_dic_down = {} #色名と割合を辞書で対応つける 色の画素の数を保持する

            color_dic_down = get_colors(rl_con_rect_img, color_dic_down, color_list)

            #print("下の服の色")
            #print(color_dic_down)
            #print(str(max(color_dic, key=color_dic.get)) + "色、" + "量:" + str(max(color_dic.values)))
            #print(str(max(color_dic_down, key=color_dic_down.get)) + "色")
            #print("\n")


    #------------------------------------------------------------------------




    #11番 右肩
    #landmark_x = min(int(landmarks.landmark[11].x * image_width), image_width - 1)
    #landmark_y = min(int(landmarks.landmark[11].y * image_height), image_height - 1)
    #landmark_visibility = min(int(landmarks.landmark[11].visibility * image_height), image_height - 1)

    #print("landmark_x=" + str(landmark_x))
    #print("landmark_y=" + str(landmark_y))
    #print("landmarks.landmark[11].visibility=" + str(landmarks.landmark[11].visibility)) #見えているかどうか
    #print("landmarks.landmark[32].visibility=" + str(landmarks.landmark[32].visibility))


    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])

        if landmark.visibility < visibility_th:
            continue


        if index == 11:  # 右肩
            cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 12:  # 左肩
            cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)

        if index == 23:  # 腰(右側)
            cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 24:  # 腰(左側)
            cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)

        if index == 25:  # 右ひざ
            cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 26:  # 左ひざ
            cv2.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)


        


    """
    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])

        if landmark.visibility < visibility_th:
            continue

        if index == 0:  # 鼻
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 1:  # 右目：目頭
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 2:  # 右目：瞳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 3:  # 右目：目尻
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 4:  # 左目：目頭
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 5:  # 左目：瞳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 6:  # 左目：目尻
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 7:  # 右耳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 8:  # 左耳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 9:  # 口：左端
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 10:  # 口：左端
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 11:  # 右肩
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 12:  # 左肩
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 13:  # 右肘
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 14:  # 左肘
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 15:  # 右手首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 16:  # 左手首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 17:  # 右手1(外側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 18:  # 左手1(外側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 19:  # 右手2(先端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 20:  # 左手2(先端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 21:  # 右手3(内側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 22:  # 左手3(内側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 23:  # 腰(右側)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 24:  # 腰(左側)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 25:  # 右ひざ
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 26:  # 左ひざ
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 27:  # 右足首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 28:  # 左足首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 29:  # 右かかと
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 30:  # 左かかと
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 31:  # 右つま先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 32:  # 左つま先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)

        # if not upper_body_only:
        if True:
            cv.putText(image, "z:" + str(round(landmark_z, 3)),
                       (landmark_x - 10, landmark_y - 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                       cv.LINE_AA)

    if len(landmark_point) > 0:
        # 右目
        if landmark_point[1][0] > visibility_th and landmark_point[2][
                0] > visibility_th:
            cv.line(image, landmark_point[1][1], landmark_point[2][1],
                    (0, 255, 0), 2)
        if landmark_point[2][0] > visibility_th and landmark_point[3][
                0] > visibility_th:
            cv.line(image, landmark_point[2][1], landmark_point[3][1],
                    (0, 255, 0), 2)

        # 左目
        if landmark_point[4][0] > visibility_th and landmark_point[5][
                0] > visibility_th:
            cv.line(image, landmark_point[4][1], landmark_point[5][1],
                    (0, 255, 0), 2)
        if landmark_point[5][0] > visibility_th and landmark_point[6][
                0] > visibility_th:
            cv.line(image, landmark_point[5][1], landmark_point[6][1],
                    (0, 255, 0), 2)

        # 口
        if landmark_point[9][0] > visibility_th and landmark_point[10][
                0] > visibility_th:
            cv.line(image, landmark_point[9][1], landmark_point[10][1],
                    (0, 255, 0), 2)

        # 肩
        if landmark_point[11][0] > visibility_th and landmark_point[12][
                0] > visibility_th:
            cv.line(image, landmark_point[11][1], landmark_point[12][1],
                    (0, 255, 0), 2)

        # 右腕
        if landmark_point[11][0] > visibility_th and landmark_point[13][
                0] > visibility_th:
            cv.line(image, landmark_point[11][1], landmark_point[13][1],
                    (0, 255, 0), 2)
        if landmark_point[13][0] > visibility_th and landmark_point[15][
                0] > visibility_th:
            cv.line(image, landmark_point[13][1], landmark_point[15][1],
                    (0, 255, 0), 2)

        # 左腕
        if landmark_point[12][0] > visibility_th and landmark_point[14][
                0] > visibility_th:
            cv.line(image, landmark_point[12][1], landmark_point[14][1],
                    (0, 255, 0), 2)
        if landmark_point[14][0] > visibility_th and landmark_point[16][
                0] > visibility_th:
            cv.line(image, landmark_point[14][1], landmark_point[16][1],
                    (0, 255, 0), 2)

        # 右手
        if landmark_point[15][0] > visibility_th and landmark_point[17][
                0] > visibility_th:
            cv.line(image, landmark_point[15][1], landmark_point[17][1],
                    (0, 255, 0), 2)
        if landmark_point[17][0] > visibility_th and landmark_point[19][
                0] > visibility_th:
            cv.line(image, landmark_point[17][1], landmark_point[19][1],
                    (0, 255, 0), 2)
        if landmark_point[19][0] > visibility_th and landmark_point[21][
                0] > visibility_th:
            cv.line(image, landmark_point[19][1], landmark_point[21][1],
                    (0, 255, 0), 2)
        if landmark_point[21][0] > visibility_th and landmark_point[15][
                0] > visibility_th:
            cv.line(image, landmark_point[21][1], landmark_point[15][1],
                    (0, 255, 0), 2)

        # 左手
        if landmark_point[16][0] > visibility_th and landmark_point[18][
                0] > visibility_th:
            cv.line(image, landmark_point[16][1], landmark_point[18][1],
                    (0, 255, 0), 2)
        if landmark_point[18][0] > visibility_th and landmark_point[20][
                0] > visibility_th:
            cv.line(image, landmark_point[18][1], landmark_point[20][1],
                    (0, 255, 0), 2)
        if landmark_point[20][0] > visibility_th and landmark_point[22][
                0] > visibility_th:
            cv.line(image, landmark_point[20][1], landmark_point[22][1],
                    (0, 255, 0), 2)
        if landmark_point[22][0] > visibility_th and landmark_point[16][
                0] > visibility_th:
            cv.line(image, landmark_point[22][1], landmark_point[16][1],
                    (0, 255, 0), 2)

        # 胴体
        if landmark_point[11][0] > visibility_th and landmark_point[23][
                0] > visibility_th:
            cv.line(image, landmark_point[11][1], landmark_point[23][1],
                    (0, 255, 0), 2)
        if landmark_point[12][0] > visibility_th and landmark_point[24][
                0] > visibility_th:
            cv.line(image, landmark_point[12][1], landmark_point[24][1],
                    (0, 255, 0), 2)
        if landmark_point[23][0] > visibility_th and landmark_point[24][
                0] > visibility_th:
            cv.line(image, landmark_point[23][1], landmark_point[24][1],
                    (0, 255, 0), 2)

        if len(landmark_point) > 25:
            # 右足
            if landmark_point[23][0] > visibility_th and landmark_point[25][
                    0] > visibility_th:
                cv.line(image, landmark_point[23][1], landmark_point[25][1],
                        (0, 255, 0), 2)
            if landmark_point[25][0] > visibility_th and landmark_point[27][
                    0] > visibility_th:
                cv.line(image, landmark_point[25][1], landmark_point[27][1],
                        (0, 255, 0), 2)
            if landmark_point[27][0] > visibility_th and landmark_point[29][
                    0] > visibility_th:
                cv.line(image, landmark_point[27][1], landmark_point[29][1],
                        (0, 255, 0), 2)
            if landmark_point[29][0] > visibility_th and landmark_point[31][
                    0] > visibility_th:
                cv.line(image, landmark_point[29][1], landmark_point[31][1],
                        (0, 255, 0), 2)

            # 左足
            if landmark_point[24][0] > visibility_th and landmark_point[26][
                    0] > visibility_th:
                cv.line(image, landmark_point[24][1], landmark_point[26][1],
                        (0, 255, 0), 2)
            if landmark_point[26][0] > visibility_th and landmark_point[28][
                    0] > visibility_th:
                cv.line(image, landmark_point[26][1], landmark_point[28][1],
                        (0, 255, 0), 2)
            if landmark_point[28][0] > visibility_th and landmark_point[30][
                    0] > visibility_th:
                cv.line(image, landmark_point[28][1], landmark_point[30][1],
                        (0, 255, 0), 2)
            if landmark_point[30][0] > visibility_th and landmark_point[32][
                    0] > visibility_th:
                cv.line(image, landmark_point[30][1], landmark_point[32][1],
                        (0, 255, 0), 2)

    """
    return image, color_dic_up, color_dic_down


def plot_world_landmarks(
    plt,
    ax,
    landmarks,
    visibility_th=0.5,
):
    landmark_point = []

    for index, landmark in enumerate(landmarks.landmark):
        landmark_point.append(
            [landmark.visibility, (landmark.x, landmark.y, landmark.z)])

    face_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    right_arm_index_list = [11, 13, 15, 17, 19, 21]
    left_arm_index_list = [12, 14, 16, 18, 20, 22]
    right_body_side_index_list = [11, 23, 25, 27, 29, 31]
    left_body_side_index_list = [12, 24, 26, 28, 30, 32]
    shoulder_index_list = [11, 12]
    waist_index_list = [23, 24]

    # 顔
    face_x, face_y, face_z = [], [], []
    for index in face_index_list:
        point = landmark_point[index][1]
        face_x.append(point[0])
        face_y.append(point[2])
        face_z.append(point[1] * (-1))

    # 右腕
    right_arm_x, right_arm_y, right_arm_z = [], [], []
    for index in right_arm_index_list:
        point = landmark_point[index][1]
        right_arm_x.append(point[0])
        right_arm_y.append(point[2])
        right_arm_z.append(point[1] * (-1))

    # 左腕
    left_arm_x, left_arm_y, left_arm_z = [], [], []
    for index in left_arm_index_list:
        point = landmark_point[index][1]
        left_arm_x.append(point[0])
        left_arm_y.append(point[2])
        left_arm_z.append(point[1] * (-1))

    # 右半身
    right_body_side_x, right_body_side_y, right_body_side_z = [], [], []
    for index in right_body_side_index_list:
        point = landmark_point[index][1]
        right_body_side_x.append(point[0])
        right_body_side_y.append(point[2])
        right_body_side_z.append(point[1] * (-1))

    # 左半身
    left_body_side_x, left_body_side_y, left_body_side_z = [], [], []
    for index in left_body_side_index_list:
        point = landmark_point[index][1]
        left_body_side_x.append(point[0])
        left_body_side_y.append(point[2])
        left_body_side_z.append(point[1] * (-1))

    # 肩
    shoulder_x, shoulder_y, shoulder_z = [], [], []
    for index in shoulder_index_list:
        point = landmark_point[index][1]
        shoulder_x.append(point[0])
        shoulder_y.append(point[2])
        shoulder_z.append(point[1] * (-1))

    # 腰
    waist_x, waist_y, waist_z = [], [], []
    for index in waist_index_list:
        point = landmark_point[index][1]
        waist_x.append(point[0])
        waist_y.append(point[2])
        waist_z.append(point[1] * (-1))
            
    ax.cla()
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)

    ax.scatter(face_x, face_y, face_z)
    ax.plot(right_arm_x, right_arm_y, right_arm_z)
    ax.plot(left_arm_x, left_arm_y, left_arm_z)
    ax.plot(right_body_side_x, right_body_side_y, right_body_side_z)
    ax.plot(left_body_side_x, left_body_side_y, left_body_side_z)
    ax.plot(shoulder_x, shoulder_y, shoulder_z)
    ax.plot(waist_x, waist_y, waist_z)
    
    plt.pause(.001)

    return


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # 外接矩形
        cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 255, 0), 2)

    return image


if __name__ == '__main__':
    #main()
    main_use()
