import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Streamlit 페이지 기본 설정
st.set_page_config(page_title="댕스널 컬러 인식표 시뮬레이터", layout="centered")

st.title("🐾 댕스널 컬러 & 레진 인식표 시뮬레이터")
st.write("반려동물의 정보와 퍼스널 컬러 베이스를 선택하여 인식표를 시뮬레이션해 보세요!")

# 1. 사이드바 - 사용자 입력
st.sidebar.header("⚙️ 인식표 옵션 설정")
pet_name = st.sidebar.text_input("반려동물 이름", value="쪼꼬")
register_no = st.sidebar.text_input("등록번호", value="410123456789123")
phone_no = st.sidebar.text_input("연락처", value="010-1234-1234")

# 퍼스널 컬러 베이스 색상 선택
color_options = {
    "민트 그린 (Mint Green)": (168, 216, 185),
    "크리밍 핑크 (Creaming Pink)": (244, 194, 194),
    "파스텔 옐로우 (Pastel Yellow)": (254, 236, 168),
    "스카이 블루 (Sky Blue)": (173, 216, 230),
    "라벤더 퍼플 (Lavender Purple)": (224, 176, 255),
    "클리어 무색 (Clear)": (240, 240, 240)
}

selected_color_name = st.sidebar.selectbox("🎨 퍼스널 컬러 베이스 선택", list(color_options.keys()))
base_color = color_options[selected_color_name]

# 2. 인식표 이미지 생성 함수
def generate_tag_image(name, reg_num, phone, color_rgb):
    # 이미지 기본 사이즈 (px)
    width, height = 600, 600
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 1. 베이스 레이어 (선택한 퍼스널 컬러)
    base_margin = 80
    draw.rounded_rectangle(
        [base_margin, base_margin, width - base_margin, height - base_margin],
        radius=60,
        fill=color_rgb + (255,),
        outline=(200, 200, 200, 255),
        width=3
    )

    # 2. 레진 커스텀 각인 레이어 (투명 테두리 효과)
    resin_margin = 100
    draw.rounded_rectangle(
        [resin_margin, resin_margin, width - resin_margin, height - resin_margin],
        radius=45,
        fill=(255, 255, 255, 180),  # 반투명 레진
        outline=(255, 255, 255, 230),
        width=4
    )

    # 3. 텍스트 각인 (이름, 등록번호, 연락처)
    try:
        # 나눔고딕 등 기본 폰트 적용 시도 (실제 환경에 맞게 경로 수정 가능)
        font_name = ImageFont.truetype("arial.ttf", 55)
        font_sub = ImageFont.truetype("arial.ttf", 28)
    except:
        font_name = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 텍스트 중앙 정렬
    draw.text((width / 2, height / 2 - 70), name, fill=(50, 50, 50, 255), font=font_name, anchor="mm")
    draw.text((width / 2, height / 2 + 10), f"NO: {reg_num}", fill=(80, 80, 80, 255), font=font_sub, anchor="mm")
    draw.text((width / 2, height / 2 + 60), f"TEL: {phone}", fill=(80, 80, 80, 255), font=font_sub, anchor="mm")
    draw.text((width / 2, height / 2 + 120), "[ 100% Food-Grade Resin ]", fill=(120, 120, 120, 255), font=font_sub, anchor="mm")

    return img

# 3. 이미지 생성 및 화면 출력
tag_img = generate_tag_image(pet_name, register_no, phone_no, base_color)

# 화면에 시원하게 크게 띄우기 (use_container_width=True 적용)
st.image(
    tag_img, 
    caption=f"✨ {pet_name} 맞춤형 레진 인식표 시뮬레이션 ({selected_color_name})", 
    use_container_width=True
)

st.success("왼쪽 사이드바에서 베이스 색상과 문구를 변경하면 시뮬레이션이 실시간으로 반영됩니다!")