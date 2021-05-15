import numpy as np
from skimage import img_as_ubyte
from skimage.transform import resize
import imageio
#from multiprocessing import Pool
#from itertools import cycle
#from tqdm import tqdm
import os


def save(path, frames, seq, format):
    if format == '.mp4':
        imageio.mimsave(path, frames)
    elif format == '.png':
        if os.path.exists(path):
            imageio.imsave(os.path.join(path, str(seq).zfill(7) + '.png'), frames)
        else:
            os.makedirs(path)
        imageio.imsave(os.path.join(path, str(seq).zfill(7) + '.png'), frames) 
    else:
        print ("Unknown format %s" % format)
        exit()
