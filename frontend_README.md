# Lenny Growth Assistant --- Frontend README

## 1. Purpose

This document is the implementation guide for the frontend of **The
Lenny Growth Assistant**.

The frontend turns the backend into a polished product experience. It
must provide:

-   Conversational chat UI
-   New-chat and session switching
-   Independent conversation display
-   Grounded source display
-   Visible LLM provider/model information
-   Loading, empty, error, and unsupported-answer states
-   Ship 30 for 30 output presentation
-   Markdown artifact rendering
-   HTML/CSS artifact rendering
-   An Artifact Viewer beside the chat
-   Safe handling of generated HTML
-   Responsive desktop/tablet/mobile behavior
-   Keyboard and accessibility support
-   Automated frontend tests and an end-to-end smoke test

The backend remains responsible for LLM calls, retrieval, agent routing,
persistence, and server-side security decisions. The frontend is
responsible primarily for interaction, presentation, and API
integration.

------------------------------------------------------------------------

## 2. Recommended Frontend Stack

  Area                Technology
  ------------------- -----------------------------------------
  Framework           React
  Language            TypeScript
  Build tool          Vite
  Styling             Tailwind CSS
  UI components       shadcn/ui
  Server state        TanStack Query
  Markdown            React Markdown
  HTML defense        DOMPurify + isolated rendering strategy
  Icons               Lucide React
  Component testing   Vitest + React Testing Library
  E2E testing         Playwright

Keep the frontend intentionally simple. Do not introduce libraries
unless they solve a real requirement.

------------------------------------------------------------------------

## 3. Product Layout

Desktop target:

``` text
┌────────────────────────────────────────────────────────────────────┐
│                    LENNY GROWTH ASSISTANT                         │
├────────────────┬──────────────────────────────┬────────────────────┤
│   SIDEBAR      │           CHAT               │     ARTIFACT       │
│                │                              │      VIEWER         │
│ + New Chat     │  User message                │                    │
│                │  Assistant response          │  Artifact title     │
│ RECENT         │                              │  ┌──────────────┐  │
│ Chat 1         │  Sources                     │  │   Preview    │  │
│ Chat 2         │  • Transcript source         │  │              │  │
│ Chat 3         │                              │  └──────────────┘  │
│                │  ┌────────────────────────┐  │                    │
│                │  │ Ask anything...       ↑│  │                    │
│                │  └────────────────────────┘  │                    │
└────────────────┴──────────────────────────────┴────────────────────┘
```

The assignment requires the Artifact Viewer to render generated Markdown
or HTML/CSS beside the chat instead of showing only raw code or
redirecting elsewhere.

------------------------------------------------------------------------

## 4. Project Structure

``` text
frontend/
│
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   └── routes.tsx
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppLayout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   └── MobileNav.tsx
│   │   │
│   │   ├── chat/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── TypingIndicator.tsx
│   │   │   └── SourceList.tsx
│   │   │
│   │   ├── artifacts/
│   │   │   ├── ArtifactViewer.tsx
│   │   │   ├── ArtifactHeader.tsx
│   │   │   ├── MarkdownArtifact.tsx
│   │   │   └── HtmlArtifact.tsx
│   │   │
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── EmptyState.tsx
│   │       ├── ErrorState.tsx
│   │       └── LoadingState.tsx
│   │
│   ├── api/
│   │   ├── client.ts
│   │   ├── sessions.ts
│   │   ├── chat.ts
│   │   └── artifacts.ts
│   │
│   ├── hooks/
│   │   ├── useSessions.ts
│   │   ├── useChat.ts
│   │   └── useArtifacts.ts
│   │
│   ├── types/
│   │   ├── session.ts
│   │   ├── message.ts
│   │   ├── artifact.ts
│   │   └── api.ts
│   │
│   ├── lib/
│   │   ├── utils.ts
│   │   └── sanitize.ts
│   │
│   ├── styles/
│   │   └── globals.css
│   │
│   ├── main.tsx
│   └── vite-env.d.ts
│
├── public/
├── tests/
│   ├── components/
│   ├── integration/
│   └── e2e/
│
├── package.json
├── tsconfig.json
├── vite.config.ts
├── playwright.config.ts
└── .env.example
```

Do not create every file before its feature is needed. Build
incrementally.

------------------------------------------------------------------------

## 5. Frontend Architecture

``` text
                         React UI
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
       Sidebar            Chat             Artifact Viewer
          │                 │                  │
          └─────────────────┼──────────────────┘
                            ▼
                       React Hooks
                            ▼
                    TanStack Query
                            ▼
                       API Client
                            ▼
                         FastAPI
```

The frontend must not implement:

-   Transcript retrieval
-   Embedding generation
-   RAG logic
-   LLM prompt construction
-   Agent routing
-   Database persistence
-   Provider credentials
-   Server-side security decisions

Those belong to the backend.

------------------------------------------------------------------------

## 6. Environment Configuration

Create:

``` text
frontend/.env.example
```

Example:

``` env
VITE_API_BASE_URL=http://localhost:8000
```

Rules:

1.  Never commit `.env`.
2.  Commit `.env.example`.
3.  Never put LLM API keys in the frontend.
4.  Only expose browser-safe configuration.
5.  Never put PostgreSQL credentials in frontend variables.

The browser communicates with FastAPI. It should not call the LLM
directly using secret credentials.

------------------------------------------------------------------------

## 7. API Client

Create one centralized API client:

``` text
src/api/client.ts
```

Flow:

``` text
React Component
      ↓
Custom Hook
      ↓
API Module
      ↓
API Client
      ↓
FastAPI
```

Avoid scattered raw `fetch()` calls.

The client should handle:

-   Base URL
-   JSON parsing
-   HTTP errors
-   Common headers
-   Consistent error conversion

------------------------------------------------------------------------

## 8. Backend API Integration

Integrate with the backend endpoints actually implemented.

Expected categories:

``` text
GET  /health

POST /sessions
GET  /sessions
GET  /sessions/{session_id}
GET  /sessions/{session_id}/messages

POST /sessions/{session_id}/messages

Artifact endpoints as defined by the backend.
```

The frontend contract must match the real backend implementation.

------------------------------------------------------------------------

## 9. TypeScript Types

Mirror backend response contracts.

Example:

``` ts
type Session = {
  id: string
  created_at: string
  updated_at?: string
}
```

``` ts
type Message = {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  created_at: string
}
```

``` ts
type Source = {
  document_id: string
  chunk_id?: string
  title: string
  source_url?: string
}
```

``` ts
type Artifact = {
  id: string
  type: "markdown" | "html"
  title?: string
  content: string
}
```

``` ts
type ApiError = {
  error: {
    code: string
    message: string
    request_id?: string
  }
}
```

Keep frontend and backend contracts synchronized.

------------------------------------------------------------------------

## 10. Sidebar

The sidebar should provide:

``` text
LENNY GROWTH ASSISTANT

+ New Chat

RECENT
────────────────
How to improve retention
Product strategy
Growth loops
```

Required behavior:

-   New chat creates a backend session.
-   Existing sessions can be selected.
-   Selected session is clearly highlighted.
-   Sessions load from the backend.
-   Loading/error states are handled.
-   Long titles truncate gracefully.
-   Mobile converts the sidebar to a drawer/navigation control.

Do not use fake local-only sessions once backend persistence exists.

------------------------------------------------------------------------

## 11. New Chat Flow

``` text
Click + New Chat
      ↓
POST /sessions
      ↓
Receive session ID
      ↓
Set active session
      ↓
Clear current messages
      ↓
Show empty state
```

A new session must not inherit another session's messages.

------------------------------------------------------------------------

## 12. Chat Window

Structure:

``` text
Header
  ↓
Message list
  ↓
Sources attached to assistant responses
  ↓
Composer
```

Example:

``` text
USER

How should we improve product retention?
```

Then:

``` text
LENNY GROWTH ASSISTANT

Based on the available transcript material...

Sources
• Building Retention Loops
• Product Growth Strategy
```

User and assistant messages must be visually distinct.

------------------------------------------------------------------------

## 13. Chat Input

Target:

``` text
┌────────────────────────────────────────────┐
│ Ask about product, growth, retention...  ↑│
└────────────────────────────────────────────┘
```

Required:

-   Enter sends.
-   Shift + Enter creates a newline.
-   Empty messages cannot submit.
-   Submit control disables appropriately.
-   Input remains stable during loading.
-   Keyboard focus is preserved where practical.
-   New messages scroll into view.
-   Errors do not silently discard the user's message.

------------------------------------------------------------------------

## 14. Chat Request Flow

``` text
User types question
        ↓
Frontend validates non-empty content
        ↓
Display user message
        ↓
POST /sessions/{id}/messages
        ↓
Show loading state
        ↓
Receive assistant response
        ↓
Display answer
        ↓
Display sources
        ↓
Display provider/model
```

Do not show a successful assistant response before the backend confirms
it.

------------------------------------------------------------------------

## 15. Loading State

Use a compact indicator:

``` text
Lenny Growth Assistant

Thinking...
● ● ●
```

It should:

-   Clearly communicate progress.
-   Prevent duplicate submissions where appropriate.
-   Keep safe parts of the UI usable.
-   Avoid unnecessary flashing for very fast responses.

------------------------------------------------------------------------

## 16. Empty State

A new session should guide the evaluator:

``` text
What can I help you with?

Ask Lenny about:

Product strategy
Growth
Retention
User research
Product-market fit
```

Keep the initial experience focused on the intended product use.

------------------------------------------------------------------------

## 17. Error States

Translate backend errors into useful messages.

Examples:

### Backend unavailable

``` text
Unable to connect to the assistant.

Check that the backend is running and try again.
```

### Ollama unavailable

``` text
The local model is unavailable.

Make sure Ollama is running and try again.
```

### Timeout

``` text
The model took too long to respond.

Please try again.
```

### Database failure

``` text
We couldn't save this conversation.

Please try again.
```

### Generic failure

``` text
Something went wrong.

Request ID: abc123
```

Never display raw stack traces.

------------------------------------------------------------------------

## 18. Unsupported / No-Grounding State

If the backend reports insufficient Lenny transcript evidence, display
it honestly:

``` text
I couldn't find enough information in the available
Lenny transcript material to answer that confidently.
```

Do not invent sources or replace the backend's grounded behavior with a
generic AI answer.

------------------------------------------------------------------------

## 19. Source Display

Attach sources to the relevant assistant response:

``` text
Sources
────────────────────────────
▣ Building Retention Loops
  Lenny's Podcast

▣ Product Growth Strategy
  Lenny's Podcast
```

Where a URL is available, make it navigable.

The UI should make grounding obvious without overwhelming the answer.

------------------------------------------------------------------------

## 20. Provider / Model Indicator

Show current provider/model:

``` text
● Ollama · local-model
```

or:

``` text
● Claude
```

The value should come from backend configuration/response, not be
hard-coded into the chat component.

This is especially useful for the required Ollama demo.

------------------------------------------------------------------------

## 21. Follow-Up Questions

The frontend must preserve the active session:

``` text
User:
How should we improve retention?

Assistant:
...

User:
What did the guests say about onboarding?

Assistant:
...
```

When switching sessions:

``` text
Session A
   ✕
Session B
```

Only the selected session's conversation should be displayed.

The backend owns actual conversation context; the frontend sends the
active session ID.

------------------------------------------------------------------------

## 22. Markdown Rendering

Render Markdown responses and Markdown artifacts as formatted content.

Support:

-   Headings
-   Paragraphs
-   Lists
-   Links
-   Bold
-   Code blocks
-   Tables where needed

Do not blindly render arbitrary HTML from Markdown.

------------------------------------------------------------------------

## 23. Artifact Viewer

The Artifact Viewer is a first-class feature.

``` text
┌──────────────────────────┬─────────────────────────┐
│ Chat                     │ Artifact                │
│                          │                         │
│ Assistant response...    │ Landing Page            │
│                          │                         │
│                          │ ┌─────────────────────┐ │
│                          │ │      PREVIEW        │ │
│                          │ │                     │ │
│                          │ └─────────────────────┘ │
└──────────────────────────┴─────────────────────────┘
```

Support:

-   Markdown artifacts
-   HTML/CSS artifacts
-   Artifact title
-   Loading state
-   Error state
-   Empty state
-   Close/hide behavior
-   Responsive behavior

------------------------------------------------------------------------

## 24. Artifact Viewer States

### Empty

``` text
No artifact yet.

Ask the assistant to create something.
```

### Loading

``` text
Creating artifact...
```

### Markdown

Render with the Markdown renderer.

### HTML

Render using the approved isolated/sanitized strategy.

### Error

``` text
This artifact couldn't be rendered.

Try generating it again.
```

------------------------------------------------------------------------

## 25. HTML Artifact Security

Generated HTML is untrusted.

Avoid:

``` tsx
<div dangerouslySetInnerHTML={{ __html: artifact }} />
```

for arbitrary AI output.

Use backend security controls plus frontend defense in depth:

``` text
AI-generated HTML
       ↓
Backend validation/sanitization
       ↓
Frontend receives artifact
       ↓
Isolated rendering
       ↓
Artifact Viewer
```

For HTML preview, prefer an isolated iframe/sandbox strategy with
deliberately restricted capabilities.

Document and test:

-   Whether scripts are allowed.
-   Whether forms are allowed.
-   Whether navigation is allowed.
-   Whether external network requests are allowed.
-   What sanitization occurs.
-   What iframe sandbox flags are used.
-   What happens when unsafe content is detected.

------------------------------------------------------------------------

## 26. Responsive Design

### Desktop

``` text
Sidebar | Chat | Artifact
```

### Tablet

``` text
Sidebar | Chat + Artifact
```

### Mobile

``` text
Header
Chat
Composer

Artifact opens as:
- drawer
- tab
- full-screen panel
```

Do not force horizontal scrolling on mobile.

------------------------------------------------------------------------

## 27. Accessibility

Implement:

-   Semantic HTML.
-   Keyboard navigation.
-   Visible focus states.
-   Proper button labels.
-   Accessible form labels.
-   Appropriate ARIA where necessary.
-   Sufficient contrast.
-   Screen-reader-friendly loading/error states.
-   Keyboard access to sidebar and artifact controls.
-   No color-only state indicators.
-   Reduced-motion support where animations are introduced.

Perform a complete keyboard-navigation pass before submission.

------------------------------------------------------------------------

## 28. Visual Design Principles

The interface should feel like a serious internal AI/productivity tool.

Prioritize:

-   Clear hierarchy.
-   Strong typography.
-   Consistent spacing.
-   Subtle borders/dividers.
-   Clear interactive states.
-   Minimal unnecessary decoration.
-   Readable assistant responses.
-   Visible but unobtrusive sources.
-   Artifact preview that feels like a workspace.

Do not prioritize visual effects over usability.

------------------------------------------------------------------------

## 29. Component Responsibilities

### `AppLayout`

Overall page layout, sidebar, chat, artifact viewer.

### `Sidebar`

Session list, new chat, session selection.

### `ChatWindow`

Active conversation and composer placement.

### `MessageList`

Message ordering, empty state, loading placement.

### `MessageBubble`

User/assistant presentation, Markdown rendering, message metadata.

### `SourceList`

Source presentation and links.

### `ChatInput`

Text entry and keyboard/submit behavior.

### `ArtifactViewer`

Artifact visibility, type, loading/error states.

### `MarkdownArtifact`

Safe Markdown presentation.

### `HtmlArtifact`

Safe HTML preview through the approved isolation strategy.

------------------------------------------------------------------------

## 30. State Management

Prefer TanStack Query for server state.

Examples:

``` text
sessions query
session messages query
send message mutation
artifact query
artifact generation mutation
```

Keep ephemeral UI state local:

``` text
active artifact panel
composer text
mobile sidebar open
artifact viewer open
```

Do not add a global state store unless genuinely necessary.

------------------------------------------------------------------------

## 31. Cache Rules

When creating a session:

``` text
Create session
↓
Refresh sessions
↓
Set new active session
↓
Load messages
```

When sending a message:

``` text
Send message
↓
Update/refetch current session
↓
Keep other sessions unchanged
```

When switching sessions:

``` text
Active session ID changes
↓
Fetch that session's messages
```

Never display cached messages from another active session.

------------------------------------------------------------------------

## 32. Testing Strategy

Use:

``` text
Vitest
React Testing Library
Playwright
```

Test user-visible behavior rather than implementation details.

------------------------------------------------------------------------

## 33. Component Tests

Test:

``` text
ChatInput
MessageBubble
SourceList
Sidebar
ArtifactViewer
LoadingState
ErrorState
```

Examples:

``` text
Empty input cannot submit.
Enter submits.
Shift+Enter inserts newline.
Assistant Markdown renders.
Sources are visible.
Active session is highlighted.
Artifact loading state appears.
Artifact error state appears.
```

------------------------------------------------------------------------

## 34. Integration Tests

Test:

``` text
Create session
↓
Display session
↓
Send message
↓
Display assistant response
↓
Display sources
↓
Switch session
↓
Load correct messages
```

Also test:

``` text
Backend error
↓
Useful frontend error
```

and:

``` text
No grounding
↓
Unsupported-answer state
```

------------------------------------------------------------------------

## 35. Artifact Tests

Test:

``` text
Markdown artifact
→ renders correctly
```

``` text
HTML artifact
→ renders in isolated viewer
```

``` text
Unsafe HTML
→ remains inside intended security boundary
```

``` text
Artifact generation failure
→ useful error state
```

Assertions must reflect the final security implementation.

------------------------------------------------------------------------

## 36. End-to-End Test

Create a Playwright smoke test:

``` text
Open application
       ↓
Create new chat
       ↓
Ask a Lenny question
       ↓
Wait for assistant response
       ↓
Verify answer visible
       ↓
Verify sources visible
       ↓
Ask follow-up
       ↓
Verify response
       ↓
Request artifact
       ↓
Verify Artifact Viewer
       ↓
Verify artifact rendered
```

This is the most important frontend automated flow.

------------------------------------------------------------------------

## 37. Manual Frontend Smoke Test

Before final submission:

``` text
1. Open frontend.
2. Verify initial empty state.
3. Create a new chat.
4. Ask a grounded question.
5. Verify response.
6. Verify sources.
7. Verify provider/model indicator.
8. Ask a follow-up.
9. Switch to a new chat.
10. Verify old messages are not shown.
11. Return to old chat.
12. Verify messages persisted.
13. Generate Ship30 content.
14. Verify formatting.
15. Generate Markdown artifact.
16. Verify Artifact Viewer.
17. Generate HTML artifact.
18. Verify safe rendering.
19. Stop backend.
20. Verify useful error.
21. Restart backend.
22. Verify recovery.
23. Test mobile layout.
24. Test keyboard navigation.
```

------------------------------------------------------------------------

## 38. Development Commands

Create the app:

``` bash
npm create vite@latest frontend -- --template react-ts
```

Install:

``` bash
npm install
```

Development:

``` bash
npm run dev
```

Build:

``` bash
npm run build
```

Production preview:

``` bash
npm run preview
```

Tests:

``` bash
npm run test
```

E2E:

``` bash
npx playwright test
```

Finalize the exact scripts in `package.json`.

------------------------------------------------------------------------

## 39. Frontend Development Order

### Phase 1 --- Application shell

``` text
Vite
React
TypeScript
Tailwind
Basic layout
```

Verify:

``` bash
npm run dev
```

### Phase 2 --- Sidebar

Build:

``` text
New Chat
Session list
Active session
```

Connect to backend.

### Phase 3 --- Chat

Build:

``` text
Message list
Message bubble
Chat input
Loading state
```

Connect to:

``` text
POST /sessions/{id}/messages
```

### Phase 4 --- Sources

Build `SourceList` and display backend source metadata.

### Phase 5 --- Session switching

Verify:

``` text
Session A
↓
Session B
↓
Session A
```

with correct persisted messages.

### Phase 6 --- Provider indicator

Display provider/model returned by backend.

### Phase 7 --- Artifact Viewer

Build:

``` text
Artifact panel
Markdown renderer
HTML preview
Loading state
Error state
```

### Phase 8 --- Security

Implement and test:

``` text
HTML validation
Sanitization
Isolation
```

### Phase 9 --- Responsive UI

Test desktop, tablet, and mobile.

### Phase 10 --- Accessibility

Test keyboard navigation, focus, semantics, and status messages.

### Phase 11 --- Automated tests

Add component, integration, and Playwright tests.

### Phase 12 --- Final polish

Review:

``` text
Spacing
Typography
Loading states
Error states
Empty states
Responsive behavior
Artifact layout
```

------------------------------------------------------------------------

## 40. Definition of Done

### Application

-   [ ] React app starts.
-   [ ] Production build succeeds.
-   [ ] Backend connection works.
-   [ ] Environment configuration works.

### Chat

-   [ ] New chat works.
-   [ ] Existing sessions load.
-   [ ] Session switching works.
-   [ ] Messages display correctly.
-   [ ] Follow-up questions work.
-   [ ] Loading state works.
-   [ ] Error state works.

### Grounding

-   [ ] Sources display.
-   [ ] Source links work where available.
-   [ ] Unsupported answers are clearly communicated.
-   [ ] Frontend never invents sources.

### LLM

-   [ ] Ollama demo works.
-   [ ] Provider/model is visible.
-   [ ] Cloud provider flow works through backend.

### Artifacts

-   [ ] Markdown renders.
-   [ ] HTML/CSS renders.
-   [ ] Artifact appears beside chat.
-   [ ] Artifact loading state works.
-   [ ] Artifact error state works.
-   [ ] HTML uses the approved security/isolation strategy.

### UX

-   [ ] Desktop works.
-   [ ] Tablet works.
-   [ ] Mobile works.
-   [ ] Keyboard navigation works.
-   [ ] Focus states work.
-   [ ] Accessible labels/states exist.
-   [ ] Empty states are useful.
-   [ ] Error states are understandable.

### Tests

-   [ ] Component tests pass.
-   [ ] Integration tests pass.
-   [ ] Playwright smoke test passes.

------------------------------------------------------------------------

## 41. Final Evaluator Flow

A fresh evaluator should be able to:

``` text
Open application
      ↓
Create new chat
      ↓
Ask:
"What can Lenny's guests teach us about retention?"
      ↓
See grounded response
      ↓
See transcript sources
      ↓
Ask follow-up:
"What about onboarding?"
      ↓
See contextual response
      ↓
Ask:
"Turn this into a Ship 30 for 30 essay."
      ↓
See formatted essay
      ↓
Ask:
"Create an HTML artifact from this."
      ↓
Artifact Viewer opens
      ↓
Rendered artifact appears beside chat
      ↓
Model indicator shows Ollama/local model
```

This should be the core frontend demonstration in the final 2--3 minute
video.

------------------------------------------------------------------------

## 42. Final Frontend Verification

Before considering the frontend finished:

``` text
1. Clone repository into a clean directory.
2. Install Node dependencies.
3. Create frontend .env from .env.example.
4. Start backend.
5. Start frontend.
6. Verify API connection.
7. Create session.
8. Send grounded question.
9. Verify sources.
10. Verify follow-up.
11. Verify session isolation.
12. Verify persisted history.
13. Verify provider/model indicator.
14. Generate Ship30 output.
15. Generate Markdown artifact.
16. Generate HTML artifact.
17. Test unsafe HTML behavior.
18. Test backend unavailable state.
19. Test mobile layout.
20. Test keyboard navigation.
21. Run component/integration tests.
22. Run Playwright.
23. Run production build.
24. Verify no secrets are present.
```

The final goal is:

> **An evaluator can understand what the assistant is doing, trust where
> an answer came from, generate an artifact, and use the application
> comfortably without knowing the underlying implementation.**
