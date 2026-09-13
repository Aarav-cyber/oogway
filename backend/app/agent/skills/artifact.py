import nh3
from typing import List, Dict, Any, Tuple, Optional
from app.llm.base import BaseLLMProvider


ARTIFACT_SYSTEM_PROMPT = """You are an Artifact Generation Expert.
Your task is to generate clean, self-contained digital artifacts based on the user request and conversation history.

Artifact Types supported:
1. 'markdown' - Structured markdown document.
2. 'html' - Self-contained, beautiful HTML document with embedded CSS styling (<style> tag).

When generating HTML:
- Include modern responsive CSS styling.
- Do NOT include external scripts or dangerous tags (<script>, <iframe>, <object>, <embed>).
- Return ONLY valid HTML or Markdown content without conversational filler.
"""


class ArtifactSkill:
    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """Sanitizes generated HTML using nh3 to strip untrusted scripts and tags."""
        allowed_tags = {
            "a", "b", "blockquote", "br", "caption", "code", "div", "em", "h1", "h2", "h3",
            "h4", "h5", "h6", "hr", "i", "img", "li", "ol", "p", "pre", "span", "strong",
            "style", "table", "tbody", "td", "th", "thead", "tr", "ul"
        }
        allowed_attributes = {
            "a": {"href", "title", "target"},
            "img": {"src", "alt", "title", "width", "height"},
            "*": {"class", "style", "id"},
        }
        return nh3.clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            clean_content_tags=set(),
        )

    @classmethod
    async def execute(
        cls,
        llm: BaseLLMProvider,
        query: str,
        conversation_history: List[Dict[str, str]],
        artifact_type: str = "markdown",
    ) -> Tuple[str, str]:
        """Generates content and returns (content, artifact_type)."""
        prompt = f"Generate a {artifact_type.upper()} artifact for: {query}"
        messages = list(conversation_history)
        messages.append({"role": "user", "content": prompt})

        raw_output = await llm.generate(
            messages=messages,
            system_prompt=ARTIFACT_SYSTEM_PROMPT,
            temperature=0.4,
            max_tokens=3000,
        )

        content = raw_output.strip()
        # Clean markdown code block wraps if present
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        if artifact_type.lower() == "html":
            content = cls.sanitize_html(content)

        return content, artifact_type.lower()
