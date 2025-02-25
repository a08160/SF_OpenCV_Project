# 상품별 모델이미지 크롤링
# 상의 메인에서 이미지를 크롤링
# 이미지에 얼굴이 인식되지 않으면 크롤링하지 않음
# 총 1000개 데이터 수집

import cv2
import dlib
import requests
from io import BytesIO
from PIL import Image
import numpy as np
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import ssl

import os

# 얼굴 인식 함수
def is_face_detected(image_url):
    try:
        # 이미지 요청
        response = requests.get(image_url)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(img_array, -1)

        # 얼굴 탐지기 로드 (dlib을 사용)
        detector = dlib.get_frontal_face_detector()

        # 이미지 그레이스케일로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 얼굴 인식
        faces = detector(gray)

        # 얼굴이 1개 이상 감지되면 True 반환
        return len(faces) > 0
    except Exception as e:
        print(f"얼굴 인식 오류: {e}")
        return False

# 이미지 저장 폴더 설정
save_dir = "C:/Users/SAMSUNG/Documents/code/OpenCV/Project/personal_color_visualization/image"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 이미지 저장 함수
def save_image(image_url, filename):
    try:
        # 이미지 요청
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # 파일 경로 설정
        image_path = os.path.join(save_dir, filename)
        
        # 이미지 저장
        img.save(image_path, 'PNG')
        print(f"이미지가 {image_path}에 저장되었습니다.")
    except Exception as e:
        print(f"이미지 저장 오류: {e}")

# 크롬 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(3)
ssl._create_default_https_context = ssl._create_unverified_context

driver.get("https://www.musinsa.com/category/002?gf=F")

# 대기 설정
wait = WebDriverWait(driver, 10)

# 데이터 저장 리스트 초기화
data = []
seen_items = set()  # 중복 방지용

# 스크롤 동작 반복
SCROLL_PAUSE_TIME = 2
count = 921

while count < 1200:  # 최대 1200개 데이터 수집
    # HTML 추출
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.select('a.gtm-view-item-list')

    for product in products:
        if count >= 1200:  # 1200개 초과 시 종료
            break

        # 상품 고유 식별자
        item_id = product['href'] if 'href' in product.attrs else None
        if item_id and item_id not in seen_items:
            seen_items.add(item_id)  # 중복 방지

            image = product.select_one('img')
            image_link = image['src'] if image and 'src' in image.attrs else "N/A"

            # 얼굴 인식
            if is_face_detected(image_link):
                # 이미지 파일명 설정 (URL에서 파일명 추출)
                image_filename = f"{count + 1}.png"
                
                # 이미지 저장
                save_image(image_link, image_filename)
                
                # 데이터 저장 (이미지 링크를 포함)
                data.append([image_link])
                count += 1
    
    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

# 드라이버 종료
driver.quit()

# CSV 파일로 저장
file_path = 'model_image.csv'
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 헤더 작성
    writer.writerow(["이미지링크"])
    # 데이터 작성
    writer.writerows(data)

print(f"데이터가 {file_path}에 저장되었습니다.")
