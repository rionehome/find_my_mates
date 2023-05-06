#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import cv2
import matplotlib
import rospy
import torch
from std_msgs.msg import String

from carry_my_luggage.msg import Detect

WIDTH = 640
HEIGHT = 480


class ImageSystem:
    def __init__(self):
        matplotlib.use("Agg")  # fix weird Gtk 2 error
        rospy.init_node("image_system")

        # person detect
        self.is_person_detect_on = False
        self.person_detect_model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        self.person_detect_switch_sub = rospy.Subscriber(
            "/image_system/person_detect/switch", String, self.person_detect_switch_callback
        )
        self.person_detect_result_pub = rospy.Publisher("/image_system/person_detect/result", Detect, queue_size=1)
        
        rospy.Subscriber("/image_system/person_detect/result", Detect, self.image_person_detect_result_callback)
        self.person_count = 0
        self.person_direction = []
        self.person_distance = []
        self.person_xmid = []
        self.person_ymid = []
        self.person_width = []
        self.person_height = []


    def person_detect_switch_callback(self, msg):
        if msg.data == "on" and self.is_person_detect_on == False:
            rospy.loginfo("image_system: Turning on person_detect")

            self.is_person_detect_on = True
            self.cap = cv2.VideoCapture(0)
        elif msg.data == "off" and self.is_person_detect_on == True:
            rospy.loginfo("image_system: Turning off person_detect")

            self.is_person_detect_on = False
            self.cap.release()
            cv2.destroyAllWindows()

        if self.is_person_detect_on:
            self.person_detect()

    def person_detect(self):
        ret, img = self.cap.read()  # 画像の大きさを取得するために1度だけ最初によびだす。

        p_count = 0  # 人が写っているかどうかを判定するための変数
        p_direction = []
        p_distance = []
        p_xmid = []
        p_ymid = []
        p_width = []
        p_height = []

        ret, img = self.cap.read()
        result = self.person_detect_model(img)

        # 推論結果を取得
        obj = result.pandas().xyxy[0]

        # 人が写っているかを調べる
        for i in range(len(obj)):
            if obj.name[i] == "person":
                p_count += 1

                xmin = obj.xmin[i]
                ymin = obj.ymin[i]
                xmax = obj.xmax[i]
                ymax = obj.ymax[i]

                width = xmax - xmin  # 矩形の幅
                height = ymax - ymin  # 矩形の高さ
                xmid = (xmax + xmin) / 2  # 矩形の中心のx座標
                ymid = (ymax + ymin) / 2  # 矩形の中心のy座標

                p_width.append(int(width))
                p_height.append(int(height))
                p_xmid.append(int(xmid))
                p_ymid.append(int(ymid))

                if xmid >= 0 and xmid <= WIDTH * (1 / 3):
                    p_direction.append("left")
                elif xmid < WIDTH and xmid <= WIDTH * (2 / 3):
                    p_direction.append("middle")
                elif xmid > WIDTH * (2 / 3) and xmid < WIDTH:
                    p_direction.append("right")

                if height >= 380:
                    p_distance.append("close")
                elif height > 360 and height < 380:
                    p_distance.append("middle")
                elif height <= 360:
                    p_distance.append("far")

        d = Detect()
        d.count = p_count
        d.direction = p_direction
        d.distance = p_distance
        d.xmid = p_xmid
        d.ymid = p_ymid
        d.width = p_width
        d.height = p_height
        self.person_detect_result_pub.publish(d)

        # バウンディングボックスを描画
        result.render()
        cv2.imshow("result", result.ims[0])
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return


if __name__ == "__main__":
    try:
        imageSystem = ImageSystem()
        rospy.spin()

    except KeyboardInterrupt:
        pass