"""
Report Generator Agent for Wind Power Systems
Generates various types of reports based on templates and data
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from agents.base_agent import BaseAgent
from core.config import AgentConfig


class ReportGeneratorAgent(BaseAgent):
    """
    Agent for generating wind power system reports
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize report generator agent
        
        Args:
            config: Agent configuration
        """
        super().__init__(config)
    
    def get_system_prompt(self) -> str:
        """Get system prompt for report generation"""
        return """你是一位风力发电行业技术报告撰写专家。你的任务是：
1. 根据用户提供的数据和要求生成专业报告
2. 确保报告结构清晰、逻辑严密
3. 使用行业标准术语和格式
4. 提供数据分析和专业建议

报告要求：
- 结构完整：标题、摘要、正文、结论、建议
- 数据准确：如实呈现数据，不夸大不隐瞒
- 分析深入：提供专业分析和见解
- 格式规范：符合行业标准

免责声明：
- 报告内容基于提供的数据和信息生成
- 使用前请核实数据准确性
- 重要决策请经专业人员审核
- 本系统不承担因使用报告产生的任何责任"""
    
    def process(
        self,
        query: str,
        report_type: str = "general",
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate report
        
        Args:
            query: Report requirements or description
            report_type: Type of report (general, fault, maintenance, performance)
            data: Optional data for report
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with generated report
        """
        # Get report template based on type
        template = self._get_report_template(report_type)
        
        # Retrieve relevant context if needed
        context = ""
        if data is None:
            context = self.retrieve_context(query, k=self.config.top_k)
        
        # Construct prompt
        prompt = self._construct_prompt(query, report_type, template, data, context)
        
        # Generate report
        report = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt()
        )
        
        return {
            "query": query,
            "report_type": report_type,
            "report": report,
            "generated_at": datetime.now().isoformat(),
            "data_used": data
        }
    
    def _get_report_template(self, report_type: str) -> str:
        """Get report template based on type"""
        templates = {
            "general": """
# {标题}

## 摘要
简要概述报告内容

## 1. 背景与目的
说明报告背景和目的

## 2. 主要内容
详细内容和数据

## 3. 分析与讨论
数据分析和专业讨论

## 4. 结论
总结主要发现

## 5. 建议
提出改进建议
""",
            "fault": """
# 故障分析报告

## 报告信息
- 报告日期：
- 设备信息：
- 故障时间：

## 1. 故障描述
详细描述故障现象

## 2. 原因分析
分析故障根本原因

## 3. 影响评估
评估故障影响范围和程度

## 4. 处理措施
已采取的处理措施

## 5. 预防措施
防止类似故障的建议

## 6. 结论
""",
            "maintenance": """
# 维护保养报告

## 报告信息
- 报告日期：
- 设备信息：
- 维护类型：

## 1. 维护项目
列出维护项目清单

## 2. 执行情况
详细记录执行情况

## 3. 发现问题
记录发现的问题

## 4. 处理结果
问题处理情况

## 5. 建议
后续维护建议
""",
            "performance": """
# 性能分析报告

## 报告信息
- 分析周期：
- 设备信息：

## 1. 性能指标
关键性能指标数据

## 2. 数据分析
详细数据分析

## 3. 趋势分析
性能变化趋势

## 4. 对比分析
与基准或历史数据对比

## 5. 问题识别
发现的性能问题

## 6. 优化建议
性能优化建议
"""
        }
        return templates.get(report_type, templates["general"])
    
    def _construct_prompt(
        self,
        query: str,
        report_type: str,
        template: str,
        data: Optional[Dict[str, Any]],
        context: str
    ) -> str:
        """Construct prompt for report generation"""
        prompt = f"""请根据以下要求生成{report_type}类型的报告：

【报告要求】
{query}

【报告模板】
{template}

"""
        if data:
            prompt += f"""【提供的数据】
{self._format_data(data)}

"""
        
        if context and context != "No relevant information found in knowledge base.":
            prompt += f"""【参考资料】
{context}

"""
        
        prompt += """请生成完整、专业的报告，确保：
1. 格式清晰，结构完整
2. 内容准确，分析深入
3. 使用专业术语
4. 提供实用建议
"""
        return prompt
    
    def _format_data(self, data: Dict[str, Any]) -> str:
        """Format data for prompt"""
        formatted = []
        for key, value in data.items():
            formatted.append(f"{key}: {value}")
        return "\n".join(formatted)
    
    def generate_summary(
        self,
        content: str,
        max_length: int = 200,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate summary of content
        
        Args:
            content: Content to summarize
            max_length: Maximum length of summary
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with summary
        """
        prompt = f"""请为以下内容生成简洁摘要（不超过{max_length}字）：

{content}

摘要要求：
- 提炼核心信息
- 保持专业性
- 简洁明了
"""
        
        summary = self.llm_client.generate(
            prompt=prompt,
            system_prompt="你是一位专业的技术文档摘要专家。"
        )
        
        return {
            "original_length": len(content),
            "summary": summary,
            "summary_length": len(summary)
        }


def create_report_generator_agent(config: Optional[AgentConfig] = None) -> ReportGeneratorAgent:
    """
    Factory function to create report generator agent
    
    Args:
        config: Optional agent configuration
        
    Returns:
        ReportGeneratorAgent instance
    """
    return ReportGeneratorAgent(config)
