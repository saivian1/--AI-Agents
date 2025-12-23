"""
Basic tests for core modules
"""
import pytest
from core.config import AgentConfig, LLMConfig, VectorDBConfig, get_config, set_config


class TestConfig:
    """Test configuration management"""
    
    def test_llm_config_defaults(self):
        """Test LLM config with default values"""
        config = LLMConfig()
        assert config.provider == "openai"
        assert config.model == "gpt-3.5-turbo"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
    
    def test_llm_config_custom(self):
        """Test LLM config with custom values"""
        config = LLMConfig(
            provider="openai",
            model="gpt-4",
            temperature=0.5,
            max_tokens=1000
        )
        assert config.provider == "openai"
        assert config.model == "gpt-4"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000
    
    def test_vector_db_config_defaults(self):
        """Test vector DB config with default values"""
        config = VectorDBConfig()
        assert config.db_type == "chromadb"
        assert config.persist_directory == "./chroma_db"
        assert config.collection_name == "wind_power_docs"
    
    def test_agent_config(self):
        """Test agent config"""
        config = AgentConfig()
        assert config.llm is not None
        assert config.vector_db is not None
        assert config.chunk_size == 1000
        assert config.chunk_overlap == 200
        assert config.top_k == 3
    
    def test_global_config(self):
        """Test global config get/set"""
        # Get default config
        config1 = get_config()
        assert isinstance(config1, AgentConfig)
        
        # Set custom config
        custom_config = AgentConfig(
            llm=LLMConfig(model="gpt-4"),
            chunk_size=1500
        )
        set_config(custom_config)
        
        # Get config again
        config2 = get_config()
        assert config2.llm.model == "gpt-4"
        assert config2.chunk_size == 1500


# Note: Tests that require API keys or network access should be marked as integration tests
# and skipped in CI/CD pipelines without proper credentials
