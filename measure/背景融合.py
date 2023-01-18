import os
import cv2
import numpy as np
def measure_merge(imgres_path,imgori_path):
    imgres = cv2.imread(imgres_path)
    #去除背景中的蓝色
    lower_blue = np.array([98, 179, 253])
    upper_blue = np.array([100, 181, 255])
    hsv = cv2.cvtColor(imgres, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #对mask取反
    mask = cv2.bitwise_not(mask)
    #使img支持mask的融合
    imgres = cv2.cvtColor(imgres, cv2.COLOR_BGR2BGRA)
    #mask部分置为透明，其余部分不变
    imgres[mask == 0] = (0, 0, 0, 0)
    # #保存透明背景图像
    # cv2.imwrite('touming.png', imgres)
    img2 = cv2.imread(imgori_path)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2BGRA)
    #将img与img2线性融合
    img_merge = cv2.addWeighted(imgres, 1, img2, 0.5, 0)
    return img_merge
    # #保存融合图像
    # cv2.imwrite('merge.png', img_merge)


if __name__ == '__main__':
    img_name = '1.jpg'
    img = measure_merge(img_name)
    cv2.imshow('merge', img/255.0)
    cv2.waitKey(0)

