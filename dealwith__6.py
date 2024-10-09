#上云相关
import cloud
import time
import serial



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
from _queue import Empty


class TemperatureData:
    def __init__(self, air_temp):
        self.air_temp_data = air_temp


class Fruit:
    def __init__(self, sort):
        if sort == "red_f":
            self.air_temp_min = 1000
            self.air_temp_max = 1000
            self.air_hum_max = -1000
            self.aif_hum_min = -1000
            self.soild_hum_max = -1000
            self.soild_hum_min = -1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 1000
            self.light_min= 1000
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
            self.air_temp_min = -1000
            self.air_temp_max = -1000
            self.air_hum_max = -1000
            self.air_hum_min = -1000
            self.soild_hum_max = 1000
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
            self.PH_max = 1000
        elif sort == "nothing" :
            self.air_temp_min = 100
            self.air_temp_max = -1000
            self.air_hum_max = 100
            self.aif_hum_min = -1000
            self.soild_hum_max = 100
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 100
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
        elif sort == "flower" :
            self.air_temp_min = 100
            self.air_temp_max = -1000
            self.air_hum_max = 100
            self.air_hum_min = -1000
            self.soild_hum_max = 100
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 100
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
        elif sort == "bud" :
            self.air_temp_min = 100
            self.air_temp_max = -1000
            self.air_hum_max = 100
            self.air_hum_min = -1000
            self.soild_hum_max = 100
            self.soild_hum_min = 1000
            self.soild_temp_max = 100
            self.soild_temp_min = 100
            self.light_max = 100
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


#设备开启关闭指令
def check_environment(Strawberry, env_data):

    device1_region = None
    device2_region = None


    if env_data.region == 1 or env_data.region == 2:
        device1_region = 2
        device2_region = 1
    elif  env_data.region == 1 or env_data.region == 2:
        device1_region = 4
        device2_region = 3
    else :
        device1_region = 5
        device2_region = 5

    #设备4风扇开
    if env_data.air_temp_data > Strawberry.air_temp_max:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,2,4,1;"#1号
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            # 将修改后的列表重新组合成字符串
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")

        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,4,4,1;" #2号
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")
    
    #设备4风扇关
    elif env_data.air_temp_data < Strawberry.air_temp_min:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,2,4,0;"#1号
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            # 将修改后的列表重新组合成字符串
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")

        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,4,4,0;" #2号
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")

    # 土壤湿度的自动化作物开水泵设备1
    if env_data.soild_hum_data < Strawberry.soild_hum_min:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "propeoty,1,1,1,1;"
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            # 将修改后的列表重新组合成字符串
            new_send_data = ','.join(parts)
            ser_send.write(new_send_data.encode())
            print(f"\nData sent:{new_send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")
    elif env_data.soild_hum_data > Strawberry.soild_hum_max:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "propeoty,1,1,1,0;"
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            # 将修改后的列表重新组合成字符串
            new_send_data = ','.join(parts)
            ser_send.write(new_send_data.encode())
            print(f"\nData sent:{new_send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")


    #土壤湿度的自动化作物开水泵设备2
    if env_data.ph_data < Strawberry.PH_min:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "propeoty,1,1,2,1;"
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            # 将修改后的列表重新组合成字符串
            new_send_data = ','.join(parts)
            ser_send.write(new_send_data.encode())
            print(f"\nData sent:{new_send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=5)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")
        #土壤湿度的自动化作物开水泵设备2
    elif env_data.ph_data > Strawberry.PH_max:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "propeoty,1,1,2,0;"
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            # 将修改后的列表重新组合成字符串
            new_send_data = ','.join(parts)
            ser_send.write(new_send_data.encode())
            print(f"\nData sent:{new_send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=5)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")


    #设备5灯带
    if env_data.lux_data < Strawberry.light_min:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,1,5,1;"#1号灯
            parts = send_data.split(',')
            parts[2] = str(device2_region)
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")
        #设备5灯带
    elif env_data.lux_data > Strawberry.light_max:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,1,5,1;"#1号灯
            parts = send_data.split(',')
            parts[2] = str(device2_region)
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)
        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")


    #设备5雾化片
    if env_data.air_hum_data < Strawberry.aif_hum_min:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,2,5,1;"#1号
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)

        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")
    elif env_data.air_hum_data > Strawberry.aif_hum_max:
        with serial.Serial(port="/dev/ttyHS1", baudrate=115200, timeout=1) as ser_send:
            send_data = "property,1,2,5,0;"#1号
            parts = send_data.split(',')
            parts[2] = str(device1_region)
            ser_send.write(send_data.encode())
            print(f"\nData sent:{send_data}\n")
        time.sleep(0.5)

        try:
            deal_data = deal_with_queue.get(timeout=1)
            # 处理 deal_data ...
        except Empty:
            print("Queue is empty, timing out after 5 seconds.")
            # 这里可以添加超时后的逻辑，例如重试或等待
        else:
            print(f"\n{deal_data} is ok\n")


if __name__ == "__main__":
    def check_environment(Strawberry, env_data):