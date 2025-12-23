"""
Regulation Q&A Agent for Wind Power Industry
Answers questions based on industry regulations and procedures
"""
from typing import Dict, Any, Optional, List
from agents.base_agent import BaseAgent
from core.config import AgentConfig


class RegulationQAAgent(BaseAgent):
    """
    Agent for answering questions about wind power regulations and procedures
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize regulation Q&A agent
        
        Args:
            config: Agent configuration
        """
        super().__init__(config)
    
    def get_system_prompt(self) -> str:
        """Get system prompt for regulation Q&A"""
        return """你是一位风力发电行业规程与标准专家。你的任务是：
1. 回答关于风电行业规程、标准、操作流程的问题
2. 基于提供的规程文档给出准确、详细的答案
3. 引用相关条款和章节
4. 提供实际操作建议

回答要求：
- 准确引用规程内容，注明出处
- 清晰解释技术术语
- 提供实用的操作指导
- 强调安全要求和注意事项

免责声明：
- 本系统提供的信息仅供参考
- 实际操作请以最新版本的官方规程为准
- 如有疑问，请咨询专业机构或监管部门"""
    
    def process(
        self,
        query: str,
        include_context: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process regulation Q&A query
        
        Args:
            query: Question about regulations
            include_context: Whether to include knowledge base context
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with answer and sources
        """
        # Retrieve relevant context
        context = ""
        retrieved_docs = []
        
        if include_context:
            context = self.retrieve_context(query, k=self.config.top_k)
            retrieved_docs = self.knowledge_base.search(query, k=self.config.top_k)
        
        # Construct prompt
        if context and context != "No relevant information found in knowledge base.":
            prompt = f"""基于以下规程文档，请回答问题：

【相关规程文档】
{context}

【用户问题】
{query}

请提供：
1. 直接回答问题
2. 引用相关规程条款（如有）
3. 详细说明和解释
4. 实际应用建议
5. 注意事项
"""
        else:
            prompt = f"""【用户问题】
{query}

请基于风电行业通用知识回答，并说明：
- 这是基于通用知识的回答
- 建议查阅最新的官方规程文档
- 如需准确信息，请咨询专业机构
"""
        
        # Generate answer
        answer = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt()
        )
        
        return {
            "query": query,
            "answer": answer,
            "context_used": context if include_context else None,
            "source_documents": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in retrieved_docs
            ]
        }
    
    def search_regulation(
        self,
        keyword: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search for specific regulation content
        
        Args:
            keyword: Search keyword
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with search results
        """
        # Search in knowledge base
        results = self.knowledge_base.search_with_score(keyword, k=5)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": float(score)
            })
        
        return {
            "keyword": keyword,
            "results": formatted_results,
            "total_found": len(formatted_results)
        }


def create_regulation_qa_agent(config: Optional[AgentConfig] = None) -> RegulationQAAgent:
    """
    Factory function to create regulation Q&A agent
    
    Args:
        config: Optional agent configuration
        
    Returns:
        RegulationQAAgent instance
    """
    return RegulationQAAgent(config)
