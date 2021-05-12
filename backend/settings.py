from os import getenv

from dotenv import load_dotenv

load_dotenv()

DEBUG = getenv("DEBUG", "").lower() in ("true", "1")

DB_CONNECTION_URI = getenv("DB_CONNECTION_URI", "sqlite:///dev.db")
FRONTEND_APP_URL = getenv("FRONTEND_APP_URL", "http://localhost:3000")
