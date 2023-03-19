# ジコログ, 【Python】OpenCVを超えたInsightFaceによる顔認識,
# https://self-development.info/%E3%80%90python%E3%80%91opencv%E3%82%92%E8%B6%85%E3%81%88%E3%81%9Finsightface%E3%81%AB%E3%82%88%E3%82%8B%E9%A1%94%E8%AA%8D%E8%AD%98/
# 2023年2月28日.

import numpy as np
import cv2
from insightface.app import FaceAnalysis
import rospy
from std_msgs.msg import String
from find_my_mates.msg import MoveAction, RealTime


class RtBioSOldComp:
    def __init__(self):
        """
        中心部からの購読者を作成する (ターゲットの名前を取得するため)
        現在、画面中央に写っている人の名前を音声認識で取得し、探すべき名前と同じならばその顔から特徴を抽出する

        音声からの購読者を作成する (ターゲット未発見時の状態で 現在中央に写っている顔がターゲットかを知るため)
        音声への出版者を作成する (ターゲットが未発見の状態 誰かの顔が見つかったときに静止し、名前を聞くため)
        制御への出版者を作成する (ターゲットが未発見、発見、または報告状態において、その人に接近し距離を調節するため)
        """

        self.realtime_sub = rospy.wait_for_message("/realtime", RealTime)
        self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)
        self.move_pub = rospy.Publisher("/move", MoveAction, queue_size=1)

        print("初期化")

    def main(self):
        app = FaceAnalysis()  # 実体化 app = FaceAnalysis(name="antelopev2")でモデルを変更できる
        app.prepare(ctx_id=0, det_size=(640, 640))

        # カメラの設定　デバイスIDは0
        cap = cv2.VideoCapture(0)

        cam_count = 0  # 1回だけカメラの画像から高さと幅を取得するための変数
        frame_w = 0  # カメラの画像の幅を保持する
        frame_h = 0  # カメラの画像の高さを保持する

        robo_face_dis = 0  # (ロボットから見た)人の顔とロボットとの距離  0:遠い 1:中距離 2:近い
        robo_face_drct = 0  # (ロボットから見た)人の顔が存在する方向      0:左   1:中央   2:右
        thrd_min = (640 / 6) / 3  # 距離の遠近の閾値の最小値 (これを下回ると距離は遠いと判断される)
        thrd_max = (640 / 6) * 3 / 2  # 距離の遠近の閾値の最大値 (これを上回ると距離は近いと判断される)
        # 閾値をこのカメラで取得した幅の値で設定したが、他のカメラでも同様のことができるようにするため数値で指定した。

        # 繰り返しのためのwhile文
        while True:
            # カメラからの画像取得
            ret, frame = cap.read()

            if cam_count == 0:
                frame_h, frame_w, _ = frame.shape
                print("カメラの画像の形状: 幅:" + str(frame_w) + "、高さ:" + str(frame_h))
                # カメラの画像の形状: 幅:640、高さ:480
                cam_count = 1

            faces = app.get(np.asarray(frame))
            print("faces:" + str(len(faces)))

            # print("\n\n")
            r_frame = app.draw_on(frame, faces)

            # カメラの画像の出力
            cv2.imshow("camera", r_frame)

            for i in range(len(faces)):
                w = faces[i]["bbox"][2] - faces[i]["bbox"][0]
                h = faces[i]["bbox"][3] - faces[i]["bbox"][1]
                c_x = (faces[i]["bbox"][2] + faces[i]["bbox"][0]) / 2
                c_y = (faces[i]["bbox"][3] + faces[i]["bbox"][1]) / 2
                gender = ["女", "男"]
                year_field = (faces[i]["age"] // 10) * 10  # 年代を保持する 年齢を10で割ったときの商かける10

                print("幅:" + str(w) + "、高さ:" + str(h))
                print("中心: x=" + str(c_x) + ", y=" + str(c_y))
                print("性別:" + str(gender[faces[i]["gender"]]))

                if year_field == 0:
                    print("年齢:10代未満")

                else:
                    print("年齢:" + str(year_field) + "代")

                    # 距離を仕分ける
                    if w < thrd_min:
                        # print(str(i) + "番目の人が遠い")
                        robo_face_dis = 0  # ロボットは人が中央に来るまで前に進む

                    elif w >= thrd_min and w <= thrd_max:
                        # print(str(i) + "番目の人が中央の距離")
                        robo_face_dis = 1  # ロボットはそのまま

                    elif w > thrd_max:
                        # print(str(i) + "番目の人が近い")
                        robo_face_dis = 2  # ロボットは人が中央に来るまで後ろに下がる

                    # 方向を仕分ける
                    if c_x < frame_w / 3:
                        # print(str(i) + "番目の人が左にいる")
                        robo_face_drct = 0  # ロボットは人が中央に来るまで左回りする

                    elif c_x > frame_w / 3 and c_x < frame_w * 2 / 3:
                        # print(str(i) + "番目の人が中央の方向")
                        robo_face_drct = 1  # ロボットはそのまま

                    elif c_x > frame_w * 2 / 3:
                        # print(str(i) + "番目の人が右にいる")
                        robo_face_drct = 2  # ロボットは人が中央に来るまで右回りする

                print(
                    str(i + 1)
                    + "番目の顔の距離:"
                    + str(robo_face_dis)
                    + "、方向:"
                    + str(robo_face_drct)
                )
                print("\n")

                """
                音声へ、距離、方向を出版する (音声側で購読したとき:ターゲット未発見状態かつ中央と中距離のときに名前を聞く または 報告状態かつ中央と中距離のときに名前や特徴を報告する)
                音声からの購読者を作成する
                制御へ、距離、方向を出版する (制御側で購読したとき:人に近づく必要性のある未発見、報告状態で位置を調整するために使う)
                """

                self.audio_pub = rospy.Publisher("/audio", String, queue_size=1)
                self.audio_sub = rospy.Subscriber("/audio", String, queue_size=1)
                self.move_pub = rospy.Publisher("/move", MoveAction, queue_size=1)

            # 繰り返し文から抜けるためのif文
            key = cv2.waitKey(10)
            if key == 27:
                break

        # メモリを解放して終了するためのコマンド
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rtbioscmp = RtBioSOldComp()
    rtbioscmp.main()
