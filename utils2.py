import cv2
import numpy as np
import collections

# coco_class = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
#         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
#         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
#         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
#         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
#         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
#         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
#         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
#         'hair drier', 'toothbrush']

coco_class = ["bud","flower","white_f","red_f"]

# coco_class = ["flower","health","ripe","fruit","fertilizer","powdery","acalcerosis","greyleaf"]

def xywh2xyxy(x):
    '''
    Box (center x, center y, width, height) to (x1, y1, x2, y2)
    '''
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y

def xyxy2xywh(box):
    '''
    Box (left_top x, left_top y, right_bottom x, right_bottom y) to (left_top x, left_top y, width, height)
    '''
    box[:, 2:] = box[:, 2:] - box[:, :2]
    return box

def NMS(dets, thresh):
    '''
    单类NMS算法
    dets.shape = (N, 5), (left_top x, left_top y, right_bottom x, right_bottom y, Scores)
    '''
    x1 = dets[:,0]
    y1 = dets[:,1]
    x2 = dets[:,2]
    y2 = dets[:,3]
    areas = (y2-y1+1) * (x2-x1+1)
    scores = dets[:,4]
    keep = []
    index = scores.argsort()[::-1]
    while index.size >0:
        i = index[0]       # every time the first is the biggst, and add it directly
        keep.append(i)
        x11 = np.maximum(x1[i], x1[index[1:]])    # calculate the points of overlap 
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])
        w = np.maximum(0, x22-x11+1)    # the weights of overlap
        h = np.maximum(0, y22-y11+1)    # the height of overlap
        overlaps = w*h
        ious = overlaps / (areas[i]+areas[index[1:]] - overlaps)
        idx = np.where(ious<=thresh)[0]
        index = index[idx+1]   # because index start from 1
 
    return dets[keep]

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)

def preprocess_img(img, target_shape:tuple=None, div_num=255, means:list=[0.485, 0.456, 0.406], stds:list=[0.229, 0.224, 0.225]):
    '''
    图像预处理:
    target_shape: 目标shape
    div_num: 归一化除数
    means: len(means)==图像通道数，通道均值, None不进行zscore
    stds: len(stds)==图像通道数，通道方差, None不进行zscore
    '''
    img_processed = np.copy(img)
    # resize
    if target_shape:
        # img_processed = cv2.resize(img_processed, target_shape)
        img_processed = letterbox(img_processed, target_shape, stride=None, auto=False)[0]

    img_processed = img_processed.astype(np.float32)
    img_processed = img_processed/div_num

    # z-score
    if means is not None and stds is not None:
        means = np.array(means).reshape(1, 1, -1)
        stds = np.array(stds).reshape(1, 1, -1)
        img_processed = (img_processed-means)/stds

    # unsqueeze
    img_processed = img_processed[None, :]

    return img_processed.astype(np.float32)
    
def convert_shape(shapes:tuple or list, int8=False):
    '''
    转化为aidlite需要的格式
    '''
    if isinstance(shapes, tuple):
        shapes = [shapes]
    out = []
    for shape in shapes:
        nums = 1 if int8 else 4
        for n in shape:
            nums *= n
        out.append(nums)
    return out

def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    coords[:, [0, 2]] -= pad[0]  # x padding
    coords[:, [1, 3]] -= pad[1]  # y padding
    coords[:, :4] /= gain
    clip_coords(coords, img0_shape)
    return coords


def clip_coords(boxes, img_shape):
    # Clip bounding xyxy bounding boxes to image shape (height, width)
    boxes[:, 0].clip(0, img_shape[1], out=boxes[:, 0])  # x1
    boxes[:, 1].clip(0, img_shape[0], out=boxes[:, 1])  # y1
    boxes[:, 2].clip(0, img_shape[1], out=boxes[:, 2])  # x2
    boxes[:, 3].clip(0, img_shape[0], out=boxes[:, 3])  # y2



# def detect_postprocess(prediction, img0shape, img1shape, conf_thres=0.25, iou_thres=0.45):
#     '''
#     检测输出后处理
#     prediction: aidlite模型预测输出
#     img0shape: 原始图片shape
#     img1shape: 输入图片shape
#     conf_thres: 置信度阈值
#     iou_thres: IOU阈值
#     return: list[np.ndarray(N, 5)], 对应类别的坐标框信息, xywh、conf
#     '''
#     h, w, _ = img1shape
#     cls_num = prediction.shape[-1] - 5
#     valid_condidates = prediction[prediction[..., 4] > conf_thres]
#     valid_condidates[:, 0] *= w
#     valid_condidates[:, 1] *= h
#     valid_condidates[:, 2] *= w
#     valid_condidates[:, 3] *= h
#     valid_condidates[:, :4] = xywh2xyxy(valid_condidates[:, :4])
#     valid_condidates = valid_condidates[(valid_condidates[:, 0] > 0) & (valid_condidates[:, 1] > 0) & (valid_condidates[:, 2] > 0) & (valid_condidates[:, 3] > 0)]
#     box_cls = valid_condidates[:, 5:].argmax(1)
#     cls_box = []
#        # 将图像宽度和高度除以2，得到分割点
#     mid_w = w / 2
#     mid_h = h / 2

#     # 初始化四个区域的类别计数字典
#     cls_counts_top_left = collections.defaultdict(int)
#     cls_counts_top_right = collections.defaultdict(int)
#     cls_counts_bottom_left = collections.defaultdict(int)
#     cls_counts_bottom_right = collections.defaultdict(int)

#     # 处理每个类别的预测框
#     for i in range(cls_num):
#         temp_boxes = valid_condidates[box_cls == i]
#         if len(temp_boxes) == 0:
#             continue

#         # 应用NMS
#         temp_boxes = NMS(temp_boxes, iou_thres)

#         # 调整坐标到原始图片尺寸并转换坐标格式
#         temp_boxes[:, :4] = scale_coords([h, w], temp_boxes[:, :4], img0shape).round()
#         temp_boxes[:, :4] = xyxy2xywh(temp_boxes[:, :4])
#         boxes_with_conf = temp_boxes[:, :5].tolist()  # 已有[x, y, w, h, class_id]
#         boxes_with_conf = [[*box, conf] for box, conf in zip(boxes_with_conf, temp_boxes[:, 4])]  # 添加置信度
#         cls_box.append(boxes_with_conf)

#         # 分割图像为四个象限并统计每个象限的类别计数
#         for box in temp_boxes:
#             x, y, w, h = box[:4]
#             x_center = box[0] + box[2] / 2.0
#             y_center = box[1] + box[3] / 2.0
#             if x_center < mid_w and y_center < mid_h:
#                 cls_counts_top_left[coco_class[i]] += 1
#             elif x_center >= mid_w and y_center < mid_h:
#                 cls_counts_top_right[coco_class[i]] += 1
#             elif x_center< mid_w and y_center >= mid_h:
#                 cls_counts_bottom_left[coco_class[i]] += 1
#             else:  # x >= mid_w and y >= mid_h
#                 cls_counts_bottom_right[coco_class[i]] += 1

#     # 将四个区域的计数合并为一个字典，或者分别返回
#     cls_counts = {
#         'top_left': dict(cls_counts_top_left),
#         'top_right': dict(cls_counts_top_right),
#         'bottom_left': dict(cls_counts_bottom_left),
#         'bottom_right': dict(cls_counts_bottom_right)
#     }
#     # for bi in range(cls_num):
#     #     if len(temp_boxes) == 0:
#     #         continue
#     #     # 在这里增加对每个类别的计数
#     #     # cls_counts[coco_class[bi]] += len(temp_boxes)
        
#     return cls_box , cls_counts


def detect_postprocess(prediction, img,img0shape, img1shape, conf_thres=0.25, iou_thres=0.45):
    h, w, _ = img1shape
    img = img.astype(np.uint8)
    height = h
    width= w
    mid_w, mid_h = width / 2, height / 2
    cls_num = prediction.shape[-1] - 5

    valid_candidates = prediction[prediction[..., 4] > conf_thres]
    valid_candidates[:, 0] *= w
    valid_candidates[:, 1] *= h
    valid_candidates[:, 2] *= w
    valid_candidates[:, 3] *= h
    valid_candidates[:, :4] = xywh2xyxy(valid_candidates[:, :4])
    valid_candidates = valid_candidates[
        (valid_candidates[:, 0] < w) & 
        (valid_candidates[:, 1] < h) &
        (valid_candidates[:, 2] >= 0) & 
        (valid_candidates[:, 3] >= 0)
    ]

    box_cls = valid_candidates[:, 5:].argmax(1)
    cls_box = []
    cls_counts_top_left = collections.defaultdict(int)
    cls_counts_top_right = collections.defaultdict(int)
    cls_counts_bottom_left = collections.defaultdict(int)
    cls_counts_bottom_right = collections.defaultdict(int)

    for class_id in range(cls_num):
        temp_boxes = valid_candidates[box_cls == class_id]
        if len(temp_boxes) == 0:
            cls_box.append([])
            continue
        temp_boxes = NMS(temp_boxes, iou_thres)
        temp_boxes[:, :4] = scale_coords([h, w], temp_boxes[:, :4], img0shape).round()
        temp_boxes[:, :4] = xyxy2xywh(temp_boxes[:, :4])

        for box in temp_boxes:
            x_center, y_center = box[0], box[1]
            if x_center <= mid_w and y_center <= mid_h:
                cls_counts_top_left[coco_class[class_id]] += 1
            elif mid_w < x_center and  y_center <= mid_h:
                cls_counts_top_right[coco_class[class_id]] += 1
            elif  x_center <= mid_w and mid_h < y_center :
                cls_counts_bottom_left[coco_class[class_id]] += 1
            elif mid_w < x_center and mid_h < y_center :
                cls_counts_bottom_right[coco_class[class_id]] += 1

        boxes_with_conf = [[*box[:4], coco_class[class_id], box[4]] for box in temp_boxes]
        cls_box.append(boxes_with_conf)

    cls_counts = {
        'top_left': dict(cls_counts_top_left),
        'top_right': dict(cls_counts_top_right),
        'bottom_left': dict(cls_counts_bottom_left),
        'bottom_right': dict(cls_counts_bottom_right)
    }

    return cls_box, cls_counts

# def detect_postprocess(prediction, img0shape, img1shape, conf_thres=0.25, iou_thres=0.45):
#     '''
#     检测输出后处理
#     prediction: aidlite模型预测输出
#     img0shape: 原始图片shape
#     img1shape: 输入图片shape
#     conf_thres: 置信度阈值
#     iou_thres: IOU阈值
#     return: list[np.ndarray(N, 5)], 对应类别的坐标框信息, xywh、conf
#     '''
#     h, w, _ = img1shape
#     cls_num = prediction.shape[-1] - 5
#     valid_condidates = prediction[prediction[..., 4] > conf_thres]
#     valid_condidates[:, 0] *= w
#     valid_condidates[:, 1] *= h
#     valid_condidates[:, 2] *= w
#     valid_condidates[:, 3] *= h
#     valid_condidates[:, :4] = xywh2xyxy(valid_condidates[:, :4])
#     valid_condidates = valid_condidates[(valid_condidates[:, 0] > 0) & (valid_condidates[:, 1] > 0) & (valid_condidates[:, 2] > 0) & (valid_condidates[:, 3] > 0)]
#     box_cls = valid_condidates[:, 5:].argmax(1)
#     cls_box = []
#     cls_counts = collections.defaultdict(int)  # 初始化一个字典来计数各类别出现次数
#     for i in range(cls_num):
#         temp_boxes = valid_condidates[box_cls == i]
#         if len(temp_boxes) == 0:
#             cls_box.append([])
#             continue
#         temp_boxes = NMS(temp_boxes, iou_thres)
#         temp_boxes[:, :4] = scale_coords([h, w], temp_boxes[:, :4], img0shape).round()
#         temp_boxes[:, :4] = xyxy2xywh(temp_boxes[:, :4])
        
#         # 包含置信度，使用tolist以便于后续处理
#         boxes_with_conf = temp_boxes[:, :5].tolist()  # 已有[x, y, w, h, class_id]
#         boxes_with_conf = [[*box, conf] for box, conf in zip(boxes_with_conf, temp_boxes[:, 4])]  # 添加置信度
#         cls_box.append(boxes_with_conf)
#         cls_counts[coco_class[i]] += len(temp_boxes)
    
#     # for bi in range(cls_num):
#     #     if len(temp_boxes) == 0:
#     #         continue
#     #     # 在这里增加对每个类别的计数
#     #     # cls_counts[coco_class[bi]] += len(temp_boxes)
        
#     return cls_box , cls_counts

def draw_detect_res(img, all_boxes):
    '''
    检测结果绘制
    '''


    img = img.astype(np.uint8)
    # 获取图像尺寸
    # 定义图像的宽度和高度
    width = img.shape[1]
    height = img.shape[0]
    #width = 1280 height =720
    
    # 定义四个区域的圆心坐标和半径
    circles = [
        ((200, height // 4), 80, (0, 255, 0)),  # 左上角
        ((400, height // 4), 80, (0, 255, 0)),  # 右上角
        ((200, 3 * height // 4), 80, (0, 255, 0)),  # 左下角
        ((400, 3 * height // 4), 80,(0, 255, 0))  # 右下角
    ]

    # 在四个区域画圆形
    for (cx, cy), radius, color in circles:
        cv2.circle(img, (cx, cy), radius, color, 2)

    color_step = int(255 / len(all_boxes)) if len(all_boxes) > 0 else 255
    for bi in range(len(all_boxes)):
        if len(all_boxes[bi]) == 0:
            continue
        for box in all_boxes[bi]:
            x, y, w, h, class_id, conf = box  # 解构出置信度
            x, y, w, h = [int(t) for t in [x, y, w, h]]  # 四个坐标转为整数
            label_text = f'{coco_class[bi]}'  # 构造包含类名和置信度的标签文本
            cv2.putText(img, label_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, bi * color_step, 255 - bi * color_step), thickness=1)
            # println(f"{(coco_class[bi])}/n")
    return img
# def draw_detect_res(img, all_boxes):
# # '''
# # 检测结果绘制，不绘制划分区域
# # '''
# # img = img.astype(np.uint8)  # 确保图像类型正确，如果已经是uint8可以注释掉此行
#     color_step = int(255 / len(all_boxes)) if len(all_boxes) > 0 else 255

#     for bi in range(len(all_boxes)):
#         if len(all_boxes[bi]) == 0:
#             continue
#         for box in all_boxes[bi]:
#             if len(box) != 6:
#                 continue  # 忽略格式不正确的边界框
#             x, y, w, h, class_id, conf = box  # 解构出x, y, w, h, class_id, 和 conf
#             x, y, w, h = [int(t) for t in [x, y, w, h]]  # 四个坐标转为整数
#             label_text = f'Class {class_id}: {conf:.2f}'  # 构造包含类名和置信度的标签文本

#             # 绘制边界框
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, bi * color_step, 255 - bi * color_step), thickness=2)

#             # 绘制标签文本
#             cv2.putText(img, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#     return img

