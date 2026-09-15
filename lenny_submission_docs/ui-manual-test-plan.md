# UI Manual Test Plan

## 1. Session and Chat
1. Start the application.
2. Create a new chat.
3. Ask a grounded product/growth question.
4. Verify transcript-backed answer and source list.
5. Ask a follow-up.
6. Create another session and verify context isolation.

## 2. Grounding Failure
1. Ask a question outside the transcript knowledge base.
2. Verify the assistant explicitly says the available material is insufficient.
3. Verify unrelated retrieved sources are not presented as supporting evidence.

## 3. Runtime LLM Switching
1. Start with Ollama.
2. Verify the active provider/model in the header.
3. Switch to Groq.
4. Verify the header changes.
5. Send a message.
6. Switch to Gemini and repeat.
7. Make Ollama unavailable.
8. Attempt to switch to Ollama.
9. Verify the switch fails and the current provider remains active.
10. Restore Ollama.

## 4. Ship 30 for 30
1. Request a Ship 30 for 30 essay.
2. Verify approximately 1,250 words.
3. Verify hook, headings, skimmability, takeaway, and source grounding.

## 5. Artifact Viewer
1. Generate Markdown.
2. Verify the viewer opens beside chat.
3. Generate HTML/CSS.
4. Verify the HTML is rendered in the viewer.
5. Verify unsafe HTML is sanitized/isolated.
6. Close and reopen the viewer.

## 6. Error Handling
- Unavailable LLM → clear provider error.
- Model timeout → clear failure state.
- Empty retrieval → insufficient-support response.
- Backend unavailable → clear UI/service state.
- Database failure → structured service error.

## 7. Responsive and Accessibility
Check desktop, tablet, and mobile widths. Test keyboard navigation, focus visibility, accessible labels, and text-based error communication.
