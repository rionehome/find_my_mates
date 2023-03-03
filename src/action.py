#全体的な流れを作る

#1つ目の添字は人を意味する
#0:オペレータ、 1:ゲスト1、 2:ゲスト2、 3:ゲスト3

#2つ目の添字は発見状況を保持する
#人=ゲストの場合、0:未発見、1:発見と特徴取得が完了
#人=オペレータの場合、3:開始、4:報告完了、 5終了

#開始
state = [0, 3] #状態を保持する


GUEST_NUM = 3 #ゲストの人数

distance = 0 #画像から送られるロボットから見た人の距離を保持 0:遠い, 1:中, 2:近い 
direction = 0 #画像から送られるロボットから見た人の方向を保持 0:左, 1:中, 2:右 

detect = False #ロボットがゲストの顔を撮影しおえて、一定以上時間がたった場合True, でない場合False

furniture_list = [] #ゲストの近くにある家具を保持

#START オペレータのとロボットは向かい合っている
#そこからlaunchファイルを起動する

#print(state)

#開始状態なら
if state == [0, 3]:
    """
    制御:180度回転する
    """
    state = [1, 0] #1人目未発見へ状態遷移 


#ゲストの人数1~3人まで繰り返す
i = 1
while i <= GUEST_NUM:


    #print(state)
    #distance = 1
    #direction = 1
    #detect = 1

    #1人目未発見なら1人目を探す 
    if state == [i, 0]:

        while True:
            """
            画像:ゲスト1の顔を見つける 特徴を抽出する
            制御:ゲスト1の顔に接近する(YOLOの顔ver)
            画像:ゲスト1との距離、位置を取得して変数distance, directionに代入
            """

            #ゲスト1とロボットとの距離がほど良い距離、方向かつ特徴抽出が完了したなら
            if distance == 1 and direction == 1 and detect == True:
                """
                画像:ゲスト1を見つけたということをバウンディングボックスで表示して待つ
                画像:ゲスト1の近くにある家具をYOLOで検知し取得し、furniture_listへ代入
                """
                state = [i, 1] #1人目発見と特徴抽出完了へ状態遷移
                break

    #print(state)



    #距離と方向の変数を別の人に適用するためもとに戻す
    distance = 0
    direction = 0


    #distance = 1
    #direction = 1

    #人目発見と特徴抽出完了ならオペレータのもとへ戻る
    if state == [i, 1]:

        """
        制御:180度回転する
        """

        while True:
            """
            画像:オペレータの顔を見つける
            制御:オペレータの顔に接近する(YOLOの顔ver)
            画像:オペレータとの距離、位置を取得して変数distance, directionに代入
            """

            #ゲスト1とロボットとの距離がほど良い距離、方向なら
            if distance == 1 and direction == 1:
                """
                音声:ゲスト1の名前、家具のリストを取得し、誰がどこにいたかを伝える
                """
                state = [0, 4] #報告完了状態へ状態遷移
                break

    #print(state)
 
    #家具の変数を別の人に適用するためもとに戻す
    furniture_list = []
    
    #報告完了状態なら
    if state == [0, 4]:
        """
        制御:180度回転する
        """
   
        i += 1

        if i <= GUEST_NUM:
            state = [i, 0] #2人目未発見へ状態遷移



#3人分の報告を終了したならば
if i == 4 and state == [0, 4]:
    state = [0, 5]

#print(state)