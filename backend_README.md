# Lenny Growth Assistant --- Backend README

## 1. Purpose

This document is the implementation guide for the backend of **The Lenny
Growth Assistant**.

The backend must provide:

-   A FastAPI HTTP API.
-   Independent chat sessions.
-   PostgreSQL persistence for sessions, messages, timestamps, and user
    metadata.
-   An agent layer using the Anthropic Claude Agent SDK or Pi Coding
    Agent.
-   A configurable LLM provider layer.
-   A mandatory local Ollama model for the demo.
-   At least one cloud LLM provider.
-   A transcript knowledge base based on Lenny's Podcast / Newsletter
    transcript material.
-   Grounded retrieval with source traceability.
-   Follow-up conversation handling.
-   A dedicated Ship 30 for 30 writing skill.
-   Markdown and HTML/CSS artifact generation.
-   Safe rendering/isolation of generated HTML.
-   Structured logging and graceful failure handling.
-   Automated tests for critical API, retrieval, routing, and
    persistence behavior.
-   A reproducible local startup path, preferably with Docker Compose.

The assignment explicitly requires FastAPI, PostgreSQL, an agent layer,
cloud + Ollama model configuration, transcript grounding, artifact
generation/viewing, resilience, tests, documentation, and operational
readiness.

------------------------------------------------------------------------

# 2. Recommended Backend Stack

  Area               Technology
  ------------------ ---------------------------------------------------
  Language           Python 3.11+
  API                FastAPI
  Validation         Pydantic / Pydantic Settings
  Database           PostgreSQL
  ORM                SQLAlchemy
  Migrations         Alembic
  Agent layer        Anthropic Claude Agent SDK or Pi Coding Agent
  Local LLM          Ollama
  Cloud LLM          Anthropic Claude or OpenAI
  HTTP client        httpx
  Testing            pytest
  Async testing      pytest-asyncio / HTTPX test client as appropriate
  Containerization   Docker + Docker Compose
  Logging            Python logging with structured JSON-style fields
  RAG                Embeddings + vector retrieval
  Artifact safety    HTML sanitization + isolated rendering strategy

The exact vector-store technology is intentionally left open by the
assignment. Prefer the simplest reliable implementation that can be
explained and operated easily.

------------------------------------------------------------------------

# 3. Backend Architecture

``` text
                    ┌──────────────────────┐
                    │      Frontend        │
                    └──────────┬───────────┘
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │                      │
                    │ Routes / Validation  │
                    │ Error Handling       │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌─────────────┐  ┌─────────────┐
       │ PostgreSQL │   │ Agent Layer │  │ RAG Layer   │
       │            │   │             │  │             │
       │ sessions   │   │ routing     │  │ retrieval   │
       │ messages   │   │ skills      │  │ sources     │
       │ metadata   │   │ tools       │  │ chunks      │
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
                     │ Ollama  │              │  Cloud   │
                     │ Local   │              │ Claude / │
                     │ LLM     │              │ OpenAI   │
                     └─────────┘              └──────────┘
```

------------------------------------------------------------------------

# 4. Project Structure

Recommended repository structure:

``` text
lenny-growth-assistant/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── health.py
│   │   │       ├── sessions.py
│   │   │       ├── chat.py
│   │   │       └── artifacts.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── errors.py
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── message.py
│   │   │   ├── artifact.py
│   │   │   └── document.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   ├── chat.py
│   │   │   ├── artifact.py
│   │   │   └── common.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── session_service.py
│   │   │   ├── chat_service.py
│   │   │   └── artifact_service.py
│   │   │
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   ├── ollama.py
│   │   │   ├── anthropic.py
│   │   │   └── openai.py
│   │   │
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── router.py
│   │   │   └── skills/
│   │   │       ├── __init__.py
│   │   │       ├── grounded_qa.py
│   │   │       ├── ship30.py
│   │   │       └── artifact.py
│   │   │
│   │   └── rag/
│   │       ├── __init__.py
│   │       ├── ingest.py
│   │       ├── chunking.py
│   │       ├── embeddings.py
│   │       ├── retriever.py
│   │       └── sources.py
│   │
│   ├── migrations/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── test_config.py
│   │   │   ├── test_llm_factory.py
│   │   │   ├── test_retriever.py
│   │   │   └── test_skills.py
│   │   └── integration/
│   │       ├── test_health.py
│   │       ├── test_sessions.py
│   │       ├── test_chat.py
│   │       ├── test_persistence.py
│   │       └── test_artifacts.py
│   │
│   ├── scripts/
│   │   ├── ingest_transcripts.py
│   │   └── seed_data.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│
├── docs/
│   ├── PRD.md
│   ├── design.md
│   └── architecture.md
│
├── agent-transcripts/
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

Do not create every file on day one. Add modules as each feature is
implemented.

------------------------------------------------------------------------

# 5. Environment Configuration

Create:

``` text
backend/.env.example
```

Example:

``` env
APP_ENV=development
LOG_LEVEL=INFO

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/lenny

LLM_PROVIDER=ollama

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=<local-model-name>

ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=

OPENAI_API_KEY=
OPENAI_MODEL=

CORS_ORIGINS=http://localhost:3000
```

Rules:

1.  Never commit `.env`.
2.  Commit only `.env.example`.
3.  Never put API keys in source code.
4.  Required variables must fail clearly when missing.
5.  Optional cloud credentials should not prevent the Ollama demo from
    starting.
6.  Document every variable.

------------------------------------------------------------------------

# 6. Database Design

The initial schema should support independent sessions and persistent
conversations.

## Users

``` text
users
-----
id
external_id       nullable
metadata          JSON/JSONB
created_at
updated_at
```

## Sessions

``` text
sessions
--------
id
user_id
title             nullable
created_at
updated_at
```

## Messages

``` text
messages
--------
id
session_id
role
content
metadata          JSON/JSONB
created_at
```

Roles should be constrained to values such as:

``` text
user
assistant
system
```

## Artifacts

``` text
artifacts
---------
id
session_id
message_id        nullable
type
content
metadata          JSON/JSONB
created_at
updated_at
```

Possible artifact types:

``` text
markdown
html
```

## Documents / transcript metadata

The exact design may depend on the selected vector-store implementation,
but source metadata should preserve enough information to trace a
retrieved chunk back to its transcript.

Useful fields:

``` text
documents
---------
id
source_id
title
source_url
episode_date      nullable
metadata
created_at
updated_at
```

Chunk records should retain a document/source identifier.

------------------------------------------------------------------------

# 7. Database Rules

Use SQLAlchemy for application database access.

Use Alembic for schema migrations.

Do not create tables manually as part of normal application startup.

Typical workflow:

``` bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

Before changing the schema:

1.  Modify SQLAlchemy models.
2.  Generate a migration.
3.  Inspect the migration.
4.  Apply it.
5.  Run database tests.

------------------------------------------------------------------------

# 8. API Design

The API should use explicit request and response schemas.

## Health

### `GET /health`

Expected response:

``` json
{
  "status": "ok"
}
```

A more detailed readiness endpoint may expose dependency status without
leaking secrets:

``` text
GET /health
GET /ready
```

Example readiness result:

``` json
{
  "status": "ok",
  "database": "ok",
  "llm": "ok"
}
```

Do not expose API keys, connection strings, or sensitive configuration.

------------------------------------------------------------------------

# 9. Session API

## Create session

``` text
POST /sessions
```

Example response:

``` json
{
  "id": "session-id",
  "created_at": "..."
}
```

## List sessions

``` text
GET /sessions
```

## Get session

``` text
GET /sessions/{session_id}
```

## Get messages

``` text
GET /sessions/{session_id}/messages
```

The backend must guarantee that messages from one session are never
accidentally included in another session.

------------------------------------------------------------------------

# 10. Chat API

Recommended endpoint:

``` text
POST /sessions/{session_id}/messages
```

Request:

``` json
{
  "content": "How can I improve product retention?"
}
```

Response should contain enough information for the frontend to display:

``` json
{
  "message": {
    "id": "...",
    "role": "assistant",
    "content": "..."
  },
  "sources": [
    {
      "title": "...",
      "source_url": "...",
      "document_id": "...",
      "chunk_id": "..."
    }
  ],
  "provider": "ollama",
  "model": "...",
  "skill": "grounded_qa"
}
```

The exact response can evolve, but the contract must remain explicit and
documented.

------------------------------------------------------------------------

# 11. Chat Processing Flow

For a normal grounded question:

``` text
POST /sessions/{id}/messages
              │
              ▼
       Validate request
              │
              ▼
       Load session history
              │
              ▼
       Determine task/skill
              │
              ▼
       Retrieve transcript chunks
              │
              ▼
       Build grounded context
              │
              ▼
       Run selected LLM
              │
              ▼
       Validate/source-map answer
              │
              ▼
       Persist assistant message
              │
              ▼
       Return answer + sources
```

Important:

-   Do not retrieve unrelated data from another session.
-   Do not claim transcript support when no relevant material was
    retrieved.
-   Preserve source metadata through the entire pipeline.

------------------------------------------------------------------------

# 12. LLM Provider Abstraction

Do not call Ollama or a cloud SDK directly throughout the application.

Create a common interface.

Conceptually:

``` python
class LLMProvider:
    async def generate(...):
        ...
```

Then implement:

``` text
OllamaProvider
AnthropicProvider
OpenAIProvider
```

Use a factory:

``` text
LLM_PROVIDER=ollama
        │
        ▼
LLMFactory
        │
        ▼
OllamaProvider
```

For:

``` text
LLM_PROVIDER=anthropic
```

the factory returns:

``` text
AnthropicProvider
```

The rest of the application should not need to know which provider was
selected.

------------------------------------------------------------------------

# 13. Ollama Requirements

Ollama is mandatory for the submitted local demo.

For an 8 GB RAM CPU-only machine, start with a small model rather than a
large model.

The model must be tested on the actual development machine.

Required configuration:

``` env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=<tested-model>
```

Before integrating it with the application, verify:

``` bash
ollama --version
ollama list
```

Then run a direct model test.

The backend should produce a useful error if Ollama is unavailable
instead of crashing.

Example behavior:

``` text
Ollama unavailable
        ↓
Backend detects failure
        ↓
Structured error
        ↓
Frontend displays useful message
```

------------------------------------------------------------------------

# 14. Cloud LLM

Implement at least one cloud provider.

Allowed examples from the assignment include:

-   Anthropic Claude
-   OpenAI

The provider should be selectable through configuration.

Example:

``` env
LLM_PROVIDER=anthropic
```

or:

``` env
LLM_PROVIDER=openai
```

Cloud credentials must never be committed.

------------------------------------------------------------------------

# 15. Agent Layer

The assignment requires the agent layer to use:

-   Anthropic Claude Agent SDK, or
-   Pi Coding Agent.

The agent layer should not become one giant prompt.

Recommended conceptual routing:

``` text
                  User request
                       │
                       ▼
                  Agent Router
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Grounded QA    Ship 30       Artifact
                    Skill          Skill
```

Each skill should have a clearly defined responsibility.

------------------------------------------------------------------------

# 16. Grounded QA Skill

Purpose:

> Answer product and growth questions using Lenny transcript knowledge.

Rules:

1.  Retrieve relevant transcript content.
2.  Give the model only the context needed for the answer.
3.  Preserve source metadata.
4.  Cite or clearly identify relevant sources.
5.  Do not invent transcript claims.
6.  If evidence is insufficient, say so.
7.  Follow-up questions must use the current session context.

Desired behavior:

``` text
Question
   ↓
Relevant transcript found
   ↓
Grounded answer + source
```

When nothing useful is found:

``` text
Question
   ↓
No reliable transcript evidence
   ↓
"I don't have enough information in the available
Lenny transcript material to answer that confidently."
```

------------------------------------------------------------------------

# 17. RAG Pipeline

The knowledge base should follow this pipeline:

``` text
Lenny transcripts
       ↓
Load
       ↓
Clean / normalize
       ↓
Chunk
       ↓
Generate embeddings
       ↓
Store index + metadata
       ↓
Retrieve relevant chunks
       ↓
Return chunks + source metadata
```

The implementation must document:

-   Data source.
-   Loading process.
-   Chunking strategy.
-   Indexing strategy.
-   Refresh strategy.
-   Source traceability.

These are explicit assignment requirements.

------------------------------------------------------------------------

# 18. Chunk Metadata

Every chunk should retain source information.

Example:

``` json
{
  "document_id": "doc-123",
  "chunk_id": "chunk-456",
  "title": "Episode title",
  "source_url": "...",
  "text": "Transcript chunk...",
  "metadata": {
    "episode": "...",
    "date": "..."
  }
}
```

Never discard source metadata during embedding/retrieval.

------------------------------------------------------------------------

# 19. Retrieval Quality

Do not assume retrieval is correct just because the code runs.

Create test questions where the expected transcript/source is known.

Test:

``` text
Question
→ Retrieved chunks
→ Expected source present?
→ Relevant evidence?
```

Also test an unrelated question.

Expected behavior:

``` text
No relevant evidence
→ No hallucinated transcript citation
→ Explicit unsupported-answer behavior
```

------------------------------------------------------------------------

# 20. Ship 30 for 30 Skill

Create a dedicated skill module:

``` text
app/agent/skills/ship30.py
```

It should encode the writing principles required by the assignment
rather than relying on an unstructured one-off prompt.

Output requirements:

-   Approximately 1,250 words.
-   Strong hook.
-   Clear narrative progression.
-   Skimmable headings.
-   Bullets where useful.
-   Selective bold emphasis.
-   Specific useful takeaway.
-   Claims grounded in transcript knowledge.

The skill should receive grounded source material rather than
independently inventing factual claims.

Test:

``` text
Grounded answer
      ↓
Ship30 skill
      ↓
Essay
      ↓
~1,250 words
      ↓
Grounding preserved
```

------------------------------------------------------------------------

# 21. Artifact Generation

The backend should support requests for generated artifacts.

Supported initial formats:

``` text
Markdown
HTML/CSS
```

Example flow:

``` text
Conversation
    ↓
Artifact request
    ↓
Artifact skill
    ↓
Generate content
    ↓
Validate artifact
    ↓
Persist artifact
    ↓
Return artifact metadata/content
    ↓
Frontend Artifact Viewer
```

Recommended response:

``` json
{
  "artifact": {
    "id": "...",
    "type": "html",
    "content": "...",
    "title": "..."
  }
}
```

------------------------------------------------------------------------

# 22. HTML Security

Generated HTML is untrusted.

Do not directly insert arbitrary generated HTML into the main
application DOM.

Use a defense-in-depth strategy such as:

``` text
Generated HTML
      ↓
Sanitize
      ↓
Restrict dangerous tags/attributes
      ↓
Isolated iframe / sandbox
      ↓
Artifact Viewer
```

The final implementation must document:

-   What HTML is permitted.
-   What is removed.
-   Whether scripts are allowed.
-   How external resources are handled.
-   How the artifact is isolated.
-   Why the chosen approach is safe enough for the assignment.

The frontend must never assume AI-generated HTML is trustworthy.

------------------------------------------------------------------------

# 23. Error Handling

Create consistent application errors.

Example categories:

``` text
SESSION_NOT_FOUND
INVALID_REQUEST
DATABASE_ERROR
LLM_CONFIGURATION_ERROR
LLM_UNAVAILABLE
LLM_TIMEOUT
OLLAMA_UNAVAILABLE
RETRIEVAL_ERROR
NO_RELEVANT_CONTEXT
ARTIFACT_GENERATION_ERROR
ARTIFACT_RENDERING_ERROR
```

Example response:

``` json
{
  "error": {
    "code": "OLLAMA_UNAVAILABLE",
    "message": "The local Ollama service is unavailable.",
    "request_id": "..."
  }
}
```

Do not expose stack traces to users.

Log the internal exception with a request ID.

------------------------------------------------------------------------

# 24. Resilience Requirements

The assignment specifically expects graceful handling of:

-   Missing API keys.
-   Unavailable Ollama.
-   Model timeouts.
-   Empty retrieval results.
-   Database connection failures.

Each condition should have:

``` text
Detection
   ↓
Structured internal error
   ↓
Safe user-facing response
   ↓
Useful log entry
```

Never allow an expected dependency failure to produce an unexplained 500
error.

------------------------------------------------------------------------

# 25. Logging / Observability

Use structured logs.

Every request should ideally have:

``` text
request_id
timestamp
endpoint
method
status
latency
session_id
provider
model
skill
retrieval_count
error_code
```

Do not log:

-   API keys.
-   Passwords.
-   Authorization headers.
-   Secrets.
-   Unnecessary personal information.

Useful events:

``` text
request_started
request_completed
session_created
message_persisted
retrieval_started
retrieval_completed
llm_started
llm_completed
llm_failed
artifact_generated
artifact_rejected
database_error
```

------------------------------------------------------------------------

# 26. API Validation

Use Pydantic schemas for all external requests.

Validate:

-   Required fields.
-   String lengths.
-   Session IDs.
-   Artifact types.
-   Provider names.
-   Empty messages.
-   Invalid payloads.

Example:

``` text
""
```

should not be accepted as a normal chat message.

Do not trust frontend validation alone.

------------------------------------------------------------------------

# 27. Security Checklist

Before considering the backend complete:

-   [ ] No secrets committed.
-   [ ] `.env` ignored.
-   [ ] `.env.example` provided.
-   [ ] API inputs validated.
-   [ ] SQL injection prevented by ORM/parameterized queries.
-   [ ] Generated HTML treated as untrusted.
-   [ ] Sensitive values excluded from logs.
-   [ ] CORS configured explicitly.
-   [ ] Error messages do not leak internals.
-   [ ] Session boundaries enforced.
-   [ ] Artifact rendering isolated.
-   [ ] Dependency failures handled safely.

------------------------------------------------------------------------

# 28. Testing Strategy

Testing should cover the most important backend behavior rather than
only achieving a coverage percentage.

## Unit tests

Test:

``` text
Configuration
LLM provider factory
Chunking
Retrieval logic
Source mapping
Agent routing
Ship30 skill
Artifact validation
Error mapping
```

## Integration tests

Test:

``` text
FastAPI
+
PostgreSQL
+
Services
```

At minimum:

``` text
Health
Session creation
Session retrieval
Message persistence
Session isolation
Chat request
Retrieval integration
Provider selection
Artifact creation
```

------------------------------------------------------------------------

# 29. Critical Test Cases

## Test 1 --- Health

``` text
GET /health
```

Expected:

``` text
200
status = ok
```

## Test 2 --- Create session

``` text
POST /sessions
```

Expected:

``` text
201
valid session ID
```

## Test 3 --- Session isolation

Create:

``` text
Session A
Session B
```

Send a message to A.

Ask a question in B that depends on A's message.

Expected:

``` text
B does NOT receive A's private conversation context.
```

## Test 4 --- Persistence

Create session and messages.

Restart backend.

Read session.

Expected:

``` text
Conversation still exists.
```

## Test 5 --- Provider switching

Run tests with:

``` text
LLM_PROVIDER=ollama
```

and:

``` text
LLM_PROVIDER=<cloud-provider>
```

Expected:

``` text
Correct provider selected without application-code changes.
```

## Test 6 --- Ollama failure

Stop Ollama.

Send chat request.

Expected:

``` text
Graceful structured error.
No application crash.
```

## Test 7 --- Empty retrieval

Ask something unrelated to Lenny transcripts.

Expected:

``` text
Assistant acknowledges insufficient source material.
```

## Test 8 --- Source grounding

Ask a known transcript question.

Expected:

``` text
Answer contains relevant source metadata.
```

## Test 9 --- Ship30

Generate an essay.

Verify:

``` text
~1,250 words
hook present
headings present
useful takeaway
grounded claims
```

## Test 10 --- Artifact

Generate Markdown.

Expected:

``` text
artifact persisted
artifact returned
```

Generate HTML.

Expected:

``` text
artifact returned
safe rendering metadata available
```

## Test 11 --- Invalid request

Send malformed JSON or missing required fields.

Expected:

``` text
4xx
structured validation error
```

## Test 12 --- Database failure

Make PostgreSQL unavailable.

Expected:

``` text
graceful error
useful server log
no secret leakage
```

------------------------------------------------------------------------

# 30. Test Commands

From `backend/`:

``` bash
pytest
```

Useful variants:

``` bash
pytest -v
```

``` bash
pytest tests/unit
```

``` bash
pytest tests/integration
```

During development:

``` bash
pytest -v -x
```

Run lint/type checks if configured:

``` bash
ruff check .
```

``` bash
mypy app
```

Only include tools that are actually configured in the project.

------------------------------------------------------------------------

# 31. Manual Backend Smoke Test

After starting the backend:

``` bash
GET /health
```

Then:

``` text
1. Create a session.
2. Verify the session is stored.
3. Send a normal Lenny question.
4. Verify a grounded answer.
5. Verify sources are returned.
6. Send a follow-up question.
7. Verify session context is preserved.
8. Create another session.
9. Verify contexts are independent.
10. Generate a Ship30 essay.
11. Generate a Markdown artifact.
12. Generate an HTML artifact.
13. Stop Ollama.
14. Verify graceful failure.
15. Restart Ollama.
16. Verify recovery.
```

------------------------------------------------------------------------

# 32. Local Development

Recommended Python setup:

``` bash
cd backend

python -m venv .venv
```

Windows:

``` bash
.venv\Scripts\activate
```

Linux/macOS:

``` bash
source .venv/bin/activate
```

Install:

``` bash
pip install -r requirements.txt
```

Start FastAPI:

``` bash
uvicorn app.main:app --reload
```

API should then be available at:

``` text
http://localhost:8000
```

FastAPI documentation should be available through the configured docs
endpoint.

------------------------------------------------------------------------

# 33. Docker Development

The final repository should provide a reproducible startup path.

Target workflow:

``` bash
docker compose up --build
```

Services may include:

``` text
backend
postgres
```

Ollama can either run directly on the host or be containerized depending
on the final development environment and hardware constraints.

For an 8 GB CPU-only development machine, keeping Ollama on the host is
a reasonable starting choice.

The final README must explain the selected approach.

------------------------------------------------------------------------

# 34. Recommended Development Order

Do not implement everything simultaneously.

## Phase 1 --- Backend foundation

Build:

``` text
FastAPI
Configuration
Logging
Health endpoint
Error handling
```

Verify:

``` bash
pytest
uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## Phase 2 --- Database

Build:

``` text
PostgreSQL
SQLAlchemy
Alembic
Users
Sessions
Messages
```

Verify:

``` text
Create session
Persist session
Persist message
Read message
Restart backend
Read again
```

------------------------------------------------------------------------

## Phase 3 --- LLM abstraction

Build:

``` text
LLMProvider
OllamaProvider
CloudProvider
LLMFactory
```

Verify:

``` text
Switch provider only through environment configuration.
```

------------------------------------------------------------------------

## Phase 4 --- RAG

Build:

``` text
Transcript loader
Chunker
Embedding/indexing
Retriever
Source metadata
```

Verify:

``` text
Known question → correct transcript evidence.
Unknown question → insufficient evidence behavior.
```

------------------------------------------------------------------------

## Phase 5 --- Agent

Build:

``` text
Agent
Router
Grounded QA skill
```

Verify:

``` text
Question → retrieval → grounded answer → sources.
```

------------------------------------------------------------------------

## Phase 6 --- Ship30

Build:

``` text
Ship30 skill
```

Verify:

``` text
Grounded input → approximately 1,250-word essay.
```

------------------------------------------------------------------------

## Phase 7 --- Artifacts

Build:

``` text
Artifact service
Markdown generation
HTML/CSS generation
Sanitization/isolation strategy
```

Verify:

``` text
Conversation → artifact → persistence → safe viewer payload.
```

------------------------------------------------------------------------

## Phase 8 --- Production readiness

Add:

``` text
Structured logs
Timeouts
Dependency failure handling
Database failure handling
Configuration validation
```

------------------------------------------------------------------------

## Phase 9 --- Tests

Add:

``` text
Unit tests
Integration tests
Retrieval tests
Routing tests
Persistence tests
Artifact tests
```

------------------------------------------------------------------------

## Phase 10 --- Docker + handoff

Verify from a clean environment:

``` bash
git clone <repo>
cd <repo>
cp backend/.env.example backend/.env
docker compose up --build
```

A fresh evaluator should be able to follow the documented instructions
without relying on undocumented local state.

------------------------------------------------------------------------

# 35. Definition of Done

The backend is not complete until all of these are true:

## API

-   [ ] FastAPI runs.
-   [ ] Health endpoint works.
-   [ ] Request/response contracts are documented.
-   [ ] Validation works.
-   [ ] Structured errors work.

## Database

-   [ ] PostgreSQL works.
-   [ ] Sessions persist.
-   [ ] Messages persist.
-   [ ] Session isolation works.
-   [ ] Migrations work from a clean database.

## LLM

-   [ ] Ollama works locally.
-   [ ] Cloud provider works.
-   [ ] Provider switching works through configuration.
-   [ ] Missing provider configuration is handled gracefully.
-   [ ] Timeouts are handled.

## RAG

-   [ ] Lenny transcript data is ingested.
-   [ ] Chunks are indexed.
-   [ ] Retrieval works.
-   [ ] Sources are traceable.
-   [ ] Unsupported questions are handled honestly.

## Agent

-   [ ] Required agent framework is integrated.
-   [ ] Agent routing is understandable.
-   [ ] Grounded QA skill works.
-   [ ] Ship30 skill works.
-   [ ] Artifact skill works.

## Artifacts

-   [ ] Markdown generation works.
-   [ ] HTML/CSS generation works.
-   [ ] Artifacts can be persisted.
-   [ ] HTML is treated as untrusted.
-   [ ] Rendering strategy is isolated/sanitized.

## Operations

-   [ ] `.env.example` exists.
-   [ ] No secrets are committed.
-   [ ] Logs are useful.
-   [ ] Ollama failure is handled.
-   [ ] Database failure is handled.
-   [ ] Empty retrieval is handled.
-   [ ] Docker startup works.

## Tests

-   [ ] API tests.
-   [ ] Retrieval tests.
-   [ ] Provider/routing tests.
-   [ ] Persistence tests.
-   [ ] Artifact tests.
-   [ ] Manual UI/backend smoke test documented.

------------------------------------------------------------------------

# 36. What We Should NOT Do

Avoid unnecessary complexity.

Do not:

-   Put the entire backend into `main.py`.
-   Hard-code an LLM provider.
-   Hard-code API keys.
-   Mix database logic directly into route handlers.
-   Let the frontend determine whether a request is valid.
-   Claim sources that were not retrieved.
-   Send every transcript to every LLM request.
-   Render arbitrary generated HTML directly in the main page.
-   Add infrastructure that does not solve an assignment requirement.
-   Skip tests until the very end.
-   Treat "it works on my PC" as deployment readiness.

------------------------------------------------------------------------

# 37. Backend Acceptance Flow

The final backend should support this complete flow:

``` text
User starts application
        ↓
Backend health check
        ↓
Create new session
        ↓
User asks Lenny-related question
        ↓
FastAPI validates request
        ↓
Session history loaded
        ↓
Agent selects grounded QA
        ↓
Retriever searches Lenny transcripts
        ↓
Relevant chunks + source metadata
        ↓
Selected LLM
        ↓
Grounded answer
        ↓
Answer + sources persisted
        ↓
Response returned to frontend
```

Then:

``` text
User asks:
"Turn that into a Ship 30 for 30 essay."
        ↓
Agent routes to Ship30 skill
        ↓
Uses grounded conversation/context
        ↓
~1,250-word essay
        ↓
Persist
        ↓
Return
```

And:

``` text
User asks:
"Create an HTML version."
        ↓
Artifact skill
        ↓
HTML/CSS generated
        ↓
Security validation
        ↓
Persist artifact
        ↓
Return artifact
        ↓
Frontend Artifact Viewer renders safely
```

------------------------------------------------------------------------

# 38. Final Backend Verification

Before calling the backend finished, perform a clean-room test.

``` text
1. Clone repository into a new directory.
2. Create .env from .env.example.
3. Start PostgreSQL.
4. Start Ollama.
5. Pull/configure the tested local model.
6. Run database migrations.
7. Run transcript ingestion.
8. Start FastAPI.
9. Run automated tests.
10. Run smoke tests.
11. Test Ollama mode.
12. Test cloud mode.
13. Test session isolation.
14. Test unsupported retrieval.
15. Test Ship30.
16. Test Markdown artifact.
17. Test HTML artifact.
18. Test Ollama outage.
19. Test database outage.
20. Verify logs.
21. Verify no secrets are present.
22. Verify Docker startup.
```

The most important final test is:

> **Could a fresh evaluator clone the repository, follow the README,
> start the system, and understand why each part exists?**

If yes, the backend is in a strong state for the assignment.
