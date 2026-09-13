import asyncio
import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import AsyncSessionLocal, engine
from app.db.base import Base
from app.rag.ingest import ingest_document


SAMPLE_TRANSCRIPTS = [
    {
        "source_id": "ep-101-brian-chesky",
        "title": "Brian Chesky on Refusing to Delegate and Managing Product",
        "source_url": "https://www.lennysnewsletter.com/p/brian-chesky",
        "episode_date": "2023-11-02",
        "content": """
Brian Chesky shares his insights on product leadership, founder-led management, and growth strategies at Airbnb.

Key Takeaways on Product Retention and Growth:
1. Focus relentlessly on the core user experience before attempting horizontal expansion.
2. Retention is driven by product quality and solving a real pain point better than alternatives.
3. Founder-led management means being in the details of design, code, and customer support.
4. Marketing should tell stories and build brand resonance rather than relying solely on performance marketing and ad spend.

When asked about product retention, Brian emphasizes: "If users aren't staying, no amount of growth marketing will save you. Fix the leaky bucket first by making something people love."
        """
    },
    {
        "source_id": "ep-102-shreyas-doshi",
        "title": "Shreyas Doshi on Product Strategy and Product-Led Growth",
        "source_url": "https://www.lennysnewsletter.com/p/shreyas-doshi",
        "episode_date": "2023-12-15",
        "content": """
Shreyas Doshi discusses product management frameworks, pre-mortems, LNO framework, and retention tactics.

Product Retention Framework:
1. Identify high-intent usage patterns: What features do top 10% retained users use in their first 7 days?
2. Eliminate friction in activation: Reduce time-to-value (TTV) so users experience the core 'Aha!' moment immediately.
3. Establish behavioral loops: Use triggers, action, reward, and investment loops to build long-term retention habits.

According to Shreyas: "Growth without retention is just a vanity exercise. Retention measures whether you have created durable value."
        """
    },
    {
        "source_id": "ep-103-elena-verna",
        "title": "Elena Verna on B2B Growth and Product-Led Sales",
        "source_url": "https://www.lennysnewsletter.com/p/elena-verna",
        "episode_date": "2024-01-10",
        "content": """
Elena Verna breaks down PLG (Product-Led Growth), viral loops, pricing monetization, and retention metrics.

Retention Metrics & Tactics:
1. Day 1, Day 7, Day 30 user retention cohorts.
2. Feature retention vs product retention: Keep track of feature usage depth.
3. Product-led monetization: Convert active, retained free users into paid accounts when they reach natural usage limits.

Elena notes: "Product-led growth starts with product-led retention. You cannot grow top-of-funnel if bottom-of-funnel is bleeding."
        """
    }
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for t in SAMPLE_TRANSCRIPTS:
            await ingest_document(
                db=session,
                source_id=t["source_id"],
                title=t["title"],
                content=t["content"],
                source_url=t["source_url"],
                episode_date=t["episode_date"]
            )
    print("Seed data successfully ingested.")

if __name__ == "__main__":
    asyncio.run(seed())
