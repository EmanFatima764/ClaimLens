"""
Central configuration for ClaimLens.

Reads keys in this order, so the app works both locally and on Streamlit
Community Cloud without any code changes:
    1. Streamlit secrets (st.secrets)  -> used on Streamlit Cloud
    2. Environment variables / .env    -> used for local development
"""

import os

from dotenv import load_dotenv

load_dotenv()  # no-op if there is no .env file, so this is always safe

try:
    import streamlit as st
    _STREAMLIT_AVAILABLE = True
except Exception:
    _STREAMLIT_AVAILABLE = False


def _get_setting(key: str, default: str = "") -> str:
    """Fetch a config value from Streamlit secrets first, then env vars."""
    if _STREAMLIT_AVAILABLE:
        try:
            if key in st.secrets:
                return str(st.secrets[key])
        except Exception:
            pass
    return os.getenv(key, default)


class Config:
    # --- API keys ---
    GROQ_API_KEY: str = _get_setting("GROQ_API_KEY", "")
    TAVILY_API_KEY: str = _get_setting("TAVILY_API_KEY", "")

    # --- Models ---
    WHISPER_MODEL: str = _get_setting("WHISPER_MODEL", "whisper-large-v3")
    GROQ_MODEL: str = _get_setting("GROQ_MODEL", "mixtral-8x7b-32768")

    # --- UI ---
    PAGE_TITLE: str = "ClaimLens - Live Fact Checker"
    PAGE_ICON: str = "🛡️"

    @classmethod
    def missing_keys(cls) -> list[str]:
        """Return a list of required keys that are not configured."""
        missing = []
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        if not cls.TAVILY_API_KEY:
            missing.append("TAVILY_API_KEY")
        return missing
