"""
LLM Client for Wind Power AI Agents
Supports multiple LLM providers with a unified interface
"""
from typing import Optional, List, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from core.config import LLMConfig, get_config


class LLMClient:
    """
    Unified LLM client supporting multiple providers
    """
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM client
        
        Args:
            config: LLM configuration, uses global config if None
        """
        self.config = config or get_config().llm
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize LLM based on configuration"""
        if self.config.provider == "openai":
            return ChatOpenAI(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                openai_api_key=self.config.api_key
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.provider}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Send chat messages and get response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt
            
        Returns:
            Response text
        """
        # Convert messages to LangChain format
        langchain_messages = []
        
        if system_prompt:
            langchain_messages.append(SystemMessage(content=system_prompt))
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))
        
        # Get response
        response = self.llm(langchain_messages)
        return response.content
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate response from a single prompt
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, system_prompt)


def create_llm_client(config: Optional[LLMConfig] = None) -> LLMClient:
    """
    Factory function to create LLM client
    
    Args:
        config: Optional LLM configuration
        
    Returns:
        LLMClient instance
    """
    return LLMClient(config)
