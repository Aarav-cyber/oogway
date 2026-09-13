import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import MessageModel
from app.services.session_service import SessionService
from app.services.artifact_service import ArtifactService
from app.agent.agent import LennyAgent
from app.llm.factory import LLMFactory
from app.core.config import settings
from app.schemas.chat import ChatResponse, MessageResponse
import logging

logger = logging.getLogger("lenny_backend")


class ChatService:
    @staticmethod
    async def process_chat_message(
        db: AsyncSession,
        session_id: str,
        user_content: str,
        provider_name: Optional[str] = None,
    ) -> ChatResponse:
        # Enforce session existence
        session = await SessionService.get_session(db, session_id)

        # Retrieve prior session messages for conversation context
        existing_messages = await SessionService.get_session_messages(db, session_id)
        conversation_history = [
            {"role": msg.role, "content": msg.content} for msg in existing_messages
        ]

        # Save user message
        user_msg = MessageModel(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="user",
            content=user_content,
        )
        db.add(user_msg)
        await db.flush()

        # Instantiate selected LLM provider via factory
        selected_provider_name = provider_name or settings.LLM_PROVIDER
        llm = LLMFactory.get_provider(selected_provider_name)

        # Run Agent pipeline
        agent = LennyAgent(llm_provider=llm)
        agent_result = await agent.run(
            db=db,
            query=user_content,
            conversation_history=conversation_history,
        )

        # If artifact was generated, persist it
        artifact_id = None
        if agent_result.artifact_content and agent_result.artifact_type:
            art = await ArtifactService.create_artifact(
                db=db,
                session_id=session_id,
                title=f"Generated {agent_result.artifact_type.upper()} Artifact",
                type=agent_result.artifact_type,
                content=agent_result.artifact_content,
                message_id=user_msg.id,
            )
            artifact_id = art.id

        # Save assistant message
        assistant_msg = MessageModel(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="assistant",
            content=agent_result.content,
            message_metadata={
                "provider": selected_provider_name,
                "skill": agent_result.skill,
                "sources_count": len(agent_result.sources),
                "artifact_id": artifact_id,
            },
        )
        db.add(assistant_msg)

        # Update session title if first message
        if not session.title or session.title == "New Chat":
            session.title = user_content[:40] + ("..." if len(user_content) > 40 else "")

        await db.flush()

        model_name = getattr(llm, "model", selected_provider_name)

        return ChatResponse(
            message=MessageResponse.model_validate(assistant_msg),
            sources=agent_result.sources,
            provider=selected_provider_name,
            model=model_name,
            skill=agent_result.skill,
            artifact_id=artifact_id,
        )
