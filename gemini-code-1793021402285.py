import time

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="댕스널 컬러 & 포 태그(PAW TAG)",
    page_icon="🐾",
    layout="wide",
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
st.markdown("##### 퍼스널 컬러 추천 & 포 태그(PAW TAG)")
st.write("---")

# 퍼스널 컬러 팔레트 정의
COLOR_PALETTES = {
    "크리밍 핑크 (Creaming Pink)": {
        "rgb": (244, 194, 194), "outline": (210, 140, 140), "strap": (230, 170, 170),
        "badge": "#FF8E9E", "tone": "Warm Spring",
        "desc": "포근하고 사랑스러운 웜톤 파스텔 핑크. 하얀 털 및 밝은 갈색 털에 완벽 착붙!",
    },
    "민트 그린 (Mint Green)": {
        "rgb": (168, 216, 185), "outline": (115, 175, 135), "strap": (140, 195, 160),
        "badge": "#4EBE8A", "tone": "Cool Summer",
        "desc": "청량하고 산뜻한 쿨톤 파스텔 그린. 청초하고 맑은 인상을 극대화해줍니다.",
    },
    "파스텔 옐로우 (Pastel Yellow)": {
        "rgb": (254, 236, 168), "outline": (220, 195, 110), "strap": (235, 210, 130),
        "badge": "#E3A820", "tone": "Warm Spring",
        "desc": "화사하고 기분 좋은 햇살 옐로우. 밝은 털빛의 활달한 친구에게 추천!",
    },
    "스카이 블루 (Sky Blue)": {
        "rgb": (173, 216, 230), "outline": (115, 170, 190), "strap": (145, 190, 210),
        "badge": "#4A90E2", "tone": "Cool Summer",
        "desc": "세련되고 신비로운 차분한 쿨 블루. 회색빛, 실버 푸들, 혹은 검은 털 포인트에 베스트.",
    },
    "라벤더 퍼플 (Lavender Purple)": {
        "rgb": (224, 176, 255), "outline": (175, 120, 215), "strap": (195, 150, 230),
        "badge": "#9B51E0", "tone": "Cool Winter",
        "desc": "고급스럽고 오묘한 매력의 라벤더 퍼플. 몽환적이고 독보적인 분위기 연출.",
    },
}

# 털색 -> 팔레트 고정 매칭 (같은 선택이면 항상 같은 결과)
COAT_TO_PALETTE = {
    "크림/아이보리": "크리밍 핑크 (Creaming Pink)",
    "갈색/베이지/골드": "파스텔 옐로우 (Pastel Yellow)",
    "화이트/순백": "민트 그린 (Mint Green)",
    "실버/회색": "스카이 블루 (Sky Blue)",
    "블랙/세이블/믹스": "라벤더 퍼플 (Lavender Purple)",
}
DEFAULT_PALETTE = "크리밍 핑크 (Creaming Pink)"


def analyze_pet_personal_color(coat_color):
    """털색 선택값만으로 결정되므로 사진이 바뀌어도 결과가 변하지 않습니다."""
    return COAT_TO_PALETTE.get(coat_color, DEFAULT_PALETTE)


# ---------- 폰트 / 그리기 도우미 ----------
FONT_CANDIDATES = [
    "NanumGothic.ttf",
    "NanumGothicBold.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/malgun.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleGothic.ttf",
    "DejaVuSans.ttf",
    "arial.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def fit_font(draw, text, max_width, start_size, min_size=22):
    size = start_size
    while size > min_size:
        font = load_font(size)
        try:
            if draw.textlength(text, font=font) <= max_width:
                return font
        except Exception:
            return font
        size -= 2
    return load_font(min_size)


def draw_centered(draw, xy, text, font, fill):
    try:
        draw.text(xy, text, fill=fill, font=font, anchor="mm")
    except (ValueError, TypeError):
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        draw.text((xy[0] - (right - left) / 2, xy[1] - (bottom - top) / 2), text, fill=fill, font=font)


# ---------- 인식표 이미지 생성 ----------
def generate_pro_tag_image(name, reg_num, phone, pal):
    width, height = 650, 700
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 목줄
    collar_y, strap_h = 40, 50
    draw.rounded_rectangle(
        [100, collar_y, width - 100, collar_y + strap_h],
        radius=15, fill=pal["strap"] + (255,), outline=pal["outline"] + (255,), width=3,
    )
    draw.ellipse(
        [width // 2 - 20, collar_y + 12, width // 2 + 20, collar_y + strap_h - 12],
        outline=(180, 185, 190, 255), width=6,
    )

    # 스테인리스 링
    ring_cx, ring_cy = width // 2, collar_y + strap_h + 20
    draw.ellipse([ring_cx - 22, ring_cy - 22, ring_cx + 22, ring_cy + 22], outline=(160, 165, 170, 255), width=6)

    # 태그 본체 (원)
    tag_left, tag_right = 85, width - 85
    tag_top = ring_cy + 15
    tag_bottom = tag_top + (tag_right - tag_left)
    draw.ellipse([tag_left + 5, tag_top + 10, tag_right + 5, tag_bottom + 10], fill=(200, 200, 200, 100))
    draw.ellipse([tag_left, tag_top, tag_right, tag_bottom], fill=pal["rgb"] + (255,), outline=pal["outline"] + (255,), width=8)

    # 안쪽 흰 원
    inner = 35
    draw.ellipse(
        [tag_left + inner, tag_top + inner, tag_right - inner, tag_bottom - inner],
        fill=(255, 255, 255, 210), outline=(255, 255, 255, 240), width=4,
    )

    # 텍스트
    cx = width / 2
    cy = (tag_top + tag_bottom) / 2
    max_text_w = (tag_right - tag_left) - 2 * inner - 40

    font_name = fit_font(draw, name, max_text_w, 54)
    font_sub = fit_font(draw, f"TEL: {phone}", max_text_w, 24, min_size=14)
    font_small = fit_font(draw, "[ 100% Food-Grade Resin ]", max_text_w, 20, min_size=12)

    draw_centered(draw, (cx, cy - 50), name, font_name, (50, 50, 50, 255))
    draw_centered(draw, (cx, cy + 15), f"NO: {reg_num}", font_sub, (70, 70, 70, 255))
    draw_centered(draw, (cx, cy + 55), f"TEL: {phone}", font_sub, (70, 70, 70, 255))
    draw_centered(draw, (cx, cy + 100), "[ 100% Food-Grade Resin ]", font_small, (110, 110, 110, 255))

    return img


# ---------- 사이드바 ----------
def file_signature(f):
    return None if f is None else (f.name, f.size)


with st.sidebar:
    st.header("⚙️ 댕스널 컬러 프로필 입력")

    pet_name = st.text_input("반려동물 이름", value="쪼꼬")
    register_no = st.text_input("동물 등록번호", value="410160013195572")
    phone_no = st.text_input("보호자 연락처", value="010-4674-6229")

    pet_breed = st.selectbox("견종 선택", ["토이푸들", "포메라니안", "말티즈", "비숑 프리제", "시바견", "기타"])
    coat_color = st.selectbox("털색 모체", list(COAT_TO_PALETTE.keys()))
    eye_color = st.selectbox("눈동자 색상", ["밝은 호박색/브라운", "다크 브라운", "블루/오드아이"])

    pet_photo = st.file_uploader("📸 반려동물 얼굴 사진 업로드 (프로필 표시용)", type=["jpg", "jpeg", "png"])

    st.divider()

    current_inputs = (
        pet_name, register_no, phone_no, pet_breed, coat_color, eye_color, file_signature(pet_photo),
    )

    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "animate" not in st.session_state:
        st.session_state.animate = False
    if "last_inputs" not in st.session_state:
        st.session_state.last_inputs = current_inputs

    if st.session_state.last_inputs != current_inputs:
        st.session_state.last_inputs = current_inputs
        st.session_state.show_result = False

    if st.button("✨ 컬러 분석 및 인식표 생성하기"):
        st.session_state.show_result = True
        st.session_state.animate = True

# ---------- 메인 화면 ----------
if not st.session_state.show_result:
    st.markdown("""
        <div class="app-card" style="text-align: center; padding: 60px 20px;">
            <h2>👋 환영합니다!</h2>
            <p style="font-size: 1.1rem; color: #666;">왼쪽 사이드바에서 반려동물 정보를 입력하고 <b>[✨ 컬러 분석 및 인식표 생성하기]</b> 버튼을 눌러주세요!</p>
        </div>
    """, unsafe_allow_html=True)
else:
    if st.session_state.animate:
        with st.spinner(f"🤖 {pet_name}의 모색과 프로필을 분석하여 퍼스널 컬러를 도출 중입니다..."):
            time.sleep(1.2)
        st.session_state.animate = False

    diagnosed_color_name = analyze_pet_personal_color(coat_color)
    palette = COLOR_PALETTES[diagnosed_color_name]

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader(f"🏷️ {pet_name} 맞춤형 3D 인식표 미리보기")
        tag_image = generate_pro_tag_image(pet_name or "PET", register_no, phone_no, palette)
        st.image(tag_image, width=520)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("✨ 퍼스널 컬러 진단 리포트")

        if pet_photo is not None:
            st.image(pet_photo, width=130, caption=f"{pet_name} 프로필 사진")

        st.markdown(
            f'<span class="tone-badge" style="background-color: {palette["badge"]};">진단 톤: {palette["tone"]}</span>',
            unsafe_allow_html=True,
        )
        st.info(
            f"💡 분석 결과, **{pet_name}**에게 가장 잘 어울리는 고유 컬러는 **[{diagnosed_color_name}]** 입니다!\n\n"
            f"{palette['desc']}"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("🎨 맞춤형 컬러 매칭 & 레이어 구조")
        st.markdown(f"""
* **매칭된 팔레트**: **{diagnosed_color_name}**
* **적용 레이어 구조**:
  * Layer 1: 고경도 UV 스크래치 방지 코팅
  * Layer 2: 식품등급 퓨어진 (순수 클리어 레진)
  * Layer 3: **맞춤형 퍼스널 컬러 베이스 & 테두리**
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
                st.success(
                    f"🎉 감사합니다, {backer_name}님! [{pet_name}] 맞춤형 [{diagnosed_color_name}] "
                    f"인식표 모의 투자의향이 접수되었습니다."
                )
            else:
                st.warning("⚠️ 서포터 성함을 입력해 주세요!")
    st.markdown('</div>', unsafe_allow_html=True)
