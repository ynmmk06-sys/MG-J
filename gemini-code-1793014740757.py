import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 웹페이지 기본 설정
st.set_page_config(page_title="댕스널 컬러 - AI 퍼스널컬러 & 커스텀 인식표", page_icon="🐾", layout="centered")

st.title("🐾 댕스널 컬러 (Daengsnal Color)")
st.caption("AI 반려동물 퍼스널 컬러 진단 & 식품등급 레진 커스텀 인식표 시뮬레이터")
st.markdown("---")

# 1. 고객 정보 입력란
st.subheader("1. 반려동물 정보 & 사진 업로드")
col1, col2 = st.columns(2)

with col1:
    pet_name = st.text_input("반려동물 이름", "쪼꼬")
    phone_no = st.text_input("보호자 연락처", "010-1234-1234")

with col2:
    reg_no = st.text_input("동물등록번호 (15자리)", "410123456789123")
    uploaded_file = st.file_uploader("반려동물 정면 사진 선택", type=["jpg", "jpeg", "png"])

# 2. 퍼스널컬러 분석 알고리즘 (털색 평균 RGB 분석)
def analyze_personal_color(img):
    img_rgb = img.convert("RGB")
    np_img = np.array(img_rgb)
    h, w, _ = np_img.shape
    crop = np_img[h//4:3*h//4, w//4:3*w//4]
    avg_color = crop.mean(axis=(0, 1))
    r, g, b = avg_color[0], avg_color[1], avg_color[2]
    
    brightness = (r + g + b) / 3
    is_warm = (r > b)
    
    if is_warm and brightness > 120:
        tone = "봄 웜 라이트 (Spring Warm Light)"
        desc = "밝고 화사한 모체색을 가진 아이로, 파스텔 옐로우와 골드 빛 레진이 인상을 더욱 밝게 만듭니다."
        recommended = ["골드 펄 레진", "파스텔 옐로우", "크리스탈 클리어"]
        hex_bg = "#FFE5B4"
    elif is_warm and brightness <= 120:
        tone = "가을 웜 딥 (Autumn Warm Deep)"
        desc = "차분하고 깊이 있는 모체색을 가진 아이로, 엠버 골드와 브론즈 레진이 고급스러운 가치를 높여줍니다."
        recommended = ["엠버 골드 레진", "에메랄드 포레스트", "샤인 브론즈"]
        hex_bg = "#E6C280"
    elif not is_warm and brightness > 120:
        tone = "여름 쿨 라이트 (Summer Cool Light)"
        desc = "맑고 깨끗한 톤을 가진 아이로, 오로라 실버와 파스텔 블루 레진이 인상을 세련되게 살려줍니다."
        recommended = ["오로라 실버 레진", "스카이 파스텔", "라벤더 펄"]
        hex_bg = "#D0E8F2"
    else:
        tone = "겨울 쿨 딥 (Winter Cool Deep)"
        desc = "선명하고 존재감 있는 털색을 가진 아이로, 미드나잇 블루와 인디고 레진이 도회적인 매력을 더해줍니다."
        recommended = ["미드나잇 블루 레진", "딥 펄 와인", "스노우 펄"]
        hex_bg = "#B8C5D6"
        
    return tone, desc, recommended, hex_bg

# 3. 결과 출력 및 인식표 시뮬레이션
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=f"업로드된 {pet_name} 사진", use_container_width=True)
    
    tone, desc, recommended, hex_bg = analyze_personal_color(image)
    
    st.markdown("---")
    st.subheader(f"🎨 {pet_name}의 댕스널 컬러 진단 결과")
    st.success(f"**진단 결과: {tone}**")
    st.info(f"💡 **분석 결과**: {desc}")
    
    st.write("✨ **추천 100% 식품등급 레진 조색 매칭:**")
    for idx, c in enumerate(recommended, 1):
        st.write(f"- {idx}. {c}")
        
    st.markdown("---")
    st.subheader("🏷️ 식품등급 레진 커스텀 인식표 미리보기")
    
    # 인식표 그래픽 시뮬레이션 합성
    tag_img = Image.new("RGBA", (500, 500), (255, 255, 255, 0))
    draw = ImageDraw.Draw(tag_img)
    
    draw.ellipse([50, 50, 450, 450], fill=hex_bg, outline="#FFD700", width=8)
    draw.ellipse([70, 70, 430, 430], outline="#FFFFFF", width=3)
    
    try:
        font_large = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_medium = ImageFont.truetype("DejaVuSans.ttf", 22)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        
    draw.text((250, 160), pet_name, fill="#333333", anchor="ms", font=font_large)
    draw.text((250, 240), f"NO: {reg_no}", fill="#555555", anchor="ms", font=font_medium)
    draw.text((250, 290), f"TEL: {phone_no}", fill="#555555", anchor="ms", font=font_medium)
    draw.text((250, 360), "[ 100% Food-Grade Resin ]", fill="#888888", anchor="ms", font=font_medium)
    
    st.image(tag_img, caption=f"{pet_name} 맞춤형 레진 인식표 시뮬레이션", width=350)
    
    if st.button("🛍️ 이 조합으로 크라우드펀딩 모의 투자의향 제출하기"):
        st.balloons()
        st.success(f"🎉 성공적으로 투자의향이 제출되었습니다! {pet_name}를 위한 특별한 레진 인식표 펀딩 소식을 가장 먼저 전해드릴게요.")