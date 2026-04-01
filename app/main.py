from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.routes import router
from app.core.config import settings
from app.core.logger import logger
from app.services.analyzer import get_analyzer

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready API for Sentiment and Emotion Analysis using HuggingFace Transformers.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Exception handler for Custom Rate Limiting (SlowAPI)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware for allowing web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up API server...")
    # Pre-load HuggingFace models in singleton instance to avoid cold-start delay
    get_analyzer()

@app.get("/health", tags=["Health"])
def health_check():
    """
    Simple health check endpoint for load balancers.
    """
    return {"status": "ok", "version": settings.APP_VERSION}

# Register the main router module
app.include_router(router, prefix=settings.API_PREFIX, tags=["Analysis"])

if __name__ == "__main__":
    import uvicorn
    # Local development server execution
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
