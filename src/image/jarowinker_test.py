import Levenshtein


def sim_name(name_list, get_str):

    jaro_dist_list = [0] #文字列の類似度を保持する変数

    #マスタでなくゲスト同士のみの名前を比較する
    for i in range(1, 4):
        jaro_dist = Levenshtein.jaro_winkler(get_str, name_list[i])
        jaro_dist_list.append(jaro_dist)
        #print("文字列1=" + str1 + "、文字列2=" + str2_list[i] + "、文同士の距離=" + str(jaro_dist))

    print("文字列の類似度のリスト=" + str(jaro_dist_list))
    print("文字列の類似度のリストの最大値=" + str(max(jaro_dist_list)))
    print("文字列の類似度のリストの最大値の添字=" + str(jaro_dist_list.index(max(jaro_dist_list))))

    get_name = name_list[jaro_dist_list.index(max(jaro_dist_list))]
    #print(name)

    return get_name


if __name__ == "__main__":

    get_str = "ガスト"
    name_list = ["マスター", "ゲスト", "マスタ", "オペレータ"]

    get_name = sim_name(name_list, get_str)

    print("名前=" + get_name)