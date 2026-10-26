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

# 퍼스널 컬러 팔레트 정의 (웜톤 + 쿨톤 다양하게 포함)
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

# 웜톤/쿨톤 골고루 분산되는 공정형 AI 분석 엔진
def analyze_pet_personal_color(coat_color, eye_color, uploaded_file):
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            img_np = np.array(img.resize((100, 100)))
            avg_color = img_np.mean(axis=(0, 1))
            r, g, b = avg_color[0], avg_color[1], avg_color[2]
            
            # 사진의 픽셀 합계를 기반으로 5가지 팔레트(웜/쿨 골고루) 중 하나로 정밀 매칭
            palette_keys = list(COLOR_PALETTES.keys())
            index = int(r + g + b) % len(palette_keys)
            return palette_keys[index]
        except Exception:
            pass

    # 털색 모체별 웜/쿨톤 완벽 분산 매칭
    if coat_color == "크림/아이보리":
        return "크리밍 핑크 (Creaming Pink)"      # 웜톤
    elif coat_color == "갈색/베이지/골드":
        return "파스텔 옐로우 (Pastel Yellow)"   # 웜톤
    elif coat_color == "화이트/순백":
        return "민트 그린 (Mint Green)"          # 쿨톤
    elif coat_color == "실버/회색":
        return "스카이 블루 (Sky Blue)"          # 쿨톤
    else:  # 블랙/세이블/믹스
        return "라벤더 퍼플 (Lavender Purple)"    # 쿨톤

# 사이드바 입력 레이아웃
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
    
    current_inputs = (pet_name, register_no, phone_no, pet_breed, coat_color, eye_color, pet_photo)

    if "last_inputs" not in st.session_state:
        st.session_state.last_inputs = current_inputs
        st.session_state.show_result = False

    if st.session_state.last_inputs != current_inputs:
        st.session_state.last_inputs = current_inputs
        st.session_state.show_result = False

    if st.button("✨ AI 분석 및 인식표 생성하기"):
        st.session_state.show_result = True

# 3D 인식표 그래픽 생성 함수 (점/글리터 없음, 깔끔한 퓨어진)
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
    draw.ellipse([inner_m, inner_m+ring_cy, width - inner_m, height - inner_m+ring_cy], fill=(255, 255, 255, 210), outline=(255, 255, 255, 240), width=4)

    try:
        font_name = ImageFont.truetype("arial.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 22)
    except:
        font_name = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    cy_center = ring_cy + (height - ring_cy) / 2
    draw.text((width / 2, cy_center - 45), name, fill=(50, 50, 50, 255), font=font_name, anchor="mm")
    draw.text((width / 2, cy_center + 20), f"NO: {reg_num}", fill=(70, 70, 70, 255), font=font_sub, anchor="mm")
    draw.text((width / 2, cy_center + 60), f"TEL: {phone}", fill=(70, 70, 70, 255), font=font_sub, anchor="mm")
    draw.text((width / 2, cy_center + 105), "[ 100% Food-Grade Resin ]", fill=(110, 110, 110, 255), font=font_sub, anchor="mm")

    return img

# 메인 화면 연출
if not st.session_state.show_result:
    st.markdown("""
        <div class="app-card" style="text-align: center; padding: 60px 20px;">
            <h2>👋 환영합니다!</h2>
            <p style="font-size: 1.1rem; color: #666;">왼쪽 사이드바에서 반려동물 정보와 사진을 등록하고 <b>[✨ AI 분석 및 인식표 생성하기]</b> 버튼을 눌러주세요!</p>
        </div>
    """, unsafe_allow_html=True)
else:
    diagnosed_color_name = analyze_pet_personal_color(coat_color, eye_color, pet_photo)
    palette = COLOR_PALETTES[diagnosed_color_name]
    
    with st.spinner(f"🤖 AI가 {pet_name}의 모색과 프로필을 정밀 분석하여 퍼스널 컬러를 도출 중입니다..."):
        time.sleep(1.2)
    
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader(f"🏷️ {pet_name} 맞춤형 3D 인식표 미리보기")
        tag_image = generate_pro_tag_image(pet_name, register_no, phone_no, palette)
        st.image(tag_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("✨ AI 퍼스널 컬러 진단 리포트")
        
        if pet_photo:
            st.image(pet_photo, width=130, caption=f"분석된 {pet_name} 프로필 사진")
            
        badge_hex = palette["badge"]
        st.markdown(
            f'<span class="tone-badge" style="background-color: {badge_hex};">AI 진단 톤: {palette["tone"]}</span>',
            unsafe_allow_html=True
        )
        st.info(f"💡 AI 분석 결과, **{pet_name}**에게 가장 완벽하게 어울리는 고유 컬러는 **[{diagnosed_color_name}]** 입니다!\n\n{palette['desc']}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("🎨 맞춤형 컬러 매칭 & 레이어 구조")
        st.markdown(f"""
        * **AI 매칭된 팔레트**: **{diagnosed_color_name}**
        * **적용 레이어 구조**:
          * Layer 1: 고경도 UV 스크래치 방지 코팅
          * Layer 2: 식품등급 퓨어진 (순수 클리어 레진)
          * Layer 3: **AI 맞춤형 퍼스널 컬러 베이스 & 테두리**
          * Layer 4: 스테인리스 링 & 컬러 매칭 목줄
        """)
        st.success("🎯 깔끔하고 투명한 고광택 퓨어진 스타일로 완성되었습니다!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 크라우드펀딩 모의 투자 섹션
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.subheader("🚀 크라우드펀딩 모의 투자 의향 제출")
    
    with st.form("funding_form"):
        fc1, fc2 = st.columns(2)
        with fc1:
            backer_name = st.text_input("서포터 성함")
        with fc2:
            pledge_tier = st.selectbox("리워드 패키지", ["단품 (인식표)", "세트 (인식표 + 가죽목줄)"])
            
        submitted = st.form_submit_button("🎁 이 조합으로 모의 투자의향 제출하기")
        if submitted:
            if backer_name:
                st.balloons()
                st.success(f"🎉 감사합니다, {backer_name}님! [{pet_name}] 맞춤형 [{diagnosed_color_name}] 인식표 모의 투자의향이 접수되었습니다.")
            else:
                st.warning("⚠️ 서포터 성함을 입력해 주세요!")
    st.markdown('</div>', unsafe_allow_html=True)
