import cv2 
import numpy as np


def get_colors(frame, color_dic, color_list):

    #BGR色空間からHSV色空間への変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #黒色
    upper = np.array([255, 255, 63])
    lower = np.array([0, 0, 0])
    #色検出しきい値範囲内の色を抽出するマスクを作成
    frame_mask = cv2.inRange(hsv, lower, upper)
    color_dic['黒'] = cv2.countNonZero(frame_mask)


    #灰色
    upper = np.array([255, 31, 191])
    lower = np.array([0, 0, 64])
    #色検出しきい値範囲内の色を抽出するマスクを作成
    frame_mask = cv2.inRange(hsv, lower, upper)
    color_dic['灰'] = cv2.countNonZero(frame_mask)


    #白色
    upper = np.array([255, 31, 255])
    lower = np.array([0, 0, 192])
    #色検出しきい値範囲内の色を抽出するマスクを作成
    frame_mask = cv2.inRange(hsv, lower, upper)
    color_dic['白'] = cv2.countNonZero(frame_mask)


    for i in range(9):
                
        #彩色
        upper = np.array([20 + i*20, 255, 255])
        lower = np.array([i*20, 32, 64])
        #色検出しきい値範囲内の色を抽出するマスクを作成
        frame_mask = cv2.inRange(hsv, lower, upper)
        color_dic[color_list[i]] = cv2.countNonZero(frame_mask)

    return color_dic



#テスト用メインルーチン
def main():

    #色検出しきい値の設定
    #hsv空間において
    #橙色 上限[20, 255, 255] ~ 下限[0, 192, 64]
    #薄い橙色 上限[20, 191, 255] ~ 下限[0, 64, 64]
    #白色 上限[255, 63, 255] ~ 下限[0, 0, 192]
    #灰色 上限[255, 63, 191] ~ 下限[0, 0, 64]
    #黒色 上限[255, 255, 63] ~ 下限[0, 0, 0]

    #len(color_list) = 12色 (9彩色、3無彩色)
    color_list = ["橙", "黄", "黄緑", "緑", "水", "青", "紫", "桃", "赤", "黒", "灰", "白"] #色の名前のリスト
    color_dic = {} #色名と割合を辞書で対応つける 色の画素の数を保持する

    for i in range(len(color_list)):  
        color_dic[color_list[i]] = 0

    # VideoCapture オブジェクトを取得します
    capture = cv2.VideoCapture(0)

    get_count = 0 #カメラの画像から1度だけ幅と高さを取得する
    height = 0 
    width = 0

    while(True):
        ret, frame = capture.read()

        if get_count == 0:
            height, width, _ = frame.shape[:3]
            all_area = height * width
            print("全体の面積=" + str(all_area))
            get_count += 1

        
        color_dic = get_colors(frame, color_dic, color_list)

        #print(color_dic)

        #辞書の値が最大・最小となるキーを取得
        max_k = max(color_dic, key=color_dic.get)
        print(max_k)


        ret, frame = capture.read()
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()    

