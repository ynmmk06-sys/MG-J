import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import io
import math

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM STYLING (MOBILE APP THEME)
# ==============================================================================
st.set_page_config(
    page_title="댕스널 컬러 - AI 퍼스널컬러 & 레진 인식표 시뮬레이터",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, mobile-app aesthetic with soft pastel tones
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* App background setup */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #edf2f7 100%);
    }
    
    /* Card Container UI */
    .app-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
        border: 1px solid #eef2f6;
        margin-bottom: 20px;
    }
    
    /* Gradient Headers */
    .gradient-header {
        background: linear-gradient(135deg, #FF8E9E 0%, #FF6B8B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2rem;
    }
    
    /* Personal Color Result Badge */
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
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eef2f6;
    }
    
    /* Button Customization */
    .stButton>button {
        border-radius: 14px;
        background: linear-gradient(135deg, #FF7B9C 0%, #FF477E 100%);
        color: white;
        font-weight: 700;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 16px rgba(255, 71, 126, 0.25);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 71, 126, 0.35);
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. COLOR PALETTES & AI DIAGNOSIS ENGINE
# ==============================================================================
COLOR_PALETTES = {
    "크리밍 핑크 (Creaming Pink)": {
        "rgb": (244, 194, 194),
        "dark_rgb": (210, 140, 140),
        "tone_type": "Warm Spring",
        "badge_color": "#FF8E9E",
        "desc": "포근하고 사랑스러운 웜톤 파스텔 핑크. 하얀 털 및 밝은 갈색 털에 완벽 착붙!"
    },
    "민트 그린 (Mint Green)": {
        "rgb": (168, 216, 185),
        "dark_rgb": (115, 175, 135),
        "tone_type": "Cool Summer",
        "badge_color": "#4EBE8A",
        "desc": "청량하고 산뜻한 쿨톤 파스텔 그린. 청초하고 맑은 인상을 극대화해줍니다."
    },
    "파스텔 옐로우 (Pastel Yellow)": {
        "rgb": (254, 236, 168),
        "dark_rgb": (220, 195, 110),
        "tone_type": "Warm Spring",
        "badge_color": "#E3A820",
        "desc": "화사하고 기분 좋은 햇살 오렌지-옐로우. 밝은 털빛의 활달한 친구에게 추천!"
    },
    "스카이 블루 (Sky Blue)": {
        "rgb": (173, 216, 230),
        "dark_rgb": (115, 170, 190),
        "tone_type": "Cool Summer",
        "badge_color": "#4A90E2",
        "desc": "세련되고 신비로운 차분한 쿨 블루. 회색빛, 실버 푸들, 혹은 검은 털 포인트에 베스트."
    },
    "라벤더 퍼플 (Lavender Purple)": {
        "rgb": (224, 176, 255),
        "dark_rgb": (175, 120, 215),
        "tone_type": "Cool Winter",
        "badge_color": "#9B51E0",
        "desc": "고급스럽고 오묘한 매력의 라벤더 퍼플. 몽환적이고 독보적인 분위기 연출."
    }
}

def analyze_pet_personal_color(coat_color, eye_color, uploaded_file):
    """
    Analyzes pet profile parameters or image input to return recommended base color.
    """
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            img_np = np.array(img.resize((100, 100)))
            avg_color = img_np.mean(axis=(0, 1))
            r, g, b = avg_color[0], avg_color[1], avg_color[2]
            
            # Simple warmth check from image average
            if r > b and g > b:
                return "크리밍 핑크 (Creaming Pink)", "Warm Spring"
            elif b >= r:
                return "스카이 블루 (Sky Blue)", "Cool Summer"
            else:
                return "민트 그린 (Mint Green)", "Cool Summer"
        except Exception:
            pass

    # Rule-based decision fallback
    if coat_color in ["크림/아이보리", "갈색/베이지/골드", "레드/어프리콧"]:
        if eye_color in ["밝은 호박색/브라운", "다크 브라운"]:
            return "크리밍 핑크 (Creaming Pink)", "Warm Spring"
        else:
            return "파스텔 옐로우 (Pastel Yellow)", "Warm Spring"
    elif coat_color in ["화이트/순백", "실버/회색"]:
        if eye_color in ["블루/오드아이", "다크 브라운"]:
            return "민트 그린 (Mint Green)", "Cool Summer"
        else:
            return "라벤더 퍼플 (Lavender Purple)", "Cool Winter"
    else:  # 블랙/세이블/믹스
        return "스카이 블루 (Sky Blue)", "Cool Summer"


# ==============================================================================
# 3. HIGH-PRECISION 3D LAYER RENDERING ENGINE
# ==============================================================================
def render_3d_resin_tag(name, reg_num, phone, base_color_name):
    """
    Renders 4-Layer 3D Resin Tag & Collar Assembly with exact color synchronization.
    Layer 1: UV Anti-Scratch High-Gloss Light Glare
    Layer 2: Food-Grade Purezin & Custom Engraving with Gold Glitter
    Layer 3: Personal Color Adjusted Base
    Layer 4: Stainless Ring & Leather Collar Harness
    """
    palette = COLOR_PALETTES[base_color_name]
    rgb = palette["rgb"]
    dark_rgb = palette["dark_rgb"]
    
    width, height = 900, 750
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # -------------------------------------------------------------
    # LAYER 4 (PART A): Synchronized Leather Collar Harness
    # -------------------------------------------------------------
    collar_y = 100
    strap_height = 55
    
    # Collar Base Shadow
    draw.rounded_rectangle([80, collar_y + 10, width - 80, collar_y + strap_height + 10], radius=18, fill=(0, 0, 0, 25))
    # Main Leather Strap (Color-matched)
    draw.rounded_rectangle([80, collar_y, width - 80, collar_y + strap_height], radius=18, fill=rgb + (255,), outline=dark_rgb + (255,), width=3)
    # Leather Stitching Line
    draw.rounded_rectangle([90, collar_y + 6, width - 90, collar_y + strap_height - 6], radius=12, outline=(255, 255, 255, 180), width=2)
    # Metal Buckle Ring on Collar
    buckle_x = width // 2
    draw.ellipse([buckle_x - 30, collar_y + 12, buckle_x + 30, collar_y + strap_height - 12], outline=(190, 195, 200, 255), width=8)

    # -------------------------------------------------------------
    # LAYER 4 (PART B): Stainless Steel Split Ring Connection
    # -------------------------------------------------------------
    ring_cx, ring_cy = width // 2, collar_y + strap_height + 25
    draw.ellipse([ring_cx - 28, ring_cy - 28, ring_cx + 28, ring_cy + 28], outline=(160, 165, 170, 255), width=7)
    draw.ellipse([ring_cx - 22, ring_cy - 22, ring_cx + 22, ring_cy + 22], outline=(220, 225, 230, 255), width=4)

    # -------------------------------------------------------------
    # LAYER 3: Personal Color Base Shell (3D Rounded Rectangle)
    # -------------------------------------------------------------
    bx, by = width // 2 - 250, ring_cy + 20
    bw, bh = 500, 380
    
    # 3D Soft Ambient Shadow
    for shadow_offset in range(15, 0, -3):
        alpha = int(25 - shadow_offset * 1.5)
        draw.rounded_rectangle(
            [bx - shadow_offset, by + 10 + shadow_offset, bx + bw + shadow_offset, by + bh + 10 + shadow_offset],
            radius=55, fill=(0, 0, 0, alpha)
        )

    # 3D Depth Edge Layer (Darker tone offset)
    draw.rounded_rectangle([bx, by + 14, bx + bw, by + bh + 14], radius=55, fill=dark_rgb + (255,))
    # Main Personal Color Base Layer
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=55, fill=rgb + (255,))
    # Inner Soft Bevel Highlight
    draw.rounded_rectangle([bx + 4, by + 4, bx + bw - 4, by + bh - 4], radius=52, outline=(255, 255, 255, 140), width=3)

    # -------------------------------------------------------------
    # LAYER 2: Purezin Crystal Glass & Custom Engraving Layer
    # -------------------------------------------------------------
    rx, ry = bx + 25, by + 25
    rw, rh = bw - 50, bh - 50
    
    # Semi-transparent Purezin Shell
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=42, fill=(255, 255, 255, 195), outline=(255, 255, 255, 240), width=4)

    # Golden Glitter Particles Simulation
    np.random.seed(101)  # Fixed aesthetic seed
    for _ in range(65):
        gx = np.random.randint(rx + 20, rx + rw - 20)
        gy = np.random.randint(ry + 20, ry + rh - 20)
        gsize = np.random.randint(2, 6)
        gold_shade = np.random.choice([(255, 215, 0), (238, 201, 0), (255, 223, 118), (218, 165, 32)])
        draw.ellipse([gx, gy, gx + gsize, gy + gsize], fill=gold_shade + (220,))

    # Engraved Typography
    try:
        font_title = ImageFont.truetype("arial.ttf", 52)
        font_sub = ImageFont.truetype("arial.ttf", 26)
        font_tag = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_title = font_sub = font_tag = ImageFont.load_default()

    draw.text((width // 2, ry + 75), name, fill=(35, 35, 35, 255), font=font_title, anchor="mm")
    draw.text((width // 2, ry + 155), f"NO. {reg_num}", fill=(70, 70, 70, 255), font=font_sub, anchor="mm")
    draw.text((width // 2, ry + 205), f"TEL. {phone}", fill=(70, 70, 70, 255), font=font_sub, anchor="mm")
    draw.text((width // 2, ry + 265), "✨ [ 100% Food-Grade Purezin ] ✨", fill=(110, 110, 110, 255), font=font_tag, anchor="mm")

    # -------------------------------------------------------------
    # LAYER 1: UV Anti-Scratch & Anti-Yellowing Gloss Coating
    # -------------------------------------------------------------
    # Glass glare diagonal highlights
    glare_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glare_overlay)
    
    # Curved top light glare
    gdraw.polygon([
        (rx + 30, ry + 10), (rx + rw - 120, ry + 10),
        (rx + rw - 200, ry + 110), (rx + 10, ry + 110)
    ], fill=(255, 255, 255, 55))
    
    img = Image.alpha_composite(img, glare_overlay)
    return img


# ==============================================================================
# 4. APPLICATION UI & CONTROLLERS
# ==============================================================================
def main():
    # Header Banner
    st.markdown('<h1 class="gradient-header">🐾 댕스널 컬러 (Pet Personal Color)</h1>', unsafe_allow_html=True)
    st.markdown("##### AI 퍼스널 컬러 진단 & 4층 입체 레진 인식표 실시간 시뮬레이터")
    st.write("---")

    # Layout Split: Left Controls, Right Preview
    col_input, col_preview = st.columns([1, 1.25], gap="large")

    with col_input:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("1. 반려동물 프로필 입력")
        
        pet_name = st.text_input("🐶 반려동물 이름", value="쪼꼬")
        
        col_id1, col_id2 = st.columns(2)
        with col_id1:
            register_no = st.text_input("인식 등록번호", value="410160013195572")
        with col_id2:
            phone_no = st.text_input("보호자 연락처", value="010-1234-5678")

        pet_breed = st.selectbox(
            "견종 / 묘종 선택",
            ["토이푸들", "포메라니안", "말티즈", "비숑 프리제", "시바견", "골든 리트리버", "믹스견", "기타"]
        )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            coat_color = st.selectbox("털색 (모체색)", ["크림/아이보리", "갈색/베이지/골드", "화이트/순백", "실버/회색", "블랙/세이블/믹스"])
        with col_c2:
            eye_color = st.selectbox("눈동자 색상", ["밝은 호박색/브라운", "다크 브라운", "블루/오드아이"])

        uploaded_photo = st.file_uploader("📸 반려동물 사진 업로드 (선택 - AI 자동진단)", type=["jpg", "png", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

        # AI Color Diagnosis Logic
        rec_color_name, rec_tone = analyze_pet_personal_color(coat_color, eye_color, uploaded_photo)

        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("2. AI 퍼스널 컬러 진단 결과")
        
        badge_hex = COLOR_PALETTES[rec_color_name]["badge_color"]
        st.markdown(
            f'<span class="tone-badge" style="background-color: {badge_hex};">AI 추천: {rec_tone}</span>',
            unsafe_allow_html=True
        )
        st.info(f"💡 **{pet_name}**에게 가장 잘 어울리는 색상은 **[{rec_color_name}]** 입니다!\n\n{COLOR_PALETTES[rec_color_name]['desc']}")

        # Color Selector override
        selected_color_name = st.selectbox(
            "🎨 레진 베이스 & 목줄 색상 수동 변경",
            list(COLOR_PALETTES.keys()),
            index=list(COLOR_PALETTES.keys()).index(rec_color_name)
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("3. 3D 레진 인식표 실시간 시뮬레이션")
        st.caption("선택하신 퍼스널 컬러에 맞춰 인식표 베이스, 테두리 및 목줄 하네스 색상이 유기적으로 연동됩니다.")

        # Render Graphic
        rendered_image = render_3d_resin_tag(pet_name, register_no, phone_no, selected_color_name)
        
        # Responsive container width display
        st.image(rendered_image, use_container_width=True)

        # Layer Details Accordion
        with st.expander("🔍 인식표 4층 입체 구조 (Layer Specification) 상세보기"):
            st.markdown("""
            * **Layer 1 (표면)**: 고경도 UV Anti-Scratch & 황변 방지 무색 투명 고광택 코팅.
            * **Layer 2 (중앙)**: 식품등급(Food-Grade) 퓨어진(Purezin) & 24K 금박 글리터 커스텀 각인 레이어.
            * **Layer 3 (베이스)**: AI 댕스널 컬러 맞춤 파스텔 조색 베이스 층.
            * **Layer 4 (연결)**: 초경량 고강도 스테인리스 모듈형 연결고리 & 컬러 매칭 가죽 목줄.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Crowdfunding Simulation Form Card
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("🚀 크라우드펀딩 모의 투자 의향 제출")
        st.write("이 디자인 조합으로 제작되는 프리미엄 인식표 펀딩에 참여할 의향이 있으신가요?")
        
        pledge_tier = st.select_slider(
            "희망 펀딩 패키지 선택",
            options=["단품 (인식표)", "세트 (인식표 + 가죽목줄)", "프리미엄 (인식표 + 목줄 + 리드줄)"]
        )
        
        if st.button("🎁 이 조합으로 모의 투자 의향 제출하기"):
            st.balloons()
            st.success(f"🎉 **{pet_name}** 보호자님! [{selected_color_name}] {pledge_tier} 모의 투자 의향이 성공적으로 접수되었습니다!")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
```

```text:Requirements:requirements.txt
streamlit
numpy
pillow