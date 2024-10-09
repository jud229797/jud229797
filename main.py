#上云相关
import cloud
import time
import serial

# import av
import cv2
import numpy as np
import subprocess
from cvs import *

# aidlux相关
import aidlite_gpu
import utils2
import utils3
import time
from collections import defaultdict

#多线程相关
import queue
import threading

#自动化相关
import fan
from _queue import Empty
import try1
import paho.mqtt.client as mqtt
import json

#病虫害和生长周期图片上传
import paramiko

#决策
import datetime
import decide__3

#邮件相关
import QQyouxiang__8

recipient_email = "2706736703@qq.com"

# MQTT 代理服务器地址和端口
broker_address = "39.108.76.174"
port = 11883
client_id = 'ccc'
USERNAME = 'ccc'
password = 'ccc'
topic_publish = "v1/devices/me/rpc/request/+"


class TemperatureData:
    def __init__(self, air_temp):
        self.air_temp_data = air_temp


class Fruit:
    def __init__(self, sort):
        if sort == "red_f":
            self.air_temp_min = -1000
            self.air_temp_max = -1000
            self.air_hum_max = 1000
            self.air_hum_min = 1000
            self.soild_hum_max = -1000
            self.soild_hum_min = -1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 10000
            self.light_min= 10000
            self.P_max = 100
            self.P_min = 100
            self.N_max = 100
            self.N_min= 100
            self.K_max = 100
            self.K_min = 100
            self.EC_max = 100
            self.EC_min = 100
            self.PH_min = -1000
            self.PH_max = -1000
        elif sort == "write_f" :
            self.air_temp_min = 1000
            self.air_temp_max = 1000
            self.air_hum_max = -1000
            self.air_hum_min = -1000
            self.soild_hum_max = 1000
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 10000
            self.light_min= 10000
            self.P_max = 100
            self.P_min = 100
            self.N_max = 100
            self.N_min= 100
            self.K_max = 100
            self.K_min = 100
            self.EC_max = 100
            self.EC_min = 100
            self.PH_min = 1000
            self.PH_max = 1000
        elif sort == "nothing" :
            self.air_temp_min = 100
            self.air_temp_max = -1000
            self.air_hum_max = -1000
            self.air_hum_min = -1000
            self.soild_hum_max = 100
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = -10000
            self.light_min= -10000
            self.P_max = 100
            self.P_min = 100
            self.N_max = 100
            self.N_min= 100
            self.K_max = 100
            self.K_min = 100
            self.EC_max = 100
            self.EC_min = 100
            self.PH_min = 1000
            self.PH_max = 100
        elif sort == "flower" :
            self.air_temp_min = 100
            self.air_temp_max = -1000
            self.air_hum_max = -1000
            self.air_hum_min = -1000
            self.soild_hum_max = 100
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 10000
            self.light_min= 10000
            self.P_max = 100
            self.P_min = 100
            self.N_max = 100
            self.N_min= 100
            self.K_max = 100
            self.K_min = 100
            self.EC_max = 100
            self.EC_min = 100
            self.PH_min = 1000
            self.PH_max = 100
        elif sort == "bud" :
            self.air_temp_min = 100
            self.air_temp_max = -1000
            self.air_hum_max = 100
            self.air_hum_min = -1000
            self.soild_hum_max = 100
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = -1000
            self.light_min= -1000
            self.P_max = 100
            self.P_min = 100
            self.N_max = 100
            self.N_min= 100
            self.K_max = 100
            self.K_min = 100
            self.EC_max = 100
            self.EC_min = 100
            self.PH_min = 1000
            self.PH_max = 100

class RegioncircleData:
    def __init__(self, region, circle_data):
        self.region = region
        self.circle_data = circle_data
    def process(self, client):
        circle_map = {
            "bud": 1,
            "flower": 2,
            "write_f": 3,
            "red_f": 4,
            "nothing": 0
        }
        # cloud.trans_circle(client, f"circle_{self.region}", circle_map.get(self.circle_data, 0))
        cloud.trans_circle(client, f"circle_{self.region}", circle_map.get(self.circle_data, 0))
        
class RegionillData:
    def __init__(self, region, ill_data):
        self.region = region
        self.ill_data = ill_data
    def process(self, client):
        ill_map = {
            "angular_leafspot": 1,
            "anthracnose_fruit_rot": 2,
            "gray_mold": 3,
            "powdery_mildew_fruit": 4,
            "nothing": 0
        }
        cloud.trans_ill(client, f"ill_{self.region}", ill_map.get(self.ill_data, 0))

class EnvironmentalData :
    def __init__(self, region, windrint_data, air_hum_data, air_temp_data, lux_data,  soild_temp_data, soild_hum_data, ph_data, EC_data ,N_data, P_data, K_data,winddirection_data):
        self.region = region   #区域 ##1为左上角，2为右上角，3为左下角，4为右下角
        self.windrint_data = windrint_data #风速
        self.air_hum_data = air_hum_data    # 湿度
        self.air_temp_data = air_temp_data  # 温度
        self.lux_data = lux_data # 光照强度
        self.soild_temp_data = soild_temp_data  # 土壤温度
        self.soild_hum_data = soild_hum_data  # 土壤湿度
        self.ph_data = ph_data     # pH值
        self.N_data = N_data   # 氮含量（假设）
        self.P_data = P_data   # 磷含量（假设）
        self.K_data = K_data # 钾含量（假设）
        self.EC_data = EC_data # 电导率（假设）
        self.winddirection_data = winddirection_data #风向
    @staticmethod
    def uart(s):
        numbers = list(map(float, s.split(',')))
        if len(numbers) < 13:  # 检查是否有足够的数据
            raise ValueError("Received data does not contain enough values")
        return EnvironmentalData(*numbers)

    def process(self, client):
        # 根据 region 确定传输的标签
        region_tag = {
            1: "top_left",
            2: "top_right",
            3: "bottom_left",
            4: "bottom_right",
        }
        
        # 传输数据
        # 传输环境温度和湿度
        cloud.trans_data(client, f"{region_tag[self.region]}", "env_temp_data", self.air_temp_data, "env_hum_data", self.air_hum_data)
        cloud.time.sleep(0.1)
        
        # 传输土壤湿度和温度
        cloud.trans_data(client, f"{region_tag[self.region]}", "soild_hum_data", self.soild_hum_data, "soild_temp_data", self.soild_temp_data)
        time.sleep(0.1)
        
        # 传输PH值和随机EC值
        cloud.trans_data(client, f"{region_tag[self.region]}", "PH_data", self.ph_data, "EC_data", random.uniform(0.4, 1))
        time.sleep(0.1)
        
        # 传输随机N值和P值
        N_value = random.randint(156, 158)
        P_value = random.randint(88, 90)
        cloud.trans_data(client, f"{region_tag[self.region]}", "N_data", N_value, "P_data", P_value)
        time.sleep(0.1)
        
        # 传输光照强度和随机K值
        K_value = random.randint(106, 108)
        cloud.trans_data(client, f"{region_tag[self.region]}", "lux_data", self.lux_data, "K_data", K_value)
        time.sleep(0.1)
        
        # 传输风向和风速
        cloud.trans_data(client, f"{region_tag[self.region]}", "winddirection_data", self.winddirection_data, "windrint_data", self.windrint_data)
        time.sleep(0.1)

classill_data_queue_topleft = queue.Queue()
classill_data_queue_topright = queue.Queue()
classill_data_queue_bottomleft = queue.Queue()
classill_data_queue_bottomright = queue.Queue()
class_data_queue_topleft = queue.Queue()
class_data_queue_topright = queue.Queue()
class_data_queue_bottomleft = queue.Queue()
class_data_queue_bottomright = queue.Queue()
data_queue_topleft = queue.Queue()
data_queue_topright = queue.Queue()
data_queue_bottomleft = queue.Queue()
data_queue_bottomright = queue.Queue()
deal_with_queue = queue.Queue()
data_ready_event = threading.Event()

def push():
   ##生长周期有关参数
    # AidLite初始化：调用AidLite进行AI模型的加载与推理，需导入aidlite
    aidlite_circle = aidlite_gpu.aidlite()
    aidlite_ill = aidlite_gpu.aidlite()
    # Aidlite模型路径
    model_path_circle = '8-7 90per circle.tflite'
    model_path_ill = '8-7 80per ill.tflite'
    # 定义输入输出shape
    in_shape = [1 * 640 * 640 * 3 * 4]
    out_shape = [1 * 25200 *  9 * 4]
    # 加载Aidlite检测模型：支持tflite, tnn, mnn, ms, nb格式的模型加载
    aidlite_circle.ANNModel(model_path_circle, in_shape, out_shape, 4, 0) 
    aidlite_ill.ANNModel(model_path_ill, in_shape, out_shape, 4, 0) 
    save_path_circle = 'output_circle.jpg'
    save_path_ill = 'output_ill.jpg'
    #跟帧数计算有关
    frame_counter_circle = 0
    frame_counter_ill = 0

    frame_class_counts_circle = {
    'top_left': collections.Counter(),
    'top_right': collections.Counter(),
    'bottom_left': collections.Counter(),
    'bottom_right': collections.Counter()
}
    frame_class_counts_ill = {
    'top_left': collections.Counter(),
    'top_right': collections.Counter(),
    'bottom_left': collections.Counter(),
    'bottom_right': collections.Counter()
}
    # #视频
    cap = cvs.VideoCapture(-1, cam_w=640, cam_h=480, quality=100)
    frame_id = 0

    width = 640
    height = 480
    fps = 5

    # 定义 FFmpeg 命令
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-f', 'rawvideo',  # 原始视频格式
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',  # OpenCV 使用 BGR 格式
        '-s', f'{width}x{height}',  # 帧大小
        '-r', str(fps),  # 帧率
        '-i', '-',  # 输入来自标准输入
        '-c:v', 'libx264',  # 使用 H.264 编码
        '-preset', 'ultrafast',  # 编码速度
        '-tune', 'zerolatency',  # 低延迟
        '-f', 'flv',  # 输出格式
        'rtmp://120.237.20.252:50036/live/test'
    ]

    # # 启动 FFmpeg 子进程+
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    while True:
        frame = cap.read()
        if frame is None:
            continue
        
        cvs.imshow(frame)
        # frame = frame.to_ndarray(format='bgr24')
        frame = cv2.resize(frame, (width, height))
        # 将帧转换为字节流
        frame_bytes = frame.tobytes()
        # 将帧写入 FFmpeg 子进程
        ffmpeg_process.stdin.write(frame.tobytes())

        frame_id += 1
        if not int(frame_id) % 2 == 0:
            img = utils2.preprocess_img(frame, target_shape=(640, 640), div_num=255, means=None, stds=None)
            aidlite_circle.setInput_Float32(img, 640, 640)
            aidlite_circle.invoke()
            pred = aidlite_circle.getOutput_Float32(0)
            pred = pred.reshape(1, 25200, 9)[0]
            pred,cls_counts =  utils2.detect_postprocess(pred, frame,frame.shape, [640, 640, 3], conf_thres = 0.4, iou_thres = 0.3)
            # 绘制推理结果
            for region, counts in cls_counts.items():
                # 输出每个区域最常见的类别
                common_class_in_region = max(counts, key=counts.get) if counts else None
                if common_class_in_region:
                    # print(f"Most common class in {region} of this frame: {common_class_in_region}")
                    for class_name, count in counts.items():
                        frame_class_counts_circle[region][class_name] += count

            frame_counter_circle += 1
            # 每处理20帧，找出并打印过去20帧中每个区域最常出现的类别
            if frame_counter_circle % 20 == 0:
                for region, counts in frame_class_counts_circle.items():
                    most_common_20_frame_class = max(counts, key=counts.get) if counts else None
                    if most_common_20_frame_class:
                        if region == "top_left":
                            class_data_queue_topleft.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "top_right":
                            class_data_queue_topright.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_right":
                            class_data_queue_bottomright.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_left":
                            class_data_queue_bottomleft.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        
                    else :
                        if region == "top_left":
                            class_data_queue_topleft.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}: nothing\n")
                        elif region == "top_right":
                            class_data_queue_topright.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_right":
                            class_data_queue_bottomright.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_left":
                            class_data_queue_bottomleft.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                res_img =  utils2.draw_detect_res(frame , pred)
                cv2.imwrite(save_path_circle, res_img)
                # print(f"Saved and overwritten image to {save_path_circle}")
                frame_counter_circle = 0
                # 重置计数器和区域类别计数
                frame_counter = 0
                for region in frame_class_counts_circle:
                    frame_class_counts_circle[region].clear()

        elif int(frame_id) % 2 == 0:
            img = utils3.preprocess_img(frame, target_shape=(640, 640), div_num=255, means=None, stds=None)
            aidlite_ill.setInput_Float32(img, 640, 640)
            aidlite_ill.invoke()
            pred = aidlite_ill.getOutput_Float32(0)
            pred = pred.reshape(1, 25200, 9)[0]
            pred,cls_counts =  utils3.detect_postprocess(pred,frame, frame.shape, [640, 640, 3], conf_thres = 0.3, iou_thres = 0.3)
            # 绘制推理结果
            for region, counts in cls_counts.items():
                # 输出每个区域最常见的类别
                common_class_in_region = max(counts, key=counts.get) if counts else None
                if common_class_in_region:
                    # print(f"Most common class in {region} of this frame: {common_class_in_region}")
                    for class_name, count in counts.items():
                        frame_class_counts_ill[region][class_name] += count

            frame_counter_ill += 1
            # 每处理20帧，找出并打印过去20帧中每个区域最常出现的类别
            if frame_counter_ill % 20 == 0:
                for region, counts in frame_class_counts_ill.items():
                    most_common_20_frame_class = max(counts, key=counts.get) if counts else None
                    if most_common_20_frame_class:
                        if region == "top_left":
                            classill_data_queue_topleft.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "top_right":
                            location = "B区"
                            classill_data_queue_topright.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_right":
                            location = "C区"
                            classill_data_queue_bottomright.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_left":
                            location = "D区"
                            classill_data_queue_bottomleft.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        
                    else :
                        if region == "top_left":
                            classill_data_queue_topleft.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}: nothing\n")
                        elif region == "top_right":
                            classill_data_queue_topright.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_right":
                            classill_data_queue_bottomright.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_left":
                            classill_data_queue_bottomleft.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                res_img =  utils3.draw_detect_res(frame , pred)
                cv2.imwrite(save_path_ill, res_img)
                # print(f"Saved and overwritten image to {save_path_circle}")
                frame_counter_ill = 0
                # 重置计数器和区域类别计数
                frame_counter = 0
                for region in frame_class_counts_ill:
                    frame_class_counts_ill[region].clear()

        # # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭 FFmpeg 子进程
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()

    # 关闭视频流
    container.close()
    cv2.destroyAllWindows()



def upload_file():
    # 服务器信息
    host = '111.230.53.161'
    port = 22
    username = 'zhu'
    password = 'zxd12345'
    # 本地文件路径和远程文件路径
    local_path_circle = '/home/aidlux/2024.4.27first.connect/output_circle.jpg'
    remote_path_circle = '/home/zhu/picture_circle.jpg'
    local_path_ill = '/home/aidlux/2024.4.27first.connect/output_ill.jpg'
    remote_path_ill = '/home/zhu/picture_ill.jpg'
    local_path_bigdata = '/home/aidlux/2024.4.27first.connect/bigdata.txt'
    remote_path_bigdata = '/home/zhu/bigdata_remote.txt'
    global env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft
    env_data_list = [env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft]
    global ill_data_topleft, ill_data_topright, ill_data_bottomright, ill_data_bottomleft
    ill_data_list = [ill_data_topleft, ill_data_topright, ill_data_bottomright, ill_data_bottomleft]
    global circle_data_topleft,circle_data_topright,circle_data_bottomright,circle_data_bottomleft
    circle_data_list = [circle_data_topleft,circle_data_topright,circle_data_bottomright,circle_data_bottomleft]
    tweather = decide__3.extract_weather_info("明天")
    send_data_storage = [[] for _ in range(4)]

    # 创建SSH对象
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
        
        with paramiko.SFTPClient.from_transport(ssh.get_transport()) as sftp:
            while True:
                # 上传图片文件
                sftp.put(local_path_circle, remote_path_circle)
                print(f"Uploaded {local_path_circle} to {remote_path_circle}")
                sftp.put(local_path_ill, remote_path_ill)
                print(f"Uploaded {local_path_ill} to {remote_path_ill}")

                for i, (env_data, sick_data,cycle_data) in enumerate(zip(env_data_list, ill_data_list,circle_data_list)):
                    # 检查病虫害数据是否存在
                    sick_status = "无病虫害" if sick_data.ill_data =="nothing" else f"有{sick_data.ill_data}"
                    if cycle_data.circle_data=="red_f" :
                        cycle="成熟期"
                    elif cycle_data.circle_data=="white_f" :
                        cycle="白果期" 
                    else :
                        cycle="花期"                    
                    send_info = f"土地{i+1} 生长周期：{cycle}；温度：{env_data.air_temp_data}；湿度：{env_data.air_hum_data}；" \
                                f"土壤温度：{env_data.soild_temp_data}；" \
                                f"土壤湿度：{env_data.soild_hum_data}；土壤pH：{env_data.ph_data}；" \
                                f"土壤N、P、K：{env_data.N_data}、{env_data.P_data}、{env_data.K_data}，" \
                                f"植株{sick_status}，明天天气：{tweather}"
                    send_data_storage[i].append(send_info)
                combined_info = "\n".join("\n".join(info) for info in send_data_storage)
                for i in range(4):
                    send_data_storage[i].clear()
                print(f"\n{combined_info}\n")
                with open(local_path_bigdata, 'w') as file:
                    file.write(combined_info)
                
                # 上传大数据文本文件
                sftp.put(local_path_bigdata, remote_path_bigdata)
                print(f"Uploaded {local_path_bigdata} to {remote_path_bigdata}")
                
                time.sleep(10)  # 等待10秒再次上传
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()

def deal_with(port, baudrate):
    with serial.Serial(port, baudrate=baudrate, timeout=None) as ser:
        try:
            while True:
                line = ser.readline().decode().strip()
                if line:
                    if "sensor" in line:
                        line = line.split(':')[1]
                        data = EnvironmentalData.uart(line)  
                        values = line.split(',')
                        region = float(values[0])
                        if region == 1:
                            data_queue_topleft.put(data)  # 将数据放入队列
                            data_ready_event.set()
                        elif region == 2:
                            data_queue_topright.put(data)  # 将数据放入队列
                            data_ready_event.set()
                        elif region == 3:
                            data_queue_bottomleft.put(data)  # 将数据放入队列
                            data_ready_event.set()
                        elif region == 4:
                            data_queue_bottomright.put(data)  # 将数据放入队列
                            data_ready_event.set()
                    else :
                        pass
        except serial.SerialException as e:
            print("Serial error:", e)




def trans_data_data() :
    global env_data_topleft,env_data_topright,env_data_bottomright,env_data_bottomleft
    while True :
        env_data_topleft = data_queue_topleft.get()
        env_data_topright = data_queue_topright.get()
        env_data_bottomright = data_queue_bottomright.get()
        env_data_bottomleft = data_queue_bottomleft.get()


        while data_queue_topleft.qsize() > 0:
            data_queue_topleft.get()
        while data_queue_topright.qsize() > 0:
            data_queue_topright.get()
        while data_queue_bottomleft.qsize() > 0:
            data_queue_bottomleft.get()
        while data_queue_bottomleft.qsize() > 0:
            data_queue_bottomleft.get()
def trans_circle_data():
    global ill_data_topleft,ill_data_topright,ill_data_bottomright,ill_data_bottomleft
    global circle_data_topleft,circle_data_topright,circle_data_bottomright,circle_data_bottomleft
    while True:
        circle_data_topleft = class_data_queue_topleft.get()
        circle_data_topright = class_data_queue_topright.get()
        circle_data_bottomright = class_data_queue_bottomright.get()
        circle_data_bottomleft = class_data_queue_bottomleft.get()
        ill_data_topleft = classill_data_queue_topleft.get()
        ill_data_topright = classill_data_queue_topright.get()
        ill_data_bottomright = classill_data_queue_bottomright.get()
        ill_data_bottomleft = classill_data_queue_bottomleft.get()
        # while class_data_queue_topleft.qsize() > 0:
        #     class_data_queue_topleft.get()
        # while class_data_queue_topright.qsize() > 0:
        #     class_data_queue_topright.get()
        # while class_data_queue_bottomright.qsize() > 0:
        #     class_data_queue_bottomright.get()
        # while class_data_queue_bottomleft.qsize() > 0:
        #     class_data_queue_bottomleft.get()
        # while classill_data_queue_topleft.qsize() > 0:
        #     classill_data_queue_topleft.get()
        # while classill_data_queue_topright.qsize() > 0:
        #     classill_data_queue_topright.get()
        # while classill_data_queue_bottomright.qsize() > 0:
        #     classill_data_queue_bottomright.get()
        # while classill_data_queue_bottomleft.qsize() > 0:
        #     classill_data_queue_bottomleft.get()

def ill_QQ():
    global ill_data_topleft,ill_data_topright,ill_data_bottomright,ill_data_bottomleft
    # global Ax,Ac,Bx,Bz,Cx,Cz,Dx,Dz#x代表现在，c代表之前
    Ax=1
    Ac=1
    Bx=1
    Bc=1
    Cx=1
    Cc=1
    Dx=1
    Dc=1
    while True:
        a,b,c,d = ill_data_topleft,ill_data_topright,ill_data_bottomright,ill_data_bottomleft
        # print(f"\n{ill_data_topleft.ill_data}55555555\n")
        # print(f"\n{ill_data_topright.ill_data}55555555\n")
        # print(f"\n{ill_data_bottomleft.ill_data}55555555\n")
        # print(f"\n{ill_data_bottomright.ill_data}55555555\n")

        if a.ill_data!= "nothing":
            Ac=Ax
            Ax=0
        elif a.ill_data== "nothing":
            Ac=Ax
            Ax=1
        if b.ill_data!= "nothing":
            Bc=Bx
            Bx=0
        elif b.ill_data== "nothing":
            Bc=Bx
            Bx=1

        if c.ill_data!= "nothing":
            Cc=Cx
            Cx=0
        elif c.ill_data== "nothing":
            Cc=Cx
            Cx=1
        if d.ill_data!= "nothing":
            Dc=Dx
            Dx=0
        elif d.ill_data== "nothing":
            Dc=Dx
            Dx=1
        
        if a.ill_data!= "nothing" and Ac!=Ax:
            location = "A区"
            print("00000000000000000000000000000000000000000000000000000")
            QQyouxiang__8.send_email(recipient_email,a.ill_data,location)
           

        if b.ill_data!= "nothing" and Bc!=Bx:
            location = "B区"
            print("00000000000000000000000000000000000000000000000000000")
            QQyouxiang__8.send_email(recipient_email,b.ill_data,location)
            

        if c.ill_data!= "nothing" and Cc!=Cx:
            location = "C区"
            print("00000000000000000000000000000000000000000000000000000")
            QQyouxiang__8.send_email(recipient_email,c.ill_data,location)
            

        if d.ill_data!= "nothing" and Dc!=Dx:
            location = "D区"
            print("00000000000000000000000000000000000000000000000000000")
            QQyouxiang__8.send_email(recipient_email,d.ill_data,location)
        

def class_cloud(client):
    global circle_data_topleft,circle_data_topright,circle_data_bottomright,circle_data_bottomleft
    global ill_data_topleft,ill_data_topright,ill_data_bottomleft,ill_data_bottomright
    while True:
        circle_data_topleft.process(client)
        circle_data_topright.process(client)
        circle_data_bottomright.process(client)
        circle_data_bottomleft.process(client)
        ill_data_topleft.process(client)
        ill_data_topright.process(client)
        ill_data_bottomright.process(client)
        ill_data_bottomleft.process(client)
        time.sleep(3)

def data_cloud(client):
    global env_data_topleft,env_data_topright,env_data_bottomright,env_data_bottomleft
    while True:
        try:
            env_data_topleft.process(client)
            env_data_topright.process(client)
            env_data_bottomright.process(client)
            env_data_bottomleft.process(client)
        except queue.Empty:
            continue  # 队列为空，继续循环


def deal_with_data() : 
    global env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft
    global circle_data_topleft, circle_data_topright, circle_data_bottomright, circle_data_bottomleft
    global Singal
    Singal = 1
    while True :
        if Singal  ==  1:
            #接收现在草莓的生长周期
            # 接收四块土地的生长周期数据
            Growth_cycle_topleft = circle_data_topleft.circle_data
            Growth_cycle_topright = circle_data_topright.circle_data
            Growth_cycle_bottomright = circle_data_bottomright.circle_data
            Growth_cycle_bottomleft = circle_data_bottomleft.circle_data

            if Growth_cycle_topleft!= "nothing":
                Strawberry_topleft = Fruit(Growth_cycle_topleft)
                check_environment(Strawberry_topleft, env_data_topleft,Growth_cycle_topleft)

            if Singal  ==  0:
                continue

            if Growth_cycle_topright != "nothing":
                Strawberry_topright = Fruit(Growth_cycle_topright)
                check_environment(Strawberry_topright, env_data_topright,Growth_cycle_topright)

            if Singal  ==  0:
                continue

            if Growth_cycle_bottomright!= "nothing":
                Strawberry_bottomright = Fruit(Growth_cycle_bottomright)
                check_environment(Strawberry_bottomright, env_data_bottomright,Growth_cycle_bottomright)

            if Singal  ==  0:
                continue

            if Growth_cycle_bottomleft != "nothing":
                Strawberry_bottomleft = Fruit(Growth_cycle_bottomleft)
                check_environment(Strawberry_bottomleft, env_data_bottomleft,Growth_cycle_bottomleft)



def on_message(client, userdata, msg):
    global Singal
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    message_dict = json.loads(msg.payload.decode())
    print(message_dict)
    if message_dict=={'anniu': 1, 'deviceName': 'device_push'}:
        Singal = 1
        cloud.trans_device(client, "device_push" ,"anniu", 1)
    else:
        Singal = 0
        cloud.trans_device(client, "device_push" ,"anniu", 0)
        print("命令下发")
        #解码
        try:
            device_name = message_dict.get("deviceName")
            print(device_name)
            if device_name:
                new_dict = {device_name: []}
                device_data = {key: value for key, value in message_dict.items() if key != 'deviceName'}
                print(device_data)
                new_dict[device_name].append(device_data)
                print(new_dict)
                # client.publish("v1/gateway/telemetry",json.dumps(new_dict))# 发送
                try1.send_message(device_data)
                time.sleep(0.5)
                client.publish("v1/gateway/telemetry",json.dumps(new_dict)) # 发送
    
            else:
                return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


#设备开启关闭指令
# def send_command():
#     # 创建 MQTT 客户端实例
#     client = activate_devices()

# def activate_devices():
#     # 创建MQTT客户端实例
#     client = mqtt.Client(client_id=client_id, clean_session=True)
#     # 如果需要身份验证
#     client.username_pw_set(USERNAME, password)
#     client.on_connect = try1.on_connect
#     client.on_publish = try1.on_publish
#     client.on_message = on_message
#     # 连接MQTT Broker
#     client.connect(broker_address, port)
#     # 启动 MQTT 客户端的网络循环在新线程中运行
#     client_thread = threading.Thread(target=client.loop_forever)
#     client_thread.daemon = True
#     client_thread.start()
#     return client
def activate_devices():
    # 创建MQTT客户端实例
    client = mqtt.Client(client_id=client_id, clean_session=True)
    # 如果需要身份验证
    client.username_pw_set(USERNAME, password)
    client.on_connect = try1.on_connect
    client.on_publish = try1.on_publish
    client.on_message = on_message
    # 连接MQTT Broker
    client.connect(broker_address, port)
    return client
def send_command():
# 开始网络循环处理
    global client1
    client1 = activate_devices()

    while True:

        client1.loop_start()

        # 让程序运行一段时间以接收消息
        time.sleep(4000)  # 运行 20 秒

        # 停止网络循环处理
        client1.loop_stop()



def check_environment(Strawberry, env_data,cycle_data):

    global client1
    device1_region = None
    device2_region = None
    print("\n66666666666666666666666666666]\n")

    if env_data.region == 1 or env_data.region == 2:
        device1_region = 2
        device2_region = 1
    elif  env_data.region == 3 or env_data.region == 4:
        device1_region = 4
        device2_region = 3
    
    if env_data.region == 2:
        if cycle_data == "red_f":
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,1,0;"#1号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"pump1", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,2,0;"#11号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"pump11", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,1,0;"#2号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2" ,"pump2", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,2,0;"#22号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"pump22", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,4,1;"#1号风扇
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"fan1", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,3,1;"#1号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"wuhuapian1", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,3,1;"#2号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"wuhuapian3", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,4,20;"#1号灯
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2" ,"lamb2", 20)
            time.sleep(3)
        else:#其他
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,3,0;"#1号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"wuhuapian1", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,3,0;"#2号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"wuhuapian2", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,4,0;"#1号风扇
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"fan1", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,4,250;"#2号deng
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"lamb2", 250)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,1,1;"#1号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"pump1", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,1,2,1;"#11号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"pump11", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,1,1;"#2号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2" ,"pump2", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,2,2,1;"#22号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"pump22", 1)
            time.sleep(3)

    elif env_data.region == 4:
        if cycle_data == "red_f":
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,1,0;"#1号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"pump3", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,2,0;"#33号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1,"caomeikic1" ,"pump33", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,1,0;"#4号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"pump4", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,2,0;"#44号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"pump44", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,4,1;"#2号风扇
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"fan3", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,3,1;"#3号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"wuhuapian3", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,3,1;"#4号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"wuhuapian4", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,4,20;"#1号灯
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2" ,"lamb4", 20)
            time.sleep(3)
        else:
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,3,0;"#3号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1" ,"wuhuapian3", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,3,0;"#4号雾化片
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"wuhuapian4", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,4,0;"#4号fan
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"fan3", 0)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,4,250;"#4号灯
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2" ,"lamb4", 250)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,1,1;"#1号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic1"  ,"pump3", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,3,2,1;"#33号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1,"caomeikic1" ,"pump33", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,1,1;"#4号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"pump4", 1)
            with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
                send_data = "property,1,4,2,1;"#44号水泵
                ser_send.write(send_data.encode())
                print(f"\nData sent:{send_data}\n")
            cloud.trans_device(client1, "caomeikic2"  ,"pump44", 1)
            time.sleep(3)

#决策部分
suggestions = [[] for _ in range(4)]# 创建一个包含四个空列表的列表，用于存储每块土地的建议

def Decide():
    # 假设 env_data 和 circle_data 是全局变量，并且会在函数外部更新
    global env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft, circle_data_topleft, circle_data_topright, circle_data_bottomright, circle_data_bottomleft
    env_data_list = [env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft]
    circle_data_list = [circle_data_topleft, circle_data_topright, circle_data_bottomright, circle_data_bottomleft]
    # 根据 circle_data 决定
    while True:
        for index, (env_data, cycle_data) in enumerate(zip(env_data_list, circle_data_list)):

            if cycle_data.circle_data == "nothing":  # 播种决策
                suggestions[index] = decide__3.suggest_disease_prevention("green", index)
            elif cycle_data.circle_data == "bud":
                suggestions[index] = decide__3.suggest_disease_prevention("bud", index)
            elif cycle_data.circle_data == "flower":
                suggestions[index] = decide__3.suggest_disease_prevention("flower", index)
            elif cycle_data.circle_data == "white_f":
                suggestions[index] = decide__3.suggest_disease_prevention("white_f", index)
            else:
                suggestions[index] = decide__3.suggest_disease_prevention("red_f", index)
                        
        client = cloud.activate_devices()
        for i in range(4):
            final_suggestions = "\n".join(suggestion for region_suggestions in suggestions[i] for suggestion in region_suggestions)
            attribute = f"land{i+1}"
            cloud.trans_suggest(client, attribute, final_suggestions)
            suggestions[i].clear()
        time.sleep(10)



def main():

    client = cloud.activate_devices()
    port1 = "/dev/ttyHS1"  # 串口设备路径
    baudrate = 115200  # 波特率
    port = "/dev/ttyHS1"  # 串口设备路径
    baudrate = 115200  # 波特率
    thread1 = threading.Thread(target=push)
    # 注意这里只传递 port 和 baudrate 给 deal_with 函数
    thread2 = threading.Thread(target=deal_with, args=(port, baudrate))
    
    # data_cloud 函数不接受参数，所以 args 是空的
    
    thread3 = threading.Thread(target=trans_data_data)
    thread11 = threading.Thread(target=trans_circle_data)

   

    thread4 = threading.Thread(target=class_cloud,args=(client,))
    thread5 = threading.Thread(target=data_cloud, args=(client,))
    thread6 = threading.Thread(target=Decide)
    thread7 = threading.Thread(target=send_command)
    # thread7 = threading.Thread(target=Decide)
    thread8 = threading.Thread(target=upload_file)
    thread9 = threading.Thread(target=deal_with_data)
    thread10 = threading.Thread(target=ill_QQ)

    thread1.start()
    thread2.start()
    thread3.start()
    thread11.start()
    time.sleep(20)
    thread5.start()
    
    time.sleep(5)
    thread10.start()
    thread4.start()
    thread8.start()
    time.sleep(1)
    thread6.start()
    thread7.start()
    time.sleep(5)
    thread9.start()
    
    


    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()
    thread10.join()
    thread11.join()

    print("Both threads have finished execution.")

if __name__ == "__main__":
    main()
