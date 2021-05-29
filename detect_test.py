from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import numpy as np
import tensorflow as tf
from yolov3_tf2.models_test import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs

def detection(img_tensor,validity, class_name): # args  → img_tensor : img 값을 직접 받기 위해 
    #physical_devices = tf.config.experimental.list_physical_devices('GPU')
    #for physical_device in physical_devices:
    #    tf.config.experimental.set_memory_growth(physical_device, True)
    #tf.debugging.set_log_device_placement(True)
    # cooc names
    labels = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
 	
	    # FLASS.tiny: 삭제   → yolov3.tiny 모델을 사용 안함

    # yolov3 model
    yolo = YoloV3(classes=80)

		# weight load & 적용
    weight = './yolov3_tf2/yolov3.tf' 
    yolo.load_weights(weight).expect_partial()


    # classes load
    classes = './yolov3_tf2/coco.names'
    class_names = [c.strip() for c in open(classes).readlines()]


    img = tf.expand_dims(img_tensor, 0) # 형상 추가 
    img = transform_images(img, 416) # (1,416,416,3) + /255 이미지 정규화 

    # detection
    boxes, scores, classes, nums = yolo(img)


    global a  # 이미지 좌표값을 저장
    a =[] 
    name = labels.index(class_name) # 원하는 class_name 위치
    
    for i in range(len(classes[0])):
    	# detection된 것들중에서 원하는 class만 저장 & 입력한 정확도보다 이상
        if (classes[0][i]==name) and (scores[0][i]>=validity): 
        	# 반정규화
            wh = np.flip(img.shape[1:3])
            x1 = (np.array(boxes[0][i][0]) * wh[0]).astype(np.int32)
            y1 = (np.array(boxes[0][i][1]) * wh[1]).astype(np.int32)
            x2 = (np.array(boxes[0][i][2]) * wh[0]).astype(np.int32)
            y2 = (np.array(boxes[0][i][3]) * wh[1]).astype(np.int32)
            a .append([x1,x2,y1,y2])

    return a

