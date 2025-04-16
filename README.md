
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

## 🧑🏽‍💻 코드 소개

### 1️⃣ 퍼스널 컬러 추출 로직 (`personal_color.py`)
- `dlib.get_frontal_face_detector` 및 68 포인트 랜드마크 모델을 이용해 **눈, 입술, 피부 영역**을 분리
- 각 부위의 **면적 비율을 계산**하여 **BGR 값에 가중치**를 부여
- BGR → Lab 색상으로 변환 후, **지배적인 색상** 추출

### 2️⃣ 퍼스널 컬러 분류 기준
- 목표: Spring Warm / Autumn Warm / Summer Cool / Winter Cool 4가지 타입으로 분류
- 대표 연예인 이미지 → 학습용 목적 변수로 활용하여 **지도 학습 모델 구성**
- **Decision Tree 분류기** 사용, `KFold` 교차검증으로 신뢰도 향상  
- 최종 분류 기준:

```python
if b >= 141.5:
    if L >= 150.5:
        return "Spring Warm"
    else:
        return "Autumn Warm"
else:
    if L >= 138.5:
        return "Summer Cool"
    else:
        return "Winter Cool"
```

### 3️⃣ 퍼스널 컬러 기반 의류 색상 추천
- 이미지에서 얼굴 색상과 유사한 영역 제거 → **의류만 남긴 이미지 생성**
- Lab 색상 분석 방식 동일하게 적용하여 **의류의 지배적 색상 추출**
- 얼굴 퍼스널 컬러를 타겟 데이터로 설정하여 의류 색상 군집화 → **추천 컬러 도출**
- 최종적으로 크롤링된 무신사 상품과 매칭하여 **퍼스널 컬러 기반 상품 추천 시스템 구축**

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
└── requirements.txt              # 패키지 의존성 목록
```

---

## 💡 실행 방법

```bash
# 1. 레포지토리 클론
git clone https://github.com/a08160/SF_OpenCV_Project

# 2. 가상환경 설정
python -m venv venv
# 윈도우
.env\Scriptsctivate
# 맥OS / 리눅스
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. FastAPI 서버 실행
uvicorn app.main:app --reload

# 5. Streamlit 앱 실행
streamlit run streamlit_app/Home.py
```
