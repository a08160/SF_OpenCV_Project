# 무신사 의류 데이터 수집
# 상품 품목 - 상의 하의(바지)
# 수집 데이터 - 대분류 / 소분류 / 성별 / 계절 / 상품명 / 링크 / 첫 번째 모델 이미지

import os
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ssl
import requests

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

        # 상품 클릭
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sc-hzhKNl lmHEaa")))
        element.click()

        # 페이지 로딩 대기
        time.sleep(5)

    except Exception as e:
        print("오류 발생:", e)

    while count < 200: # 상품별 최대 200개의 데이터 수집
        break
    
    finally:
        driver.quit()

products = ["상의", "바지"] # 수집할 데이터

product_info("상의")
