import os
from pathlib import Path

from dotenv import load_dotenv

# NLtoSQL/ (this file lives in NLtoSQL/src/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"


def get_database_url() -> str:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing. Add it to NLtoSQL/.env.")
    return DATABASE_URL


def get_jwt_secret() -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is missing. Add it to NLtoSQL/.env.")
    return JWT_SECRET
