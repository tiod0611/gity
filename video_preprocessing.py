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

# 객체 번호별 이미지 저장 (Images save by object number)
def save(path, frames, seq, obj_num):
    if os.path.exists(path):
        imageio.imsave(os.path.join(path, str(seq).zfill(7) + '#' + str(obj_num).zfill(1) + '.png'),frames)
    else:
        os.makedirs(path)
    imageio.imsave(os.path.join(path, str(seq).zfill(7) + '#' + str(obj_num).zfill(1) + '.png'), frames)


# RGB합계값으로 객체 세분화 및 번호 부여 (Object segmentation by RGB value)
def obj_segmentation(crop_rgb_dict, crop_sum):
	obj_num = 0
	if crop_rgb_dict == {}:
		crop_rgb_dict[1] = crop_sum
		obj_num = 1
	else:
		for key, value in crop_rgb_dict.items():
			# 기준객체의 +- 20% 값으로 동일객체 판단
			if crop_sum <= (value * 1.2) and crop_sum >= (value * 0.8):
				obj_num = key
				break
		if obj_num == 0:
			crop_rgb_dict[max(crop_rgb_dict.keys()) + 1] = crop_sum
			obj_num = max(crop_rgb_dict.keys())

	return crop_rgb_dict, obj_num


# 비디오 불러오기, 좌표값을 받아 이미지 자르기 (Load video, Crop images by coordinate value)
# def run(data):
def run(download, acc, image_shape, out_folder, video_id):
    # video_id, args = data
	video_path = os.path.join(download, os.listdir(download)[0])
	reader = imageio.get_reader(video_path)
	crop_rgb_dict = {}

	try:
		for i, frame in enumerate(reader):
			# import detection coordinate (bbox location = (x1, x2, y1, y2))
			# resize to detection model input size (416, 416)
			if i % 5 == 0:
				frame = img_as_ubyte(resize(frame, (416,416), anti_aliasing=True))
				bboxes = detection(frame, acc) # 프레임 데이터와 검출정확도
				print(i, bboxes) # 프레임 별 좌표 검출 정보
			else:
				continue

			for bbox in bboxes:
				x1, x2, y1, y2 = bbox
				crop = frame[y1:y2, x1:x2]
				# 잘라낸 이미지의 RGB값 합계
				crop_sum = crop[:, :, 0].sum() + crop[:, :, 1].sum() + crop[:, :, 2].sum()
				crop_rgb_dict, obj_num = obj_segmentation(crop_rgb_dict, crop_sum)
				
				# 입력받은 이미지 크기(shape)로 재조정
				if image_shape is not None:
					crop = img_as_ubyte(resize(crop, image_shape, anti_aliasing=True))
				# 이미지 저장 경로 설정
				first_part = ""
				first_part += '#' + video_id
				path = first_part + '.mp4' + '#' + str(obj_num)
				save(os.path.join(out_folder, path), crop, i, obj_num)
	except imageio.core.format.CannotReadFrameError:
		None 
