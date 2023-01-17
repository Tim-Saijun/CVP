# #加权线性融合
# import cv2
# import numpy as np
# alpha = 0.5 #0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9
# filename = str(alpha)+r'.png'
# img1 = cv2.imread('1.bmp')
# img2 = cv2.imread('return.png')
# img1_resize = cv2.resize(img1, (400 , 400))
# img2_resize = cv2.resize(img2, (400 , 400))
# img_merge = alpha * img1_resize + (1 - alpha) * img2_resize
# cv2.imshow(filename, img_merge/255.0)
# cv2.waitKey(0)
# cv2.imwrite(filename, img_merge)

"""
import cv2
import numpy as np
img1 = cv2.imread('1.bmp')
img2 = cv2.imread('return.png')
img1_resize = cv2.resize(img1, (400 , 400))
img2_resize = cv2.resize(img2, (400 , 400))
#利用seamlessClone函数进行图像融合
img_seamless = cv2.seamlessClone(img2_resize, img1_resize, img2_resize, (200, 200), cv2.NORMAL_CLONE)
cv2.imshow('seamless', img_seamless/255.0)
cv2.waitKey(0)
"""

import cv2
import numpy as np
img1 = cv2.imread('1.bmp')
img2 = cv2.imread('return.png')
img1_resize = cv2.resize(img1, (400 , 400))
img2_resize = cv2.resize(img2, (400 , 400))

#去除img2的背景,保存为mask
img2_gray = cv2.cvtColor(img2_resize, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
cv2.imshow('mask', mask/255.0)
cv2.imshow('mask_inv', mask_inv/255.0)
cv2.waitKey(0)


