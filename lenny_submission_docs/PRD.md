# Product Requirements Document — Lenny Growth Assistant

## 1. Product Summary

The Lenny Growth Assistant is a full-stack AI-powered conversational assistant for product management and growth questions. It uses Lenny's Podcast / Newsletter transcript knowledge base as the primary source of truth and combines retrieval-augmented generation (RAG), an agent layer with specialized skills, persistent chat sessions, runtime LLM switching, and an in-app artifact viewer.

The product is designed for users who want practical, source-grounded product/growth guidance without manually searching long transcripts.

## 2. Primary User

A product manager, founder, growth practitioner, or product-focused operator who wants to:
- ask product and growth questions naturally;
- continue conversations with context preserved;
- trace answers to relevant Lenny transcript sources;
- turn an answer into a Ship 30 for 30-style essay;
- generate Markdown or HTML artifacts beside the conversation;
- change the active LLM provider without editing code or restarting the application.

## 3. Problem

Lenny's content contains a large amount of product and growth knowledge, but finding the right passage and turning it into an actionable answer requires manual searching, reading, synthesis, and writing.

The product should reduce that effort while preserving source grounding. A useful answer should be traceable to available transcript material and should explicitly acknowledge when the material does not support a claim.

## 4. Goals

1. Provide grounded conversational answers from the transcript knowledge base.
2. Preserve independent session context and persist conversations in PostgreSQL.
3. Route requests through an agent layer with clear skill boundaries.
4. Provide a dedicated Ship 30 for 30 writing workflow.
5. Generate Markdown or HTML artifacts inside the application.
6. Allow runtime switching between configured LLM providers.
7. Handle provider, retrieval, model, database, and artifact failures gracefully.
8. Leave behind a reproducible system another engineer can run and extend.

## 5. Success Metrics

### Primary
**Grounded answer usefulness rate:** percentage of evaluator questions where the response contains a relevant answer and correct supporting transcript source when the knowledge base supports the question.

### Operational
- Health/readiness endpoints provide actionable status.
- Critical automated tests remain green.
- Runtime switching succeeds for configured and available providers.
- An unavailable provider is rejected without replacing the active provider.
- A fresh evaluator can start the system using documented steps.

## 6. Assumptions

- Lenny transcript content is the authoritative knowledge source for grounded answers.
- At least one cloud provider can be configured for evaluation; Ollama is available locally for the demo.
- Authentication and multi-tenant authorization are outside assignment scope.
- Runtime switching changes provider state for the running backend process.
- Provider/model choices are controlled by backend configuration, not arbitrary browser input.

## 7. Scope

### In scope
- FastAPI backend.
- PostgreSQL persistence and migrations.
- Session/message APIs.
- Transcript ingestion, chunking, indexing/retrieval, and source metadata.
- Agent routing and Grounded QA, Ship 30 for 30, and Artifact Generation skills.
- Ollama local model support.
- Configured cloud model support.
- Runtime LLM switching from the UI.
- Markdown/HTML artifact viewer.
- HTML sanitization/isolation.
- Structured errors, health/readiness, and operational logs.
- Automated tests and UI manual testing.
- Docker Compose startup path and environment examples.

### Out of scope
- User authentication/account management.
- Multi-tenant permissions.
- Production billing/quotas.
- Model fine-tuning/training.
- Arbitrary web browsing as the grounded source of truth.
- Browser-supplied provider credentials.
- Collaborative artifact editing.

## 8. Core User Flows

### A. Grounded Q&A
1. User creates a chat.
2. User asks a product/growth question.
3. Backend loads session context.
4. Agent routes to Grounded QA.
5. Retriever selects relevant transcript chunks.
6. Skill creates a grounded answer.
7. Response and metadata are persisted.
8. UI renders answer and sources.
9. If evidence is insufficient, the assistant explicitly says so.

### B. Follow-up
1. User asks a follow-up in the same session.
2. Previous messages are loaded.
3. Agent uses conversation context plus newly retrieved evidence.
4. Response is persisted in the same session.

### C. Ship 30 for 30
1. User requests an essay.
2. Router selects the Ship 30 for 30 skill.
3. Relevant transcript content is retrieved.
4. Dedicated writing structure is applied.
5. Output targets approximately 1,250 words with a strong hook, narrative progression, skimmable formatting, and a useful takeaway.
6. Sources remain attached to grounded claims.

### D. Artifact generation
1. User requests Markdown or HTML/CSS.
2. Router selects the artifact skill.
3. Current conversation context is supplied to generation.
4. Generated HTML is sanitized.
5. Frontend renders it beside the chat.

### E. Runtime LLM switching
1. User opens the provider selector.
2. UI lists configured providers/models.
3. User selects a provider.
4. Frontend calls `POST /config/llm`.
5. Backend validates and checks availability.
6. Successful selection updates runtime state.
7. Failed selection leaves the previous provider active.
8. UI updates only after successful confirmation.

## 9. Acceptance Criteria

### Assistant
- New chats work.
- Session context is isolated and persisted.
- Grounded questions return transcript-backed answers.
- Unsupported questions produce an explicit lack-of-support response.

### LLM configuration
- Provider switching needs no source-code changes.
- Ollama is usable for the demo.
- At least one cloud provider is configurable.
- Active provider/model is visible.
- Unavailable providers are rejected without changing runtime state.

### Knowledge base
- Transcripts can be ingested.
- Chunks retain source metadata.
- Retrieval returns relevant context.
- Responses expose supporting sources.

### Ship 30 for 30
- Dedicated routing/skill exists.
- Output is approximately 1,250 words.
- Strong hook and narrative progression.
- Skimmable headings/bullets/selective emphasis.
- Specific useful takeaway.
- Claims grounded in transcript knowledge.

### Artifacts
- Markdown renders correctly.
- HTML/CSS renders beside the chat.
- Generated HTML is treated as untrusted and sanitized/isolated.

### Operations
- `.env.example` has safe defaults/placeholders.
- Secrets are not committed.
- Health/readiness endpoints exist.
- Failures return structured errors/logs.
- Docker Compose or equivalent is documented.
- Critical automated tests exist.

## 10. Risks and Trade-offs

| Risk | Decision |
|---|---|
| Hallucination | Retrieval-grounded prompts, sources, and explicit unsupported-answer behavior. |
| Local model quality | Ollama is used for the required local demo; cloud providers remain configurable. |
| Ollama latency | Configurable request timeout and visible active-provider state. |
| Cloud cost | Runtime provider choice plus local Ollama for development/demo. |
| Provider outage | Availability check before switching; preserve previous provider on failure. |
| Unsafe HTML | Sanitization and constrained rendering. |
| Retrieval miss | Clear lack-of-support response rather than invented evidence. |
| Provider coupling | `LennyAgent` depends on `BaseLLMProvider`, not provider-specific agents. |

## 11. Implementation Plan

1. FastAPI, PostgreSQL, sessions, and persistence.
2. LLM abstraction and Ollama.
3. Cloud provider behind the same abstraction.
4. Transcript ingestion/chunking/indexing/retrieval.
5. Agent routing and skills.
6. Grounded source display and unsupported-answer handling.
7. Artifact generation, sanitization, and viewer.
8. Runtime LLM configuration and UI selector.
9. Automated tests and failure-path verification.
10. Documentation, demo, and fresh-clone verification.
