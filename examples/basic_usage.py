"""
Example: Basic usage of Fault Diagnosis Agent
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.fault_diagnosis import create_fault_diagnosis_agent
from core.knowledge_base import create_knowledge_base


def main():
    """
    Demonstrate basic usage of fault diagnosis agent
    """
    print("=" * 60)
    print("风电故障诊断智能体 - 基础示例")
    print("=" * 60)
    print()
    
    # Create knowledge base and load documents
    print("📚 初始化知识库...")
    kb = create_knowledge_base()
    
    # Load sample documents
    knowledge_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge')
    if os.path.exists(knowledge_dir):
        try:
            kb.add_from_directory(knowledge_dir)
            print("✅ 知识库加载完成")
        except Exception as e:
            print(f"⚠️  知识库加载警告: {e}")
            print("   继续使用通用知识...")
    
    print()
    
    # Create agent
    print("🤖 创建故障诊断智能体...")
    agent = create_fault_diagnosis_agent()
    print("✅ 智能体创建完成")
    print()
    
    # Example queries
    example_queries = [
        "发电机后轴承温度达到85度，振动值略有上升，这是什么问题？",
        "变桨系统响应变慢，电机电流偏高，如何处理？",
        "齿轮箱油温持续在75度以上，需要注意什么？",
    ]
    
    print("=" * 60)
    print("开始诊断示例")
    print("=" * 60)
    print()
    
    for i, query in enumerate(example_queries, 1):
        print(f"【示例 {i}】")
        print(f"故障描述: {query}")
        print()
        
        try:
            # Process query
            result = agent.process(query)
            
            print("诊断结果:")
            print("-" * 60)
            print(result["diagnosis"])
            print("-" * 60)
            print()
            
            # Show source documents if available
            if result.get("source_documents"):
                print(f"参考了 {len(result['source_documents'])} 份相关文档")
            
        except Exception as e:
            print(f"❌ 诊断出错: {e}")
            print("   提示: 请确保已设置 OPENAI_API_KEY 环境变量")
        
        print()
        print("=" * 60)
        print()
    
    print("✅ 示例演示完成")
    print()
    print("💡 提示:")
    print("   1. 设置环境变量: export OPENAI_API_KEY='your-api-key'")
    print("   2. 或创建 .env 文件配置 API key")
    print("   3. 可以在 knowledge/ 目录添加更多文档")


if __name__ == "__main__":
    main()
