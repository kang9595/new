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
def generate_science_topic(api_key, subject):
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
    학생이 입력한 내용을 바탕으로 과학탐구주제를 만들어줘:

    과목: {subject}

    과학탐구주제:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("과학탐구주제 추천")

# 앱 사용법 설명 추가
st.markdown("""
이 앱은 분야에 맞는 과학탐구 주제를 추천해줍니다.

### 사용법:
1. 드롭다운 메뉴에서 분야를 선택하세요.
2. '추천' 버튼을 클릭하세요.
3. 추천된 과학탐구 주제가 화면에 표시됩니다.
""")

# 사용자 입력 받기
subject = st.selectbox("분야를 선택하세요.", ["물리", "화학", "생물", "지학"])

if st.button("추천"):
    # API 키로 과학탐구주제 생성 시도
    science_topic = generate_science_topic(api_key, subject)

    # 결과 출력
    if science_topic is not None:
        st.markdown(to_markdown(science_topic))
    else:
        st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.") 

# 제작자 이름 추가
st.markdown("<small>제작자: kang</small>", unsafe_allow_html=True)
