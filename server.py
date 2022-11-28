import time
from logging import *
import cv2

from models.BiSeNetOFF.tools.demo import inferenceByBiSeNet

start_time_inference=time.time()
img=inferenceByBiSeNet("models/BiSeNetOFF/1.bmp")
end_time_inference=time.time()
cv2.imshow("sdf",img)
cv2.waitKey()
time_inference = end_time_inference - start_time_inference
print("推理时间：%f秒"%time_inference)

