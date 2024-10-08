import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io

hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
gemini_api_key1 = secrets.get("gemini_api_key1")
gemini_api_key2 = secrets.get("gemini_api_key2")

def try_generate_content(api_key, image):
    # API 키를 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(["이 사진은 화석표본입니다. 화석의 이름을 말해주고, 현재 존재한 동물 중 유사한 생김새를 가진 동물을 말해주세요. 해당 생물이 살았던 환경도 묘사해주세요.", image])
        response.resolve()
        return response
    except Exception as e:
        # 예외 발생 시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("핸드폰으로 화석표본을 가로로 예쁘게 찍어주세요.", type=["jpg", "jpeg", "png"])

# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
    # 이미지 바이트 문자열로 변환
    img_bytes = uploaded_file.read()

    # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
    img = Image.open(io.BytesIO(img_bytes))

    with st.spinner("잠시만 기다리십시오"):
        # 첫 번째 API 키로 시도
        response = try_generate_content(gemini_api_key1, img)
        
        # 첫 번째 API 키 실패 시, 두 번째 API 키로 재시도
        if response is None and gemini_api_key2 is not None:
            print("첫 번째 API 호출에 실패하여 두 번째 API 키로 재시도합니다.")
            response = try_generate_content(gemini_api_key2, img)
    
    # 결과가 성공적으로 반환되었는지 확인
    if response is not None:
        # 결과 표시
        st.image(img)  # 업로드된 사진 출력
        st.markdown(response.text)
    else:
        st.markdown("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")
else:
    st.markdown("핸드폰 사진을 업로드하세요.")
