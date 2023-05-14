# %load test.py
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from operator import itemgetter
import numpy as np
import cv2
import math
import requests

def script_method(fn, _rcb=None):
    return fn


def script(obj, optimize=True, _frames_up=0, _rcb=None):
    return obj


import torch.jit
script_method1 = torch.jit.script_method
script1 = torch.jit.script
torch.jit.script_method = script_method
torch.jit.script = script



# url = 'http://119.3.189.44/online/photo/pic1.png'
# response = requests.get(url, stream=True)

# # 检查响应状态码是否为200
# if response.status_code == 200:
#     # 打开文件以写入二进制数据
#     with open('image.png', 'wb') as f:
#         # 写入数据
#         for chunk in response.iter_content(1024):
#             f.write(chunk)

#     # 返回图像本地存储路径
#     local_path = 'image.png'
# else:
#     print('未能下载图片')


# scripts for crop images
def crop_image(img, position):
    def distance(x1,y1,x2,y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    position = position.tolist()
    for i in range(4):
        for j in range(i+1, 4):
            if(position[i][0] > position[j][0]):
                tmp = position[j]
                position[j] = position[i]
                position[i] = tmp
    if position[0][1] > position[1][1]:
        tmp = position[0]
        position[0] = position[1]
        position[1] = tmp

    if position[2][1] > position[3][1]:
        tmp = position[2]
        position[2] = position[3]
        position[3] = tmp

    x1, y1 = position[0][0], position[0][1]
    x2, y2 = position[2][0], position[2][1]
    x3, y3 = position[3][0], position[3][1]
    x4, y4 = position[1][0], position[1][1]

    corners = np.zeros((4,2), np.float32)
    corners[0] = [x1, y1]
    corners[1] = [x2, y2]
    corners[2] = [x4, y4]
    corners[3] = [x3, y3]

    img_width = distance((x1+x4)/2, (y1+y4)/2, (x2+x3)/2, (y2+y3)/2)
    img_height = distance((x1+x2)/2, (y1+y2)/2, (x4+x3)/2, (y4+y3)/2)

    corners_trans = np.zeros((4,2), np.float32)
    corners_trans[0] = [0, 0]
    corners_trans[1] = [img_width - 1, 0]
    corners_trans[2] = [0, img_height - 1]
    corners_trans[3] = [img_width - 1, img_height - 1]

    transform = cv2.getPerspectiveTransform(corners, corners_trans)
    dst = cv2.warpPerspective(img, transform, (int(img_width), int(img_height)))
    return dst

def order_point(coor):
    arr = np.array(coor).reshape([4, 2])
    sum_ = np.sum(arr, 0)
    centroid = sum_ / arr.shape[0]
    theta = np.arctan2(arr[:, 1] - centroid[1], arr[:, 0] - centroid[0])
    sort_points = arr[np.argsort(theta)]
    sort_points = sort_points.reshape([4, -1])
    if sort_points[0][0] > centroid[0]:
        sort_points = np.concatenate([sort_points[3:], sort_points[:3]])
    sort_points = sort_points.reshape([4, 2]).astype('float32')
    return sort_points

#自动确定浮动值
def auto_float(img):
    height=img.shape[0]
    rate=15/1080
    float_rate=0.75*rate*height
    return float_rate

#判断内容是否为值
def jugde_value(text):
    n=0
    #text 刚开始为列表
    text=text[0];
    for i in text:
        if i.isdigit():
            n = n + 1
    if n>=2:
        return True;
    else:
        return False;

def ocr_full(img_path):
    ocr_detection = pipeline(Tasks.ocr_detection, model='damo/cv_resnet18_ocr-detection-line-level_damo')
    ocr_recognition = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-document_damo')

    #添加图片地址
    #img_path = 'pic1.png'
    image_full = cv2.imread(img_path)
    det_result = ocr_detection(image_full)
    det_result = det_result['polygons']
    #print(det_result)
    highest_limit = 0 #需要扫描的区域的上限
    key_set=[]
    value_set=[]

    for i in range(det_result.shape[0]):
        pts = order_point(det_result[i])
        image_crop = crop_image(image_full, pts)
        #print(image_crop)
        result = ocr_recognition(image_crop)
        temp=det_result[i].tolist() #将numpy数组转为lsit
        temp.append(result['text'][0])
        #print(temp)
        if result['text'][0]=='2D MeasurementsAUA' or result['text'][0]=='2D Measurements':
            highest_limit=((temp[5]+temp[7])/2)
        if(jugde_value(result['text'])):
            value_set.append(temp)
        else:
            key_set.append(temp)
        # print("box: %s" % ','.join([str(e) for e in list(pts.reshape(-1))]))
        # print("text: %s" % result['text'])
    key_set = [i for i in key_set if i[5] > (highest_limit+10)] #筛选出有效元素
    value_set = [i for i in value_set if i[5] > (highest_limit+10)]

    key_set=sorted(key_set,key=itemgetter(1)) #按照纵坐标进行升序排序，从图片上方到图片下方
    value_set=sorted(value_set,key=itemgetter(1))


    float_rate = 15 #同一行的垂直误差（像素）
    float_rate=auto_float(image_full)

    key_map=[]
    temp=[]
    key_line=key_set[0][1]; #水平线
    #print(key_line)
    for i in key_set:
        if abs(key_line-i[1])<float_rate:
            temp.append(i)
        else:
            key_line = i[1] #更新水平线
            if len(temp)!=0:
                key_map.append(sorted(temp,key=itemgetter(0)))
            temp=[]
            temp.append(i)
    key_map.append(sorted(temp,key=itemgetter(0)))

    #print(key_set)
    value_map=[]
    temp=[]

    value_line=value_set[0][1]; #水平线
    #print(value_line)
    for i in value_set:
        if abs(value_line-i[1])<float_rate:
            temp.append(i)
        else:
            value_line = i[1] #更新水平线
            if len(temp)!=0:
                value_map.append(sorted(temp,key=itemgetter(0)))
            temp=[]
            temp.append(i)
    value_map.append(sorted(temp,key=itemgetter(0)))


    # print(len(key_map))
    # print(len(value_map))

    # print(key_map)
    # print(value_map)


    dict = {}
    for i in range(6):
        if len(key_map[i])>0 and len(value_map[1])>0 :
            #key=key_map[i][0][8]
            key='M'+str(i+1)
            dict[key]=value_map[i][0][8]
    # for i in range(2):
    #     if len(key_map[i])>0 and len(value_map[1])>0 :
    #         dict[key_map[i+7][0][8]]=value_map[i+6][0][8]
    #     if len(key_map[i])>1 and len(value_map[1])>1 :
    #         dict[key_map[i+7][1][8]]=value_map[i+6][1][8]
    # if len(key_map[9])>0 and len(value_map[8])>0 :
    #     dict[key_map[9][0][8]]=value_map[8][0][8]
    for i in range(3):
        key='C'+str(i+1)
        dict[key]=value_map[i+6][0][8]
    for i in range(2):
        key='C'+str(i+4)
        dict[key]=value_map[i+6][1][8]

    for key,value in dict.items():
        print(key+": "+str(value))
    return dict
    

