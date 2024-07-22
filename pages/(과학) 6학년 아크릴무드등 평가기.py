import pathlib
import textwrap
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
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

# 코드 구조 및 가독성 개선
def to_markdown(text):
    return textwrap.indent(text.replace('•', '*'), '> ')

# secrets.toml 파일 경로 간소화
secrets_path = pathlib.Path(__file__).resolve().parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기 및 API 키 값 가져오기
def load_secrets():
    with open(secrets_path, "r") as f:
        return toml.load(f)

secrets = load_secrets()
gemini_api_key7 = secrets.get("gemini_api_key7")
gemini_api_key8 = secrets.get("gemini_api_key8")

# 안전 설정을 포함한 콘텐츠 생성 시도 함수
def try_generate_content(api_key, uploaded_file):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    img_bytes = uploaded_file.getvalue()
    image_parts = {
        "mime_type": "image/jpeg",
        "data": img_bytes
    }

    prompt_parts = [
        "이 사진은 학생이 아크릴과 조명으로 만든 무드등입니다. 학생이 그린 그림을 자세히 묘사한 뒤 긍정적으로 평가해주고, AAA규격의 건전지 2개로 불빛이 나오는 이 아크릴 무드등의 전기회로 원리를 설명해주세요.:\n",
        image_parts,
    ]

    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"API 호출 실패: {e}"

# 스트림릿 UI 설정
st.title("아크릴 무드등 활동")

uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "jpeg", "png"])

# 스트림릿 UI 설정과 응답 처리 로직 업데이트
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("잠시만 기다리십시오"):
        # 첫 번째 API 키를 사용하여 시도
        response_text = try_generate_content(gemini_api_key7, uploaded_file)
        
        # 첫 번째 API 키로 실패했을 경우 두 번째 키로 재시도
        if not response_text or "API 호출 실패" in response_text:
            response_text = try_generate_content(gemini_api_key8, uploaded_file)

    if response_text and not "API 호출 실패" in response_text:
        st.write(to_markdown(response_text))
    else:
        st.error("텍스트 생성에 실패했습니다.")
