import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

# few-shot 프롬프트 구성 함수 수정
def generate_science_topic(api_key, topic):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 256,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    )
    prompt = f"""
    중학교 3학년 학생이 입력한 내용을 바탕으로 과학탐구주제를 만들어줘:

    주제: {topic}

    예시 주제:
    1. 주제: 체세포 분열
       설명: 체세포 분열이란 세포가 두 개의 동일한 딸세포로 나뉘는 과정입니다. 예를 들어, 피부 세포가 손상되었을 때 체세포 분열이 일어나 새로운 피부 세포가 만들어집니다.
    2. 주제: 생식세포 분열
       설명: 생식세포 분열은 정자와 난자가 만들어지는 과정입니다. 예를 들어, 생식세포 분열을 통해 부모의 유전자가 자식에게 전달됩니다.
    3. 주제: 발생
       설명: 발생은 수정란이 성체로 성장하는 과정입니다. 예를 들어, 개구리의 알이 올챙이를 거쳐 성체 개구리로 성장하는 과정을 연구할 수 있습니다.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("과학탐구주제 추천")

# 사용자 입력 받기
topic = st.selectbox("주제를 선택하세요.", ["체포 분열이 필요한 이유", "체세포 분열", "생식세포 분열", "발생"])

if st.button("추천"):
    # API 키로 과학탐구주제 생성 시도
    science_topic = generate_science_topic(api_key, topic)

    # 결과 출력
    if science_topic is not None:
        st.markdown(to_markdown(science_topic))
    else:
        st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 제작자 이름 표시
st.sidebar.write("제작자: passsionkang")

