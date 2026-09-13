import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.llm.base import BaseLLMProvider
from app.llm.factory import LLMFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class MockLLMProvider(BaseLLMProvider):
    async def check_availability(self) -> bool:
        return True

    async def generate(
        self,
        messages,
        system_prompt=None,
        temperature=0.7,
        max_tokens=2048,
    ) -> str:
        last_msg = messages[-1]["content"] if messages else ""
        if "ship 30" in last_msg.lower() or "essay" in last_msg.lower():
            return "# Hook Title\n\nThis is a 1,250 word atomic essay on product growth.\n\n## Key Takeaways\n- Focus on retention.\n- Measure time to value."
        elif "html" in last_msg.lower():
            return "<div class='artifact'><h1>Generated HTML Title</h1><p>Grounded content</p></div>"
        elif "markdown" in last_msg.lower():
            return "# Markdown Document\n\n* Grounded points"
        else:
            return "Based on Brian Chesky's podcast transcript, retention is the foundation of product growth."


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_llm_factory(monkeypatch):
    mock_provider = MockLLMProvider()
    monkeypatch.setattr(LLMFactory, "get_provider", lambda provider_name=None: mock_provider)
