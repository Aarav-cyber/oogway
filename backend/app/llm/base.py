from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a text response given message history and optional system prompt."""
        pass

    @abstractmethod
    async def check_availability(self) -> bool:
        """Check if the provider service is reachable and configured."""
        pass
