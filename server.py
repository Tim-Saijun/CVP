import time
from logging import *
import cv2

from models.BiSeNetOFF.tools.demo import inferenceByBiSeNet
from  measure.外接矩形 import  measure_im

#模型分割
start_time_inference=time.time()
img=inferenceByBiSeNet("models/BiSeNetOFF/1.bmp")
end_time_inference=time.time()
cv2.imshow("sdf",img)
cv2.waitKey()
time_inference = end_time_inference - start_time_inference
print("推理时间：%f秒"%time_inference)

#测距
start_time_measure=time.time()
measimg, whs, centers = measure_im(img)
end_time_measure=time.time()
time_measure = end_time_measure - start_time_measure
print("测距时间：%f秒"%time_measure)
cv2.imshow("sdf",measimg)
cv2.waitKey()
for i in range (0,5):
    print("目标%d长:%s,宽%s"%(i,whs[i][0],whs[i][1]))
