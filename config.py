from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    data_dir: Path = ROOT_DIR / os.getenv("COURSE_DATA_DIR", ".")
    chroma_dir: Path = ROOT_DIR / os.getenv("CHROMA_DIR", "chroma_db")
    adzuna_app_id: str = os.getenv("ADZUNA_APP_ID", "")
    adzuna_app_key: str = os.getenv("ADZUNA_APP_KEY", "")
    country: str = os.getenv("JOB_COUNTRY", "in")
    results_per_page: int = int(os.getenv("JOB_RESULTS_PER_PAGE", "8"))

settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
