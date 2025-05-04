from pydantic_settings import BaseSettings # type: ignore
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str="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"
    CHROMA_PERSIST_DIRECTORY: str = "db"
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    CHUNK_SIZE: int = 1000
    
    class Config:
        env_file = ".env"

settings = Settings() 