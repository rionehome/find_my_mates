#FMMの特徴量抽出mainルーチン

import os
import cv2
import time

from img_glasses_detect import get_glasses_tf_set, get_glasses_tf

from UDP_module import UDP_send

def main():
    sock = UDP_send("始まり")

    count = 0 #繰り返し回数を数える

    #ディレクトリのパスを指定
    DIR = 'memory/'
    
    #print(file_num)

    MAX_FILE_NUM = 10

    while (True):

        #ファイル数を出力
        file_num = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
        

        #写真が揃ってからまだ一回も実行していないときに、特徴を抽出する
        if file_num == MAX_FILE_NUM and count == 0:
            time.sleep(1.5)
            img_analysis_sub(sock=sock)
            count = 1

        #写真が揃っていないときに、カウントを0に戻す
        elif file_num < MAX_FILE_NUM:
            count = 0

    UDP_send("終了", sock=sock)



def img_analysis_sub(sock):


    model = get_glasses_tf_set()
    img_c = 1 

    while(True):
        # 画像を読み込む #####################################################
        read_path = "memory/person" + str(img_c) + ".png"


        #ファイルが存在するとき読み込み
        if os.path.exists(read_path):
        
            image = cv2.imread(read_path)

            if image is not None:

                print(str(img_c) + ":")

                glstf = get_glasses_tf(model, image)
                print(":glstf=" + glstf)

                print("\n")

                img_c += 1

                sock = UDP_send("繰り返し", sock=sock, send_data=glstf)

        #存在しなければ終了
        else:
            break



if __name__ == "__main__":
    #img_analysis_sub()
    main()
    
    