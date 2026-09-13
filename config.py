import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")    
    WHISPER_MODEL = "whisper-large-v3"
    GROQ_MODEL = "llama-3.3-70b-versatile"
    
    PAGE_TITLE = "AI Pitch Auditor - Live Fact Checker"
    PAGE_ICON = "🎙️"
