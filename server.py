import time
import logging
import my_logging
import cv2
from flask import Flask, request, jsonify, send_from_directory, render_template,send_file
from models.BiSeNetOFF.tools.demo import inferenceByBiSeNet
from  measure.外接矩形 import  measure_im

logger = logging.getLogger("server")  # 生成logger实例
my_logging.load_my_logging_cfg(model='')  # 在你程序文件的入口加载自定义logging配置
app = Flask("server")

@app.route("/")
def hello():
    logger.info("访问主界面")
    return render_template('test000.html')

@app.route("/inference")
def inference():
    logger.info("请求模型分割")
    #模型分割
    start_time_inference=time.time()
    logger.debug("分割开始，调用模型中...")
    img=inferenceByBiSeNet("models/BiSeNetOFF/1.bmp")
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
    cv2.imwrite("return.png",measimg)
    for i in range (0,5):
        logger.info("目标%d长:%s,宽%s"%(i,whs[i][0],whs[i][1]))
    res = {"code": 200,
           'msg': "成功响应",
           "time_inference":time_inference,
           "time_measure":time_measure,
           "data":str(whs)}
    return jsonify(res)

@app.route("/download_inference")
def download_inference():
    #客户端如何下载图片：https://blog.csdn.net/lzanze/article/details/99706611
    return send_file("return.png")
app.run()


#TODO:flask接收客户端文件https://www.cnblogs.com/niulang/p/14620913.html
