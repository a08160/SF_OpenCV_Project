# 🎨 SF_OpenCV_Project  
**퍼스널 컬러 진단 & 패션 아이템 추천 시스템**

---

## 🧩 프로젝트 소개

### 🔍 프로젝트 개요
사용자의 얼굴 이미지를 분석하여 **퍼스널 컬러**를 진단하고, 진단된 컬러 타입에 적합한 **무신사 패션 아이템**을 추천하는 시스템입니다.  

### 🎯 목표 및 방향
- OpenCV, PIL, PyTorch, U2Net 등의 영상 처리 및 딥러닝 모델을 활용해 **정확한 퍼스널 컬러 진단**
- 지도학습 기반 클러스터링 기법으로 **퍼스널 컬러 분류 정확도 향상**
- 사용자 맞춤형 아이템 추천 시스템과 이력 관리 기능 구현

---

## 🚀 주요 기능

1. **이미지 업로드 또는 실시간 촬영(LiveCam) 기능**  
   - 사용자는 사진을 직접 업로드하거나 웹캠을 통해 촬영할 수 있습니다.

2. **퍼스널 컬러 자동 진단**  
   - 얼굴에서 피부톤을 분석하여 봄웜, 여름쿨, 가을웜, 겨울쿨 중 하나로 분류

3. **컬러 타입 기반 맞춤 패션 아이템 추천**  
   - 진단 결과에 따라 무신사 상품 데이터에서 최적의 아이템 추천

4. **추천 이력 저장 및 관리 기능 (DB 연동)**  
   - MySQL을 활용하여 추천 이력을 저장 및 추후 활용 가능

---

## 🛠️ 기술 스택

| 분야         | 사용 기술                         |
|------------|----------------------------------|
| **Frontend** | Streamlit                        |
| **Backend**  | FastAPI                          |
| **Database** | MySQL                            |
| **AI/ML**    | OpenCV, PIL, PyTorch, Scikit-learn |
| **크롤링**   | Selenium, BeautifulSoup 등 사용 (무신사 데이터 수집용) |

---

## 📂 프로젝트 구조

```plaintext
SF_OpenCV_Project/
│
├── app/                          # FastAPI 백엔드 코드
│   ├── main.py                   # FastAPI 진입점
│   ├── personal_color.py         # 퍼스널 컬러 진단 로직
│   ├── item_recommendation.py    # 추천 알고리즘
│   └── sql_app/                  # DB 모델 및 연결 설정
│
├── streamlit_app/                # 프론트엔드 (Streamlit)
│   ├── Home.py
│   └── pages/
│
├── personal_color_classify/      # 컬러 분류 및 클러스터링 관련 코드
│
├── personal_color_visualization/ # 시각화 및 이미지 처리
│
├── musinsa_crawling/             # 무신사 크롤링 코드
│
├── sql_dataset/                  # DB 연동용 데이터 및 업로드 코드
│
├── model_image.csv               # 예시 이미지 정보
└── requirements.txt              # 패키지 의존성
