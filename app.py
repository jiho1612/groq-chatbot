import streamlit as st
from groq import Groq

# ==============================
# 기본 설정
# ==============================
st.set_page_config(page_title="FAST 챗봇 AI", page_icon="⚡")
st.title("⚡ FAST 챗봇 AI")
st.caption("초고속 Groq API 기반 나만의 AI 챗봇")

# ==============================
# Groq 클라이언트
# ==============================
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ==============================
# 사이드바 설정
# ==============================
with st.sidebar:
    st.header("⚙️ 챗봇 설정")

    # 역할 선택
    role_option = st.selectbox(
        "🎭 역할 선택",
        [
            "코딩 선생님",
            "AI 전문가",
            "아이디어 기획자",
            "블로그 작가",
            "자유 대화 모드"
        ]
    )

    # ==============================
    # ✅ 응답 스타일 (버튼 클릭 방식으로 변경)
    # ==============================
    st.markdown("### 📝 응답 스타일 선택")

    col1, col2 = st.columns(2)

    if col1.button("🔍 간단하게"):
        st.session_state.style_option = "🔍 간단하게"

    if col1.button("📖 자세하게"):
        st.session_state.style_option = "📖 자세하게"

    if col2.button("🧑‍🏫 초보자용"):
        st.session_state.style_option = "🧑‍🏫 초보자용"

    if col2.button("🚀 전문가용"):
        st.session_state.style_option = "🚀 전문가용"

    # 기본값 설정
    if "style_option" not in st.session_state:
        st.session_state.style_option = "🔍 간단하게"

    style_option = st.session_state.style_option

    # 고성능 모드 토글
    high_performance = st.toggle("🚀 고성능 모드 (70B 모델 사용)")

    # 대화 초기화 버튼
    if st.button("🗑️ 대화 내용 지우기"):
        st.session_state.messages = []
        st.success("대화가 초기화되었습니다!")

# ==============================
# 역할 프롬프트 구성
# ==============================

role_prompts = {
    "코딩 선생님": "너는 코딩을 아주 쉽게 알려주는 친절한 선생님이야.",
    "AI 전문가": "너는 인공지능과 머신러닝을 전문적으로 설명하는 전문가야.",
    "아이디어 기획자": "너는 창의적인 아이디어를 잘 제안하는 기획자야.",
    "블로그 작가": "너는 가독성 좋게 글을 작성하는 블로그 작가야.",
    "자유 대화 모드": "너는 친근하고 똑똑한 AI야."
}

style_prompts = {
    "🔍 간단하게": "답변은 핵심만 짧고 간단하게 해줘.",
    "📖 자세하게": "답변은 최대한 자세하고 구체적으로 설명해줘.",
    "🧑‍🏫 초보자용": "완전 초보자도 이해할 수 있도록 아주 쉽게 설명해줘.",
    "🚀 전문가용": "전문 용어를 사용해서 깊이 있게 설명해줘."
}

system_prompt = role_prompts[role_option] + " " + style_prompts[style_option]

# ==============================
# 모델 선택 (최신 모델)
# ==============================
model_name = "llama-3.1-8b-instant"

if high_performance:
    model_name = "llama-3.1-70b-versatile"

# ==============================
# 세션 상태 초기화
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# 이전 대화 출력
# ==============================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================
# 질문 자동 추천 버튼
# ==============================
st.markdown("### 💡 추천 질문")

col1, col2, col3 = st.columns(3)

if col1.button("파이썬 반복문 쉽게 설명해줘"):
    st.session_state.auto_prompt = "파이썬 반복문 쉽게 설명해줘"

if col2.button("Streamlit 기본 구조 알려줘"):
    st.session_state.auto_prompt = "Streamlit 기본 구조 알려줘"

if col3.button("AI 챗봇 만드는 방법 알려줘"):
    st.session_state.auto_prompt = "AI 챗봇 만드는 방법 알려줘"

# ==============================
# 사용자 입력
# ==============================
user_input = st.chat_input("무엇이든 물어보세요!")

# 자동 질문 처리
if "auto_prompt" in st.session_state:
    user_input = st.session_state.auto_prompt
    del st.session_state.auto_prompt

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": system_prompt}]
                     + st.session_state.messages
        )

        ai_reply = response.choices[0].message.content
        st.markdown(ai_reply)

    # AI 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )