import cv2
import numpy as np
from 提取单色 import generate_mask_array

def rectangle(img):#img是二值图像
    contours, hierarchy = cv2.findContours(img,
                                                   cv2.RETR_LIST,
                                                   cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大的轮廓,简单的聚类
    area = []
    for k in range(len(contours)):
        area.append(cv2.contourArea(contours[k]))
    max_idx = np.argmax(np.array(area))
    # x,y,w,h = cv2.boundingRect(contours[0])
    # brcnt = np.array([[[x,y]], [[x+w,y]], [[x+w,y+h]], [[x,y+h]]] )
    # cv2.drawContours(0,[brcnt],-1,(255,255,255),2)
    rect = cv2.minAreaRect(contours[max_idx])
    #rect [(中心x,中心y),(长,宽),偏转角度]
    # print("返回值rect:\n",rect)
    points = cv2.boxPoints(rect)
    print("\n转换后的points：\n",points)
    points=np.int0(points)#取整

    # image = img
    # image = cv2.drawContours(img,[points],0,(255,255,255),2)
    # # image = cv2.putText(img,"w:%f h:%f"%(rect[1][0],rect[1][1]),rect[0],cv2.FONT_HERSHEY_SIMPLEX,12,(255,255,255),3)
    # image = cv2.putText(img,"sd",rect[0],cv2.FONT_HERSHEY_SIMPLEX,4,127,3)
    # cv2.imshow("result",image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return points,rect

if __name__ == '__main__':
    o = cv2.imread(r'imgs/1/bb{F798F706-F882-4E3F-8709-FF265AF63BB8}.bmp')
    masks=generate_mask_array(o)
    points = []
    centers=[]
    whs = []
    for i in range (0,5):
        img = masks[i]
        _, binaryzation = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        tpoints,rect=rectangle(binaryzation)
        points.append(tpoints)
        centers.append(rect[0])
        whs.append(rect[1])

    image = cv2.drawContours(o, points, -1, (255, 255, 255),1)
    for i in range (0,5):
         image = cv2.putText(image,"w:%d h:%d"%(whs[i][0],whs[i][1]), (int(centers[i][0]),int(centers[i][1])) ,
                             cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
    cv2.imshow("result",image)
    cv2.waitKey()
    cv2.destroyAllWindows()
