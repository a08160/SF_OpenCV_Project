# 무신사 의류 데이터 수집
# 상품 품목 - 상의 하의(바지)
# 수집 데이터 - 대분류 / 성별 / 계절 / 상품명 / 링크 

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

    # 상품 카테고리 클릭
    category_element = driver.find_element(By.XPATH, f'//*[@id="commonLayoutContents"]/div[3]/div[1]//*[contains(text(), "{product}")]')
    category_element.click()

    # 카테고리 ID 가져오기
    category_id_element = driver.find_element(By.XPATH, '//*[@id="commonLayoutContents"]/div[3]/div[1]/p[4]')
    category_id = category_id_element.get_attribute("data-category-id")

    # 대기 설정
    wait = WebDriverWait(driver, 10)

    # 데이터 저장 리스트 초기화
    data = []
    seen_items = set()  # 중복 방지용

    # 스크롤 동작 반복
    SCROLL_PAUSE_TIME = 2
    count = 0

    try:
        genders = ["남성_M", "여성_F"]
        seasons = ["봄", "여름", "가을", "겨울"]

        for gender in genders:
            for season in seasons:
                # 상품 전체보기로 이동
                driver.get(f"https://www.musinsa.com/category/{category_id}?gf=A")
            
                # 성별 선택
                driver.find_element(By.XPATH, '//*[contains(text(), "성별")]').click()

                element1 = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{gender}"]')))
                element1.click()
                
                element2= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "상세옵션")]')))
                element2.click()

                element3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:rm:"]/div/div/div/div[3]/div/div/span[7]')))
                element3.click()

                element4 = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[contains(text(), "{season}")]')))
                element4.click()

                driver.find_element(By.XPATH,'//*[@id="radix-:rm:"]/div/div/div/div[6]/button').click()

                while count < 10: # 최대 200개 데이터 수집
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    products = soup.select('a.gtm-view-item-list')

                    # 페이지 로딩 대기
                    time.sleep(5)

                    for product in products:
                        if count >= 10:
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
                            data.append([product, gender, season, brand_name, product_name, image_link])
                            count += 1

                    # 스크롤 내리기
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)

        driver.quit()
        return data
    
    except Exception as e:
        print("오류 발생:", e)
        driver.quit()

products = ["상의", "바지"] # 수집할 데이터
all_data = []  # 모든 데이터를 모을 리스트

for product in products:
    data = product_info(product)
    all_data.extend(data)  # 각 상품 유형 데이터를 모음

# CSV로 저장
with open('product_info.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 헤더 작성
    writer.writerow(["대분류", "성별", "계절", "브랜드명", "상품명", "이미지링크"])
    # 데이터 작성
    writer.writerows(all_data)
