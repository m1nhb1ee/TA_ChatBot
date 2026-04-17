"""
Configuration constants for the AI Teaching Assistant Backend.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
SLIDES_DIR = KNOWLEDGE_BASE_DIR / "slides"
CODE_SAMPLES_DIR = KNOWLEDGE_BASE_DIR / "code_samples"
FAISS_INDEX_DIR = BASE_DIR / "faiss_index"
FAQ_PATH = KNOWLEDGE_BASE_DIR / "faq.md"
COURSE_INFO_PATH = KNOWLEDGE_BASE_DIR / "course_info.json"
APP_DATA_DIR = BASE_DIR / "app_data"

# Ensure app_data directory exists
APP_DATA_DIR.mkdir(exist_ok=True)

# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Warn if API key is not set (but don't crash - let the app handle it)
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY is not set. The chatbot will not function properly.")
    print("   Please set the environment variable: OPENAI_API_KEY=sk-...")

LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.3
EMBEDDING_MODEL = "text-embedding-3-large"

# --- RAG ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 5  # Number of documents to retrieve

# --- Course ---
COURSE_NAME = "Lập trình C/C++ cơ bản"
COURSE_CODE = "CS101"

# --- API ---
API_TITLE = "TA ChatBot API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Backend API for AI Teaching Assistant"
