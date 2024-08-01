import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyAd_MdoezucSMvvAv-BFL2XzxqtTsyQ3EQ"

# few-shot 프롬프트 구성 함수 수정
def try_generate_content(api_key, prompt):
    # API 키를 설정
    genai.configure(api_key=api_key)
   
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config={
                                      "temperature": 0.7,
                                      "top_p": 1,
                                      "top_k": 50,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

def extract_score(feedback):
    # 피드백에서 점수 추출 (임의의 방식으로 추출 예제)
    score_line = [line for line in feedback.split('\n') if '점수' in line]
    if score_line:
        try:
            score = int(score_line[0].split()[-1])
            return score
        except:
            return None
    return None

st.title("세포 분열과 발생 논술 평가 도구 📝")

st.markdown("""
학생이 세포 분열(체세포 분열, 생식세포 분열)과 발생에 대해 학습한 내용을 바탕으로,
'한 개의 세포가 어떻게 사람이 될까?'라는 주제로 논술을 작성하고 피드백을 받는 도구입니다.
""")

input_text = st.text_area("논술을 작성하세요:", height=300)

if st.button("평가하기"):
    if input_text.strip() == "":
        st.warning("논술을 입력해주세요!")
    else:
        st.info("논술을 평가 중입니다... 잠시만 기다려주세요...")
        
        # 프롬프트 구성
        prompt = f"학생이 작성한 다음 논술을 평가하고, 25점 만점으로 점수를 매기고, 피드백을 제공해주세요:\n\n{input_text}\n\n"
        
        # 평가 결과 생성
        feedback = try_generate_content(api_key, prompt)
        
        if feedback:
            st.success("논술 평가가 완료되었습니다!")
            st.markdown(to_markdown(feedback))
            
            # 점수 추출 및 표시
            score = extract_score(feedback)
            if score is not None:
                st.write(f"점수: {score} / 25")
            else:
                st.warning("점수를 추출할 수 없습니다.")
        else:
            st.error("논술 평가에 실패했습니다. 다시 시도해주세요.")
