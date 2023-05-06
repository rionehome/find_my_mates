import cv2
import torch
import numpy as np


#初期化
def get_glasses_tf_set():
    YOLO_PATH = '/home/ri-one/Github_Local_repo/yolov5' #大会用PC
    #YOLO_PATH = '/home/ri-one/Desktop/github_local_repository/yolov5' #個人用PC

    MODEL_PATH = '/home/ri-one/catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/19sbest_glasses.pt' #大会用PC
    #MODEL_PATH = '/home/ri-one/fksg_catkin_ws/src/find_my_mates/src/img_tasks/mediapipe_main/19sbest_glasses.pt'
    
    model = torch.hub.load(YOLO_PATH, 'custom', path=MODEL_PATH, source='local')
    model.conf = 0.5

    return model

#繰り返し
def get_glasses_tf(model, image):

    #Qiita, yolov5のモデルをオフラインで使用する, https://qiita.com/Decwest/items/6ef2383787baa7b83143, 2023年3月19日.
    #yolov5のパスは絶対、モデルのパスは相対で指定した。
    
    #print(model.names)

    glasses_count = 0 #メガネが検出されたかどうか

    #image = gmmma_hosei(image)
    result = model(image)
    

    #推論結果を取得
    obj = result.pandas().xyxy[0]

    
    #人が写っているかを調べる
    for i in range(len(obj)):
        if obj.name[i] == "glasses":
            glasses_count += 1
            break

    
    
    #メガネが写っていないとき
    if glasses_count == 0:

        #メガネをかけていない。
        put_glss = 0

        return "眼鏡なし"



    #メガネが写っているとき
    if glasses_count == 1:

        glss_w_l = [] #検出されたメガネの大きさを保持
        glss_idx_l = [] #検出されたメガネの添字を保持


        #バウンディングボックスの情報を取得
        for  i in range(len(obj)):
            
            #検出された物体がメガネのときに
            if obj.name[i] == "glasses":

                #人のときだけ計算することで無駄な計算を削減する。
                xmin = obj.xmin[i]
                ymin = obj.ymin[i]
                xmax = obj.xmax[i]
                ymax = obj.ymax[i]

                glss_w_l.append(xmax-xmin) #幅を計算して追加する
                glss_idx_l.append(i) #添字を追加する

                #print("name =", name, "xmin =", xmin, "ymin =", ymin, "xmax =", ymax, "ymin =", ymax)

            
            #print("(x_min=" + str(xmin) + ", y_min=" + str(ymin) + ")" + "(x_max=" + str(xmax) + ", y_max=" + str(ymax) + ")")
                
            #print("名前" + str(name) + "幅:" + str(w) + ", 高さ:" + str(h))

        #一番近くにあるメガネを検出する
        max_w_idx = glss_w_l.index(max(glss_w_l))
        print("glss_idx_l[max_w_idx]=" + str(glss_idx_l[max_w_idx]))

        #一番近くにあるメガネのみを判定に掛ける
        #xmin = obj.xmin[glss_idx_l[max_w_idx]]
        #ymin = obj.ymin[glss_idx_l[max_w_idx]]
        #xmax = obj.xmax[glss_idx_l[max_w_idx]]
        #ymax = obj.ymax[glss_idx_l[max_w_idx]]
        
        #print("メガネをかけている=" + str(put_glss))

        return "眼鏡をかけている"



def main_use():
    model = get_glasses_tf_set()

    for i in range(15):
        print(str(i+1) + "番目")
        image = cv2.imread("memory/person" + str(i+1) + ".png")
        glstf = get_glasses_tf(model, image)
        print(str(i+1) + ":glstf=" + glstf)

    
if __name__ == "__main__":
    main_use()