import cv2
import numpy as np
import os
import time
import logging
import my_logging
from measure.提取单色 import generate_mask_array

logger = logging.getLogger(__name__)  # 生成logger实例
my_logging.load_my_logging_cfg("DO_NOT_DEBUG")  # 在你程序文件的入口加载自定义logging配置
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
    logger.debug("返回值rect:%s\n"%str(rect))
    points = cv2.boxPoints(rect)
    logger.debug("转换后的points：%s\n"%str(points))
    points=np.int0(points)#取整

    return points,rect
def outfit(o,name):
    masks = generate_mask_array(o)
    points = []
    centers = []
    whs = []
    for i in range(0, 5):
        img = masks[i]
        _, binaryzation = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        # 开运算：先腐蚀，再膨胀,闭运算反之
        kernel = np.ones((15, 15), np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
        tpoints, rect = rectangle(opening)
        points.append(tpoints)
        centers.append(rect[0])
        whs.append(rect[1])

    image = cv2.drawContours(o, points, -1, (255, 255, 255), 1)
    for i in range(0, 5):
        image = cv2.putText(image, "w:%d h:%d" % (whs[i][0], whs[i][1]), (int(centers[i][0]), int(centers[i][1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    print(name)
    cv2.imwrite(name,image)

def measure_im(img):
    #直接从内存中传过来图片，也返回图片
    # 直接传入模型分割的图片，返回测距的图片与距离信息
    #     o = cv2.imread(img)
        o = img
        try:
            masks = generate_mask_array(o)
            points = []
            centers = []
            whs = []
            for i in range(0, 5):
                img = masks[i]
                _, binaryzation = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
                # 开运算：先腐蚀，再膨胀,闭运算反之
                # kernel = np.ones((15, 15), np.uint8)
                # opening = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel,iterations=3)
                tpoints, rect = rectangle(binaryzation)
                points.append(tpoints)
                centers.append(rect[0])
                whs.append(rect[1])

            image = cv2.drawContours(o, points, -1, (255, 165, 0), 1)
            for i in range(0, 5):
                image = cv2.putText(image, "w:%d h:%d" % (whs[i][0], whs[i][1]),
                                    (int(centers[i][0]), int(centers[i][1])),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            return image, whs, centers
        except:
            print("错误,图片中目标缺失")
            #TODO:目标缺失时仍能测距



if __name__ == '__main__':
    #导入一个模型分割的结果图片目录，批量输出测距之后的图片
    imgs=os.listdir(r'/imgs/out')
    count=0
    for img in imgs:
        name=img
        img=os.path.join("../imgs/out/", img)
        o = cv2.imread(img)
        # try:
        #     outfit(name,o)
        # except IndexError:
        #     count+=1
        # except:
        #     continue
        # print("不足五类的数量%d",count)
        try:
            masks=generate_mask_array(o)
            points = []
            centers=[]
            whs = []
            for i in range (0,5):
                img = masks[i]
                _, binaryzation = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
                # 开运算：先腐蚀，再膨胀,闭运算反之
                # kernel = np.ones((15, 15), np.uint8)
                # opening = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel,iterations=3)
                tpoints,rect=rectangle(binaryzation)
                points.append(tpoints)
                centers.append(rect[0])
                whs.append(rect[1])

            image = cv2.drawContours(o, points, -1, (255, 255, 255),1)
            for i in range (0,5):
                 image = cv2.putText(image,"w:%d h:%d"%(whs[i][0],whs[i][1]), (int(centers[i][0]),int(centers[i][1])) ,
                                     cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
            print(name)
            cv2.imwrite(name, image)
        except:
            count+=1
            print("错误%d",count)
    # cv2.imshow("result",image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
