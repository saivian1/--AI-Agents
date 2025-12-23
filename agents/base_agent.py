"""
Base Agent class for Wind Power AI Agents
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from core.llm_client import LLMClient, create_llm_client
from core.knowledge_base import KnowledgeBase, create_knowledge_base
from core.config import AgentConfig, get_config


class BaseAgent(ABC):
    """
    Base class for all agents
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize base agent
        
        Args:
            config: Agent configuration, uses global config if None
        """
        self.config = config or get_config()
        self.llm_client = create_llm_client(self.config.llm)
        self.knowledge_base = create_knowledge_base(self.config.vector_db)
    
    @abstractmethod
    def process(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a query and return results
        
        Args:
            query: User query
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with results
        """
        pass
    
    def get_system_prompt(self) -> str:
        """
        Get system prompt for the agent
        Override in subclasses
        
        Returns:
            System prompt string
        """
        return "You are a helpful AI assistant for wind power industry."
    
    def retrieve_context(self, query: str, k: Optional[int] = None) -> str:
        """
        Retrieve relevant context from knowledge base
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            Formatted context string
        """
        documents = self.knowledge_base.search(query, k=k)
        
        if not documents:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Document {i}]\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
