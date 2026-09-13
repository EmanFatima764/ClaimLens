import streamlit as st
from config import Config
from services import STTService, ClaimExtractor, SearchService, FactChecker
import logging

# ==========================================
# 0. LOGGING SETUP
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ClaimLens",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1A. STARTUP CONFIG CHECK
# ==========================================
_missing = Config.missing_keys()
if _missing:
    st.error(
        "⚠️ **ClaimLens is not fully configured.** Missing: "
        + ", ".join(f"`{k}`" for k in _missing)
        + "\n\nOn Streamlit Cloud: **App settings → Secrets** and add:\n"
        + "```toml\nGROQ_API_KEY = \"...\"\nTAVILY_API_KEY = \"...\"\n```\n"
        + "Locally: add the same values to a `.env` file in the project root."
    )
    st.stop()

# ==========================================
# 1B. GLOBAL STYLING (visual only — no logic here)
# ==========================================
st.markdown("""
<style>

    /* ---------- Base ---------- */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 0%, #131722 0%, #0b0d13 55%, #0a0c11 100%);
    }

    /* ---------- Hide default chrome ---------- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12141c 0%, #0d0f16 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.04);
        color: #e6e8ef;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        text-align: left;
        transition: all 0.15s ease-in-out;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(124, 137, 255, 0.15);
        border: 1px solid rgba(124, 137, 255, 0.45);
        color: #ffffff;
        transform: translateX(2px);
    }

    /* ---------- Hero header ---------- */
    .hero-wrap {
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(99,102,241,0.18) 0%, rgba(16,185,129,0.08) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.4rem;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #f5f6fa;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        color: #9aa0b4;
        font-size: 1rem;
        margin-top: 0.35rem;
    }
    .hero-badges {
        margin-top: 0.9rem;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .hero-badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.28rem 0.7rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        color: #c7cbe0;
    }

    /* ---------- Input area card ---------- */
    .input-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.1rem 1.2rem 0.4rem 1.2rem;
        margin-bottom: 1rem;
    }
    .input-card-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #8b90a8;
        margin-bottom: 0.6rem;
    }

    /* ---------- Chat bubbles ---------- */
    div[data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 0.4rem 0.2rem;
        margin-bottom: 0.6rem;
    }

    /* ---------- Verdict cards (rendered via markdown) ---------- */
    .verdict-card {
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
    }
    .verdict-claim {
        font-size: 1.02rem;
        font-weight: 600;
        color: #f0f1f7;
        margin-bottom: 0.5rem;
    }
    .verdict-pill {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        margin-right: 0.5rem;
        text-transform: uppercase;
    }
    .pill-true { background: rgba(16,185,129,0.18); color: #34d399; border: 1px solid rgba(52,211,153,0.4);}    
    .pill-false { background: rgba(239,68,68,0.18); color: #f87171; border: 1px solid rgba(248,113,113,0.4);}    
    .pill-unverified { background: rgba(245,158,11,0.18); color: #fbbf24; border: 1px solid rgba(251,191,36,0.4);}    
    .verdict-category {
        font-size: 0.78rem;
        color: #9aa0b4;
        font-weight: 500;
    }
    .verdict-explanation {
        margin-top: 0.6rem;
        color: #cdd0de;
        font-size: 0.93rem;
        line-height: 1.5;
    }
    .verdict-sources {
        margin-top: 0.6rem;
        font-size: 0.8rem;
        color: #7d8299;
    }

    /* ---------- Divider ---------- */
    .soft-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
    """BUG FIX: Reset state properly before rerun"""
    st.session_state.messages = []
    st.session_state.current_chat_id = None
    st.rerun()

def load_chat(chat_id):
    """BUG FIX: Add validation for chat_id"""
    if not isinstance(chat_id, (int, str)):
        logger.error(f"Invalid chat_id type: {type(chat_id)}")
        st.error("Invalid chat ID.")
        return
        
    for chat in st.session_state.saved_chats:
        if chat.get("id") == chat_id:
            # BUG FIX: Safely copy messages, check if it's a list
            messages = chat.get("messages", [])
            if isinstance(messages, list):
                st.session_state.messages = messages.copy()
            else:
                logger.warning(f"Chat messages not a list for chat_id {chat_id}")
                st.session_state.messages = []
            st.session_state.current_chat_id = chat_id
            st.rerun()
            return
    
    logger.warning(f"Chat not found with id: {chat_id}")

def save_current_session(user_title, messages_list):
    """BUG FIX: Validate input parameters"""
    if not isinstance(user_title, str) or not user_title.strip():
        logger.warning("Invalid user_title provided to save_current_session")
        user_title = "Untitled Audit"
    
    if not isinstance(messages_list, list):
        logger.error(f"messages_list must be a list, got {type(messages_list)}")
        return
    
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
            if chat.get("id") == st.session_state.current_chat_id:
                chat["messages"] = messages_list.copy()
                break

# ==========================================
# 3. SIDEBAR (CHAT HISTORY & CONTROLS)
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 0.6rem 0 1rem 0;">
            <div style="font-size: 2.2rem;">🛡️</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #f5f6fa;">ClaimLens</div>
            <div style="font-size: 0.8rem; color: #8b90a8;">AI-powered fact checking</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("➕  New Audit", use_container_width=True):
        create_new_chat()

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.78rem; font-weight:700; text-transform:uppercase; '
        'letter-spacing:0.06em; color:#8b90a8; margin-bottom:0.5rem;">📜 Chat History</div>',
        unsafe_allow_html=True
    )
    if not st.session_state.saved_chats:
        st.caption("No saved chats yet — start an audit above.")
    else:
        # BUG FIX: Safely iterate with validation
        for chat in reversed(st.session_state.saved_chats):
            chat_title = chat.get("title", "Untitled")[:40]  # Truncate to prevent UI overflow
            if st.button(f"💬  {chat_title}", key=f"chat_{chat.get('id')}", use_container_width=True):
                load_chat(chat.get("id"))

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

    if st.button("🗑️  Clear History", use_container_width=True):
        st.session_state.saved_chats = []
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.markdown(
    """
    <div class="hero-wrap">
        <p class="hero-title">🛡️ ClaimLens</p>
        <p class="hero-sub">Paste a claim, record your pitch, or upload an audio file — I'll extract the factual claims and check them for you.</p>
        <div class="hero-badges">
            <span class="hero-badge">🎙️ Voice input</span>
            <span class="hero-badge">📁 File upload</span>
            <span class="hero-badge">🔍 Live fact-checking</span>
            <span class="hero-badge">✅ Verdict scoring</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Display Chat History
for message in st.session_state.messages:
    # BUG FIX: Validate message structure
    if not isinstance(message, dict):
        logger.warning(f"Skipping invalid message format: {type(message)}")
        continue
        
    role = message.get("role", "user")
    content = message.get("content", "")
    
    if not content:
        logger.warning("Empty message content found")
        continue
    
    avatar = "🧑‍💼" if role == "user" else "🛡️"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

# Standard Inputs (File & Mic)
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-card-label">Provide your pitch</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📁 Upload Audio File", type=["mp3", "wav", "m4a"])
with col2:
    recorded_audio = st.audio_input("🎙️ Record Audio Pitch")
st.caption("Supports MP3, WAV, M4A — up to ~25MB / a few minutes of audio.")
st.markdown('</div>', unsafe_allow_html=True)

# Chat Input Bar
prompt = st.chat_input("Paste claim or ask here...")

# ==========================================
# 5. AUDIT & FACT CHECK LOGIC
# ==========================================
if prompt or uploaded_file or recorded_audio:
    # BUG FIX: Validate inputs before processing
    if prompt and not isinstance(prompt, str):
        st.error("Invalid prompt input.")
        st.stop()
    
    # BUG FIX: Determine input source safely
    if prompt:
        user_text = prompt.strip()
        audio_source = None
    elif recorded_audio:
        user_text = "🎙️ [Voice Audio]"
        audio_source = recorded_audio
    elif uploaded_file:
        user_text = f"📁 {uploaded_file.name}"
        audio_source = uploaded_file
    else:
        st.error("No input provided.")
        st.stop()

    # BUG FIX: Check for empty text input
    if not user_text or not user_text.strip():
        st.error("Please provide some input.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.write(user_text)

    with st.chat_message("assistant", avatar="🛡️"):
        with st.spinner("🔎 Processing pitch and checking facts..."):
            transcript = ""
            
            try:
                # BUG FIX: Handle audio transcription with proper error handling
                if audio_source:
                    stt = STTService()
                    transcript = stt.transcribe_audio(audio_source)
                    if not transcript or not isinstance(transcript, str):
                        st.error("Failed to transcribe audio. Please try again.")
                        logger.error(f"Invalid transcription result: {type(transcript)}")
                        st.stop()
                else:
                    transcript = prompt.strip() if prompt else ""

                if not transcript or not transcript.strip():
                    st.error("No clear speech or text input found.")
                    st.stop()

                # BUG FIX: Extract claims with error handling
                extractor = ClaimExtractor()
                claims = extractor.extract_claims(transcript)
                
                if not isinstance(claims, list):
                    st.error("Failed to extract claims from input.")
                    logger.error(f"Claims extraction returned non-list: {type(claims)}")
                    st.stop()

                response_markdown = ""
                
                if not claims:
                    response_markdown = "No verifiable factual claims were found."
                    st.info(response_markdown)
                else:
                    # BUG FIX: Initialize services once, with error handling
                    try:
                        searcher = SearchService()
                        checker = FactChecker()
                    except Exception as e:
                        st.error(f"Failed to initialize services: {str(e)}")
                        logger.error(f"Service initialization error: {e}")
                        st.stop()

                    # BUG FIX: Process each claim with robust error handling
                    for idx, item in enumerate(claims):
                        try:
                            # Validate claim structure
                            if not isinstance(item, dict):
                                logger.warning(f"Claim {idx} is not a dict, skipping")
                                continue
                            
                            claim_text = item.get("claim", "")
                            if not claim_text or not isinstance(claim_text, str):
                                logger.warning(f"Invalid claim text at index {idx}")
                                continue
                            
                            claim_category = item.get("category", "General Fact")
                            if not isinstance(claim_category, str):
                                claim_category = "General Fact"

                            # BUG FIX: Search with error handling
                            search_res = searcher.search_claim(claim_text)
                            if not isinstance(search_res, list):
                                logger.warning(f"Search returned non-list for claim: {claim_text}")
                                search_res = []

                            # BUG FIX: Verify claim with error handling
                            verdict_info = checker.verify_claim(claim_text, search_res)
                            if not isinstance(verdict_info, dict):
                                logger.warning(f"Verdict info is not a dict for claim: {claim_text}")
                                verdict_info = {
                                    "verdict": "UNVERIFIED",
                                    "explanation": "Could not verify claim.",
