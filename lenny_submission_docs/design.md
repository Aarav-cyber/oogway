# Design Specification — Lenny Growth Assistant

## 1. Design Objective

The interface should feel like a focused growth-advisory workspace rather than a generic chatbot. Conversation is primary; evidence and generated artifacts are supporting surfaces that stay close to the conversation.

## 2. UX Principles

### Grounded by default
Answers are visually paired with their evidence so users can understand where a response came from.

### Conversation first
The main workspace prioritizes the chat. Secondary panels support, rather than replace, the conversation.

### Understandable system state
The active LLM provider/model is visible in the header. Runtime switching is exposed as a compact control.

### Clear failure states
Errors explain what failed. A failed LLM switch does not silently alter the active provider.

### Generate in place
Markdown and HTML artifacts appear in an adjacent Artifact Viewer so users do not lose conversational context.

## 3. Information Architecture

```text
Application
├── Header
│   ├── Product name
│   ├── Active LLM provider/model
│   └── Artifact toggle
├── Sidebar
│   ├── New Chat
│   └── Recent Chats
└── Main workspace
    ├── Chat Window
    │   ├── Message List
    │   ├── Source List
    │   └── Chat Input
    └── Artifact Viewer
        ├── Artifact Header
        ├── Markdown Renderer
        └── Sanitized HTML Renderer
```

## 4. Key Interaction States

| State | Expected behavior |
|---|---|
| Empty session | Introduction and suggested prompts. |
| Sending | Loading state and duplicate-send prevention. |
| Success | Assistant answer plus sources. |
| Unsupported question | Explicit lack-of-support response. |
| LLM switching | Current provider shown; UI updates after backend success. |
| LLM unavailable | Clear error; current provider remains active. |
| Artifact open | Viewer beside conversation. |
| Artifact closed | Chat returns to primary workspace. |
| Backend unavailable | Sending is blocked or a clear service/network error is surfaced. |

## 5. Responsive Behavior

### Desktop
Persistent sidebar, main chat workspace, and right-side Artifact Viewer when open.

### Tablet
Collapsible/reduced sidebar and narrower artifact panel.

### Mobile
Mobile navigation, full-width chat, and focused artifact surface without horizontal overflow.

## 6. Accessibility

- Semantic buttons for interactive controls.
- Keyboard-accessible provider selector.
- Visible focus states.
- Accessible labels for icon-only controls.
- Readable text contrast.
- Loading/error states communicated by text, not color alone.
- Generated HTML constrained so embedded content cannot take over application navigation.

## 7. Conversation Design

Assistant responses prioritize:
1. Direct answer.
2. Practical implications.
3. Supporting transcript sources.
4. Optional next action/artifact when relevant.

Raw API payloads and internal routing details are kept out of the user-facing interface.

## 8. Source Design

Source UI should answer:
- Which transcript was used?
- What retrieved excerpt/chunk supports the answer?
- Why does this source matter?

Unsupported responses should not present unrelated retrieval results as supporting evidence.

## 9. Runtime LLM Selector

The header displays the active provider/model, for example:

```text
CPU  Ollama • llama3.2  ▾
```

The selector lists configured choices such as:

```text
Ollama  — llama3.2
Groq    — openai/gpt-oss-20b
Gemini  — gemini-2.5-flash
```

Switching:

```text
Select provider
      ↓
POST /config/llm
      ↓
Validate + availability check
   ↙                 ↘
success              failure
  ↓                    ↓
update UI          keep current provider
```

Credentials never appear in the browser.

## 10. Artifact Viewer

Supports:
- Markdown rendering.
- HTML/CSS preview.
- Copy functionality.
- Open/close controls.
- Sanitization/isolation for untrusted generated HTML.

## 11. Visual Design Decisions

- Dark application shell for a focused workspace.
- Subtle borders and compact cards for hierarchy.
- Monospaced type for provider/model system status.
- Consistent spacing and constrained message width.
- Accent treatment reserved for actions and state.

## 12. Design Trade-offs

### Persistent sidebar vs chat width
A compact sidebar improves navigation while preserving most conversation width; it collapses on smaller screens.

### Inline sources vs separate source page
Inline sources reduce navigation cost and make grounding easier to inspect.

### Header selector vs settings page
Provider selection is an active runtime state, so it is exposed where system state is already visible.

### Side-by-side artifacts vs new page
A side panel preserves context and matches the flow of generating an artifact from conversation.

## 13. UI Manual Test Plan

### Chat
- Create a chat.
- Send a grounded product/growth question.
- Verify the answer and relevant sources.
- Ask a follow-up and verify context.
- Ask an unsupported question and verify lack-of-support behavior.

### LLM switching
- Verify current provider/model.
- Switch Ollama → Groq → Gemini.
- Verify header state and successful chat requests.
- Make Ollama unavailable and verify the switch is rejected while the prior provider remains active.
- Restore Ollama.

### Ship 30 for 30
- Request an essay.
- Verify approximately 1,250 words, hook, narrative, skimmable structure, takeaway, and source grounding.

### Artifacts
- Generate Markdown and verify rendering.
- Generate HTML/CSS and verify rendering.
- Verify unsafe content is sanitized/isolated.

### Resilience
- Unavailable provider.
- Model timeout.
- Empty retrieval.
- Backend unavailable.
- Database failure.

### Accessibility
- Keyboard navigation.
- Visible focus.
- Accessible button names.
- Text-based error communication.
