<!-- =============================================== -->
<!-- AI PITCH AUDITOR - README -->
<!-- =============================================== -->

# 🛡️ AI Pitch Auditor

**Real-time AI-powered fact-checking for startup pitches**

Live Demo: [ai-pitch-auditor-eyxbove2nm5qwnjhatmzeq.streamlit.app](https://ai-pitch-auditor-eyxbove2nm5qwnjhatmzeq.streamlit.app/)

---

## ✨ Overview

**AI Pitch Auditor** is an intelligent fact-checking system designed to audit startup pitch claims in real-time. It uses advanced AI models to extract factual statements from pitch transcripts and verify them against live internet search evidence—helping investors, entrepreneurs, and pitch evaluators identify accurate and misleading claims instantly.

**Perfect for:**
- 🎤 Pitch competitions and accelerator demos
- 📊 Investor due diligence
- 🏢 Corporate presentations
- 📈 Funding applications
- 🎯 Pitch validation and improvement

---

## 🎯 Key Features

### 🎙️ **Multi-Modal Input**
- **Text Input**: Paste written claims directly
- **Voice Recording**: Record pitches using your microphone
- **Audio Upload**: Upload pre-recorded MP3, WAV, or M4A files
- **Real-Time Transcription**: Powered by Groq Whisper-V3

### 🔍 **Intelligent Claim Extraction**
- Extracts **8 claim categories**:
  - 💰 Financial (Revenue, ARR/MRR, Pricing)
  - 📈 Traction (Users, Customers, Partnerships)
  - 🚀 Growth (Growth %, YoY metrics)
  - 🎯 Market Size (TAM, SAM, SOM)
  - 💵 Funding (Rounds, Valuations)
  - ⚡ Performance (Accuracy, Speed, Conversion)
  - 📚 Industry Facts (Statistics, Research)
  - 📋 General Facts (Other verifiable claims)

- **Filters out**:
  - Opinions and subjective statements
  - Future goals and hypotheticals
  - Generic marketing language
  - Plans vs. actual achievements

### ✅ **Real-Time Fact Verification**
- Searches live internet evidence using Tavily API
- AI-powered verdict scoring: **TRUE | FALSE | MIXED | UNVERIFIED**
- Confidence scoring (0.0 - 1.0)
- Source attribution with URLs
- Detailed explanations for each verdict

### 💬 **Chat History & Session Management**
- Save audit sessions in sidebar
- Load and review previous audits
- Clear history with one click
- Persistent session state

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  USER INPUT LAYER                        │
│  (Text, Voice, Audio Upload via Streamlit UI)           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            TRANSCRIPTION SERVICE (STTService)            │
│  Groq Whisper-V3 → Audio to Text Conversion             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           CLAIM EXTRACTION (ClaimExtractor)              │
│  Groq LLM (llama-3.3-70b) + JSON Mode                   │
│  → Factual claim identification                          │
│  → Category classification                              │
│  → Duplicate removal                                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│             SEARCH SERVICE (SearchService)               │
│  Tavily API → Live Internet Search                      │
│  → Retrieve relevant evidence                            │
│  → Parse snippets & URLs                                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            FACT CHECKER (FactChecker)                    │
│  Groq LLM + Search Evidence → Verify                    │
│  → Compare claim vs. evidence                            │
│  → Generate verdict (TRUE/FALSE/MIXED/UNVERIFIED)       │
│  → Provide confidence score                              │
│  → Cite sources                                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         PRESENTATION LAYER (Streamlit UI)                │
│  Beautiful verdict cards with visual indicators         │
│  Session history & chat persistence                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit (Python) |
| **Speech-to-Text** | Groq Whisper-V3 |
| **LLM** | Groq API (llama-3.3-70b-versatile) |
| **Web Search** | Tavily API |
| **Language** | Python 3.9+ |
| **Hosting** | Streamlit Cloud |

### APIs Used
- **Groq API**: Fast LLM inference + Whisper transcription
- **Tavily API**: Real-time web search with source attribution

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- Groq API Key
- Tavily API Key
- pip

### Step 1: Clone Repository
```bash
git clone https://github.com/EmanFatima764/AI-Pitch-Auditor.git
cd AI-Pitch-Auditor
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

---

## 🔑 API Keys

### Getting Groq API Key
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into `.env`

### Getting Tavily API Key
1. Visit [tavily.com](https://tavily.com)
2. Sign up for free
3. Go to API Keys in dashboard
4. Copy your API key
5. Add to `.env`

---

## 📁 Project Structure

```
AI-Pitch-Auditor/
├── app.py                          # Main Streamlit application
├── config.py                       # Environment & config management
├── services/
│   ├── __init__.py
│   ├── stt_service.py              # Speech-to-Text transcription
│   ├── claim_extractor.py          # Factual claim extraction
│   ├── search_service.py           # Web search integration
│   └── fact_checker.py             # Claim verification
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in git)
└── README.md                       # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main UI logic, session management, audit workflow |
| `config.py` | Configuration loader, API keys, model settings |
| `services/stt_service.py` | Converts audio to text using Groq Whisper |
| `services/claim_extractor.py` | Extracts verifiable claims from transcripts |
| `services/search_service.py` | Searches the web for claim evidence |
| `services/fact_checker.py` | Verifies claims against search evidence |

---

## 💡 How It Works

### Step-by-Step Process

#### 1️⃣ **Input**
User provides pitch via:
- Text input (paste claim)
- Voice recording (microphone)
- Audio file upload (MP3, WAV, M4A)

#### 2️⃣ **Transcription**
If audio is provided:
- Groq Whisper-V3 converts audio to text
- Handles multiple languages & accents
- Result: Clean transcript

#### 3️⃣ **Claim Extraction**
Groq LLM analyzes transcript:
- Identifies factual, verifiable statements
- Categorizes into 8 claim types
- Filters opinions and future plans
- Returns structured JSON

**Example:**
```
Input: "We have 50,000 active users and raised $2M in Series A"
Output: [
  {"claim": "Company has 50,000 active users", "category": "Traction"},
  {"claim": "Company raised $2M in Series A", "category": "Funding"}
]
```

#### 4️⃣ **Web Search**
For each claim:
- Tavily API searches the internet
- Retrieves top 3 relevant results
- Extracts snippets and source URLs
- Creates evidence context

#### 5️⃣ **Fact Verification**
Groq LLM evaluates claim vs. evidence:
- Compares claim statement with search results
- Assigns verdict: `TRUE | FALSE | MIXED | UNVERIFIED`
- Provides confidence score (0.0-1.0)
- Cites sources used for verification

**Verdict Meanings:**
- ✅ **TRUE**: Strong evidence supports the claim
- ❌ **FALSE**: Evidence contradicts the claim
- 🟡 **MIXED**: Partially true or conflicting evidence
- ⚠️ **UNVERIFIED**: No reliable evidence found

#### 6️⃣ **Presentation**
Streamlit UI displays:
- Beautiful verdict cards with visual indicators
- Claim text + Category + Verdict + Confidence
- Detailed explanation for each verdict
- Source URLs for verification
- Chat history in sidebar

---

## 🖥️ User Interface

### Main Dashboard
```
┌─────────────────────────────────────────┐
│  🛡️ AI PITCH AUDITOR                   │
│  Paste claim, record pitch, or upload   │
│  audio file for instant fact-checking   │
└─────────────────────────────────────────┘

📁 Upload Audio File  |  🎙️ Record Audio Pitch

[Paste claim or ask here...]

RESULTS:
┌─────────────────────────────────────┐
│ 💬 "50,000 active users"            │
│ ✅ TRUE | 🏷️ Traction              │
│ Evidence supports this claim        │
│ 🔗 Sources: example.com/users       │
└─────────────────────────────────────┘
```

### Sidebar Features
- ➕ **New Audit**: Start fresh session
- 📜 **Chat History**: Load previous audits
- 🗑️ **Clear History**: Remove all saved sessions

---

## 🔧 Configuration

### `config.py` - Adjust These Settings

```python
# API Keys (from .env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Models
WHISPER_MODEL = "whisper-large-v3"  # Transcription
GROQ_MODEL = "llama-3.3-70b-versatile"  # LLM

# UI Settings
PAGE_TITLE = "AI Pitch Auditor - Live Fact Checker"
PAGE_ICON = "🎙️"
```

---

## 🐛 Error Handling & Logging

The application includes:
- ✅ Comprehensive input validation
- ✅ Try-catch blocks around API calls
- ✅ Logging for debugging
- ✅ User-friendly error messages
- ✅ Graceful fallbacks for failed services
- ✅ HTML injection prevention
- ✅ Type validation for all data

**Logs appear in console** for debugging service issues.

---

## 📊 Claim Categories Explained

### 💰 **Financial**
Revenue, ARR/MRR, pricing, contract values, financial performance

### 📈 **Traction**
Number of users/customers, partnerships, customer relationships, adoption metrics

### 🚀 **Growth**
Growth percentages, YoY/MoM growth rates, user/revenue growth

### 🎯 **Market Size**
TAM, SAM, SOM, market share, market sizing

### 💵 **Funding**
Funding raised, investment amounts, investors, valuations, funding rounds

### ⚡ **Performance**
Accuracy metrics, speed, processing volume, cost reduction, conversion rates

### 📚 **Industry Fact**
Industry statistics, research-backed claims, WHO/Gartner/McKinsey citations

### 📋 **General Fact**
Other specific, factual statements verifiable by external evidence

---

## 🎯 Use Cases

### 1. **Investor Due Diligence**
- Verify startup claims before investing
- Identify misleading or false metrics
- Cross-check market positioning claims

### 2. **Pitch Competition Judge**
- Instantly verify claims during competition
- Provide real-time feedback to pitchers
- Objective claim validation

### 3. **Founder Self-Review**
- Check your own pitch for accuracy before presenting
- Improve credibility by verifying claims
- Catch embarrassing mistakes

### 4. **Media/Press**
- Verify startup claims in press releases
- Fact-check interviews and announcements
- Build reliable reporting

### 5. **Accelerator Programs**
- Audit batch companies' pitches
- Create audit reports for founders
- Set baseline accuracy standards

---

## 📈 Performance Metrics

- ⚡ **Response Time**: < 30 seconds per audit
- 🎯 **Accuracy**: Depends on availability of online evidence
- 🔗 **Source Coverage**: Tavily searches top 100+ domains
- 💬 **Language Support**: Multilingual (Whisper handles 99 languages)

---

## 🔐 Privacy & Data

- ✅ No data stored permanently
- ✅ Sessions stored locally in browser (Streamlit)
- ✅ No user tracking
- ✅ API calls use industry-standard encryption
- ✅ GDPR compliant

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect GitHub repository
5. Set environment variables:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
6. Click "Deploy"

**Live Demo URL:**  
[ai-pitch-auditor-eyxbove2nm5qwnjhatmzeq.streamlit.app](https://ai-pitch-auditor-eyxbove2nm5qwnjhatmzeq.streamlit.app/)

### Deploy Locally with Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 📚 Example Workflows

### Example 1: Text Claim
```
User Input:
"Our platform has 10,000 paying customers"

Extracted Claim:
"Company has 10,000 paying customers"
Category: Traction

Verification Result:
✅ TRUE (90% confidence)
Sources: Company website, crunchbase.com
```

### Example 2: Audio Pitch
```
User Input:
[Records 2-minute pitch about AI startup]

Transcribed Text:
"We process 1 million documents monthly using our AI..."

Extracted Claims:
1. "Process 1 million documents monthly" (Performance)
2. "Founded by Stanford PhDs" (General Fact)
3. "Raised $5M Series A" (Funding)

Verification Results:
1. ✅ TRUE - Evidence confirms
2. 🟡 MIXED - Some founders from Stanford
3. ❌ FALSE - Only raised $3M
```

### Example 3: Pitch Upload
```
User Input:
[Uploads recorded pitch video: pitch.mp3]

STT Conversion:
Audio → Transcript (automatic)

Processing:
Claims extracted → Searched → Verified

Output:
Complete audit report with 12 claims verified
```

---

## 🛠️ Troubleshooting

### Issue: "GROQ_API_KEY is not configured"
**Solution**: Ensure `.env` file exists with valid `GROQ_API_KEY`

### Issue: "No clear speech or text input found"
**Solution**: 
- Check microphone permissions
- Ensure audio file is clear and not corrupted
- Try again with louder/clearer speech

### Issue: "Failed to extract claims"
**Solution**:
- Check Groq API status
- Ensure transcript is not empty
- Try with simpler, shorter input

### Issue: "Search Failed"
**Solution**:
- Check Tavily API key
- Verify internet connection
- Check API usage limits

### Issue: "UNVERIFIED" for all claims
**Solution**:
- Claims may be too niche or recent
- Try searching manually for the same claims
- Tavily may lack coverage for that topic

---

## 🎓 How to Improve Accuracy

1. **Use specific, measurable claims**: "50,000 users" is better than "many users"
2. **Include time context**: "As of 2024" helps fact-checkers
3. **Provide source attribution**: "According to Gartner..." improves verification
4. **Use verified metrics**: Company-reported numbers are easier to verify
5. **Avoid ambiguous language**: Be precise in your claims

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Support for more languages
- [ ] Extended claim categories
- [ ] Multi-document analysis
- [ ] Batch processing for multiple pitches
- [ ] Export audit reports as PDF
- [ ] Integration with pitch scoring
- [ ] Historical tracking of claim accuracy
- [ ] Advanced analytics dashboard

---

## 📄 License

This project is open-source under the **MIT License**.

---

## 👨‍💻 Author

**Eman Fatima**  
GitHub: [@EmanFatima764](https://github.com/EmanFatima764)

---

## 🙏 Acknowledgments

- **Groq** for fast LLM inference and Whisper transcription
- **Tavily** for reliable web search API
- **Streamlit** for beautiful, fast web app framework
- Hackathon community for inspiration and feedback

---

## 📞 Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review **GitHub Issues** in the repository
3. Contact via GitHub

---

## 🎉 Ready to Audit?

**[Start Fact-Checking Now →](https://ai-pitch-auditor-eyxbove2nm5qwnjhatmzeq.streamlit.app/)**

---

<div align="center">

**Made with ❤️ for hackathons and pitch perfection**

⭐ Found this helpful? Star the repository!

</div>
