#module
from crawler import crawling
import os
import subprocess
from argparse import ArgumentParser

from video_preprocessing import run

from multiprocessing import Pool
from itertools import cycle


def download(video_id, video_path, youtube):
    
    # youtube_dl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "youtube-dl.exe")
    path = os.path.join(video_path, video_id + ".mp4")
    subprocess.run([ youtube, "-f", 
                    "247","https://www.youtube.com/watch?v=" + video_id, "--output", path], shell=True)

#main

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--keyword", required=True, help="다운로드할 영상 키워드를 입력")
    parser.add_argument("--download", default="download", help="다운로드할 위치")
    parser.add_argument("--num_video", default=10, type=int, help="정수형, 다운로드 갯수는 n*40")
    
    parser.add_argument("--youtube", default='./youtube-dl', help='Path to youtube-dl')

    parser.add_argument("--workers", default=1, type=int, help='Number of workers')
    parser.add_argument("--out_folder", default='gity_test', help='Path to output')
    parser.add_argument("--acc", default="0.5", help="검출 정확도")

    args = parser.parse_args()

    video_ids = crawling(args.keyword, args.num_video)
   
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.download)

    if not os.path.exists(path):
            os.makedirs(path)
   
    pool = Pool(processes=args.workers)
    
    for video in video_ids:
        download(video, args.download, args.youtube) # 동영상 다운로드
        # Pool.imap_unordered(run(args_list, video))
        run(args, video)
        os.remove(os.path.join(path, video+".mp4")) #동영상 삭제



    





