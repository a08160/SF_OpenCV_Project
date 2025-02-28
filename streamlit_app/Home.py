import streamlit as st
import base64

def main():
    # 페이지 설정
    st.set_page_config(layout="wide", page_title="AURA Fashion Recommendation")
    
    # Streamlit 기본 요소 숨기기
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 배경 이미지 설정
    background_image_path = "homepgim.jpg"
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    background_image_base64 = get_base64_of_bin_file(background_image_path)

    # 모던한 디자인 CSS
    css_code = f"""
    <style>
    /* 기본 레이아웃 설정 */
    html, body, [data-testid="stAppViewContainer"],
    .main, .block-container, .stApp {{
        height: 100vh;
        margin: 0;
        padding: 0;
        font-family: 'Pretendard', sans-serif;
    }}

    /* 배경 설정 */
    .stApp {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.5)),
                    url("data:image/jpg;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* 텍스트 스타일링 */
    .modern-text {{
        font-size: 3.5rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        letter-spacing: -0.02em;
        line-height: 1.4;
        text-shadow: 2px 2px 15px rgba(0, 0, 0, 0.3);
        transform: translateX(80px);
        opacity: 0;
        animation: slideIn 1s ease-out forwards;
    }}

    .subtitle {{
        font-size: 2rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 400;
        margin-top: 1rem;
        transform: translateX(80px);
        opacity: 0;
        animation: slideIn 1s ease-out 0.3s forwards;
    }}

    /* 애니메이션 정의 */
    @keyframes slideIn {{
        from {{
            transform: translateX(80px);
            opacity: 0;
        }}
        to {{
            transform: translateX(0);
            opacity: 1;
        }}
    }}

    /* 반응형 디자인 */
    @media (max-width: 768px) {{
        .modern-text {{
            font-size: 2.5rem;
        }}
        .subtitle {{
            font-size: 1.5rem;
        }}
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

    # 메인 컨텐츠
    main_content = """
    <div style="padding: 2rem;">
        <div class="modern-text">패션의 모든 것</div>
        <div class="subtitle">AURA에서 쉽고 간편하게</div>
    </div>
    """
    st.markdown(main_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
