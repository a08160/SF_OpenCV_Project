# SF_OpenCV_Project
OpenCV 프로젝트 | 퍼스널 컬러 진단 및 의류 추천 시스템

---
## 프로젝트 소개
1. **프로젝트 내용**
사용자의 이미지를 분석하여 퍼스널 컬러를 진단하고 각 퍼스널 컬러에 맞는 무신사 의류 제품 추천

2. **목표 및 방향 설정**
- U2Net/mRNN/PIL 의 알고리즘을 이해
- 지도학습의 클러스터링 기법을 활용하여 퍼스널 컬러에 대한 정확도를 높임

## 주요 기능
**1. 퍼스널 컬러를 진단하고 자하는 사용자의 이미지 업로드 혹은 LiveCam을 활용한 사진 촬용을 통한 업로드**
**2. 진단 결과에 따른 맞춤 패션 아이템 추천**
**3. DB 관리를 통한 아이템 추천 이력 관리**

## 기술 스택
|분야|사용 스택|
|-----|-----|
|Frontend|Streamlit|
|Backend|FastAPI
|Database|MySQL|
|Data Analysis|OpenCV, PIL, Pytorch, Scikit-learn|

# 실행 방법
**1. 레포지토리 내려받기 **
<code>git clone https://github.com/a08160/SF_OpenCV_Project</code>
**2. 가상환경 설정**
<code>python -m venv venv
.\venv\Scripts\activate</code>
**3. 의존성 설치** 
<code> pip install -r requirements.txt</code>
**4. FastAPI 서버 실행**
<code> uvicorn app.main:app --reload</code>
**5. Streamlit 실행**
<code> streamlit run stremlit/home.py</code>

## 프로젝트 구조
|-- README.md
|-- app
|   |-- __pycache__
|   |-- item_recommendation.py
|   |-- main.py
|   |-- personal_color.py
|   |-- shape_predictor_68_face_landmarks.dat
|   `-- sql_app
|-- model_image.csv
|-- musinsa_crawling # 무신사 상품 데이터 크롤링
|   |-- cloth_personal_color.py
|   |-- complete_data
|   |-- data
|   |-- hardcoding_crawl.py
|   `-- musinsa_crawling.py
|-- personal_color_classify
|   |-- cloth_classification.py
|   |-- color_classification.py
|   |-- color_clustering.py
|   |-- complete_personal_color.xlsx
|   |-- lab_colors.xlsx
|   |-- personal_color_complete.py
|   |-- test.py
|  
|-- personal_color_visualization
|   |-- Cloth_image
|   |-- Noukky.py
|   |-- Noukky_image
|   |-- cloth_color.py
|   |-- cloth_color_preprocessing.py
|   |-- face_color.py
|   |-- model_image_crawl.py
|   |-- original_image
|   |-- shape_predictor_68_face_landmarks.dat
|   `-- test.py
|-- sql_dataset
|   |-- fashion_data.xlsx
|   `-- sql_data_upload.py
`-- streamlit_app
    |-- Home.py
    `-- pages
