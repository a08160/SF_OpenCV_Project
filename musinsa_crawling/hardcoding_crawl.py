from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import ssl
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(3)
ssl._create_default_https_context = ssl._create_unverified_context

driver.get("https://www.musinsa.com/category/003?gf=F&attribute=31%5E364")

# 대기 설정
wait = WebDriverWait(driver, 10)

# 데이터 저장 리스트 초기화
data = []
seen_items = set()  # 중복 방지용

# 스크롤 동작 반복
SCROLL_PAUSE_TIME = 2
count = 0

while count < 200:  # 최대 200개 데이터 수집
    # HTML 추출
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.select('a.gtm-view-item-list')

    for product in products:
        if count >= 200:  # 200개 초과 시 종료
            break

        # 상품 고유 식별자
        item_id = product['href'] if 'href' in product.attrs else None
        if item_id and item_id not in seen_items:
            seen_items.add(item_id)  # 중복 방지

            # 브랜드명 추출
            brand_name = product['data-brand-id'] if 'data-brand-id' in product.attrs else "N/A"

            # 상품명 및 이미지 링크 추출
            image = product.select_one('img')
            product_name = image['alt'] if image and 'alt' in image.attrs else "N/A"
            image_link = image['src'] if image and 'src' in image.attrs else "N/A"

            # 데이터 저장
            data.append(["하의", "여성", "겨울", brand_name, product_name, image_link])
            count += 1
    
    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

# 드라이버 종료
driver.quit()

# CSV 파일로 저장
file_path = f'musinsa_bottom_winter_f.csv'
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 헤더 작성
    writer.writerow(["대분류", "성별", "계절", "브랜드명", "상품명", "이미지링크"])
    # 데이터 작성
    writer.writerows(data)

print(f"데이터가 {file_path}에 저장되었습니다.")