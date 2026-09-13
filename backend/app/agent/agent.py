from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.llm.base import BaseLLMProvider
from app.agent.router import AgentRouter, AgentSkillType
from app.agent.skills.grounded_qa import GroundedQASkill
from app.agent.skills.ship30 import Ship30Skill
from app.agent.skills.artifact import ArtifactSkill
from app.rag.retriever import Retriever
from app.rag.sources import SourceMetadata, RetrievedChunk
import logging

logger = logging.getLogger("lenny_backend")


class AgentExecutionResult:
    def __init__(
        self,
        content: str,
        skill: str,
        sources: List[SourceMetadata],
        artifact_content: Optional[str] = None,
        artifact_type: Optional[str] = None,
    ):
        self.content = content
        self.skill = skill
        self.sources = sources
        self.artifact_content = artifact_content
        self.artifact_type = artifact_type


class LennyAgent:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider

    async def run(
        self,
        db: AsyncSession,
        query: str,
        conversation_history: List[Dict[str, str]],
        forced_skill: Optional[str] = None,
    ) -> AgentExecutionResult:
        """Runs the agent pipeline: routes intent, retrieves transcript context, and executes the target skill."""
        if forced_skill:
            try:
                skill_type = AgentSkillType(forced_skill)
            except ValueError:
                skill_type = AgentRouter.route_request(query)
        else:
            skill_type = AgentRouter.route_request(query)

        logger.info(f"Routed request to skill: {skill_type.value}")

        # Retrieve transcript context for QA or Ship30
        chunks: List[RetrievedChunk] = []
        if skill_type in [AgentSkillType.GROUNDED_QA, AgentSkillType.SHIP30]:
            chunks = await Retriever.retrieve_chunks(db, query=query, top_k=5)

        if skill_type == AgentSkillType.SHIP30:
            essay, sources = await Ship30Skill.execute(
                llm=self.llm,
                query=query,
                conversation_history=conversation_history,
                chunks=chunks,
            )
            return AgentExecutionResult(
                content=essay,
                skill=skill_type.value,
                sources=sources,
            )

        elif skill_type == AgentSkillType.ARTIFACT:
            art_type = "html" if "html" in query.lower() else "markdown"
            artifact_code, art_type = await ArtifactSkill.execute(
                llm=self.llm,
                query=query,
                conversation_history=conversation_history,
                artifact_type=art_type,
            )
            summary = f"Generated {art_type.upper()} artifact."
            return AgentExecutionResult(
                content=summary,
                skill=skill_type.value,
                sources=[],
                artifact_content=artifact_code,
                artifact_type=art_type,
            )

        else:  # GROUNDED_QA
            answer, sources = await GroundedQASkill.execute(
                llm=self.llm,
                query=query,
                conversation_history=conversation_history,
                chunks=chunks,
            )
            return AgentExecutionResult(
                content=answer,
                skill=skill_type.value,
                sources=sources,
            )
