import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-key-change-me-0123456789abcdef")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 8

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tracking.db")

PROVIDER_URL = os.getenv("PROVIDER_URL", "http://localhost:9000/api/devices/positions")
PROVIDER_KEY = os.getenv("PROVIDER_KEY", "demo-key-123")
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "5"))
