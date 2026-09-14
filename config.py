import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")    
    WHISPER_MODEL = "whisper-large-v3"
    GROQ_MODEL = "openai/gpt-oss-120b"
    
    PAGE_TITLE = "ClaimLens - Live Fact Checker"
    PAGE_ICON = "🎙️"
