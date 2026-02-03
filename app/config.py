from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    chroma_dir: str = os.getenv("CHROMA_DIR", ".chroma")
    model_dir: str = os.getenv("MODEL_DIR", ".models")
    collection_name: str = os.getenv("COLLECTION_NAME", "incidents_kb")

settings = Settings()
