import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from leascentry.config import Settings


async def main() -> None:
    settings = Settings()
    engine = create_async_engine(settings.database_url)

    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version()"))
        print(result.scalar())
        result = await conn.execute(
            text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')")
        )
        has_vector = result.scalar()
        if has_vector:
            print("pgvector: enabled")
        else:
            print("pgvector: missing")

        
    await engine.dispose()


asyncio.run(main())
