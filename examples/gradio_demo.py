"""
Gradio Demo for Wind Power AI Agents
Interactive web interface for all three agents

Note: Run this example from the project root directory after installing:
    pip install -e .
Or if running directly, make sure the parent directory is in Python path.
"""
import os
import sys

# Add parent directory to path (for development/testing without installation)
# In production, install the package with: pip install -e .
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from agents.fault_diagnosis import create_fault_diagnosis_agent
from agents.regulation_qa import create_regulation_qa_agent
from agents.report_generator import create_report_generator_agent
from core.knowledge_base import create_knowledge_base


# Initialize agents
print("🚀 初始化智能体系统...")

try:
    # Initialize knowledge base
    kb = create_knowledge_base()
    knowledge_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge')
    if os.path.exists(knowledge_dir):
        try:
            kb.add_from_directory(knowledge_dir)
            print("✅ 知识库加载完成")
        except Exception as e:
            print(f"⚠️  知识库加载警告: {e}")
    
    # Create agents
    fault_agent = create_fault_diagnosis_agent()
    qa_agent = create_regulation_qa_agent()
    report_agent = create_report_generator_agent()
    print("✅ 智能体初始化完成")
    
except Exception as e:
    print(f"❌ 初始化错误: {e}")
    print("提示: 请确保已设置 OPENAI_API_KEY 环境变量")
    fault_agent = None
    qa_agent = None
    report_agent = None


def diagnose_fault(query):
    """故障诊断接口"""
    if not fault_agent:
        return "❌ 智能体未正确初始化，请检查配置"
    
    if not query.strip():
        return "请输入故障描述"
    
    try:
        result = fault_agent.process(query)
        
        output = f"## 诊断结果\n\n{result['diagnosis']}\n\n"
        
        if result.get('source_documents'):
            output += f"\n---\n📚 参考了 {len(result['source_documents'])} 份相关文档\n"
        
        return output
    
    except Exception as e:
        return f"❌ 诊断出错: {str(e)}\n\n请检查 API 配置或网络连接"


def answer_regulation(query):
    """规程问答接口"""
    if not qa_agent:
        return "❌ 智能体未正确初始化，请检查配置"
    
    if not query.strip():
        return "请输入您的问题"
    
    try:
        result = qa_agent.process(query)
        
        output = f"## 回答\n\n{result['answer']}\n\n"
        
        if result.get('source_documents'):
            output += f"\n---\n📚 参考了 {len(result['source_documents'])} 份相关文档\n"
        
        return output
    
    except Exception as e:
        return f"❌ 回答出错: {str(e)}\n\n请检查 API 配置或网络连接"


def generate_report(query, report_type):
    """报告生成接口"""
    if not report_agent:
        return "❌ 智能体未正确初始化，请检查配置"
    
    if not query.strip():
        return "请输入报告要求"
    
    try:
        result = report_agent.process(query, report_type=report_type)
        
        output = f"{result['report']}\n\n"
        output += f"\n---\n生成时间: {result['generated_at']}\n"
        
        return output
    
    except Exception as e:
        return f"❌ 生成出错: {str(e)}\n\n请检查 API 配置或网络连接"


# Create Gradio interface
with gr.Blocks(
    title="风电AI智能体",
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown("""
    # 🌬️ 风电AI智能体工具包
    
    基于大模型与RAG技术的风电行业智能助手
    
    **⚠️ 免责声明**: 
    - 本系统提供的所有信息仅供参考，不作为实际操作依据
    - 实际操作请严格遵循设备制造商的官方文档和相关法规
    - 涉及安全的作业必须由具备相应资质的专业人员执行
    - 使用本系统产生的任何后果由使用者自行承担
    """)
    
    with gr.Tabs():
        # Tab 1: Fault Diagnosis
        with gr.Tab("🔧 故障诊断"):
            gr.Markdown("""
            ### 故障诊断智能体
            描述设备的故障现象，智能体将基于知识库提供诊断建议。
            """)
            
            with gr.Row():
                with gr.Column():
                    fault_input = gr.Textbox(
                        label="故障描述",
                        placeholder="例如：发电机轴承温度过高，振动值上升...",
                        lines=5
                    )
                    fault_button = gr.Button("开始诊断", variant="primary")
                
                with gr.Column():
                    fault_output = gr.Markdown(label="诊断结果")
            
            fault_button.click(
                fn=diagnose_fault,
                inputs=fault_input,
                outputs=fault_output
            )
            
            gr.Examples(
                examples=[
                    ["发电机后轴承温度达到85度，振动值略有上升"],
                    ["变桨系统响应缓慢，电机电流偏高"],
                    ["齿轮箱油温持续超过70度，伴有异常噪音"],
                    ["偏航系统卡滞，对风误差大"],
                ],
                inputs=fault_input
            )
        
        # Tab 2: Regulation Q&A
        with gr.Tab("📋 规程问答"):
            gr.Markdown("""
            ### 规程问答智能体
            询问关于风电运维规程、标准、操作流程等问题。
            """)
            
            with gr.Row():
                with gr.Column():
                    qa_input = gr.Textbox(
                        label="您的问题",
                        placeholder="例如：齿轮箱润滑油多久更换一次？",
                        lines=5
                    )
                    qa_button = gr.Button("获取答案", variant="primary")
                
                with gr.Column():
                    qa_output = gr.Markdown(label="回答")
            
            qa_button.click(
                fn=answer_regulation,
                inputs=qa_input,
                outputs=qa_output
            )
            
            gr.Examples(
                examples=[
                    ["日常巡检应该检查哪些项目？"],
                    ["机组紧急停机的条件有哪些？"],
                    ["齿轮箱润滑油的更换周期是多久？"],
                    ["高空作业的安全要求有哪些？"],
                ],
                inputs=qa_input
            )
        
        # Tab 3: Report Generation
        with gr.Tab("📊 报告生成"):
            gr.Markdown("""
            ### 报告生成智能体
            根据您的要求生成专业的技术报告。
            """)
            
            with gr.Row():
                with gr.Column():
                    report_input = gr.Textbox(
                        label="报告要求",
                        placeholder="例如：生成3号机组的月度维护报告...",
                        lines=5
                    )
                    report_type = gr.Dropdown(
                        choices=["general", "fault", "maintenance", "performance"],
                        value="general",
                        label="报告类型",
                        info="选择要生成的报告类型"
                    )
                    report_button = gr.Button("生成报告", variant="primary")
                
                with gr.Column():
                    report_output = gr.Markdown(label="生成的报告")
            
            report_button.click(
                fn=generate_report,
                inputs=[report_input, report_type],
                outputs=report_output
            )
            
            gr.Examples(
                examples=[
                    ["生成2号机组本月的维护保养报告", "maintenance"],
                    ["生成发电机轴承温度异常的故障分析报告", "fault"],
                    ["生成风场第一季度的性能分析报告", "performance"],
                ],
                inputs=[report_input, report_type]
            )
    
    gr.Markdown("""
    ---
    ### 📖 使用说明
    
    1. **故障诊断**: 详细描述故障现象，系统会给出可能原因和解决方案
    2. **规程问答**: 询问操作规程、安全要求等问题
    3. **报告生成**: 说明报告要求，选择报告类型，系统会生成结构化报告
    
    ### ⚙️ 配置要求
    
    - 需要设置 `OPENAI_API_KEY` 环境变量
    - 可在项目根目录创建 `.env` 文件配置
    - 确保 `knowledge/` 目录下有相关文档
    
    ### 🔗 项目信息
    
    - GitHub: [saivian1/--AI-Agents](https://github.com/saivian1/--AI-Agents)
    - 文档: 查看项目 README
    - 反馈: 提交 Issue 或 Pull Request
    """)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("启动 Gradio 演示界面...")
    print("=" * 60)
    print("\n访问地址将在下方显示\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
