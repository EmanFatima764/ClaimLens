import streamlit as st
from config import Config
from services import STTService, ClaimExtractor, SearchService, FactChecker

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Pitch Auditor",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

def create_new_chat():
    st.session_state.messages = []
    st.session_state.current_chat_id = None
    st.rerun()

def load_chat(chat_id):
    for chat in st.session_state.saved_chats:
        if chat["id"] == chat_id:
            st.session_state.messages = chat["messages"].copy()
            st.session_state.current_chat_id = chat_id
            st.rerun()

def save_current_session(user_title, messages_list):
    if st.session_state.current_chat_id is None:
        new_id = len(st.session_state.saved_chats) + 1
        st.session_state.current_chat_id = new_id
        st.session_state.saved_chats.append({
            "id": new_id,
            "title": user_title,
            "messages": messages_list.copy()
        })
    else:
        for chat in st.session_state.saved_chats:
            if chat["id"] == st.session_state.current_chat_id:
                chat["messages"] = messages_list.copy()

# ==========================================
# 3. SIDEBAR (CHAT HISTORY & CONTROLS)
# ==========================================
with st.sidebar:
    st.title("🛡️ Pitch Auditor")
    
    if st.button("➕ New Audit", use_container_width=True):
        create_new_chat()

    st.divider()

    st.subheader("📜 Chats")
    if not st.session_state.saved_chats:
        st.caption("No saved chats.")
    else:
        for chat in reversed(st.session_state.saved_chats):
            if st.button(f"💬 {chat['title']}", key=f"chat_{chat['id']}", use_container_width=True):
                load_chat(chat["id"])

    st.divider()
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.saved_chats = []
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.title("AI Pitch Auditor")
st.write("Paste your claim, record audio, or upload a pitch file to audit.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Standard Inputs (File & Mic)
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])
with col2:
    recorded_audio = st.audio_input("Record Audio Pitch")

# Chat Input Bar
prompt = st.chat_input("Paste claim or ask here...")

# ==========================================
# 5. AUDIT & FACT CHECK LOGIC
# ==========================================
if prompt or uploaded_file or recorded_audio:
    user_text = prompt if prompt else ("🎙️ [Voice Audio]" if recorded_audio else f"📁 {uploaded_file.name}")
    audio_source = recorded_audio or uploaded_file

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Processing pitch and checking facts..."):
            transcript = ""
            if audio_source:
                stt = STTService()
                transcript = stt.transcribe_audio(audio_source)
            else:
                transcript = prompt.strip() if prompt else ""

            if not transcript:
                st.error("No clear speech or text input found.")
                st.stop()

            extractor = ClaimExtractor()
            claims = extractor.extract_claims(transcript)

            response_markdown = ""
            if not claims:
                response_markdown = "No verifiable factual claims were found."
                st.info(response_markdown)
            else:
                searcher = SearchService()
                checker = FactChecker()

                for item in claims:
                    claim_text = item.get("claim", "")
                    if claim_text:
                        search_res = searcher.search_claim(claim_text)
                        verdict_info = checker.verify_claim(claim_text, search_res)
                        
                        verdict = verdict_info.get("verdict", "UNVERIFIED")
                        explanation = verdict_info.get("explanation", "")
                        sources = verdict_info.get("sources", [])
                        sources_str = ", ".join(sources) if sources else "None"

                        card = f"**Claim:** \"{claim_text}\"\n\n" \
                               f"**Verdict:** `{verdict}` | **Category:** {item.get('category', 'General')}\n\n" \
                               f"**Explanation:** {explanation}\n\n" \
                               f"**Sources:** {sources_str}\n"

                        response_markdown += card + "\n---\n"

                        if verdict == "TRUE":
                            st.success(card)
                        elif verdict == "FALSE":
                            st.error(card)
                        else:
                            st.warning(card)

        st.session_state.messages.append({"role": "assistant", "content": response_markdown})

        
        # Save to Sidebar History
        title = user_text[:25] + "..." if len(user_text) > 25 else user_text
        save_current_session(title, st.session_state.messages)
