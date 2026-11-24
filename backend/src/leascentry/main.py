import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from leascentry.config import Settings
from leascentry.db import check_database, make_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    app.state.engine = make_engine(settings.database_url)
    yield
    await app.state.engine.dispose()


app = FastAPI(title="Leascentry", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready(request: Request) -> JSONResponse:
    engine = request.app.state.engine
    try:
        ready = await check_database(engine)
    except Exception:
        logger.exception("readiness check failed")
        ready = False

    if ready:
        return JSONResponse(content={"status": "ready"})
    return JSONResponse(content={"status": "not_ready"}, status_code=503)
