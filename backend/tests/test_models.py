import asyncio
import secrets

from leascentry.config import Settings
from leascentry.db import make_engine
from leascentry.models import Document
from sqlalchemy.ext.asyncio import AsyncSession
settings = Settings()


async def _test_database_connection() -> None:
    engine = make_engine(settings.database_url)
    try:
        async with AsyncSession(engine) as session:
            doc = Document(
                filename="test-lease.pdf",
                content_type="application/pdf",
                sha256=secrets.token_hex(32),  # random each run → no unique clash
                storage_path="/tmp/test-lease.pdf",
            )
            session.add(doc)
            await session.commit()
            await session.refresh(doc)

            assert doc.id is not None
            assert doc.created_at is not None
            assert doc.status == "pending"

            await session.delete(doc)
            await session.commit()

    finally:
        await engine.dispose()


def test_document_insert_fills_defaults() -> None:
    # pytest only runs normal `def` tests, so we run the async helper ourselves
    asyncio.run(_test_database_connection())
