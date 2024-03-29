import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io
import base64

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
gemini_api_key7 = secrets.get("gemini_api_key7")
gemini_api_key8 = secrets.get("gemini_api_key8")

def try_generate_content(api_key, image):
    # API 키를 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(["이 사진은 6학년 학생이 아크릴과 조명으로 만든 무드등입니다. 학생이 그린 그림을 자세히 묘사한 뒤 긍정적으로 평가해주고, AAA규격의 건전지2개로 불빛이 나오는 이 아크릴 무드등의 전기회로 원리를 설명해주세요.", image])
        response.resolve()
        return response
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("핸드폰으로 학생이 그린 작품을 찍어주세요.")

if uploaded_file is not None:
    # 이미지 바이트 문자열로 변환
    img_bytes = uploaded_file.read()

    # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
    img = Image.open(io.BytesIO(img_bytes))

    # 첫 번째 API 키로 시도
    response = try_generate_content(gemini_api_key7, img)
    
    # 첫 번째 API 키 실패 시, 두 번째 API 키로 재시도
    if response is None and gemini_api_key8 is not None:
        print("첫 번째 API 호출에 실패하여 두 번째 API 키로 재시도합니다.")
        response = try_generate_content(gemini_api_key8, img)
    
    # 결과가 성공적으로 반환되었는지 확인
    if response is not None:
        # 결과 표시
        st.image(img)  # 업로드된 사진 출력
        st.markdown(response.text)

        # 이미지 다운로드 버튼 생성
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        st.download_button(label="이미지 다운로드", data=img_bytes.getvalue(), file_name="generated_image.jpg", mime="image/jpeg")
        
        # 텍스트 다운로드 버튼 생성
        st.download_button(label="텍스트 다운로드", data=response.text.encode('utf-8'), file_name="generated_text.txt", mime="text/plain")
        
    else:
        st.markdown("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")
else:
    st.markdown("핸드폰 사진을 업로드하세요.")
