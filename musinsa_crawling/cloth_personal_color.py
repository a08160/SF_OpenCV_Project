# musinsa 제품에 대한 퍼스널 컬러 라벨링

import pandas as pd
import cv2
import numpy as np
import os
import requests
import tempfile
from rembg import remove
from PIL import Image

# URL에서 이미지 다운로드 후 저장
def url_to_image(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(response.content)
                temp_filename = temp_file.name
            return temp_filename  # 임시 파일 경로 반환
    except Exception as e:
        print(f"이미지 다운로드 실패: {url} - {str(e)}")
    return None

# 배경 제거 후 이미지 저장
def remove_background(input_path):
    try:
        img = Image.open(input_path)
        output = remove(img)  # 배경 제거
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            output.save(temp_file.name)
            return temp_file.name  # 배경 제거된 임시 파일 경로 반환
    except Exception as e:
        print(f"배경 제거 실패: {input_path} - {str(e)}")
    return None

# Lab 색 공간 변환 및 Personal Color 추출
def cloth_personal_color(file):
    df = pd.read_csv(file)
    personal_colors = []

    i = 1
    for image_url in df["이미지링크"]:
        # 1️⃣ URL에서 이미지 다운로드
        image_path = url_to_image(image_url)
        if image_path is None:
            personal_colors.append("Unknown")
            continue

        # 2️⃣ 배경 제거
        bg_removed_path = remove_background(image_path)
        os.remove(image_path)  # 원본 이미지 삭제
        if bg_removed_path is None:
            personal_colors.append("Unknown")
            continue

        # 3️⃣ OpenCV로 이미지 로드
        image = cv2.imread(bg_removed_path, cv2.IMREAD_UNCHANGED)
        os.remove(bg_removed_path)  # 배경 제거된 이미지 삭제
        if image is None:
            personal_colors.append("Unknown")
            continue

        # 4️⃣ 배경이 제거된 상태에서 주요 색상 추출
        if image.shape[2] == 4:  # RGBA (투명도 포함)
            mask = image[:, :, 3] > 0  # 알파 채널이 0이 아닌 부분 선택
            pixels = image[mask][:, :3]  # BGR 색상 정보만 남김
        else:  # 알파 채널이 없으면 전체 픽셀 사용
            pixels = image.reshape(-1, 3)

        if len(pixels) == 0:  # 색상 정보가 없는 경우
            personal_colors.append("Unknown")
            continue

        # 평균 색상 계산
        cloth_bgr = np.mean(pixels, axis=0).astype(int)

        # BGR → LAB 변환
        color_1x1 = np.uint8([[[cloth_bgr[0], cloth_bgr[1], cloth_bgr[2]]]])
        lab_1x1 = cv2.cvtColor(color_1x1, cv2.COLOR_BGR2LAB)[0, 0]
        L_lab, a_lab, b_lab = lab_1x1

        # 퍼스널 컬러 결정
        if b_lab <= 131.5:
            personal_colors.append("Summer Cool" if L_lab >= 136.5 else "Winter Cool")
        else:
            personal_colors.append("Spring Warm" if L_lab >= 142.5 else "Autumn Warm")
        
        i += 1
        print(f"{i} 번째 이미지 완료")

    df["퍼스널컬러"] = personal_colors
    return df

# 🔹 데이터 처리
seasons = ["spring", "summer", "fall", "winter"]
clothes = ["top", "bottom"]
genders = ["m", "f"]

for season in seasons:
    for cloth in clothes:
        for gender in genders:
            file_path = f"musinsa_crawling/data/musinsa_{cloth}_{season}_{gender}.csv"

            if not os.path.exists(file_path):
                print(f"파일 없음: {file_path}")
                continue

            df = cloth_personal_color(file_path)
            save_path = f"musinsa_crawling/complete_data/musinsa_{cloth}_{season}_{gender}.xlsx"
            df.to_excel(save_path, index=False)
            print(f"완료: {save_path}")