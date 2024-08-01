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
st.write("수업시간에만 사용합니다. ")


# 끝
st.write("인공지능과 함께 하는 과학수업")
