import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Streamlit 페이지 기본 설정
st.set_page_config(page_title="댕스널 컬러 인식표 시뮬레이터", layout="centered")

st.title("🏷️ 식품등급 레진 커스텀 인식표 미리보기")
st.write("반려동물의 정보와 퍼스널 컬러 베이스를 선택하여 인식표를 시뮬레이션해 보세요!")

# 1. 사이드바 - 사용자 입력
st.sidebar.header("⚙️ 인식표 옵션 설정")
pet_name = st.sidebar.text_input("반려동물 이름", value="쪼꼬")
register_no = st.sidebar.text_input("등록번호", value="410160013195572")
phone_no = st.sidebar.text_input("연락처", value="010-4674-6229")

# 퍼스널 컬러 베이스 색상 선택
color_options = {
    "파스텔 옐로우 (Pastel Yellow)": (254, 236, 168),
    "크리밍 핑크 (Creaming Pink)": (244, 194, 194),
    "민트 그린 (Mint Green)": (168, 216, 185),
    "스카이 블루 (Sky Blue)": (173, 216, 230),
    "라벤더 퍼플 (Lavender Purple)": (224, 176, 255)
}

selected_color_name = st.sidebar.selectbox("🎨 퍼스널 컬러 베이스 선택", list(color_options.keys()))
base_color = color_options[selected_color_name]

# 2. 원형 인식표 이미지 생성 함수
def generate_tag_image(name, reg_num, phone, color_rgb):
    width, height = 600, 600
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 1. 베이스 레이어 (선택한 퍼스널 컬러 - 원형)
    margin = 60
    draw.ellipse(
        [margin, margin, width - margin, height - margin],
        fill=color_rgb + (255,),
        outline=(230, 200, 100, 255),
        width=5
    )

    # 2. 내부 레진 레이어 (안쪽 원)
    inner_margin = 90
    draw.ellipse(
        [inner_margin, inner_margin, width - inner_margin, height - inner_margin],
        fill=(255, 255, 255, 180),  # 반투명 레진 느낌
        outline=(255, 255, 255, 230),
        width=3
    )

    # 3. 텍스트 각인
    try:
        font_name = ImageFont.truetype("arial.ttf", 45)
        font_sub = ImageFont.truetype("arial.ttf", 24)
    except:
        font_name = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 텍스트 중앙 배치
    draw.text((width / 2, height / 2 - 60), name, fill=(60, 60, 60, 255), font=font_name, anchor="mm")
    draw.text((width / 2, height / 2 + 10), f"NO: {reg_num}", fill=(80, 80, 80, 255), font=font_sub, anchor="mm")
    draw.text((width / 2, height / 2 + 55), f"TEL: {phone}", fill=(80, 80, 80, 255), font=font_sub, anchor="mm")
    draw.text((width / 2, height / 2 + 105), "[ 100% Food-Grade Resin ]", fill=(110, 110, 110, 255), font=font_sub, anchor="mm")

    return img

# 3. 이미지 생성 및 화면 출력 (크기 확대)
tag_img = generate_tag_image(pet_name, register_no, phone_no, base_color)

st.image(
    tag_img, 
    caption=f"{pet_name} 맞춤형 레진 인식표 시뮬레이션", 
    use_container_width=True
)

# 모의 투자 의향 버튼 예시
if st.button("🛍️ 이 조합으로 크라우드펀딩 모의 투자의향 제출하기"):
    st.balloons()
    st.success(f"'{pet_name}'의 [{selected_color_name}] 인식표 모의 투자의향이 성공적으로 제출되었습니다! 감사합니다.")