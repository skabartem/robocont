"""Main FastAPI application for crypto content automation."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from common.config import settings
from common.database import init_db
from common.logger import setup_logger
from common.models import HealthResponse, APIRootResponse

# Setup logger
logger = setup_logger(__name__, "logs/main.log")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting Crypto Content Automation API")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down API")


# Create main app
app = FastAPI(
    title="Crypto Content Automation API",
    description="AI-powered content generation for crypto projects",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and mount service routers (will be added when services are implemented)
# from research.api import router as research_router
# from text_gen.api import router as text_router
# from image_gen.api import router as image_router
# from video_gen.api import router as video_router
#
# app.include_router(research_router, prefix="/api/research", tags=["research"])
# app.include_router(text_router, prefix="/api/text", tags=["text"])
# app.include_router(image_router, prefix="/api/image", tags=["image"])
# app.include_router(video_router, prefix="/api/video", tags=["video"])


@app.get("/", response_model=APIRootResponse)
async def root():
    """API root endpoint."""
    return {
        "message": "Crypto Content Automation API",
        "version": "1.0.0",
        "services": {
            "research": "/api/research/docs",
            "text": "/api/text/docs",
            "image": "/api/image/docs",
            "video": "/api/video/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True  # Disable in production
    )
