import numpy as np
import imageio
import os
import warnings
from detect_test import detection
from argparse import ArgumentParser
from skimage import img_as_ubyte
from skimage.transform import resize
warnings.filterwarnings("ignore")

DEVNULL = open(os.devnull, 'wb')


# Image save function
def save(path, frames, seq, obj_num):
    if os.path.exists(path):
        imageio.imsave(os.path.join(path, str(seq).zfill(7) + '#' + str(obj_num).zfill(1) + '.png'),frames)
    else:
        os.makedirs(path)
    imageio.imsave(os.path.join(path, str(seq).zfill(7) + '#' + str(obj_num).zfill(1) + '.png'), frames)


# 비디오 불러오기 및 좌표데이터 이용해 자르기
def run(data):
    video_id, args = data
    reader = imageio.get_reader(os.path.join(args.video_folder, video_id + '.mp4'))

    try:
        for i, frame in enumerate(reader):
            frame = img_as_ubyte(resize(frame, (416,416), anti_aliasing=True))
            bboxes = detection(frame, args.acc) # 프레임 데이터와 검출정확도
            print(i, bboxes) # 프레임 별 좌표 검출 정보
            for j, bbox in enumerate(bboxes):
            	x1, x2, y1, y2 = bbox
            	crop = frame[y1:y2, x1:x2]
            	# 입력받은 이미지 크기(shape)로 재조정
            	if args.image_shape is not None:
                	crop = img_as_ubyte(resize(crop, args.image_shape, anti_aliasing=True))
                # 이미지 저장 경로 설정
            	first_part = ""
            	first_part += '#' + video_id
            	path = first_part + '.mp4'
            	save(os.path.join(args.out_folder, path), crop, i, j)
    except imageio.core.format.CannotReadFrameError:
        None
