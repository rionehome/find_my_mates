#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import torch
import cv2
import time
import os
import rospy
from std_msgs.msg import Bool

"""
  [‘person’, ‘bicycle’, ‘car’, ‘motorcycle’, ‘airplane’, ‘bus’, 
  ‘train’, ‘truck’, ‘boat’, ‘traffic light’, ‘fire hydrant’, ‘stop sign’, 
  ‘parking meter’, ‘bench’, ‘bird’, ‘cat’, ‘dog’, ‘horse’, ‘sheep’, ‘cow’, 
  ‘elephant’, ‘bear’, ‘zebra’, ‘giraffe’, ‘backpack’, ‘umbrella’, ‘handbag’, 
  ‘tie’, ‘suitcase’, ‘frisbee’, ‘skis’, ‘snowboard’, ‘sports ball’, ‘kite’, 
  ‘baseball bat’, ‘baseball glove’, ‘skateboard’, ‘surfboard’, ‘tennis racket’, 
  ‘bottle’, ‘wine glass’, ‘cup’, ‘fork’, ‘knife’, ‘spoon’, ‘bowl’, ‘banana’, 
  ‘apple’, ‘sandwich’, ‘orange’, ‘broccoli’, ‘carrot’, ‘hot dog’, ‘pizza’, 
  ‘donut’, ‘cake’, ‘chair’, ‘couch’, ‘potted plant’, ‘bed’, ‘dining table’, 
  ‘toilet’, ‘tv’, ‘laptop’, ‘mouse’, ‘remote’, ‘keyboard’, ‘cell phone’, 
  ‘microwave’, ‘oven’, ‘toaster’, ‘sink’, ‘refrigerator’, ‘book’, ‘clock’, 
  ‘vase’, ‘scissors’, ‘teddy bear’, ‘hair drier’, ‘toothbrush’]

"""

class Person:
  def __init__(self):
    #self.state = "移動中"
    self.state = '到着'

  def main(self):

    #self.state = "移動中"
    # self.state = "到着"

    # Model
    #model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model = torch.hub.load('/home/ri-one/Github_Local_repo/yolov5', 'custom', path='yolov5s.pt', source='local')

    #--- 検出の設定 ---
    model.conf = 0.5 #--- 検出の下限値（<1）。設定しなければすべて検出
    model.classes = [0] #--- 0:person クラスだけ検出する。設定しなければすべて検出
    print(model.names) #--- （参考）クラスの一覧をコンソールに表示

    #--- カメラの設定 ---
    PC_CAM_DEV = 0 #PC内蔵カメラのデバイス番号
    WEB_CAM_DEV = 4#self.cam_dev_dtc() #Webカメラのデバイス番号

    camera = cv2.VideoCapture(PC_CAM_DEV)      #内蔵カメラを取得
    web_camera = cv2.VideoCapture(WEB_CAM_DEV)


    
    while(True):
      """
      self.stateを購読する
      """


      if self.state == "到着":
        self.person_dtc_wrt(model, camera, web_camera) #人の写真を切り抜く
        self.state = "移動中"

      elif self.state == "移動中":
        self.person_exist(model, camera)

        


    

  def person_detect(self):
    self.state = "到着"

  #使用可能なカメラのデバイス番号を調べる。	
  def cam_dev_dtc(self, START_NUM=2, VIDEO_DEV_NUM=10):	
    #VIDEO_DEV_NUM = 10	
    #START_NUM = 3

    WEB_CAM_DEV = 2

    #webカメラの番号を取得する。	
    for i in range(START_NUM, VIDEO_DEV_NUM+1):	
      web_camera = cv2.VideoCapture(i) #USBカメラを取得	
      w_ret, w_imgs = web_camera.read()

      #画像を取得できる番号ときに、その番号をusbカメラとして使用できる。	
      if w_imgs is not None:	
        WEB_CAM_DEV = i	
        #print("WEB_CAM_DEV=" + str(WEB_CAM_DEV))	
        break

    print("WEB_CAM_DEV=" + str(WEB_CAM_DEV))	
    return WEB_CAM_DEV



  def person_exist(self, model, camera):
    check_exit_pub = rospy.Publisher("/person", Bool, queue_size=1)

    person_exit = False #存在しない。   

    #--- 画像の取得 ---
    #  imgs = 'https://ultralytics.com/images/bus.jpg'#--- webのイメージファイルを画像として取得
    #  imgs = ["../pytorch_yolov3/data/dog.png"] #--- localのイメージファイルを画像として取得
    ret, imgs = camera.read()              #--- 映像から１フレームを画像として取得

    #--- 推定の検出結果を取得 ---
    #results = model(imgs) #--- サイズを指定しない場合は640ピクセルの画像にして処理
    results = model(imgs, size=160) #--- 160ピクセルの画像にして処理

    #--- 出力 ---
    #--- 検出結果を画像に描画して表示 ---
    #--- 各検出について

    person_dtc_list = [] #人が複数人見つかったら、リストに追加する。(一番近い人がターゲットになる。)

    
    #検出した人がいないとき
    if len(person_dtc_list) == 0:
      #人が写っていない前提で初期化する
      person_exit = False #存在しない。


    person_dtc_list = [] #人が複数人見つかったら、リストに追加する。(一番近い人がターゲットになる。)
    
    #検出した人がいないとき
    if len(person_dtc_list) == 0:
      #人が写っていない前提で初期化する
      person_exit = False #存在しない。


    box_w_list = [] #幅が一番大きい(一番距離が近い人)を追跡する。


    for *box, conf, cls in results.xyxy[0]:  # xyxy, confidence, class

      box_w = box[2] - box[0] #バウンディングボックスの幅
      box_w_list.append(box_w) #リストに矩形の幅を追加


    #人が検出されており、
    if len(box_w_list) != 0:
      
      box_w_max = max(box_w_list) #最大となる矩形の幅を取得する
      #矩形の幅が150を超えているものがあれば
      if box_w_max >= 150:
        person_exit = True


    print("person_exit=" + str(person_exit))

    b = Bool()
    b.data = person_exit
    check_exit_pub.publish(b)

    """
    画像から メインへ 人がいるかどうか[person_exit]を出版する
    """

    


  def person_dtc_wrt(self, model, camera, web_camera):


    #person_exit = False #人が存在するか False:存在しない、True:存在する

    #memory内の画像を消去する
    p_img_c = 1
    f_img_c = 1

    FOLDER_PATH = "/home/ri-one/catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/memory"

    #--------------------------------------------------------------


    #---以前の画像を削除する--------
    while(True):

      # 画像を読み込む #####################################################
      p_read_path = FOLDER_PATH + "/person" + str(p_img_c) + ".png"
      f_read_path = FOLDER_PATH + "/face" + str(f_img_c) + ".png"

      #ファイルが存在するとき削除し
      if os.path.exists(p_read_path):
        os.remove(p_read_path)
        p_img_c += 1

      elif os.path.exists(f_read_path):
        os.remove(f_read_path)
        f_img_c += 1

      #なければ終了する
      else:
        break
    #-------------------------------



    #--- 映像の読込元指定 ---
    #camera = cv2.VideoCapture("../pytorch_yolov3/data/sample.avi")#--- localの動画ファイルを指定

    cap_count = 0 #1回だけ画像のサイズを取得する。

    #--- 画像のこの位置より左で検出したら、ヒットとするヒットエリアのためのパラメータ ---
    #pos_x = 240

    #人が写っていない前提で初期化する
    #robo_p_dis = 3 #ロボットと人との距離感覚
    #robo_p_drct = 3 #ロボットと人との方向感覚

    heigh = 0 #カメラから取得した画像の高さを保持
    width = 0 #カメラから取得した画像の幅を保持

    start_time = 0 #開始時間
    end_time = 0   #終了時間
    delta_time = 1 #1秒

    person_c = 1 #画像の保存番号
    MAX_PERSON_C = 10 #撮影最大番号

    time_count = 0 #時間の経過を数える
    END_TIME_COUNT = 20 #20病後に窓を閉じる

    #-----繰り返し処理--------------------------------------------


    #10枚まで撮影を続ける
    while True:
    

      #--- 画像の取得 ---
      #  imgs = 'https://ultralytics.com/images/bus.jpg'#--- webのイメージファイルを画像として取得
      #  imgs = ["../pytorch_yolov3/data/dog.png"] #--- localのイメージファイルを画像として取得
      ret, imgs = camera.read()              #--- 映像から１フレームを画像として取得
      w_ret, w_img = web_camera.read()

      #--- 画像の大きさを取得する
      if cap_count == 0:
        height, width = imgs.shape[:2]    
        print("幅:" + str(width) + "、高さ:" + str(height))
        cap_count = 1 

      #--- 推定の検出結果を取得 ---
      #results = model(imgs) #--- サイズを指定しない場合は640ピクセルの画像にして処理
      results = model(imgs, size=160) #--- 160ピクセルの画像にして処理

      #--- 出力 ---
      #--- 検出結果を画像に描画して表示 ---
      #--- 各検出について

      person_dtc_list = [] #人が複数人見つかったら、リストに追加する。(一番近い人がターゲットになる。)



      box_w_list = [] #幅が一番大きい(一番距離が近い人)を追跡する。
      box_cx_list = [] #幅が一番大きい(一番距離が近い人)を追跡する。

      #print("results.xyxy[0]=" + str(results.xyxy[0]))
      #print("len(results.xyxy[0])=" + str(len(results.xyxy[0])))

      for *box, conf, cls in results.xyxy[0]:  # xyxy, confidence, class

          #--- クラス名と信頼度を文字列変数に代入
          s = model.names[int(cls)]+":"+'{:.1f}'.format(float(conf)*100)

          #--- ヒットしたかどうかで枠色（cc）と文字色（cc2）の指定
          cc = (255,0,0)
          cc2 = (255, 255, 255)

        
          box_w = box[2] - box[0] #バウンディングボックスの幅
          box_c_x = (box[2] + box[0])/2 #バウンディングボックスの中心のx

          box_w_list.append(box_w) #リストに矩形の幅を追加
          box_cx_list.append(box_c_x) #リストに矩形の中心を追加

          #print("int(box[0])=" + str(int(box[0]))) xmin
          #print("int(box[1])=" + str(int(box[1]))) ymin
          #print("int(box[2])=" + str(int(box[2]))) xmax
          #print("int(box[3])=" + str(int(box[3]))) ymax

          #--- 枠描画

      #以下のような矩形を追跡する(距離と位置で挙動を変える。)
      #print("results.xyxy[0]=" + str(results.xyxy[0]))

      end_time = time.time() #現在時刻を終了時刻として取得する


      #人が検出されており、
      if len(box_w_list) != 0:
        
        box_w_max = max(box_w_list) #最大となる矩形の幅を取得する
        box_w_max_idx = box_w_list.index(box_w_max) #最大となる矩形の添字を取得する
        box_cx = box_cx_list[box_w_max_idx] #その添字番目の矩形の中心のx座標を取得する

        #print("box_w_max=" + str(box_w_max))

        #幅が350のバウンディングボックスを対象にする。
        if box_w_max >= 150:    

          box = results.xyxy[0][box_w_max_idx] #最大のバウンディングボックスを取得する

          #time_count += 1 #時間を数える

          #delta_time(1秒)以上の時間が経過していたら、
          if end_time - start_time >= delta_time:
            start_time = time.time() #現在時刻を開始時刻として取得する
  

            if person_c < 11:
              # img[top : bottom, left : right]
              cv2.imwrite(FOLDER_PATH + "/person" + str(person_c) + ".png", imgs[int(box[1]):int(box[3]), int(box[0]):int(box[2])])

              if w_img is not None:
                cv2.imwrite(FOLDER_PATH + "/face" + str(person_c) + ".png", w_img)

              person_c += 1 #番号をどんどん増やす


            time_count += 1


            #--- 枠描画
          cv2.rectangle(
              imgs,
              (int(box[0]), int(box[1])),
              (int(box[2]), int(box[3])),
              color=cc,
              thickness=2,
              )

          #--- 文字枠と文字列描画
          #yoloの中よりも自分で描画した方が非常に高速
          cv2.rectangle(imgs, (int(box[0]), int(box[1])-20), (int(box[0])+len(s)*10, int(box[1])), cc, -1)
          cv2.putText(imgs, s, (int(box[0]), int(box[1])-5), cv2.FONT_HERSHEY_PLAIN, 1, cc2, 1, cv2.LINE_AA)

          #追いかけるマーカーを描画
          cv2.circle(imgs, (int((box[0]+box[2])/2), int((box[1]+box[3])/2)), 15, (255, 255, 255), thickness=-1)


          #print("追跡する矩形の添字番号=" + str(box_w_max_idx))
          #print("距離:" + str(robo_p_dis) + "、方向:" + str(robo_p_drct))

      #--- 描画した画像を表示
      cv2.imshow("camera",imgs)

      print("w_img=" + str(w_img))
      if w_img is not None:
        cv2.imshow("web_camere", w_img)

      """
      ここでperson_existを出版する。
      True:立ち止まって撮影する
      False:なにもしない
      """

        #for i in range(len(results.xyxy)):
        #    print(results.pandas().xyxy[i])

        #print(results.pandas().xyxy[0])

      #--- （参考）yolo標準機能を使った出力 ---
      #  results.show()#--- yolo標準の画面表示
      #  results.print()#--- yolo標準のコンソール表示

      #--- （参考）yolo標準の画面を画像取得してopencvで表示 ---
      #  pics = results.render()
      #  pic = pics[0]
      #  cv2.imshow('color',pic)

      #--- 「q」キー操作があればwhileループを抜ける ---
      print("time_count=" + str(time_count))

      #qキーが押され、
      if cv2.waitKey(1) & 0xFF == ord('q') or (person_c > MAX_PERSON_C and delta_time > END_TIME_COUNT):
        cv2.destroyAllWindows()
        break

    #while(video.isOpened()):

    #    r, bgr = video.read()

    #    cv2.

    # Images
    #imgs = ['https://ultralytics.com/images/zidane.jpg']  # batch of images

    # Inference
    #results = model(bgr)

    # Results
    #results.print()
    #results.save()  # or .show()

    #print(results.xyxy[0])
    #print(results.pandas().xyxy[0])
    #esults.xyxy[0]  # img1 predictions (tensor)
    #results.pandas().xyxy[0]  # img1 predictions (pandas)

if __name__ == '__main__':
  rospy.init_node("img_per_detect")
  p = Person()
  p.main()

  while not rospy.is_shutdown():
    rospy.Rate(10).sleep()