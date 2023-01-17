import cv2
import numpy as np
img = cv2.imread('return.png')
#去除背景中的蓝色
lower_blue = np.array([98, 179, 253])
upper_blue = np.array([100, 181, 255])
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_blue, upper_blue)
#对mask取反
mask = cv2.bitwise_not(mask)
#使img支持mask的融合
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
#mask部分置为透明，其余部分不变
img[mask == 0] = (0, 0, 0, 0)
#保存透明背景图像
cv2.imwrite('touming.png', img)

img2 = cv2.imread('1.bmp')
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2BGRA)
#将img与img2线性融合
img_merge = cv2.addWeighted(img, 1, img2, 0.5, 0)
#保存融合图像
cv2.imwrite('merge.png', img_merge)
cv2.imshow('merge', img_merge/255.0)


cv2.waitKey(0)



#
# res = cv2.bitwise_and(img, img, mask=mask)
# cv2.imshow('img', img)
# cv2.imshow('mask', mask)
# cv2.imshow('res', res)
# cv2.waitKey(0)