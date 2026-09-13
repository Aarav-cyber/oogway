from enum import Enum


class AgentSkillType(str, Enum):
    GROUNDED_QA = "grounded_qa"
    SHIP30 = "ship30"
    ARTIFACT = "artifact"


class AgentRouter:
    @staticmethod
    def route_request(query: str) -> AgentSkillType:
        """Determines the appropriate skill based on user query intent."""
        query_lower = query.lower()

        # Ship 30 triggers
        ship30_keywords = ["ship 30", "ship30", "atomic essay", "essay", "1250 words", "writing skill"]
        if any(kw in query_lower for kw in ship30_keywords):
            return AgentSkillType.SHIP30

        # Artifact triggers
        artifact_keywords = [
            "create html", "generate html", "create artifact", "generate artifact",
            "make a webpage", "html page", "html artifact", "markdown artifact", "generate markdown"
        ]
        if any(kw in query_lower for kw in artifact_keywords):
            return AgentSkillType.ARTIFACT

        # Default to Grounded QA
        return AgentSkillType.GROUNDED_QA
