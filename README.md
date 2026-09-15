# Lenny Growth Assistant

A full-stack AI-powered conversational assistant for product and growth questions, grounded in Lenny's Podcast / Newsletter transcript knowledge base.

The application combines:

- FastAPI backend
- PostgreSQL persistence
- SQLAlchemy + Alembic
- Agent routing with specialized skills
- Retrieval-Augmented Generation (RAG)
- Runtime LLM switching
- Ollama local inference
- Groq cloud inference
- Gemini cloud inference
- Ship 30 for 30 essay generation
- Markdown and HTML/CSS artifact generation
- In-app Artifact Viewer
- HTML sanitization and constrained rendering
- Automated backend and frontend tests

---

## 1. Architecture Overview

```text
                         ┌──────────────────────────┐
                         │        React UI          │
                         │                          │
                         │  Chat                    │
                         │  Sessions                │
                         │  LLM Selector            │
                         │  Artifact Viewer          │
                         └────────────┬─────────────┘
                                      │
                                      │ HTTP
                                      ▼
                         ┌──────────────────────────┐
                         │         FastAPI           │
                         │                          │
                         │  Sessions / Chat          │
                         │  Runtime LLM Config      │
                         │  Health / Readiness      │
                         └──────────┬───────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
              ┌─────────────┐              ┌─────────────┐
              │  LennyAgent │              │ PostgreSQL  │
              └──────┬──────┘              └─────────────┘
                     │
                     ▼
              ┌────────────────┐
              │  Agent Router  │
              └───────┬────────┘
                      │
             ┌────────┼───────────────┐
             ▼        ▼               ▼
       Grounded QA  Ship 30 for 30  Artifacts
             │
             ▼
       Retriever / RAG
             │
             ▼
      Transcript Knowledge Base
````

### Runtime LLM Path

```text
React LLM Selector
        │
        ▼
POST /config/llm
        │
        ▼
Validate Provider
        │
        ▼
Check Availability
        │
        ▼
Switch Runtime Provider
        │
        ▼
LLMFactory
   ┌────┼────────┐
   ▼    ▼        ▼
Ollama Groq    Gemini
```

For detailed system architecture, see:

```text
architecture.md
```

---

## 2. Features

### Grounded Conversational Assistant

Answers product and growth questions using retrieved Lenny transcript material.

The system:

1. Receives the user's question.
2. Loads conversation context.
3. Routes the request to the appropriate skill.
4. Retrieves relevant transcript chunks.
5. Generates a grounded response.
6. Returns source metadata with the response.
7. Acknowledges when available source material is insufficient.

### Session Persistence

Each chat session maintains independent context.

Stored data includes:

* Sessions
* Messages
* Timestamps
* User/session metadata
* Documents/chunks
* Generated artifacts

PostgreSQL schema changes are managed with Alembic.

### Runtime LLM Switching

The active LLM provider can be switched directly from the frontend without changing source code or restarting the backend.

Supported providers:

| Provider | Model                |
| -------- | -------------------- |
| Ollama   | `llama3.2`           |
| Groq     | `openai/gpt-oss-20b` |
| Gemini   | `gemini-2.5-flash`   |

The initial provider is selected using the backend `.env` configuration.

After startup, the provider can be changed using the frontend LLM selector.

Runtime flow:

```text
Frontend Selector
       ↓
POST /config/llm
       ↓
Validate Provider
       ↓
Check Availability
       ↓
Update Runtime Provider
```

If the requested provider is unavailable:

* The switch is rejected.
* A structured error is returned.
* The currently active provider remains active.

Cloud API credentials remain on the backend and are never exposed to the frontend.

### Ship 30 for 30 Skill

The dedicated writing skill generates approximately 1,250-word essays with:

* Strong opening hook
* Narrative progression
* Headings
* Bullets
* Selective emphasis
* Practical takeaway
* Grounding in transcript knowledge

### Artifact Generation

The assistant can generate:

* Markdown artifacts
* HTML/CSS artifacts

Generated HTML is treated as untrusted content.

The backend sanitizes generated HTML and the frontend renders it inside a constrained Artifact Viewer.

---

## 3. Requirements

### Development Environment

Recommended:

* Python 3.10+
* Node.js 18+
* npm
* PostgreSQL
* Ollama
* Docker
* Docker Compose

---

## 4. Environment Variables

Backend configuration:

```text
backend/.env
```

Create it from:

```text
backend/.env.example
```

### Windows PowerShell

```powershell
Copy-Item backend/.env.example backend/.env
```

### Backend Variables

| Variable          | Purpose                  | Example                    |
| ----------------- | ------------------------ | -------------------------- |
| `APP_ENV`         | Application environment  | `development`              |
| `LOG_LEVEL`       | Logging level            | `INFO`                     |
| `DATABASE_URL`    | PostgreSQL connection    | `postgresql+asyncpg://...` |
| `LLM_PROVIDER`    | Initial LLM provider     | `ollama`                   |
| `OLLAMA_BASE_URL` | Ollama API endpoint      | `http://localhost:11434`   |
| `OLLAMA_MODEL`    | Ollama model             | `llama3.2`                 |
| `OLLAMA_TIMEOUT`  | Local generation timeout | `180`                      |
| `GROQ_API_KEY`    | Groq API key             | `<your-key>`               |
| `GROQ_MODEL`      | Groq model               | `openai/gpt-oss-20b`       |
| `GEMINI_API_KEY`  | Gemini API key           | `<your-key>`               |
| `GEMINI_MODEL`    | Gemini model             | `gemini-2.5-flash`         |
| `CORS_ORIGINS`    | Allowed frontend origins | `http://localhost:5173`    |

### Important

Never commit:

```text
backend/.env
frontend/.env
```

Only the following should be committed:

```text
backend/.env.example
frontend/.env.example
```

Never place cloud API keys in frontend environment files.

---

# 5. Quick Start

## Option A — Local Development

This is the simplest setup when using Ollama on Windows.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd oogway
```

### 2. Configure Backend

```powershell
Copy-Item backend/.env.example backend/.env
```

Edit:

```text
backend/.env
```

For local Ollama:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=180
```

If using Groq or Gemini, configure the required API key and model.

### 3. Configure Frontend

```powershell
Copy-Item frontend/.env.example frontend/.env
```

### 4. Install Backend Dependencies

```powershell
cd backend

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 5. Start PostgreSQL

Make sure PostgreSQL is running and that `DATABASE_URL` in `backend/.env` points to the correct database.

### 6. Run Database Migrations

```powershell
alembic upgrade head
```

### 7. Seed Required Data

```powershell
python scripts/seed_data.py
```

### 8. Ingest Transcript Knowledge Base

```powershell
python scripts/ingest_transcripts.py
```

### 9. Start Ollama

Install Ollama and pull the required model:

```powershell
ollama pull llama3.2
```

Start Ollama if it is not already running:

```powershell
ollama serve
```

Verify Ollama:

```powershell
curl.exe http://localhost:11434/api/tags
```

The response should contain:

```text
llama3.2:latest
```

### 10. Start Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

### 11. Start Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 6. Docker Compose

Docker Compose can be used to run the application services together.

Start the stack:

```bash
docker compose up --build
```

Expected services:

```text
Frontend
Backend
PostgreSQL
```

Expected endpoints:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs
```

### Ollama with Docker

Ollama runs on the host machine while the backend can run inside Docker.

When the backend runs inside Docker, `localhost` refers to the container itself.

Therefore, the backend should use:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

The Docker Compose configuration should provide:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Make sure Ollama is running on the host:

```powershell
ollama serve
```

Verify it from the host:

```powershell
curl.exe http://localhost:11434/api/tags
```

The Docker backend should then connect to:

```text
http://host.docker.internal:11434
```

---

# 7. Knowledge Base

Transcript ingestion is handled by:

```text
backend/scripts/ingest_transcripts.py
```

Seed/setup support is handled by:

```text
backend/scripts/seed_data.py
```

The RAG flow is:

```text
Transcript Files
       ↓
Load
       ↓
Chunk
       ↓
Index
       ↓
Store Source Metadata
       ↓
Retrieve Relevant Chunks
       ↓
Agent Skill
       ↓
Grounded Answer
```

Retrieved chunks retain source information so that responses can identify the transcript material used.

---

# 8. API Overview

| Method | Endpoint                          | Purpose                                 |
| ------ | --------------------------------- | --------------------------------------- |
| `GET`  | `/health`                         | Basic service health                    |
| `GET`  | `/ready`                          | Readiness including database/LLM status |
| `POST` | `/sessions`                       | Create a new session                    |
| `GET`  | `/sessions`                       | List sessions                           |
| `GET`  | `/sessions/{session_id}`          | Retrieve session                        |
| `POST` | `/sessions/{session_id}/messages` | Send a chat message                     |
| `GET`  | `/config/llm`                     | Read active runtime provider/model      |
| `POST` | `/config/llm`                     | Switch runtime provider                 |

Complete API documentation:

```text
http://localhost:8000/docs
```

---

# 9. LLM Configuration

## Ollama

Default local configuration:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=180
```

Pull the model:

```powershell
ollama pull llama3.2
```

Check installed models:

```powershell
ollama list
```

Check currently loaded models:

```powershell
ollama ps
```

Verify the API:

```powershell
curl.exe http://localhost:11434/api/tags
```

### Ollama Docker Configuration

When the backend runs inside Docker:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

Do not use:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

inside the Docker backend if Ollama is running on the Windows host.

---

## Groq

Configure:

```env
GROQ_API_KEY=<your-key>
GROQ_MODEL=openai/gpt-oss-20b
```

The provider can then be selected from the frontend.

---

## Gemini

Configure:

```env
GEMINI_API_KEY=<your-key>
GEMINI_MODEL=gemini-2.5-flash
```

The provider can then be selected from the frontend.

---

## Runtime Provider Switching

The initial provider is configured through:

```env
LLM_PROVIDER=ollama
```

After the backend starts, the frontend selector can switch between configured providers.

No source-code modification or backend restart is required for runtime switching.

The frontend obtains the active provider/model from the backend readiness endpoint:

```text
GET /ready
```

This keeps the UI synchronized with the actual backend runtime configuration.

---

# 10. Agent Routing

The application uses a provider-agnostic LLM abstraction:

```text
LennyAgent
     ↓
BaseLLMProvider
     ↓
LLMFactory
     ↓
Active Provider
```

Requests are routed into specialized skills:

```text
User Message
     ↓
Agent Router
     ├── Grounded QA
     ├── Ship 30 for 30
     └── Artifact Generation
```

Provider-specific logic is isolated inside provider implementations.

The agent and skills do not require separate implementations for Ollama, Groq, or Gemini.

---

# 11. Artifact Security

Generated HTML is treated as untrusted content.

The rendering flow is:

```text
Generated HTML
      ↓
Backend Sanitization
      ↓
Frontend Sanitization / Constrained Rendering
      ↓
Artifact Viewer
```

The goal is to prevent generated markup from gaining unrestricted control over the parent application.

Additional security and architecture details are documented in:

```text
architecture.md
```

---

# 12. Testing

## Backend Tests

From the repository root:

```powershell
cd backend
pytest
```

The backend test suite covers:

* Chat flow
* Grounding
* Session isolation
* Health/readiness
* Persistence
* Session APIs
* Configuration
* LLM factory
* Runtime LLM configuration
* Retrieval
* Agent routing
* Artifact sanitization

## Frontend Tests

```powershell
cd frontend
npm test
```

## Frontend Production Build

```powershell
npm run build
```

A successful production build confirms that the frontend TypeScript/Vite application compiles correctly.

---

# 13. Troubleshooting

## Ollama Is Unavailable

Check whether the Ollama server is running:

```powershell
curl.exe http://localhost:11434/api/tags
```

Start Ollama:

```powershell
ollama serve
```

Check installed models:

```powershell
ollama list
```

Pull the model if necessary:

```powershell
ollama pull llama3.2
```

Check loaded models:

```powershell
ollama ps
```

---

## Runtime Switch Says LLM Is Unavailable

The backend checks provider availability before changing runtime state.

Check:

1. Provider credentials are configured.
2. Ollama is reachable when using Ollama.
3. The configured model exists.
4. The backend is running.
5. `/ready` reports the expected readiness state.

An unavailable provider should be rejected without replacing the currently active provider.

---

## Ollama Requests Time Out

Local LLM inference can take longer on CPU-only systems.

Check:

```env
OLLAMA_TIMEOUT=180
```

Increase the value if the machine requires more generation time.

Also verify that Ollama is reachable:

```powershell
curl.exe http://localhost:11434/api/tags
```

If running the backend inside Docker, verify:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

## Cloud Provider Is Unavailable

For Groq:

```env
GROQ_API_KEY=<your-key>
GROQ_MODEL=openai/gpt-oss-20b
```

For Gemini:

```env
GEMINI_API_KEY=<your-key>
GEMINI_MODEL=gemini-2.5-flash
```

Do not put these credentials in frontend files.

---

## Database Connection Failure

Verify PostgreSQL is running.

Check that:

```env
DATABASE_URL=...
```

points to the correct:

* Host
* Port
* Database
* Username
* Password

Then run:

```powershell
alembic upgrade head
```

---

## Empty Retrieval / Unsupported Question

The assistant should acknowledge when available transcript material is insufficient rather than inventing an answer.

Verify that the knowledge base has been ingested:

```powershell
python scripts/ingest_transcripts.py
```

---

## Frontend Cannot Reach Backend

Confirm FastAPI is running:

```text
http://localhost:8000/health
```

Also verify that the frontend API base URL is configured correctly.

---

## Docker Issues

Stop the stack:

```bash
docker compose down
```

Rebuild and start:

```bash
docker compose up --build
```

Inspect logs:

```bash
docker compose logs
```

Inspect a specific service:

```bash
docker compose logs backend
```

---

# 14. Project Structure

```text
.
├── README.md
├── PRD.md
├── design.md
├── architecture.md
├── ui-manual-test-plan.md
├── agent-transcripts/
│   └── runtime-llm-switching.md
├── docker-compose.yml
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── migrations/
│   ├── scripts/
│   ├── tests/
│   │   ├── integration/
│   │   └── unit/
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── app/
    │   ├── components/
    │   ├── hooks/
    │   ├── lib/
    │   ├── styles/
    │   └── types/
    ├── tests/
    │   ├── components/
    │   └── e2e/
    ├── .env.example
    ├── Dockerfile
    ├── package.json
    └── vite.config.ts
```

---

# 15. Supporting Documentation

## Product Requirements

```text
PRD.md
```

Contains:

* User
* Problem
* Goals
* Success metrics
* Assumptions
* Scope
* User flows
* Acceptance criteria
* Risks and trade-offs
* Implementation plan

## UI/UX Design

```text
design.md
```

Contains:

* UX principles
* Information architecture
* Interaction states
* Responsive behavior
* Accessibility
* Visual decisions
* LLM selector
* Artifact Viewer
* UI manual testing

## System Architecture

```text
architecture.md
```

Contains:

* Database schema
* API endpoints
* Component boundaries
* Ingestion/retrieval
* Agent routing
* Runtime model toggle
* Security
* Deployment topology

## Agent Transcripts / Engineering Log

```text
agent-transcripts/
```

Records implementation decisions, failed attempts, corrections, and verification without exposing secrets.

## UI Manual Test Plan

```text
ui-manual-test-plan.md
```

Contains the manual frontend verification procedures.

---

# 16. Security

The application follows these security principles:

* `.env` files are excluded from Git.
* `.env.example` contains placeholders only.
* Cloud API credentials remain backend-side.
* Arbitrary provider names are not accepted by the runtime selector.
* Provider availability is checked before runtime switching.
* Generated HTML is treated as untrusted content.
* Generated HTML is sanitized/constrained before rendering.
* API failures are returned as structured application errors.
* Frontend code does not contain cloud API credentials.

---

# 17. Operational Readiness

The system provides:

* Docker Compose startup path
* Environment configuration examples
* Health endpoint
* Readiness endpoint
* Structured application errors
* Request tracing/correlation information
* LLM availability checks
* Configurable local-model timeout
* PostgreSQL persistence
* Automated tests
* Troubleshooting documentation

---

# 18. Evaluator Verification Checklist

A fresh evaluator should be able to:

1. Clone the repository.
2. Create environment files from `.env.example`.
3. Start PostgreSQL / Docker services.
4. Start Ollama and pull `llama3.2`.
5. Start the application.
6. Open the frontend.
7. Create a chat.
8. Ask a grounded product/growth question.
9. Inspect supporting transcript sources.
10. Ask a follow-up question.
11. Generate a Ship 30 for 30 essay.
12. Generate a Markdown artifact.
13. Generate an HTML artifact.
14. Switch between Ollama, Groq, and Gemini from the UI.
15. Test unavailable-provider behavior.
16. Run backend and frontend tests.
17. Run the frontend production build.

---

# 19. Demo Flow

The recommended 2–3 minute demo:

## 1. Problem

Briefly explain the need for a grounded growth assistant over Lenny's content.

## 2. Grounded Q&A

Ask a product/growth question and demonstrate:

* Answer
* Transcript sources
* Follow-up context

## 3. Runtime Model Switching

Show the LLM selector:

```text
Ollama • llama3.2
        ↓
Groq • openai/gpt-oss-20b
        ↓
Gemini • gemini-2.5-flash
```

Switch between providers without restarting the backend.

## 4. Local Ollama

Switch to Ollama and demonstrate that the local model answers the request.

## 5. Artifact Generation

Generate an HTML or Markdown artifact and open it in the Artifact Viewer.

## 6. Technical Trade-off

Explain the trade-off between:

* Local Ollama inference
* Cloud model quality
* Latency
* Availability
* Runtime provider abstraction

---

# 20. License / Assignment

This repository was created as part of the Forward Deployed Engineer take-home assessment for The Lenny Growth Assistant.

