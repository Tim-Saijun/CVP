import cv2 as cv
import numpy as np
import copy

def original(i, j,  ksize, img):
    """
    :param i:  横坐标
    :param j: 纵坐标
    :param ksize:滤波器尺寸
    :param img:图像数据
    :return:返回ksize*ksize个像素数据
    """
    # 找到矩阵坐标
    x1 = y1 = -ksize // 2
    x2 = y2 = ksize + x1
    xingzhaun=(ksize*ksize,3)
    temp = np.zeros(xingzhaun,dtype=np.int32)
    count=0
    # 处理图像
    for m in range(x1, x2):
        for n in range(y1, y2):
            if i + m < 0 or i + m > img.shape[0] - 1 or j + n < 0 or j + n > img.shape[1] - 1:
                temp[count] = img[i, j]
            else:
                temp[count] = img[i + m, j + n]
            count += 1
    return temp

# 自定义滤波器
def max_min_functin(ksize, img):
    img0 = copy.copy(img)
    for i in range(0, img.shape[0]):
        for j in range(2, img.shape[1]):
                temp = original(i, j, ksize, img0)
                temp=[tuple(x) for x in temp.tolist()]
                b={}
                for k in range(0, len(temp)):
                    if temp[k] in b:
                        b[temp[k]] += 1
                    else:
                        b[temp[k]] = 0
                img[i, j] =max(temp)
    return img

#读取数据，进行滤波，如果效果不好，则二次滤波？
#超参数ksize2-5？
img = cv.imread('data/out/bb{F798F706-F882-4E3F-8709-FF265AF63BB8}.bmp')
min_img = max_min_functin(5, copy.copy(img))
result=max_min_functin(5,copy.copy(min_img))
cv.imwrite("bb{F798F706-F882-4E3F-8709-FF265AF63BB8}.bmp",result)
cv.waitKey(0)
