# Lenny Growth Assistant --- Backend

This repository contains the backend implementation for **The Lenny Growth Assistant**, built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, an Agent framework with RAG transcript grounding, multi-LLM provider abstraction (Ollama, Anthropic, OpenAI), Ship 30 for 30 writing skill, and HTML/Markdown artifact generation.

---

## 🚀 Quickstart Guide

### Option 1: Docker Compose (Recommended)

1. **Clone the repository and prepare environment variables**:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. **Ensure Ollama is running locally** (if using `LLM_PROVIDER=ollama`):
   ```bash
   ollama pull llama3.2
   ollama serve
   ```

3. **Start services**:
   ```bash
   docker compose up --build
   ```
   The backend API will be live at `http://localhost:8000` and automatic OpenAPI docs at `http://localhost:8000/docs`.

---

### Option 2: Local Setup with Python

1. **Set up Python environment**:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   ```

3. **Run Database Migrations & Seed Data**:
   Ensure PostgreSQL is running on `localhost:5432` (or adjust `DATABASE_URL` in `.env`):
   ```bash
   alembic upgrade head
   python scripts/seed_data.py
   ```

4. **Launch Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🧪 Running Automated Tests

Run unit and integration tests:
```bash
pytest backend/tests -v
```

All 16 test cases cover:
- Health and readiness endpoints
- Session creation and session isolation logic
- RAG retrieval quality and ungrounded query behavior
- LLM Provider factory and switching
- Agent skill routing (Grounded QA, Ship 30 for 30, Artifact generation)
- HTML sanitization and untrusted code isolation
- Message & artifact persistence

---

## 🏛️ System Architecture

```text
               ┌──────────────────────┐
               │  Frontend / Client   │
               └──────────┬───────────┘
                          │ HTTP
                          ▼
               ┌──────────────────────┐
               │       FastAPI        │
               │                      │
               │ Routes / Validation  │
               │ Structured Logging   │
               └──────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
  ┌────────────┐   ┌─────────────┐  ┌─────────────┐
  │ PostgreSQL │   │ Agent Layer │  │ RAG Layer   │
  │            │   │             │  │             │
  │ sessions   │   │ router      │  │ retrieval   │
  │ messages   │   │ skills      │  │ BM25/IDF    │
  │ artifacts  │   │ grounding   │  │ sources     │
  └────────────┘   └──────┬──────┘  └──────┬──────┘
                          │                │
                          └───────┬────────┘
                                  ▼
                         ┌─────────────────┐
                         │ LLM Provider    │
                         └────────┬────────┘
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
                ┌─────────┐              ┌──────────┐
                │ Ollama  │              │ Cloud    │
                │ Local   │              │ Claude / │
                │ LLM     │              │ OpenAI   │
                └─────────┘              └──────────┘
```

---

## 🔑 Key Features

- **FastAPI HTTP API**: Validated with Pydantic schemas, explicit error models, and request tracing.
- **PostgreSQL Persistence**: Fully managed schema for users, sessions, messages, documents, chunks, and artifacts with Alembic migrations.
- **LLM Provider Abstraction**: Switch seamlessly between local Ollama, Anthropic Claude, and OpenAI GPT-4 via `LLM_PROVIDER` environment variable.
- **RAG Pipeline**: Ingests transcript files, chunks content, indices chunks, and retrieves source-attributed passages with score thresholds.
- **Agent Skill System**:
  - `Grounded QA`: Answers growth questions using retrieved Lenny transcript context. Fallback message provided when evidence is missing.
  - `Ship 30 for 30`: Generates 1,250-word atomic essays formatted with hooks, skimmable headings, and grounded insights.
  - `Artifact Generation`: Generates safe Markdown or HTML/CSS artifacts. Generated HTML is sanitized using `nh3` to strip unsafe scripts (`<script>`, `<iframe>`).
- **Resilience & Health**: Readiness endpoint `/ready` monitors database and LLM dependency availability. Structured JSON logs output per request.
