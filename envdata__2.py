import serial



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


def deal_with(port, baudrate):
    with serial.Serial(port, baudrate=baudrate, timeout=None) as ser:
        try:
            while True:
                line = ser.readline().decode().strip()
                if line:
                    if line.startswith("sensor:"):
                        line = line.split(':')[1]
                        #data = EnvironmentalData.uart(line)  (检查数据是否足够)
                        values = line.split(',')
                        region = float(values[0])
                        if region == 1:
                            print(f"\nlefttop {line}\n")
                        elif region == 2:
                            print(f"\nrighttop {line}\n")
                        elif region == 3:
                            print(f"\nleftbottom {line}\n")
                        elif region == 4:
                            print(f"\nleftbottom {line}\n")
                    elif line.startswith("kic:"):
                        print("\nkic_ok\n")
                        continue
                    elif line.startswith("Offline:"):
                        line = line.split(':')[1]
                        values = line.split(',')
                        region = float(values[0])
                        print(f"\n{region}\n")
        except serial.SerialException as e:
            print("Serial error:", e)

if __name__ == "__main__":
    port = "/dev/ttyHS1"  # 串口设备路径
    baudrate = 115200  # 波特率
    deal_with(port, baudrate)
        


# def deal_with(port1, baudrate1):
#     with serial.Serial(port, baudrate=baudrate, timeout=None) as ser:
#         try:
#             while True:
#                 line1 = ser.readline().decode().strip()
#                 if line1:
#                     if line1.startswith("sensor:"):
#                         line1 = line1.split(':')[1]
#                         data = EnvironmentalData.uart(line)  
#                         values = line.split(',')
#                         region = float(values[0])
#                         if region == 1:
#                             data_queue_topleft.put(data)  # 将数据放入队列
#                             data_ready_event.set()
#                         elif region == 2:
#                             data_queue_topright.put(data)  # 将数据放入队列
#                             data_ready_event.set()
#                         elif region == 3:
#                             data_queue_bottomleft.put(data)  # 将数据放入队列
#                             data_ready_event.set()
#                         elif region == 4:
#                             data_queue_bottomright.put(data)  # 将数据放入队列
#                             data_ready_event.set()

#         except serial.SerialException as e:
#             print("Serial error:", e)



# def deal_device(port, baudrate):
#     with serial.Serial(port, baudrate=baudrate, timeout=None) as ser:
#         try:
#             while True:
#                 line1 = ser.readline().decode().strip()
#                 if line:
#                     if line1.startswith("kic:"):
#                         deal_with_queue.put(line)
#                     if line1.startswith("Offline:"):
#                         deal_with_queue.put(line)

#                         continue
#         except serial.SerialException as e:
#             print("Serial error:", e)
