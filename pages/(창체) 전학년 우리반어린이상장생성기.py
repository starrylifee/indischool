"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ')

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent / "secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
gemini_api_key3 = secrets.get("gemini_api_key3")
gemini_api_key4 = secrets.get("gemini_api_key4")

def try_generate_content(api_key, prompt_parts):
    # API 키를 설정
    genai.configure(api_key=api_key)
    
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config={
                                      "temperature": 1,
                                      "top_p": 0.95,
                                      "top_k": 64,
                                      "max_output_tokens": 8192,
                                      "response_mime_type": "text/plain",
                                  })
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("재치있는 상장명과 문구 생성기")

input_text = st.text_area("친구의 좋은점이나 함께 놀았던 추억을 적어보세요.:", "")

if st.button("상장명과 문구 생성"):
    prompt_parts = [
        "초등학생에게 평소 생활을 반영하는 상장을 수여하고자 합니다. 입력의 내용을 참고하여 재치있는 상장명과 문구를 생성해주세요.",
        "input: 민수는 체육대회에서 친구들과 함께 열심히 뛰면서 서로 응원하고 도와주었어요.",
        "output 2: 운동장 히어로상: 민수는 체육대회에서 친구들과 함께 열심히 뛰면서 서로 응원하고 도와주었던 것을 기리기 위해 이 상장을 수여합니다. 친구들과의 돈독한 우정을 칭찬합니다.",
        "input: 지수는 우리 반 친구들과 함께 과학 프로젝트를 준비하며 많은 시간을 함께 보냈고, 결국 좋은 성과를 거두었어요.",
        "output 2: 과학 마법사상: 지수는 과학 프로젝트를 준비하며 친구들과 협력하여 좋은 성과를 거두었습니다. 협동심과 노력하는 모습을 높이 평가합니다.",
        "input: 소라는 새 학기에 전학 온 친구를 반 친구들과 함께 도와주고 학교 생활에 적응할 수 있도록 도왔어요.",
        "output 2: 친절 요정상: 소라는 전학 온 친구를 도와주고 학교 생활에 잘 적응하도록 도왔습니다. 친절하고 배려심 깊은 모습을 칭찬합니다.",
        "input: 영호는 친구가 어려운 일을 겪을 때 옆에서 함께 이야기하고 위로해 주었어요.",
        "output 2: 마음 히어로상: 영호는 친구가 어려운 일을 겪을 때 옆에서 이야기하고 위로해 준 것을 인정하여 이 상장을 수여합니다. 따뜻한 마음과 위로하는 자세를 칭찬합니다.",
        "input: 나연이는 시험 기간 동안 친구와 함께 도서관에서 공부하며 서로 격려하고 도움을 주었어요.",
        "output 2: 공부 파트너상: 나연이는 시험 기간 동안 친구와 함께 도서관에서 공부하며 서로 격려하고 도움을 주었습니다. 함께 공부하는 자세와 친구를 돕는 마음을 칭찬합니다.",
        "input: 민호는 학교에서 매일 쓰레기를 주워 환경을 깨끗하게 유지하려고 노력했어요.",
        "output 2: 환경 지킴이 슈퍼스타상: 민호는 학교에서 매일 쓰레기를 주워 환경을 깨끗하게 유지하려고 노력한 것을 인정하여 이 상장을 수여합니다. 환경을 아끼는 마음을 높이 평가합니다.",
        "input: 은지는 매일 아침 일찍 등교하여 반 친구들을 위해 칠판을 깨끗이 지워주었어요.",
        "output 2: 조기 출석 청소 요정상: 은지는 매일 아침 일찍 등교하여 반 친구들을 위해 칠판을 깨끗이 지워주었습니다. 친구들을 위한 봉사와 헌신적인 자세를 칭찬합니다.",
        "input: 재훈이는 수업 시간에 항상 발표를 열심히 하고 친구들의 질문에 친절하게 답해주었어요.",
        "output 2: 발표왕: 재훈이는 수업 시간에 항상 발표를 열심히 하고 친구들의 질문에 친절하게 답해주었습니다. 적극적인 학습 태도와 도움의 정신을 칭찬합니다.",
        "input: 수현이는 친구들과 함께 놀 때 항상 규칙을 잘 지키고 모두가 즐거울 수 있도록 했어요.",
        "output 2: 놀이 천재상: 수현이는 친구들과 함께 놀 때 항상 규칙을 잘 지키고 모두가 즐거울 수 있도록 노력한 것을 인정하여 이 상장을 수여합니다. 놀이의 즐거움과 규칙을 잘 지키는 모습을 칭찬합니다.",
        "input: 윤호는 학교 도서관에서 책을 많이 읽고, 친구들에게 재미있는 책을 추천해 주었어요.",
        "output 2: 책벌레 챔피언상: 윤호는 학교 도서관에서 책을 많이 읽고, 친구들에게 재미있는 책을 추천해 준 것을 인정하여 이 상장을 수여합니다. 독서의 즐거움을 나누는 자세를 칭찬합니다.",
        "input: 용석이는 급식실에서 내가 먹고 싶은 음식을 줬어요",
        "output 2: 급식실 천사상: 용석이는 급식실에서 친구가 먹고 싶은 음식을 챙겨주는 따뜻한 마음을 가진 친구입니다! 친구를 배려하는 마음씨에 감동했어요!",
        f"input: {input_text}",
        "output 2: ",
    ]
    
    # 첫 번째 API 키로 시도
    response_text = try_generate_content(gemini_api_key3, prompt_parts)
    
    # 첫 번째 API 키 실패 시, 두 번째 API 키로 재시도
    if response_text is None and gemini_api_key4 is not None:
        print("첫 번째 API 호출에 실패하여 두 번째 API 키로 재시도합니다.")
        response_text = try_generate_content(gemini_api_key4, prompt_parts)
    
    # 결과 출력
    if response_text is not None:
        st.markdown(to_markdown(response_text))
    else:
        st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")
