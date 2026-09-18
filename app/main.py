from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.api.routes import health, chat

# 1. Load environment variables first
load_dotenv()

# 2. Configure global logging format and output stream
configure_logging()

# 3. Initialize FastAPI application
app = FastAPI(title="ZX Bank AI Knowledge Assistant")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include application routers
app.include_router(health.router)
app.include_router(chat.router)