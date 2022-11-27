import cv2
from models.BiSeNetOFF.tools.demo import inferenceByBiSeNet

img=inferenceByBiSeNet("models/BiSeNetOFF/1.bmp")
cv2.imshow("sdf",img)
cv2.waitKey()
