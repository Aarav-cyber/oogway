import asyncio
import os
import glob
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import AsyncSessionLocal
from app.rag.ingest import ingest_document


async def main():
    transcript_dir = os.environ.get("TRANSCRIPTS_DIR", "agent-transcripts")
    if not os.path.exists(transcript_dir):
        print(f"Directory '{transcript_dir}' not found. Seeding default sample data instead.")
        from scripts.seed_data import seed
        await seed()
        return

    files = glob.glob(os.path.join(transcript_dir, "**/*.txt"), recursive=True) + \
            glob.glob(os.path.join(transcript_dir, "**/*.md"), recursive=True)

    if not files:
        print("No transcript files found. Seeding sample data...")
        from scripts.seed_data import seed
        await seed()
        return

    async with AsyncSessionLocal() as session:
        for file_path in files:
            filename = os.path.basename(file_path)
            source_id = os.path.splitext(filename)[0]
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            title = source_id.replace("-", " ").replace("_", " ").title()
            await ingest_document(
                db=session,
                source_id=source_id,
                title=title,
                content=content
            )
            print(f"Processed: {filename}")

if __name__ == "__main__":
    asyncio.run(main())
