import cv2
import numpy as np

# 滑动条的回调函数，获取滑动条位置处的值
"""
拖拽HSV的六个进度条确定图中某种颜色的HSV值，pycharm的HSV颜色提取不准确
labels_info = [
    {"hasInstances": False, "category": "human", "catid": 0, "name": "person", "ignoreInEval": False, "id": 0, "color": [0,0,0], "trainId": 0},
    {"hasInstances": True, "category": "human", "catid": 1, "name": "rider", "ignoreInEval": False, "id": 1, "color": [255, 0, 0], "trainId": 1},
    {"hasInstances": True, "category": "vehicle", "catid": 2, "name": "car", "ignoreInEval": False, "id": 2, "color": [0, 0, 142], "trainId": 2},
    {"hasInstances": True, "category": "vehicle", "catid": 3, "name": "train", "ignoreInEval": False, "id": 3, "color": [0, 80, 100], "trainId": 3},
    {"hasInstances": True, "category": "vehicle", "catid": 4, "name": "motorcycle", "ignoreInEval": False, "id": 4, "color": [0, 0, 230], "trainId": 4},
    {"hasInstances": True, "category": "vehicle", "catid": 5, "name": "bicycle", "ignoreInEval": False, "id": 5, "color": [119, 11, 32], "trainId": 5}
]
"""
def empty(a):
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    return h_min, h_max, s_min, s_max, v_min, v_max


path = r'imgs/out/bb{1D4CEA06-0483-4F90-AF69-94D611385A71}.bmp'
# 创建一个窗口，放置6个滑动条
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 19, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 110, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 240, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 153, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 调用回调函数，获取滑动条的值
    h_min, h_max, s_min, s_max, v_min, v_max = empty(0)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    # 获得指定颜色范围内的掩码
    mask = cv2.inRange(imgHSV, lower, upper)
    # 对原图图像进行按位与的操作，掩码区域保留
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", imgResult)

    cv2.waitKey(1)
