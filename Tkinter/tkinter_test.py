# Python 기능 구현

import cv2
import pandas as pd
import sys
import numpy as np

sys.path.append('/personal_color_visualization') # Noukky.py face_color.py import 

from Noukky import remove_background
from face_color import Color_extract

mode = int(input("""기능1. 사진 업로드
                 기능2. 웹캠 사진 촬영
                 기능을 선택하세요(숫자만 입력):
                 """))

def image_upload(mode):
    # 사진 업로드
    if mode == 1:
        img = cv2.imread("test_image.png")
        return img
    
    # 웹캠 사진 촬영
    else:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("웹캠을 열 수 없습니다.")
            exit()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            cv2.imshow('Webcam', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                cv2.imwrite('Captured_image.png', frame)
                img = cv2.imread('Captured_image.png')
                return img
            
            break
        cap.release()
        cv2.destroyAllWindows()

