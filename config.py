
import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

PERSIST_DIRECTORY = "db"
COLLECTION_NAME = "documento_base"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 0

TOP_K = 4

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "No se encontro GROQ_API_KEY. Copia .env.example a .env y completa tu clave "
    )
if not GROQ_API_KEY:
    raise EnvironmentError(
        "No se encontro GROQ_API_KEY. Copia .env.example a .env y completa tu clave "
    )
