#FMMの特徴量抽出mainルーチン

import os
import cv2
import time

from img_glasses_detect import get_glasses_tf_set, get_glasses_tf

from UDP_module import UDP_send


def img_analysis_sub():


    sock = UDP_send("始まり")


    model = get_glasses_tf_set()
    img_c = 1 
       
    while(True):
        # 画像を読み込む #####################################################
        read_path = "memory/person" + str(img_c) + ".png"


        #ファイルが存在するとき読み込み
        if os.path.exists(read_path):
        
            image = cv2.imread(read_path)


            print(str(img_c) + ":")

            glstf = get_glasses_tf(model, image)
            print(":glstf=" + glstf)

            print("\n")

            img_c += 1

            UDP_send("繰り返し", sock=sock, send_data=glstf)

        #存在しなければ終了
        #else:
        #    break

    UDP_send("終了", sock=sock)


if __name__ == "__main__":
    img_analysis_sub()
    
    