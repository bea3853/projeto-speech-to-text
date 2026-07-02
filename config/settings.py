import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Captura a URL bruta do banco de dados
raw_db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

# Força o uso do driver psycopg (Psycopg 3) caso a URL venha crua do Neon/Render
if raw_db_url.startswith("postgres://"):
    DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif raw_db_url.startswith("postgresql://") and not raw_db_url.startswith("postgresql+psycopg://"):
    DATABASE_URL = raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = raw_db_url

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/tmp/images")
LOG_FILE = os.getenv("LOG_FILE", "/tmp/logs/app.log")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
