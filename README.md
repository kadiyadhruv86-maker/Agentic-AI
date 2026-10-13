# Personalized Learning & Career Agent

A modular Python project that separates:
- **Course-content questions** grounded in a syllabus, notes, or textbook.
- **General internet search** for current information, tutorials, documentation, and source links (via the `ddgs` search package).
- **External opportunity searches** for jobs and internships related to a study topic.
- **Combined requests** that need multiple tools.

Stack: ChatOllama, LangChain `create_agent`, `PyPDFLoader` / `TextLoader`, `RecursiveCharacterTextSplitter`, Ollama embeddings, persistent Chroma, `@tool`, DuckDuckGo search via `ddgs`, job APIs, and Streamlit.

## 1. Requirements

- Python 3.10 or newer (Python 3.11 recommended).
- Ollama installed and running: https://ollama.com/
- Internet connection for installing packages and searching opportunities.
- A local model with enough memory for your device.

## 2. Install and run

Open a terminal in this project folder:

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```powershell
.venv\\Scripts\\activate
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Pull a chat model and embedding model:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

Ensure Ollama is running, then test the ChatOllama call first:

```bash
python llm_setup.py
```

Expected output is similar to: `ChatOllama is working.`

## 3. Add course material

Put your course files directly in the project root folder (the same folder as `app.py`). Supported types:
- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`)

The included `course_notes.txt` is a small demonstration dataset. Replace it or add your official syllabus, lecture notes, or permitted textbook material. Avoid uploading copyrighted books unless you have the right to use them.

Build/test the retrieval index:

```bash
python rag.py
```

This checks both:
1. Narrow factual query: “What is a text splitter?”
2. Broad conceptual query: “Explain how RAG works and why retrieval is useful.”

The Chroma index is persisted to `chroma_db/`. After adding or changing files, delete `chroma_db/` or click **Rebuild course index** in the app sidebar.

## 4. Optional Adzuna configuration

Copy `.env.example` to `.env` and add your Adzuna API credentials to use Adzuna job search. If credentials are blank, the project uses Remotive's public remote-jobs API as a fallback. The fallback mainly returns remote listings; location and eligibility vary. APIs can change their access rules or limits.

```env
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
JOB_COUNTRY=in
```

Never commit `.env` or publish API keys.

## 5. Launch the study companion

```bash
streamlit run app.py
```

Try:
- `What is a text splitter?`
- `Explain how RAG works in simple language.`
- `Search the web for the official Python tutorial.`
- `Find Python internships in India.`
- `Explain embeddings and then find entry-level opportunities related to them.`
- `Explain RAG from my notes and search the web for an official reference.`

## 6. Project structure

```text
personalized_learning_career_agent/
├── app.py                  # Streamlit interface
├── agent.py                # create_agent and system prompt
├── config.py               # environment settings and paths
├── llm_setup.py            # first ChatOllama smoke test
├── rag.py                  # loading, splitting, Chroma, retriever tests
├── course_tool.py          # course retrieval @tool
├── opportunity_search.py   # jobs/internships @tool and API logic
├── web_search.py           # general internet search @tool
├── requirements.txt
├── .env.example
├── course_notes.txt
├── test_retriever.py
└── chroma_db/              # created on first indexing; not included in ZIP
```

## 7. Notes and troubleshooting

- `Connection refused` from Ollama: start Ollama and check `OLLAMA_BASE_URL`.
- Model not found: run `ollama pull llama3.1` and check `.env`.
- Embedding model missing: run `ollama pull nomic-embed-text`.
- No course documents: add a PDF/TXT/MD file directly in the project root folder.
- Poor retrieval: try adjusting `chunk_size`, `chunk_overlap`, and `k` in `rag.py`, then rebuild the index. Test paraphrased and conceptual questions, not only exact keyword matches.
- Web search failure: check the internet connection; the public search service may be temporarily unavailable.
- Search failure: check internet/API credentials and the external service's current limits.
- This is a starter project, not a guarantee of correct answers or active job listings. Verify important study answers and every opportunity on the original source.

## Bonus extension

For a FastMCP version, expose the two functions as MCP tools on a separate server, then connect them at runtime using `MultiServerMCPClient`. This project implements course retrieval, general web search, and job/internship search as direct agent tools. A FastMCP server remains an optional extension.
