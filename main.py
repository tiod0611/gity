#module
from crawler import crawling
import os
import subprocess
from argparse import ArgumentParser

from video_preprocessing import run

from multiprocessing import Pool
from itertools import cycle

def download(video_id, video_path):
    path = os.path.join(video_path, video_id + ".mp4")
    os.system("./youtube-dl -f 247 https://www.youtube.com/watch?v={} --output {}".format(video_id, path))

#main

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--keyword", required=True, help="다운로드할 영상 키워드를 입력")
    parser.add_argument("--class_name", required=True, help="저장할 클래스명")

    parser.add_argument("--download", default="download", help="다운로드할 위치")
    parser.add_argument("--num_video", default=10, type=int, help="정수형, 다운로드 갯수는 n*40")
    parser.add_argument("--out_folder", default='output', help='Path to output')
    parser.add_argument("--accuracy", default="0.75", help="검출 정확도", type=float)
    parser.add_argument("--image_shape", default=(224, 224), type=lambda x: tuple(map(int, x.split(','))), help="Image shape, None for no resize")
    args = parser.parse_args()

    existed_video=[]
   
    # path_download = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.download)
    # path_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.out_folder)
    
    
    if not os.path.exists(args.download):
        os.makedirs(args.download)

    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)
        
    existed_video = os.listdir(args.out_folder)


    video_ids = crawling(args.keyword, args.num_video)
    video_ids = [x for x in video_ids if x not in existed_video]

    for video in video_ids:
        print(video)
        try:
            download(video, args.download) # 동영상 다운로드
        except:
            continue
		
        run(args.download, args.accuracy, args.image_shape, args.out_folder, video, args.class_name)
        
        if os.path.exists(os.path.join(args.download, video+".mp4")):
            os.remove(os.path.join(args.download, video+".mp4")) #동영상 삭제
        
       
	


    





