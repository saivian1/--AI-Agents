"""
Configuration management for Wind Power AI Agents
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMConfig(BaseModel):
    """LLM configuration"""
    provider: str = Field(default="openai", description="LLM provider")
    model: str = Field(default="gpt-3.5-turbo", description="Model name")
    api_key: Optional[str] = Field(default=None, description="API key")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=2000, description="Maximum tokens")
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY", "")


class VectorDBConfig(BaseModel):
    """Vector database configuration"""
    db_type: str = Field(default="chromadb", description="Vector DB type")
    persist_directory: str = Field(default="./chroma_db", description="Persistence directory")
    collection_name: str = Field(default="wind_power_docs", description="Collection name")


class AgentConfig(BaseModel):
    """Agent configuration"""
    llm: LLMConfig = Field(default_factory=LLMConfig)
    vector_db: VectorDBConfig = Field(default_factory=VectorDBConfig)
    chunk_size: int = Field(default=1000, description="Document chunk size")
    chunk_overlap: int = Field(default=200, description="Chunk overlap")
    top_k: int = Field(default=3, description="Top K results for retrieval")


# Global config instance
_config: Optional[AgentConfig] = None


def get_config() -> AgentConfig:
    """Get global configuration"""
    global _config
    if _config is None:
        _config = AgentConfig()
    return _config


def set_config(config: AgentConfig):
    """Set global configuration"""
    global _config
    _config = config
