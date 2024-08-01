import streamlit as st

# 업로드된 파일 목록
files = [
    {"name": "test.py", "path": "/mnt/data/test.py"},
    {"name": "test2.py", "path": "/mnt/data/test2.py"},
    {"name": "test3.py", "path": "/mnt/data/test3.py"},
    {"name": "test4.py", "path": "/mnt/data/test4.py"},
    {"name": "test5.py", "path": "/mnt/data/test5.py"},
    {"name": "test6.py", "path": "/mnt/data/test6.py"},
    {"name": "code1.py", "path": "/mnt/data/1 code1.py"},
    {"name": "code2.py", "path": "/mnt/data/2 code2.py"},
]

# Streamlit 앱 시작
st.title("열정강선생님과 함께하는 수업")
st.write("중학교 3학년 과학수업 자료")
st.write("업로드된 파일들의 목록과 각 파일에 대한 간단한 설명을 제공합니다.")


# 끝
st.write("이 페이지를 통해 파일들에 대한 기본 정보를 확인할 수 있습니다. 각 파일의 내용을 확인하려면 직접 열어보세요!")
