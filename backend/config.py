import os
from pathlib import Path

# Database configuration
DATABASE_URL = "sqlite:///./cards.db"

# API configuration
API_HOST = "127.0.0.1"
API_PORT = 8000

# Logging configuration
LOG_LEVEL = "INFO"

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative React dev server
]
