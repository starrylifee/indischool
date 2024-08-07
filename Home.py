import streamlit as st

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

# 홈 페이지의 타이틀 설정
st.title('초등학생용 인공지능도구 모음')

# 애플리케이션 소개
st.markdown("""
    ## 🌟 안녕하세요!
    이 애플리케이션은 여러 가지 인공지능 도구들을 모아 놓은 곳입니다.
""")

# 추가적인 정보 제공
st.markdown("""
    ## 🚀 시작하기
    왼쪽의 탐색 바를 사용하여 원하는 도구를 선택하고 사용해 보세요.  '>' 표시를 누르면 인공지능 도구 리스트가 나옵니다.
""")

# 구글 폼 링크 추가
st.markdown("""
    ## 📝 인공지능 수업 도구 의뢰
    특별한 인공지능 수업 도구가 필요하신가요?  직접 제작해드리겠습니다.  [이곳을 클릭](https://forms.gle/HC8ePNYhQzoX2Mio9)하여 구글 폼에 접속해 주세요.
""", unsafe_allow_html=True)

# 도구 1: 내 작품 평가 받기
st.subheader('(미술) 작품 평가받기')
st.write('이 도구를 사용하면 내가 그린 그림의 제목을 추천해주고, 장점과 보완할 점을 알려줍니다.')

# 도구 2: 반론 생성기
st.subheader('(국어) 반론생성기')
st.write('이 도구를 사용하면 나의 주장과 근거에 따른 반론을 예상해 줍니다.')

# 도구 3: 아이디어 생성기
st.subheader('(실과) 발명아이디어생성 보조도구')
st.write('이 도구를 사용하면 특정 물건에 대한 불편한 점을 생성해줍니다.')