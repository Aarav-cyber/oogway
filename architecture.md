# Lenny Growth Assistant --- Architecture Specification

## Overview

The Lenny Growth Assistant is an AI-powered growth advisor built over Lenny's Podcast and Newsletter transcripts. It combines RAG (Retrieval-Augmented Generation), an Agent framework with specialized skills (Grounded QA, Ship 30 for 30 Atomic Essays, Artifact Generation), and runtime LLM provider switching.

---

## 1. High-Level Architecture Diagram

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

## 2. Model-Toggle & LLM Configuration Architecture

### Runtime State Management
The backend maintains an in-process runtime state (`app/llm/runtime.py`) determining the currently selected provider and model.

- **Initial State**: Bootstrapped from `.env` (`LLM_PROVIDER=ollama`).
- **Dynamic Switch**: The `POST /config/llm` endpoint validates the requested provider, verifies its health and credentials (`check_availability()`), and updates the active runtime state without restarting the server or editing `.env`.
- **Factory Pattern**: `LLMFactory` delegates requests to the active provider instance:
  - `OllamaProvider` (`llama3.2`)
  - `GroqProvider` (`openai/gpt-oss-20b`)
  - `GeminiProvider` (`gemini-2.5-flash`)
- **Agent Abstraction Decoupling**: `LennyAgent` and all downstream agent skills (`GroundedQASkill`, `Ship30Skill`, `ArtifactSkill`) interact strictly with `BaseLLMProvider`. Changing the provider requires zero code changes to agent or RAG logic.

### Server-Side Security & Credentials
- All API keys (`GROQ_API_KEY`, `GEMINI_API_KEY`) remain strictly server-side in backend environment variables.
- The frontend never receives API keys and only interacts with `POST /config/llm` and `GET /ready`.

---

## 3. RAG & Retrieval Engine
- **Chunking**: Overlapping sliding window chunker splitting documents at paragraph/sentence boundaries.
- **Indexing & Retrieval**: BM25 relevance scoring calculating IDF frequencies over database `chunks` table.
- **Source Attribution**: Retained chunk metadata (`source_id`, `title`, `source_url`, `episode_date`) attached to assistant messages for explicit source grounding.

---

## 4. Artifact Rendering & Security
- **Defense in Depth**: Generated HTML/CSS artifacts undergo backend sanitization (`nh3`) and frontend sanitization (`DOMPurify`).
- **Iframe Sandbox**: Rendered inside an isolated `<iframe>` with strict sandbox flags (`sandbox="allow-same-origin allow-popups"`), preventing untrusted script execution.
