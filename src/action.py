from find_my_mates.msg import MoveAction 
def main(self):
    people = [1,2,3]
#@(画像)オペレーターを識別するために、この人の情報を取得しておく
#@(画像)下をfor文で回すため、個人情報が混ざらないようにループの外で、ゲストのそれぞれの情報を習得するようにしておく

    #forループ開始
#挑戦するゲストの数だけループするようにする
    for i in people:

#最初OPの近くにいる
    #@(画像)OP以外を認識して、ゲストの場所に行くようにする
    
    
# 回転して、ゲストを見つける
    #@(制御)だいきが作った回転する部分を実装する
    #@(画像)ゲストを認識したときに、何か値をmain.pyに送る


# ゲストの前まで移動する
    #@(制御)person_detect.pyをOP以外の人間に対して動くようにする必要がある
    
    
# ゲストの特徴を取得する
    #@(制御)ゲストに名前を聞き、情報として取得する
    
    
# 回転して、OPの位置まで移動する
    #@(制御)だいきが作った回転する部分を実装する


# OPに、ゲストの名前、特徴を知らせる

    #forループ終了


#プログラムを終了する
    m = MoveAction()
    m.time = 0.1
    m.angle_speed = 0.0
    m.angle_speed = 0.0
    m.direction = "forward"
    m.distance = "normal"
    self.move_pub.publish(m)
    self.audio_pub.publish("実行終了しました")