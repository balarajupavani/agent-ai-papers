import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from server.config import get_settings
from server.db.factory import make_database

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan for the API.
    """
    logger.info("Starting RAG API...")

    settings = get_settings()
    app.state.settings = settings

    database = make_database()
    app.state.database = database
    logger.info("Database connected")

    logger.info("API ready")
    yield

    # Cleanup
    database.teardown()
    logger.info("API shutdown complete")


def main():
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello from parse-ai-papers!')  # Press F9 to toggle the breakpoint.
    uvicorn.run(app, port=8000, host="0.0.0.0")

app = FastAPI(
    title="arXiv Paper Curator API",
    description="Personal arXiv CS.AI paper curator with RAG capabilities",
    version=os.getenv("APP_VERSION", "0.1.0"),
    lifespan=lifespan,
)

# Include routers