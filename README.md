# GITY
Gather Image Through Youtube
---
유튜브에서 원하는 객체를 검출하여 이미지로 저장해주는 코드입니다.  
이 저장소는 [this_repository](https://github.com/AliaksandrSiarohin/video-preprocessing)에서 영감을 받았습니다.

## 참고
- 이 저장소는 리눅스 환경에서 테스트를 진행했습니다.

## 목차
- [설치](#installation)
- [작성자](#author)

## installation
0. clone repogitory
```
git clone https://github.com/kyeul611/gity.git
cd ./gity
```
1. 모듈 설치
```
pip install -r requirements.txt
```

2. chromedrive
```
apt-get update
apt install chromium-chromedriver
```
3. youtube-dl
```
wget https://yt-dl.org/downloads/latest/youtube-dl -O youtube-dl
chmod a+rx youtube-dl
```

4. detection-weight

[이곳](https://drive.google.com/drive/folders/1zB0tJ1U7zNmxUGGbpSF9RhG2szbK1m1r)에서 
 __yolov3.tf.data-00000-of-00001__ 파일을 다운받아 __gity/yolov3_tf2__ 폴더 안으로 옮겨주세요.

## run

example:
터미널에서 아래 명령어를 실행
```
python main.py --keyword [키워드] --class_name [클래스 종류]
```

## references
1.

## author
```python
{
	"박 결" : "gyul611@gmail.com",
	"정민혁" : "tlsfk48@gmail.com",
	"이제헌" : "dlwpgjs0723@gmail.com",
}
```
