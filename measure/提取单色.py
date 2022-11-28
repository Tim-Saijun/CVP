import cv2
import numpy as np
"""
左心房 红 [1,159,176]
右心房 紫 [126,105,109]
左心室 绿 [63,78,182]
右心室 深蓝 [108,168,178]
降主动脉 黄 [26,139,239]
"""
def generate_mask_array(img):
    #转到HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    HSV_TABLE=np.array([[1,159,176],[126,105,109], [63,78,182],[108,168,178],[26,139,239]])
    maskarray=[]
    for i in range (0,5):
        #设置阈值
        l_blue = HSV_TABLE[i]
        h_blue = HSV_TABLE[i]
        #构建掩模
        mask = cv2.inRange(hsv, l_blue, h_blue)
        maskarray.append(mask)
        #进行位运算
        # res = cv2.bitwise_and(img, img, mask = mask)#恢复原来的色彩
    return maskarray

if __name__ == '__main__':
    img = cv2.imread(r'../imgs/out/bb{1D4CEA06-0483-4F90-AF69-94D611385A71}.bmp')
    maskarray=generate_mask_array(img)
    print(maskarray)
    cv2.imshow("img", img)
    for  i in range(0,5):
        cv2.imshow(str(i), maskarray[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
