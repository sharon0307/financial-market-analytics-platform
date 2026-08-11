import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parents[3]

load_dotenv(BASE_DIR / ".env")


class Config:

    PROJECT_NAME = "Financial Market Analytics Platform"

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)
    ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
    ANGEL_CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
    ANGEL_PASSWORD = os.getenv("ANGEL_PASSWORD")
    ANGEL_TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")
    
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

config = Config()