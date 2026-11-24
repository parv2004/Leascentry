from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def make_engine(database_url: str) -> AsyncEngine:
    """
    Create an asynchronous SQLAlchemy engine.

    Args:
        database_url (str): The database URL.

    Returns:
        AsyncEngine: An instance of the asynchronous SQLAlchemy engine.
    """
    return create_async_engine(database_url, echo=True)


async def check_database(engine: AsyncEngine) -> bool:
    """
    Check the database for version and pgvector extension.

    Args:
        engine (AsyncEngine): The asynchronous SQLAlchemy engine.
    """
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')")
        )
        return bool(result.scalar())
