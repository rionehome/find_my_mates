#ジコログ, 【Python】OpenCVを超えたInsightFaceによる顔認識,
#https://self-development.info/%E3%80%90python%E3%80%91opencv%E3%82%92%E8%B6%85%E3%81%88%E3%81%9Finsightface%E3%81%AB%E3%82%88%E3%82%8B%E9%A1%94%E8%AA%8D%E8%AD%98/
#2023年2月28日.

import numpy as np
import cv2
from insightface.app import FaceAnalysis


#初期化
def get_sex_age_set():
    app = FaceAnalysis() #実体化 app = FaceAnalysis(name="antelopev2")でモデルを変更できる
    app.prepare(ctx_id=0, det_size=(640, 640))

    return app


#繰り返し
def get_sex_age(app, image):
    
    #画像から年齢と性別を取得
    faces = app.get(np.asarray(image))


    #顔が検出されてなかったら
    if len(faces) == 0:
        return "なし", "なし"
    
    #顔が検出されたら
    else: 
        #顔が1つだけのとき
        if len(faces) == 1:

            gender = ["女", "男"]
            year_field = (faces[0]['age'] // 10) * 10 #年代を保持する 年齢を10で割ったときの商かける10 

            print("性別:" + gender[faces[0]['gender']])
            print(str(faces[0]['age']) + "歳")
            
            if year_field == 0:
                print("年齢:10代未満")

            else:
                print("年齢:" + str(year_field) + "代")

            


        #顔が複数写っている場合
        else:

            w_list = [] #幅のリスト

            #一番大きな矩形を調べる
            for i in range(len(faces)):
                w = faces[i]['bbox'][2] - faces[i]['bbox'][0] #幅を計算
                w_list.append(w) #幅を追加


            w_max_idx = w_list.index(max(w_list)) #幅の最大値の添字

            gender = ["woman", "man"]
            year_field = (faces[w_max_idx]['age'] // 10) * 10 #年代を保持する 年齢を10で割ったときの商かける10 


            #print("幅:" + str(w) + "、高さ:" + str(h))
            #print("中心: x=" + str(c_x) + ", y=" + str(c_y)) 
            print("性別:" + str(gender[faces[w_max_idx]['gender']]))

            print(str(faces[w_max_idx]['age']) + "歳")
            
            if year_field == 0:
                print("年齢:10代未満")

            else:
                print("年齢:" + str(year_field) + "代")

        return faces[0]['age'], gender[faces[0]['gender']]


def main_use():
    app = get_sex_age_set()

    for i in range(15):
        print(str(i+1) + "番目")
        image = cv2.imread("memory/person" + str(i+1) + ".png")
        age, sex = get_sex_age(app, image)
        print(str(i+1) + ":age=" + str(age) + "、sex=" + str(sex))

        

if __name__ == '__main__':
    main_use()