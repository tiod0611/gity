import numpy as np
import imageio
import os
import warnings
from detect import detection
from argparse import ArgumentParser
from skimage import img_as_ubyte
from skimage.transform import resize
import tqdm

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
def obj_segmentation(crop_rgb_dict, crop_list):
	obj_num = 0
	if crop_rgb_dict == {}:
		crop_rgb_dict[1] = crop_list
		obj_num = 1
	else:
		for key, value in crop_rgb_dict.items():
			# 기준객체의 RGB값 각각 +- 20% 값으로 동일객체 판단
			pass_crop = 0
			for i, rgb in enumerate(value):
				if crop_list[i] <= (rgb * 1.2) and crop_list[i] >= (rgb * 0.8):
					pass_crop += 1
					if pass_crop == 3: # r,g,b 모두 조건에 맞다면 해당 key_number 부여
						obj_num = key
						break
				else :
					break
					
		if obj_num == 0:
			crop_rgb_dict[max(crop_rgb_dict.keys()) + 1] = crop_list
			obj_num = max(crop_rgb_dict.keys())

	return crop_rgb_dict, obj_num

def padding(bbox):
	x1,x2,y1,y2 = bbox
	add_frame = 10
	x1 -= add_frame
	y1 -= add_frame
	x2 += add_frame
	y2 += add_frame

	if (x2-x1) > (y2-y1): #가로가 더 긴 경우 
		center = (y2+y1)/2
		add_padding = (x2-x1)/2
		if center-add_padding < 0: # x1이 맨 왼쪽인 경우
			y1 = 0
			y2 = (center+add_padding) + abs((center-add_padding)) 
		elif center+add_padding > 416: # x2가 맨 오른쪽인 경우
			y1 = (center-add_padding) - ((center+add_padding)-416)
			y2 = 416
		else:
			y1 = center-add_padding
			y2 = center+add_padding
	else :  # 세로가 더 긴 경우
		center = (x2+x1)/2
		add_padding = (y2-y1)/2
		if center-add_padding < 0: # y1이 맨 밑인 경우
			x1 = 0
			x2 = (center+add_padding) + abs((center-add_padding))
		elif center+add_padding > 416: # y2가 맨 위인 경우
			x1 = (center-add_padding) - ((center+add_padding)-416)
			x2 = 416
		else:
			x1 = center-add_padding
			x2 = center+add_padding



	return int(x1), int(x2), int(y1), int(y2)

# 비디오 불러오기, 좌표값을 받아 이미지 자르기 (Load video, Crop images by coordinate value)
# def run(data):
def run(download, accuracy, image_shape, out_folder, video_id, class_name):
    # video_id, args = data
	if os.path.exists(os.path.join(download, video_id+'.mp4')):
		video_path = os.path.join(download, video_id+'.mp4')
	else: 
		return 
	reader = imageio.get_reader(video_path)
	crop_rgb_dict = {}

	try:
		for i, frame in enumerate(reader):
			# import detection coordinate (bbox location = (x1, x2, y1, y2))
			# resize to detection model input size (416, 416)
			if i % 10 == 0:
				frame = img_as_ubyte(resize(frame, (416,416), anti_aliasing=True))
				bboxes = detection(frame, accuracy, class_name) # 프레임 데이터와 검출정확도
				
				print(i, bboxes) # 프레임 별 좌표 검출 정보

			else:
				continue

			for bbox in bboxes:
				# 이미지 여백 추가 
				p_x1,p_x2,p_y1,p_y2=padding(bbox)
				x1,x2,y1,y2 = bbox
				crop_p = frame[p_y1:p_y2, p_x1:p_x2]
				crop = frame[y1:y2, x1:x2]
				
				# 잘라낸 이미지의 RGB값 합계
				crop_list = [crop[:, :, 0].sum(), crop[:, :, 1].sum(), crop[:, :, 2].sum()]
				crop_rgb_dict, obj_num = obj_segmentation(crop_rgb_dict, crop_list)
				
				# 입력받은 이미지 크기(shape)로 재조정
				try:
					if image_shape is not None:
						crop = img_as_ubyte(resize(crop_p, image_shape, anti_aliasing=True))
					# 이미지 저장 경로 설정
					first_part = ""
					first_part += '#' + video_id
					path = first_part + '.mp4' + '#' + str(obj_num)
					save(os.path.join(out_folder, video_id, path), crop, i, obj_num)
				except:
					pass
	except :
		None 
