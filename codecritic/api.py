"""
FastAPI backend for CodeCritic
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os

from .core import CodeCritic
from .models import ReviewRequest, ReviewResponse, Config

app = FastAPI(
    title="CodeCritic API",
    description="AI-powered code review and analysis tool",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CodeCritic
config = Config(
    api_key=os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"),
    model=os.getenv("CODECRITIC_MODEL", "anthropic/claude-3-sonnet-20240229")
)
critic = CodeCritic(config)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CodeCritic API",
        "version": "1.0.0",
        "author": "Rishu Singh",
        "docs": "/docs"
    }


@app.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    """Review code and provide feedback"""
    try:
        start_time = time.time()
        response = critic.review(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    ) 