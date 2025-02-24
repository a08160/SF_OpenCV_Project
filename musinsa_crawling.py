# 무신사 의류 데이터 수집
# 상품 품목 - 상의 하의(바지)
# 수집 데이터 - 대분류 / 성별 / 계절 / 상품명 / 링크 / 첫 번째 모델 이미지

import os
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv

# 데이터 수집 함수 정의
def product_info(product):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920x1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(3)

    driver.get("https://www.musinsa.com/menu?storeCode=musinsa")

    # 대기 설정
    wait = WebDriverWait(driver, 10)

    # 데이터 저장 리스트 초기화
    data = []
    seen_items = set()  # 중복 방지용

    # 스크롤 동작 반복
    SCROLL_PAUSE_TIME = 2
    count = 0

    try:
        # 상품 카테고리 클릭
        category_element = driver.find_element(By.XPATH, f'//*[@id="commonLayoutContents"]/div[3]/div[1]//*[contains(text(), "{product}")]')
        category_element.click()

        # 카테고리 ID 가져오기
        category_id_element = driver.find_element(By.XPATH, '//*[@id="commonLayoutContents"]/div[3]/div[1]/p[4]')
        category_id = category_id_element.get_attribute("data-category-id")

        # 상품 전체보기로 이동
        driver.get(f"https://www.musinsa.com/category/{category_id}")
        
        # 성별 선택
        driver.find_element(By.XPATH, '//*[@id="commonLayoutContents"]/div[2]/div/div[1]/div[1]/div[2]/span/svg').click()

        genders = ["남성", "여성"]

        for gender in genders:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="radix-:rm:"]/div/div/div/div[5]/div/div/div[1]/div/div/div/ul//*[contains(text(), "{gender}")]')))
            element.click()

            while count < 200: # 최대 200개 데이터 수집
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                products = soup.select('a.gtm-view-item-list')

                # 페이지 로딩 대기
                time.sleep(5)

                for product in products:
                    if count >= 200:
                        break

                    # 상품 고유 식별자
                    item_id = product['href'] if 'href' in product.attrs else None
                    if item_id and item_id not in seen_items:
                        seen_items.add(item_id)  # 중복 방지

                        # 브랜드명 추출
                        brand_name = product['data-brand-id'] if 'data-brand-id' in product.attrs else "N/A"

                        # 상품명 및 이미지 링크 추출
                        season_element = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[12]/div/div[2]/div/div/dl/div[3]/dd')
                        season = season_element.text if season_element else "N/A"
                        image1 = product.select_one('img') # 대표 이미지
                        image2_element = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[12]/div/div[2]/div/div/div[2]/div/img') # 모델 이미지
                        image2_link = image2_element.get_attribute('src') if image2_element else "N/A"
                        product_name = image1['alt'] if image1 and 'alt' in image1.attrs else "N/A"
                        image_link = image1['src'] if image1 and 'src' in image1.attrs else "N/A" # 대표 링크

                        # 데이터 저장
                        data.append([product, gender, season, brand_name, image1, image2_link, product_name, image_link])
                        count += 1

        return data
    
    except Exception as e:
        print("오류 발생:", e)

products = ["상의", "바지"] # 수집할 데이터

for product in products:
    product_info(product)

    with open(f"info_{product}", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['상품 링크', '성별', '시즌', '브랜드명', '대표 이미지', '모델 이미지', '상품명', '상품 이미지 링크'])
        writer.writerows(data)