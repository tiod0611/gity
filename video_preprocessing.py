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
from util import save
from argparse import ArgumentParser
from skimage import img_as_ubyte
from skimage.transform import resize
warnings.filterwarnings("ignore")

DEVNULL = open(os.devnull, 'wb')



def run(data):
    video_id, args = data
    reader = imageio.get_reader(os.path.join(args.video_folder, video_id + '.mp4'))

    try:
        for i, frame in enumerate(reader):
            # import detection info (bbox location = (x1, x2, y1, y2))
            # detector(frame)
            x1, x2, y1, y2 = [97, 419, 0, 387]
            crop = frame[y1:y2, x1:x2]
            if args.image_shape is not None:
                crop = img_as_ubyte(resize(crop, args.image_shape, anti_aliasing=True))
            first_part = ""
            first_part += '#' + video_id
            path = first_part + '.mp4'
            save(os.path.join(args.out_folder, path), crop, i, '.png')
    except imageio.core.format.CannotReadFrameError:
        None
        
        
        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--video_folder", default='youtube-taichi', help='Path to youtube videos')
    parser.add_argument("--out_folder", default='gity_test', help='Path to output')
    parser.add_argument("--format", default='.png', help='Storing format')
    parser.add_argument("--workers", default=1, type=int, help='Number of workers')
    parser.add_argument("--youtube", default='./youtube-dl', help='Path to youtube-dl')
    parser.add_argument("--image_shape", default=(256, 256), type=lambda x: tuple(map(int, x.split(','))),
                        help="Image shape, None for no resize")

    args = parser.parse_args()
    if not os.path.exists(args.video_folder):
        os.makedirs(args.video_folder)
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)
    # partition func add later?
#     for partition in ['test', 'train']:
#         if not os.path.exists(os.path.join(args.out_folder, partition)):
#             os.makedirs(os.path.join(args.out_folder, partition))

    pool = Pool(processes=args.workers)
    args_list = cycle([args])
    video_ids = ['6yFLXG5IxKg'] # crawling list is here
    for chunks_data in tqdm(pool.imap_unordered(run, zip(video_ids, args_list))):
        None  
