import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Streamlit 페이지 설정 (모바일 앱 스타일 감성)
st.set_page_config(
    page_title="댕스널 컬러 & 레진 인식표 시뮬레이터", 
    page_icon="🐾", 
    layout="centered"
)

# 커스텀 CSS 적용 (모바일 앱 카드 스타일 및 세련된 UI)
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 52px;
        font-weight: bold;
        font-size: 16px;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff5252 0%, #ff7630 100%);
        color: white;
    }
    div.stSelectbox, div.stTextInput {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.title("🐾 댕스널 컬러 진단 & 레진 인식표")
st.markdown("##### 우리 아이 모색과 눈동자에 딱 맞는 퍼스널 컬러 베이스를 찾아보세요!")
st.divider()

# 사이드바 옵션 설정
st.sidebar.header("⚙️ 댕스널 컬러 & 커스텀 설정")

# 반려동물 정보 입력
pet_name = st.sidebar.text_input("반려동물 이름", value="쪼꼬")
register_no = st.sidebar.text_input("동물 등록번호", value="410160013195572")
phone_no = st.sidebar.text_input("보호자 연락처", value="010-4674-6229")

# 반려동물 사진 업로드 (선택사항)
pet_photo = st.sidebar.file_uploader("📸 반려동물 얼굴 사진 업로드", type=["jpg", "jpeg", "png"])

st.sidebar.divider()
st.sidebar.subheader("🎨 퍼스널 컬러 베이스 선택")

# 퍼스널 컬러 팔레트 (베이스, 테두리, 목줄 연동 톤)
color_options = {
    "크리밍 핑크 (Creaming Pink)": {
        "base": (244, 194, 194),
        "outline": (210, 150, 150),
        "strap": (230, 170, 170),
        "desc": "따뜻하고 화사한 웜톤 코랄 베이스로 사랑스러움을 극대화합니다."
    },
    "민트 그린 (Mint Green)": {
        "base": (168, 216, 185),
        "outline": (120, 175, 140),
        "strap": (140, 195, 160),
        "desc": "청량하고 싱그러운 파스텔 민트 톤으로 시원한 인상을 줍니다."
    },
    "파스텔 옐로우 (Pastel Yellow)": {
        "base": (254, 236, 168),
        "outline": (210, 185, 110),
        "strap": (235, 210, 130),
        "desc": "발랄하고 생기 넘치는 밝은 노란빛으로 활력을 불어넣습니다."
    },
    "스카이 블루 (Sky Blue)": {
        "base": (173, 216, 230),
        "outline": (120, 170, 195),
        "strap": (145, 190, 210),
        "desc": "맑고 차분한 청량감을 주는 쿨톤 블루 베이스입니다."
    },
    "라벤더 퍼플 (Lavender Purple)": {
        "base": (224, 176, 255),
        "outline": (175, 130, 210),
        "strap": (195, 150, 230),
        "desc": "몽환적이고 우아한 무드의 파스텔 퍼플 톤입니다."
    }
}

selected_color_name = st.sidebar.selectbox("추천 베이스 팔레트", list(color_options.keys()))
palette = color_options[selected_color_name]

# 메인 화면 구성 (2열 레이아웃)
col1, col2 = st.columns([1.1, 0.9])

with col1:
    st.subheader(f"🏷️ {pet_name} 맞춤형 3D 인식표 미리보기")
    
    # 3D 레이어 인식표 그래픽 생성 함수
    def generate_pro_tag_image(name, reg_num, phone, pal):
        width, height = 650, 650
        img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # 0. 매칭 목줄/스트랩 라인 프리뷰 (상단 고리 형태)
        strap_color = pal["strap"] + (255,)
        draw.rounded_rectangle([250, 25, 400, 65], radius=15, fill=strap_color, outline=(100, 100, 100, 200), width=2)
        draw.ellipse([310, 55, 340, 85], outline=(150, 150, 150, 255), width=5) # 메탈 링

        # 1. 베이스 레이어 (선택한 퍼스널 컬러 및 연동 테두리)
        margin = 70
        base_color = pal["base"] + (255,)
        outline_color = pal["outline"] + (255,)
        
        # 입체 그림자 효과
        draw.ellipse([margin+5, margin+15, width - margin+5, height - margin+15], fill=(220, 220, 220, 150))
        # 메인 베이스 원
        draw.ellipse([margin, margin, width - margin, height - margin], fill=base_color, outline=outline_color, width=8)

        # 2. 식품등급 퓨어진 레진 레이어 (반투명 아크릴/레진 질감)
        inner_margin = 105
        draw.ellipse([inner_margin, inner_margin, width - inner_margin, height - inner_margin], fill=(255, 255, 255, 200), outline=(255, 255, 255, 240), width=4)

        # 3. 금박 글리터 효과 뿌리기
        np.random.seed(77)
        for _ in range(35):
            gx = np.random.randint(inner_margin + 30, width - inner_margin - 30)
            gy = np.random.randint(inner_margin + 30, height - inner_margin - 30)
            draw.ellipse([gx, gy, gx + 4, gy + 4], fill=(218, 165, 32, 220)) # 골드 글리터

        # 4. 각인 텍스트 삽입
        try:
            font_name = ImageFont.truetype("arial.ttf", 48)
            font_sub = ImageFont.truetype("arial.ttf", 22)
        except:
            font_name = ImageFont.load_default()
            font_sub = ImageFont.load_default()

        # 텍스트 중앙 정렬 렌더링
        draw.text((width / 2, height / 2 - 55), name, fill=(50, 50, 50, 255), font=font_name, anchor="mm")
        draw.text((width / 2, height / 2 + 15), f"NO: {reg_num}", fill=(70, 70, 70, 255), font=font_sub, anchor="mm")
        draw.text((width / 2, height / 2 + 55), f"TEL: {phone}", fill=(70, 70, 70, 255), font=font_sub, anchor="mm")
        draw.text((width / 2, height / 2 + 100), "[ 100% Food-Grade Resin ]", fill=(120, 120, 120, 255), font=font_sub, anchor="mm")

        return img

    # 이미지 생성 및 출력
    tag_image = generate_pro_tag_image(pet_name, register_no, phone_no, palette)
    st.image(tag_image, use_container_width=True)

with col2:
    st.subheader("✨ AI 진단 리포트 & 컬러 매칭")
    
    if pet_photo:
        st.image(pet_photo, caption=f"업로드된 {pet_name}의 프로필 사진", width=180)
    else:
        st.info("💡 사이드바에서 반려동물 사진을 올리면 모색 정밀 분석이 가능합니다!")
        
    st.markdown(f"""
    * **선택된 컬러**: **{selected_color_name}**
    * **컬러 특징**: {palette['desc']}
    * **적용 레이어**: 
      * Layer 1: 고경도 UV 스크래치 방지 코팅
      * Layer 2: 퓨어진 + 금박 글리터 각인
      * Layer 3: **퍼스널 컬러 맞춤형 베이스 & 테두리**
      * Layer 4: 초경량 스테인리스 링 & 매칭 스트랩
    """)
    
    st.success("🎯 아이의 털 색상과 완벽하게 조화되는 톤온톤 매칭이 적용되었습니다!")

st.divider()

# 크라우드펀딩 모의 투자 신청 섹션
st.subheader("🚀 댕스널 컬러 인식표 크라우드펀딩 참여")
st.write("본 시뮬레이션에서 조합하신 세상에 단 하나뿐인 인식표로 사전 투자의향을 남겨보세요!")

with st.form("funding_form"):
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        backer_name = st.text_input("서포터 성함", placeholder="홍길동")
    with f_col2:
        backer_email = st.text_input("이메일 주소", placeholder="example@email.com")
        
    pledge_quantity = st.slider("참여 수량 선택", 1, 5, 1)
    
    submitted = st.form_submit_button("🛍️ 이 조합으로 크라우드펀딩 모의 투자의향 제출하기")
    if submitted:
        if backer_name:
            st.balloons()
            st.success(f"🎉 감사합니다, {backer_name}님! [{pet_name}] 맞춤형 [{selected_color_name}] 인식표 {pledge_quantity}개의 모의 투자의향이 성공적으로 접수되었습니다.")
        else:
            st.warning("⚠️ 서포터 성함을 입력해 주세요!")