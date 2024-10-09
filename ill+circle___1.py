# aidlux相关
from cvs import *
import aidlite_gpu
# from utils2 import detect_postprocess, preprocess_img, draw_detect_res
# from zxd import utils2
import utils2
import utils3
# import time
import cv2
from collections import defaultdict


def Strawberry_Growth_cycle():
    ##生长周期有关参数
    # AidLite初始化：调用AidLite进行AI模型的加载与推理，需导入aidlite
    aidlite_circle = aidlite_gpu.aidlite()
    aidlite_ill = aidlite_gpu.aidlite()
    # Aidlite模型路径
    model_path_circle = '8-7 90per circle.tflite'
    model_path_ill = 'best-fp16.tflite'
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
    frame_class_counts_circle = defaultdict(int)
    frame_counter_ill = 0
    frame_class_counts_ill = defaultdict(int)

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

    # 读取视频进行推理
    cap = cvs.VideoCapture(-1, cam_w=640, cam_h=480, quality=100)
    frame_id = 0
    while True:
        frame = cap.read()
        if frame is None:
            continue
        
        cvs.imshow(frame)

        frame_id += 1
        if not int(frame_id) % 2 == 0:
            img = utils2.preprocess_img(frame, target_shape=(640, 640), div_num=255, means=None, stds=None)
            aidlite_circle.setInput_Float32(img, 640, 640)
            aidlite_circle.invoke()
            pred = aidlite_circle.getOutput_Float32(0)
            pred = pred.reshape(1, 25200, 9)[0]
            pred,cls_counts =  utils2.detect_postprocess(pred, frame,frame.shape, [640, 640, 3], conf_thres = 0.4, iou_thres = 0.3)
            # print(f"\n{cls_counts}\n")
            # 绘制推理结果
            for region, counts in cls_counts.items():
                # 输出每个区域最常见的类别
                common_class_in_region = max(counts, key=counts.get) if counts else None

                if common_class_in_region:
                    print(f"Most common class in {region} of this frame: {common_class_in_region}")
                    for class_name, count in counts.items():
                        frame_class_counts_circle[region][class_name] += count

            frame_counter_circle += 1
            # 每处理20帧，找出并打印过去20帧中每个区域最常出现的类别
            if frame_counter_circle % 20 == 0:
                for region, counts in frame_class_counts_circle.items():
                    most_common_20_frame_class = max(counts, key=counts.get) if counts else None
                    if most_common_20_frame_class:
                        if region == "top_left":
                            # class_data_queue_topleft.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "top_right":
                            # class_data_queue_topright.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_right":
                            # class_data_queue_bottomright.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_left":
                            # class_data_queue_bottomleft.put(RegioncircleData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        
                    else :
                        if region == "top_left":
                            # class_data_queue_topleft.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}: nothing\n")
                        elif region == "top_right":
                            # class_data_queue_topright.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_right":
                            # class_data_queue_bottomright.put(RegioncircleData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_left":
                            # class_data_queue_bottomleft.put(RegioncircleData(region,"nothing"))
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
            pred,cls_counts =  utils3.detect_postprocess(pred,frame, frame.shape, [640, 640, 3], conf_thres = 0.2, iou_thres = 0.3)
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
                            # classill_data_queue_topleft.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "top_right":
                            # classill_data_queue_topright.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_right":
                            # classill_data_queue_bottomright.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        elif region == "bottom_left":
                            # classill_data_queue_bottomleft.put(RegionillData(region,most_common_20_frame_class))
                            print(f"\nMost common class in the last 20 frames for {region}: {most_common_20_frame_class}\n")
                        
                    else :
                        if region == "top_left":
                            # classill_data_queue_topleft.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}: nothing\n")
                        elif region == "top_right":
                            # classill_data_queue_topright.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_right":
                            # classill_data_queue_bottomright.put(RegionillData(region,"nothing"))
                            print(f"\nMost common class in the last 20 frames for {region}:  nothing\n")
                        elif region == "bottom_left":
                            # classill_data_queue_bottomleft.put(RegionillData(region,"nothing"))
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

if __name__ == "__main__":
    Strawberry_Growth_cycle()
        
