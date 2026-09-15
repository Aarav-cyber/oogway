# Lenny Growth Assistant

This repository contains the full stack implementation for **The Lenny Growth Assistant**, built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, an Agent framework with RAG transcript grounding, multi-LLM provider abstraction (Ollama, Groq, Gemini), Ship 30 for 30 writing skill, and HTML/Markdown artifact generation in React + TypeScript.

---

## 🚀 Quickstart Guide

### Option 1: Docker Compose (Recommended)

1. **Clone the repository and prepare environment variables**:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
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
   The application will be live at `http://localhost:3000` and API docs at `http://localhost:8000/docs`.

---

## 🔄 Runtime LLM Switching

The application supports runtime switching between configured LLM providers from the frontend without modifying application code or restarting the backend.

### Supported Providers:

- **Ollama** — `llama3.2`
- **Groq** — `openai/gpt-oss-20b`
- **Gemini** — `gemini-2.5-flash`

The `LLM_PROVIDER` value in `.env` determines the initial provider at startup. After startup, the provider can be changed from the frontend LLM selector in the top header bar.

Changing the provider does not require modifying application source code or restarting the backend.

API credentials remain server-side and are never exposed to the frontend.

Before switching, the backend validates the requested provider and checks availability. If the provider is unavailable, the switch is rejected and the currently active provider remains unchanged.

---

## 🧪 Running Automated Tests

Run backend unit and integration tests:
```bash
pytest backend/tests -v
```

Run frontend Vitest component tests:
```bash
cd frontend
npm run test
```

All 22 backend test cases and 8 frontend test cases pass.

---

## 🏛️ System Architecture

```text
                         ┌──────────────────────┐
                         │       React UI       │
                         │                      │
                         │     LLM Selector     │
                         │                      │
                         │  Ollama              │
                         │  Groq                │
                         │  Gemini              │
                         └──────────┬───────────┘
                                    │
                             POST /config/llm
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │                      │
                         │ Runtime LLM Config   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                              LLMFactory
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                 Ollama           Groq            Gemini
                llama3.2      gpt-oss-20b      gemini-2.5-flash
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                              LennyAgent
                                    │
                                    ▼
                         ┌────────────────────┐
                         │ Grounded QA        │
                         │ Ship 30 for 30     │
                         │ Artifacts          │
                         └────────────────────┘
```

---

## 🔑 Key Features

- **FastAPI HTTP API**: Validated with Pydantic schemas, explicit error models, and request tracing.
- **PostgreSQL Persistence**: Fully managed schema for users, sessions, messages, documents, chunks, and artifacts with Alembic migrations.
- **Runtime LLM Switching**: Seamless switching between local Ollama, Groq, and Gemini from the header selector without backend restarts.
- **RAG Pipeline**: Ingests transcript files, chunks content, indices chunks, and retrieves source-attributed passages with score thresholds.
- **Agent Skill System**:
  - `Grounded QA`: Answers growth questions using retrieved Lenny transcript context. Fallback message provided when evidence is missing.
  - `Ship 30 for 30`: Generates 1,250-word atomic essays formatted with hooks, skimmable headings, and grounded takeaways.
  - `Artifact Generation`: Generates safe Markdown or HTML/CSS artifacts. Generated HTML is sanitized using `nh3` and `DOMPurify` and rendered in an isolated sandbox iframe.
