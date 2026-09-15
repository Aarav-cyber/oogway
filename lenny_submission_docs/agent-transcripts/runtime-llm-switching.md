# Coding-Agent Transcript / Engineering Log

> This document summarizes the coding-agent work for runtime LLM configuration. Secrets and sensitive values are omitted.

## Objective

Allow the evaluator to switch the active LLM provider from the frontend without editing source code or restarting the backend.

## Implementation Sequence

1. Added runtime provider state in `backend/app/llm/runtime.py`.
2. Added cloud provider implementations for the configured providers.
3. Updated `LLMFactory` to resolve the provider from runtime state.
4. Updated environment configuration and `.env.example`.
5. Added `POST /config/llm` and `GET /config/llm`.
6. Updated readiness reporting to expose active provider/model.
7. Added backend tests for runtime LLM configuration.
8. Added frontend API functions.
9. Added `useLLMConfig` state.
10. Updated the header with an interactive provider/model selector.
11. Connected selector actions to the backend switching endpoint.
12. Added frontend selector tests.
13. Updated README and architecture documentation.

## Architecture Decision

```text
LennyAgent
    ↓
BaseLLMProvider
    ↓
LLMFactory
    ↓
Runtime-selected provider
```

Provider-specific logic stays inside provider implementations rather than creating separate agents.

## Availability Validation

```text
Select unavailable provider
        ↓
POST /config/llm
        ↓
Validate provider
        ↓
Availability check
        ↓
Failure → structured error + keep current provider
Success → update runtime provider
```

## Verification

Backend test suite:

```text
22 passed
```

Frontend test suite:

```text
4 test files passed
8 tests passed
```

Frontend production build also succeeded during implementation verification.

## Failed Attempt / Correction Log

### Ollama timeout

**Problem:** RAG-backed local Ollama requests could exceed the initial fixed request timeout.

**Correction:** Made the Ollama request timeout configurable and used a larger timeout appropriate for CPU-based local inference.

**Result:** Ollama chat requests completed successfully after the timeout adjustment.

### Unavailable Ollama

**Test:** Temporarily pointed the backend Ollama URL at an unavailable endpoint.

**Observed behavior:** Runtime switching to Ollama returned an LLM-provider-unavailable error rather than activating the broken provider.

**Correction:** Restored the local Ollama URL and confirmed the service was reachable again.

### Unsupported source question

**Observed behavior:** An unsupported question produced an explicit lack-of-support response, but the UI could still show unrelated retrieved source cards.

**Follow-up refinement:** Treat source display as a grounding UX improvement so unsupported answers do not visually imply that unrelated retrieved chunks support the answer.

## Security / Privacy

- Real provider keys are not recorded in this document.
- `.env` is excluded from version control.
- `.env.example` contains configuration placeholders.
