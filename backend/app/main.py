from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
import app.models.user  # noqa: F401 - ensure models are registered
import app.models.listing  # noqa: F401
import app.models.favorite  # noqa: F401
import app.models.chat  # noqa: F401
import app.models.inquiry  # noqa: F401
import app.models.review  # noqa: F401
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="AutoCH API",
    description="Swiss automotive classifieds platform API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

if not settings.USE_SUPABASE:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return Response(status_code=200)
