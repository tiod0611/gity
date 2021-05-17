#module
from crawler import crawling
import os
import subprocess
from argparse import ArgumentParser


def download(video_id, video_path):
    
    youtube_dl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "youtube-dl.exe")
    path = os.path.join(video_path, video_id + ".mp4")
    subprocess.run([ youtube_dl, "-f", 
                    "247","https://www.youtube.com/watch?v=" + video_id, "--output", path], shell=True)

#main

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("--keyword", required=True, help="다운로드할 영상 키워드를 입력")
    parser.add_argument("--output", default="output", help="다운로드할 위치")
    parser.add_argument("--num_video", default=10, type=int, help="정수형, 다운로드 갯수는 n*40")

    args = parser.parse_args()

    video_ids = crawling(args.keyword, args.num_video)
   
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)

    if not os.path.exists(path):
            os.makedirs(path)
   
    for video in video_ids:
        download(video, args.output)
        os.remove(os.path.join(path, video+".mp4"))



    





