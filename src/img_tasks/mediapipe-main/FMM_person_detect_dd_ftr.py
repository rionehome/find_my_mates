#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import torch
import cv2
import time
import os
import rospy


def person_pic():
  #state = "移動中"
  state = "到着"


  #while(True):
  print("state=" + str(state))

  if state == "到着":
    
    person_dtc_wrt() #人の写真を切り抜く
    
    state = "移動中"

    return person_dtc_wrt

      

    

      #subprocess.call('python %s' % PATH1)
      #subprocess.call('python %s' % PATH2)

      



def person_dtc_wrt():

  #memory内の画像を消去する
  img_c = 1

  while(True):
        # 画像を読み込む #####################################################
        read_path = "memory/person" + str(img_c) + ".png"

        #ファイルが存在するとき削除し
        if os.path.exists(read_path):
          os.remove(read_path)
          img_c += 1

        #なければ終了する
        else:
          break



  # Model
  #model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
  model = torch.hub.load('/home/ri-one/Desktop/github_local_repository/yolov5', 'custom', path='yolov5s.pt', source='local')


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

  #--- 検出の設定 ---
  model.conf = 0.5 #--- 検出の下限値（<1）。設定しなければすべて検出
  model.classes = [0] #--- 0:person クラスだけ検出する。設定しなければすべて検出
  print(model.names) #--- （参考）クラスの一覧をコンソールに表示

  #--- 映像の読込元指定 ---
  #camera = cv2.VideoCapture("../pytorch_yolov3/data/sample.avi")#--- localの動画ファイルを指定
  camera = cv2.VideoCapture(0)                #--- カメラ：Ch.(ここでは0)を指定
  cap_count = 0 #1回だけ画像のサイズを取得する。

  #--- 画像のこの位置より左で検出したら、ヒットとするヒットエリアのためのパラメータ ---
  #pos_x = 240

  #人が写っていない前提で初期化する
  robo_p_dis = 3 #ロボットと人との距離感覚
  robo_p_drct = 3 #ロボットと人との方向感覚

  heigh = 0 #カメラから取得した画像の高さを保持
  width = 0 #カメラから取得した画像の幅を保持

  start_time = 0 #開始時間
  end_time = 0   #終了時間
  delta_time = 1 #1秒

  person_c = 1 #画像の保存番号
  MAX_PERSON_C = 10 #撮影最大番号

  #10枚まで撮影を続ける
  while True:
   

    #--- 画像の取得 ---
    #  imgs = 'https://ultralytics.com/images/bus.jpg'#--- webのイメージファイルを画像として取得
    #  imgs = ["../pytorch_yolov3/data/dog.png"] #--- localのイメージファイルを画像として取得
    ret, imgs = camera.read()              #--- 映像から１フレームを画像として取得

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

    
    #検出した人がいないとき
    if len(person_dtc_list) == 0:
      #人が写っていない前提で初期化する
      robo_p_dis = 3 #ロボットと人との距離感覚
      robo_p_drct = 3 #ロボットと人との方向感覚


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


    end_time = time.time() #現在時刻を終了時刻として取得する


    #人が検出されており、
    if len(box_w_list) != 0:
      
      box_w_max = max(box_w_list) #最大となる矩形の幅を取得する
      box_w_max_idx = box_w_list.index(box_w_max) #最大となる矩形の添字を取得する
      box_cx = box_cx_list[box_w_max_idx] #その添字番目の矩形の中心のx座標を取得する

      #print("box_w_max=" + str(box_w_max))

      #幅が350のバウンディングボックスを対象にする。
      if box_w_max >= 150:
        
        #delta_time(1秒)以上の時間が経過していたら、
        if end_time - start_time >= delta_time:
          start_time = time.time() #現在時刻を開始時刻として取得する

          # img[top : bottom, left : right]
          cv2.imwrite("memory/person" + str(person_c) + ".png", imgs[int(box[1]):int(box[3]), int(box[0]):int(box[2])])
          person_c += 1 #番号をどんどん増やす


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
    cv2.imshow('color',imgs)

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
    if cv2.waitKey(1) & 0xFF == ord('q') or person_c > MAX_PERSON_C:
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
  for i in range(3):
    person_pic()
    time.sleep(10)
