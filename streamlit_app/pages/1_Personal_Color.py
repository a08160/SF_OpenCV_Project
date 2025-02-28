import streamlit as st
import requests
from PIL import Image
import os

def main():
    st.set_page_config(layout="wide", page_title="퍼스널 컬러 진단")
    
    # 사이드바 구현
    with st.sidebar:
        st.markdown("<h3>이미지 업로드</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("얼굴 이미지를 업로드해주세요", type=['jpg', 'jpeg', 'png'])

    # 2) 커스텀 CSS 스타일
    custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 전체 페이지 스타일 */
    .stApp {
        background-color: #ffffff;
        font-family: 'Pretendard', sans-serif;
        padding: 2rem 0;
    }

    /* 헤더 스타일 */
    .main-header {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 3rem 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 2rem auto;
        max-width: 1200px;
        transition: all 0.3s ease;
    }

    /* 결과 카드 스타일 */
    .result-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 2rem auto;
        max-width: 900px;
        transition: transform 0.3s ease;
        text-align: center;
    }

    .result-card:hover {
        transform: translateY(-5px);
    }

    /* 이미지 컨테이너 스타일 */
    .image-container {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }

    .image-container:hover {
        transform: translateY(-5px);
    }

    /* 업로드 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        color: white;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    /* 텍스트 스타일 */
    h1 {
        color: #000000;
        font-weight: 700;
        letter-spacing: -0.5px;
        line-height: 1.3;
    }

    h2, h3 {
        color: #000000;
        font-weight: 600;
        letter-spacing: -0.3px;
    }

    p {
        color: #4a4a4a;
        line-height: 1.7;
    }

    /* 연예인 카드 스타일 */
    .celeb-card {
        background: #fafafa;
        padding: 1.2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        margin: 0.8rem 0;
        transition: transform 0.3s ease;
    }

    .celeb-card:hover {
        transform: translateY(-3px);
    }

    /* 파일 업로더 스타일 */
    .uploadfile-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed #e0e0e0;
        margin: 2rem auto;
        max-width: 600px;
        transition: all 0.3s ease;
    }

    .uploadfile-box:hover {
        border-color: #000000;
    }

    /* 결과 섹션 그리드 */
    .result-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        padding: 1.5rem;
    }

    /* 이미지 뷰어 컨트롤 완전히 숨기기 */
    .stImage > img {
        cursor: default !important;
    }
    .stImage > button {
        display: none !important;
    }
    .stImage > div[data-testid="StyledFullScreenButton"] {
        display: none !important;
    }
    </style>
    """

    # CSS 적용
    st.markdown(custom_css, unsafe_allow_html=True)

    # 3) 메인 헤더
    st.markdown("""
        <div class='main-header'>
            <h1 style='text-align:center; color: #000000; font-size: 2.5rem; margin-bottom: 1rem;'>
                퍼스널 컬러 진단 시스템
            </h1>
            <p style='text-align:center; color: #666; font-size: 1.1rem;'>
                AURA가 분석하는 당신만의 퍼스널 컬러
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 4) 세션 상태 관리
    if 'personal_color' not in st.session_state:
        st.session_state.personal_color = None
        st.session_state.uploaded_image = None

    if uploaded_file:
        files = {'file': uploaded_file}
        try:
            response = requests.post('http://localhost:8000/predict', files=files)
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    st.session_state.personal_color = result['personal_color']
                    st.session_state.uploaded_image = uploaded_file
                else:
                    st.error("😢 퍼스널 컬러 분석에 실패했습니다.")
        except requests.exceptions.RequestException as e:
            st.error(f"😢 서버 연결에 실패했습니다: {e}")

    # 6) 결과 표시
    if st.session_state.personal_color:
        personal_color = st.session_state.personal_color
        
        color_info = {
            "Spring Warm": {
                "title": "Spring Warm",
                "celebs": {
                    "아이유": "밝고 화사한 이미지",
                    "윈터": "생기 넘치는 분위기",
                    "윤아": "청순하고 사랑스러운 이미지",
                    "수지": "밝고 고급스러운 분위기"
                },
                "emoji": "🌸"
            },
            "Summer Cool": {
                "title": "Summer Cool",
                "celebs": {
                    "정채연": "시원하고 청순한 이미지",
                    "아이린": "차분하고 우아한 분위기",
                    "장원영": "청량하고 세련된 이미지",
                    "태연": "시크하고 세련된 분위기"
                },
                "emoji": "🌊"
            },
            "Autumn Warm": {
                "title": "Autumn Warm",
                "celebs": {
                    "제니": "고급스럽고 세련된 이미지",
                    "이효리": "자연스럽고 섹시한 분위기",
                    "신세경": "차분하고 지적인 이미지",
                    "이성경": "부드럽고 우아한 분위기"
                },
                "emoji": "🍁"
            },
            "Winter Cool": {
                "title": "Winter Cool",
                "celebs": {
                    "지수": "도도하고 시크한 이미지",
                    "임지연": "강렬하고 매혹적인 분위기",
                    "선미": "카리스마 있고 고급스러운 분위기",
                    "뷔": "시크하고 세련된 이미지"
                },
                "emoji": "❄️"
            }
        }

        info = color_info.get(personal_color, {"title": personal_color, "celebs": {}})
        
        # 결과 카드 부분
        st.markdown(f"""
            <div class='result-card'>
                <h2 style='text-align:center; font-size: 2rem; margin-bottom: 1rem;'>
                    분석 결과
                </h2>
                <h3 style='text-align:center; color: #000000; font-size: 1.8rem; margin-bottom: 1.5rem;'>
                    TAVY의 퍼스널 컬러는 {info['title']} 입니다
                </h3>
                <div style='text-align:center; font-size: 1.1rem; background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
                    <p style='font-weight: 700; margin-bottom: 1rem; color: #000000;'>대표 연예인과 이미지</p>
                    <div style='display: flex; flex-direction: column; gap: 1rem;'>
        """, unsafe_allow_html=True)

        # 연예인 정보 카드 수정
        for name, desc in info['celebs'].items():
            st.markdown(f"""
                <div class='celeb-card'>
                    <p style='font-weight: 700; font-size: 1.1rem; margin: 0 0 0.5rem 0;'>{name}</p>
                    <p style='color: #666666; font-size: 0.95rem; margin: 0;'>{desc}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(custom_css, unsafe_allow_html=True)

        st.markdown("""
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 이미지 섹션
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.session_state.uploaded_image:
                st.markdown("<div class='image-container'>", unsafe_allow_html=True)
                image = Image.open(st.session_state.uploaded_image)
                image = image.resize((300, 450))  # 크기를 300x450으로 줄임
                st.image(image, caption="업로드된 이미지", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                images_dir = os.path.join(script_dir, "images", personal_color.lower())
                
                if os.path.isdir(images_dir):
                    image_files = [f for f in os.listdir(images_dir) 
                                if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                    
                    if image_files:
                        st.markdown("<div class='image-container'>", unsafe_allow_html=True)
                        cols = st.columns(2)
                        for i, image_file in enumerate(sorted(image_files)[:4]):  
                            with cols[i % 2]:
                                image_path = os.path.join(images_dir, image_file)
                                color_image = Image.open(image_path)
                                color_image = color_image.resize((150, 225))  # 크기를 150x225로 줄임
                                st.image(color_image, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("😢 추천 이미지를 불러오는데 실패했습니다.")


if __name__ == "__main__":
    main()
