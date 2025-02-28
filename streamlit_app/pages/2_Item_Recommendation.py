import streamlit as st
import requests
from PIL import Image
import io

# 페이지 기본 설정
st.set_page_config(
    page_title="퍼스널 컬러 추천 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stButton>button {
            width: 100%;
            background-color: #000000;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
            transition: all 0.3s ease;  /* 부드러운 호버 효과 */
        }
        .stButton>button:hover {
            background-color: #333333;  /* 호버 시 약간 밝은 검정색 */
            transform: translateY(-2px);  /* 호버 시 살짝 위로 이동 */
        }
        .uploadedFile {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            padding: 20px;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 30px;
        }
        h2 {
            color: #34495e;
            padding: 15px 0;
            font-size: 1.8rem;
            font-weight: 600;
        }
        .personal-color-result {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .recommendation-section {
            margin-top: 30px;
        }
            .item-card {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .item-card:hover {
            transform: translateY(-5px);
        }
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown("<h1>퍼스널 컬러 및 아이템 추천</h1>", unsafe_allow_html=True)
    
    # 두 개의 컬럼으로 나누기
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h2>이미지 업로드</h2>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "이미지를 선택하세요...", 
            type=["jpg", "jpeg", "png"],
            help="JPG, JPEG, PNG 형식의 이미지 파일을 업로드해주세요."
        )
        
        st.markdown("<h2>성별 선택</h2>", unsafe_allow_html=True)
        gender = st.radio(
            "성별을 선택하세요:",
            ("여성", "남성"),
            horizontal=True
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)
        
        if st.button("분석 시작하기"):
            if uploaded_file is None:
                st.warning("이미지를 먼저 업로드해주세요!")
                return
                
            with st.spinner("분석 중입니다..."):
                files = {"file": ("image.jpg", uploaded_file.getvalue(), "image/jpeg")}
                data = {"gender": gender}
                response = requests.post("http://127.0.0.1:8000/predict-and-recommend", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["success"]:
                        with col2:            
                            # 퍼스널 컬러 결과 표시
                            st.markdown(f"""
                            <div class="personal-color-result">
                                <h2>분석 결과</h2>
                                <p style='font-size: 1.5rem; color: #2c3e50;'>
                                    TAVY의 퍼스널 컬러는 <span style='color: #505764; font-weight: 700;'>{result["personal_color"]}</span> 입니다.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("""
                            <div class="recommendation-section">
                                <h2>맞춤 스타일 추천</h2>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for category, items in result["recommendations"].items():
                                with st.expander(f"{category} 추천"):
                                    item_cols = st.columns(len(items))
                                    for idx, item in enumerate(items):
                                        with item_cols[idx]:
                                            st.image(item["image_url"], use_container_width=True)
                                            st.markdown(f"""
                                            **{item["item_name"]}**  
                                            {item["brand_name"]}
                                            """)
                    else:
                        st.error("예측 및 추천에 실패했습니다. 다시 시도해주세요.")
                else:
                    st.error("서버 연결에 실패했습니다.")

if __name__ == "__main__":
    main()
