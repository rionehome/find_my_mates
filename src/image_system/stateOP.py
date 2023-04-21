



def get_kagu(pos_state, drct_state):
    kagu = ""

    if pos_state == 1:

        if drct_state == 2:
            kagu = "びん"

    elif pos_state == 2:
        
        if drct_state == 0:
            kagu = "ほわいとてーぶる"

        elif drct_state == 2:
            kagu = "ろんぐてーぶる"


    elif pos_state == 3:
        
        if drct_state == 0:
            kagu = "とーるてーぶる"

        elif drct_state == 2:
            kagu = "どろーわー"
        
    else:
        kagu = "なし"


    return kagu


pos_state = 0 #位置状態 0:スタート地点、1:左にbinがある、2左にlong_table、3左にdrawer
drct_state = 0 #方向状態 0:マスターの方、1:出口側、2bin、3出口の逆

print(get_kagu(1, 2))



