import numpy as np
import pandas as pd
import imageio
import os
import subprocess
from multiprocessing import Pool
from itertools import cycle
import warnings
import glob
import time
from tqdm import tqdm
from argparse import ArgumentParser
from skimage import img_as_ubyte
from skimage.transform import resize
warnings.filterwarnings("ignore")

DEVNULL = open(os.devnull, 'wb')


def save(path, frames, seq, obj_num):
    if os.path.exists(path):
        imageio.imsave(os.path.join(path, str(seq).zfill(7) + '#' + str(obj_num).zfill(1) + '.png'),frames)
    else:
        os.makedirs(path)
    imageio.imsave(os.path.join(path, str(seq).zfill(7) + '#' + str(obj_num).zfill(1) + '.png'), frames)



def run(data):
    video_id, args = data
    reader = imageio.get_reader(os.path.join(args.video_folder, video_id + '.mp4'))

    try:
        for i, frame in enumerate(reader):
            # import detection info (bbox location = (x1, x2, y1, y2))
            # detector(frame)
            bboxes = detect()
            for j, bbox in enumerate(bboxes):
            	x1, x2, y1, y2 = bbox
            	crop = frame[y1:y2, x1:x2]
            	if args.image_shape is not None:
                	crop = img_as_ubyte(resize(crop, args.image_shape, anti_aliasing=True))
            	first_part = ""
            	first_part += '#' + video_id
            	path = first_part + '.mp4'
            	save(os.path.join(args.out_folder, path), crop, i, j)
    except imageio.core.format.CannotReadFrameError:
        None
