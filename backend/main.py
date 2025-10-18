from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trading Card API", 
    version="1.0.0",
    description="API for managing trading card collections"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from api.routes.cards import router as cards_router
app.include_router(cards_router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Trading Card API is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}
