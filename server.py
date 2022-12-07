import time
import logging
import my_logging
import cv2
import os
from flask import Flask, request, jsonify, send_from_directory, render_template,send_file
from models.BiSeNetOFF.tools.demo import inferenceByBiSeNet
from  measure.外接矩形 import  measure_im

logger = logging.getLogger("server")  # 生成logger实例
my_logging.load_my_logging_cfg(model='')  # 在你程序文件的入口加载自定义logging配置
app = Flask("server")

@app.route("/")
def hello():
    logger.info("访问主界面")
    return render_template('test000.html')\

@app.route("/upload", methods = ['GET','POST'])
def upload():
    img_name = request.form.get('img_name')
    img_data = request.files.get('img')
    logger.info("成功GET图片")
    if not os.path.exists('imgs/origin'):
        os.makedirs('imgs/origin')
    img_path = os.path.join('imgs','origin',img_name)
    img_data.save(img_path)
    if os.path.exists(img_path):
        logger.info("成功接收图片"+str(img_path))
        # inference(img_path)
    else:
        logger.warning("接收图片失败"+str(img_path))
    res = {"code": 200,
           'msg': "服务器已成功接收当前选中的图片！"}
    return jsonify(res)

@app.route("/inference")
def inference():
    logger.info("请求模型分割")
    #模型分割
    img_name = request.args['img_name']
    img_path = os.path.join('imgs', 'origin', img_name)
    start_time_inference=time.time()
    logger.debug("分割开始，调用模型中..."+str(img_path))
    img=inferenceByBiSeNet(img_path)
    img_name = os.path.basename(img_path)
    logger.debug("分割结束")
    end_time_inference=time.time()
    # cv2.imshow("sdf",img)
    # cv2.waitKey()
    time_inference = end_time_inference - start_time_inference
    logger.info("推理时间：%f秒"%time_inference)
    #测距
    logger.debug("测距开始...")
    start_time_measure=time.time()
    measimg, whs, centers = measure_im(img)
    end_time_measure=time.time()
    time_measure = end_time_measure - start_time_measure
    logger.debug("测距结束...")
    logger.info("测距时间：%f秒"%time_measure)
    # cv2.imshow("sdf",measimg)
    # cv2.waitKey()
    if not os.path.exists('imgs/result'):
        os.makedirs('imgs/result')
    img_path = os.path.join('imgs','result',img_name)
    cv2.imwrite(img_path,measimg)
    for i in range (0,5):
        logger.info("目标%d长:%s,宽%s"%(i,whs[i][0],whs[i][1]))
    res = {"code": 200,
           'msg': "成功响应",
           "time_inference":time_inference,
           "time_measure":time_measure,
           "whs":str(whs)}
    return jsonify(res)

@app.route("/download_inference")
def download_inference():
    #客户端如何下载图片：https://blog.csdn.net/qq_34663267/article/details/103404120
    img_name = request.args['img_name']
    img_path = os.path.join('imgs', 'result', img_name)
    return send_file(img_path)
app.run()



