import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="댕스널 컬러 & 레진 인식표 시뮬레이터", 
    page_icon="🐾", 
    layout="wide"
)

# 커스텀 스타일링
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #edf2f7 100%);
    }
    .app-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
        border: 1px solid #eef2f6;
        margin-bottom: 20px;
    }
    .gradient-header {
        background: linear-gradient(135deg, #FF8E9E 0%, #FF6B8B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
    }
    .tone-badge {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown('<h1 class="gradient-header">🐾 댕스널 컬러 (Pet Personal Color)</h1>', unsafe_allow_html=True)
st.markdown("##### AI 퍼스널 컬러 진단 & 4층 입체 레진 인식표 실시간 시뮬레이터")
st.write("---")

# 세션 스테이트 초기화 (결과 표시 여부 관리)
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# 퍼스널 컬러 팔레트 정의 (AI 자동 매칭용)
COLOR_PALETTES = {
    "크리밍 핑크 (Creaming Pink)": {
        "rgb": (244, 194, 194), "outline": (210, 140, 140), "strap": (230, 170, 170),
        "badge": "#FF8E9E", "tone": "Warm Spring", "desc": "포근하고 사랑스러운 웜톤 파스텔 핑크. 하얀 털 및 밝은 갈색 털에 완벽 착붙!"
    },
    "민트 그린 (Mint Green)": {
        "rgb": (168, 216, 185), "outline": (115, 175, 135), "strap": (140, 195, 160),
        "badge": "#4EBE8A", "tone": "Cool Summer", "desc": "청량하고 산뜻한 쿨톤 파스텔 그린. 청초하고 맑은 인상을 극대화해줍니다."
    },
    "파스텔 옐로우 (Pastel Yellow)": {
        "rgb": (254, 236, 168), "outline": (220, 195, 110), "strap": (235, 210, 130),
        "badge": "#E3A820", "tone": "Warm Spring", "desc": "화사하고 기분 좋은 햇살 오렌지-옐로우. 밝은 털빛의 활달한 친구에게 추천!"
    },
    "스카이 블루 (Sky Blue)": {
        "rgb": (173, 216, 230), "outline": (115, 170, 190), "strap": (145, 190, 210),
        "badge": "#4A90E2", "tone": "Cool Summer", "desc": "세련되고 신비로운 차분한 쿨 블루. 회색빛, 실버 푸들, 혹은 검은 털 포인트에 베스트."
    },
    "라벤더 퍼플 (Lavender Purple)": {
        "rgb": (224, 176, 255), "outline": (175, 120, 215), "strap": (195, 150, 230),
        "badge": "#9B51E0", "tone": "Cool Winter", "desc": "고급스럽고 오묘한 매력의 라벤더 퍼플. 몽환적이고 독보적인 분위기 연출."
    }
}

# AI 자동 분석 엔진
def analyze_pet_personal_color(coat_color, eye_color, uploaded_file):
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            img_np = np.array(img.resize((100, 100)))
            avg_color = img_np.mean(axis=(0, 1))
            r, g, b = avg_color[0], avg_color[1], avg_color[2]
            
            if r > b and g > b:
                return "크리밍 핑크 (Creaming Pink)"
            elif b >= r:
                return "스카이 블루 (Sky Blue)"
            else:
                return "민트 그린 (Mint Green)"
        except Exception:
            pass

    # 규칙 기반 AI 진단 폴백
    if coat_color in ["크림/아이보리", "갈색/베이지/골드", "레드/어프리콧"]:
        if eye_color in ["밝은 호박색/브라운", "다크 브라운"]:
            return "크리밍 핑크 (Creaming Pink)"
        else:
            return "파스텔 옐로우 (Pastel Yellow)"
    elif coat_color in ["화이트/순백", "실버/회색"]:
        if eye_color in ["블루/오드아이", "다크 브라운"]:
            return "민트 그린 (Mint Green)"
        else:
            return "라벤더 퍼플 (Lavender Purple)"
    else:
        return "스카이 블루 (Sky Blue)"

# 사이드바 입력 레이아웃 (수동 팔레트 선택 제거됨)
with st.sidebar:
    st.header("⚙️ 댕스널 컬러 프로필 입력")
    
    pet_name = st.text_input("반려동물 이름", value="쪼꼬")
    register_no = st.text_input("동물 등록번호", value="410160013195572")
    phone_no = st.text_input("보호자 연락처", value="010-4674-6229")

    pet_breed = st.selectbox("견종 선택", ["토이푸들", "포메라니안", "말티즈", "비숑 프리제", "시바견", "기타"])
    coat_color = st.selectbox("털색 모체", ["크림/아이보리", "갈색/베이지/골드", "화이트/순백", "실버/회색", "블랙/세이블/믹스"])
    eye_color = st.selectbox("눈동자 색상", ["밝은 호박색/브라운", "다크 브라운", "블루/오드아이"])

    pet_photo = st.file_uploader("📸 반려동물 얼굴 사진 업로드 (AI 정밀 진단용)", type=["jpg", "jpeg", "png"])

    st.divider()
    
    # 생성하기 버튼
    if st.button("✨ AI 분석 및 인식표 생성하기"):
        st.session_state.show_result = True

# 3D 인식표 그래픽 생성 함수
def generate_pro_tag_image(name, reg_num, phone, pal):
    width, height = 650, 650
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    collar_y = 60
    strap_h = 50
    draw.rounded_rectangle([100, collar_y, width - 100, collar_y + strap_h], radius=15, fill=pal["strap"]+(255,), outline=pal["outline"]+(255,), width=3)
    draw.ellipse([width//2 - 20, collar_y + 12, width//2 + 20, collar_y + strap_h - 12], outline=(180, 185, 190, 255), width=6)

    ring_cx, ring_cy = width // 2, collar_y + strap_h + 20
    draw.ellipse([ring_cx - 22, ring_cy - 22, ring_cx + 22, ring_cy + 22], outline=(160, 165, 170, 255), width=6)

    margin = 80
    draw.ellipse([margin+5, margin+20+ring_cy, width - margin+5, height - margin+20+ring_cy], fill=(200, 200, 200, 100))
    draw.ellipse([margin, margin+ring_cy, width - margin, height - margin+ring_cy], fill=pal["rgb"]+(255,), outline=pal["outline"]+(255,), width=8)

    inner_m = 115
    draw.ellipse([inner_m, inner_m+ring_cy, width - inner_m, height - inner_m+ring_cy], fill=(255, 255