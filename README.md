# 🤖 AI Job Search Agent

A personal career intelligence assistant powered by Google Gemini AI. 
Autonomously searches the web, Wikipedia, and your uploaded documents 
to answer any job market question with cited sources.

🌐 **Live Demo:** [https://job-search-agent-327358117698.us-central1.run.app](https://job-search-agent-327358117698.us-central1.run.app)

---

## 🎯 What It Does

Ask any career or job market question and the agent:
- 🧠 **Decides** which sources to search automatically
- 🌐 **Searches the web** for latest job market data
- 📚 **Searches Wikipedia** for company/technology backgrounds
- 📄 **Searches your documents** (resume, certifications)
- 💡 **Synthesizes** a comprehensive answer with cited sources

### Example Questions:
- *"What companies in Hyderabad are hiring Cloud Architects?"*
- *"What is the average salary for ML Engineers in India 2025?"*
- *"Tell me about Google India AI strategy and open roles"*
- *"How does my resume match current market demands?"*
- *"What certifications should I get for GCP roles?"*
- *"Latest trends in enterprise AI adoption in India"*

---

## 🏗️ Architecture

\`\`\`
User Question
      │
      ▼
┌─────────────────────────────────┐
│   Gemini Agent (Brain)          │
│                                 │
│   Step 1: Analyze question      │
│   Step 2: Decide which tools    │
│   Step 3: Execute tools         │
│   Step 4: Synthesize answer     │
└──────┬──────────────────────────┘
       │
       ├──► 🌐 Tavily Web Search
       │    Real-time job market data
       │    Company news and openings
       │
       ├──► 📚 Wikipedia API
       │    Company backgrounds
       │    Technology definitions
       │
       └──► 📄 ChromaDB Vector Store
            User uploaded PDFs
            Resume, certifications
                 │
                 ▼
        Synthesized Answer
        with cited sources ✅
\`\`\`

---

## 🧠 How the Agent Decides

The agent uses a **two-step process:**

### Step 1 — Planning
```json
{
  "tools_needed": ["web_search", "wikipedia_search"],
  "web_query": "Google India AI hiring Hyderabad 2025",
  "wiki_query": "Google India",
  "reasoning": "Need current job data + company background"
}
```

### Step 2 — Execution & Synthesis
- Executes only the needed tools
- Combines results intelligently
- Generates comprehensive answer with sources

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM & Agent Brain | Google Gemini 2.5 Flash |
| Web Search | Tavily Search API |
| Encyclopedia | Wikipedia API |
| Vector Database | ChromaDB |
| PDF Processing | PyPDF2 |
| Embeddings | Gemini Embedding API |
| AI Framework | LangChain |
| Web UI | Streamlit |
| Containerization | Docker |
| Cloud Deployment | Google Cloud Run |
| Image Registry | Google Artifact Registry |

---

## 💡 Key Design — Agentic RAG

This project demonstrates **Agentic RAG** — the evolution beyond basic RAG:

\`\`\`
Basic RAG (Project 1):
Fixed documents → Always retrieves → Answers
❌ Can't access live data
❌ Limited to pre-loaded documents

Agentic RAG (This project):
Question → Agent DECIDES → Dynamic retrieval → Answers
✅ Live web search
✅ Multiple source types
✅ Intelligent tool selection
✅ Self-directed research
\`\`\`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Tavily API key from [Tavily](https://tavily.com)

### Local Setup

\`\`\`bash
# Clone the repository
git clone https://github.com/chandranakkalakunta/job-search-agent.git
cd job-search-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set API keys
export GEMINI_API_KEY="your-gemini-key"
export TAVILY_API_KEY="your-tavily-key"

# Run
streamlit run app.py
\`\`\`

---

## 🐳 Docker Deployment

\`\`\`bash
# Build for AMD64 (Cloud Run requirement)
docker buildx build --platform linux/amd64 \
  -t us-central1-docker.pkg.dev/YOUR_PROJECT/YOUR_REPO/job-search-agent:latest \
  --push .

# Deploy to Cloud Run
gcloud run deploy job-search-agent \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT/YOUR_REPO/job-search-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,TAVILY_API_KEY=$TAVILY_API_KEY \
  --memory 2Gi \
  --port 8080
\`\`\`

---

## 📁 Project Structure

\`\`\`
job-search-agent/
├── tools.py            # Web search, Wikipedia, PDF tools
├── agent.py            # AI agent brain and orchestration
├── app.py              # Streamlit web UI
├── Dockerfile          # Container configuration
├── .dockerignore       # Docker build exclusions
├── requirements.txt    # Python dependencies
├── .gitignore          # Git exclusions
└── README.md           # This file
\`\`\`

---

## 🗺️ Roadmap

- [ ] Add LinkedIn job scraping
- [ ] Salary comparison across cities
- [ ] Interview question generator
- [ ] Company culture analyzer
- [ ] Skills gap learning path generator
- [ ] Email alerts for matching jobs

---

## 👨‍💻 Author

**Chandra Nakkalakunta**
Principal Cloud & AI/ML Architect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/chandra-nakkalakunta)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/chandranakkalakunta)

---

## 🔗 Related Projects

- [Smart Document Q&A Bot](https://github.com/chandranakkalakunta/doc-qa-bot) — RAG-based document Q&A
- [AI Resume Analyzer](https://github.com/chandranakkalakunta/resume-analyzer) — AI-powered resume matching

---

## 📄 License

MIT License — feel free to use this project as a reference.
