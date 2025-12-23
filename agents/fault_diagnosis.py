"""
Fault Diagnosis Agent for Wind Power Systems
Diagnoses issues based on symptoms and provides recommendations
"""
from typing import Dict, Any, Optional, List
from agents.base_agent import BaseAgent
from core.config import AgentConfig


class FaultDiagnosisAgent(BaseAgent):
    """
    Agent for diagnosing faults in wind power systems
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize fault diagnosis agent
        
        Args:
            config: Agent configuration
        """
        super().__init__(config)
    
    def get_system_prompt(self) -> str:
        """Get system prompt for fault diagnosis"""
        return """你是一位风力发电系统故障诊断专家。你的任务是：
1. 分析用户描述的故障症状
2. 基于提供的技术文档和知识库，诊断可能的故障原因
3. 提供详细的排查步骤和解决方案
4. 给出安全注意事项

请用专业、清晰的语言回答，确保技术准确性。

重要提示：
- 所有诊断仅供参考，实际操作前必须遵循制造商规程
- 涉及高压、高空作业时，必须由专业人员操作
- 本系统提供的建议不承担任何法律责任"""
    
    def process(
        self,
        query: str,
        include_context: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process fault diagnosis query
        
        Args:
            query: Fault description
            include_context: Whether to include knowledge base context
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with diagnosis results
        """
        # Retrieve relevant context
        context = ""
        retrieved_docs = []
        
        if include_context:
            context = self.retrieve_context(query, k=self.config.top_k)
            retrieved_docs = self.knowledge_base.search(query, k=self.config.top_k)
        
        # Construct prompt
        if context and context != "No relevant information found in knowledge base.":
            prompt = f"""基于以下技术文档和知识库信息，请诊断故障：

【相关技术文档】
{context}

【故障描述】
{query}

请提供：
1. 可能的故障原因（按可能性排序）
2. 详细的排查步骤
3. 解决方案和维修建议
4. 安全注意事项
"""
        else:
            prompt = f"""【故障描述】
{query}

请基于通用风电系统知识提供：
1. 可能的故障原因（按可能性排序）
2. 详细的排查步骤
3. 解决方案和维修建议
4. 安全注意事项

注：由于知识库未找到直接相关文档，本诊断基于通用经验。
"""
        
        # Generate diagnosis
        diagnosis = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt()
        )
        
        return {
            "query": query,
            "diagnosis": diagnosis,
            "context_used": context if include_context else None,
            "source_documents": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in retrieved_docs
            ]
        }
    
    def diagnose_with_history(
        self,
        query: str,
        history: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Diagnose fault with conversation history
        
        Args:
            query: Current fault description
            history: Previous conversation history
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with diagnosis results
        """
        # Retrieve context
        context = self.retrieve_context(query, k=self.config.top_k)
        
        # Construct messages with history
        messages = []
        for msg in history:
            messages.append(msg)
        
        # Add current query with context
        current_prompt = f"""【相关技术文档】
{context}

【故障描述】
{query}

请继续诊断并提供建议。
"""
        messages.append({"role": "user", "content": current_prompt})
        
        # Generate diagnosis
        diagnosis = self.llm_client.chat(
            messages=messages,
            system_prompt=self.get_system_prompt()
        )
        
        return {
            "query": query,
            "diagnosis": diagnosis,
            "context_used": context
        }


def create_fault_diagnosis_agent(config: Optional[AgentConfig] = None) -> FaultDiagnosisAgent:
    """
    Factory function to create fault diagnosis agent
    
    Args:
        config: Optional agent configuration
        
    Returns:
        FaultDiagnosisAgent instance
    """
    return FaultDiagnosisAgent(config)
