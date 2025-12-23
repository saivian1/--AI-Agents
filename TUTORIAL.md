# 快速入门教程

本教程将帮助您快速上手风电AI智能体工具包。

## 目录

1. [环境准备](#1-环境准备)
2. [安装配置](#2-安装配置)
3. [第一个示例](#3-第一个示例)
4. [使用知识库](#4-使用知识库)
5. [Web演示界面](#5-web演示界面)
6. [自定义智能体](#6-自定义智能体)
7. [常见问题](#7-常见问题)

---

## 1. 环境准备

### 系统要求

- Python 3.8 或更高版本
- 至少 4GB 可用内存
- 稳定的网络连接（用于访问LLM API）

### 检查Python版本

```bash
python --version
# 或
python3 --version
```

如果版本低于 3.8，请升级Python。

---

## 2. 安装配置

### 步骤1: 克隆项目

```bash
git clone https://github.com/saivian1/--AI-Agents.git
cd --AI-Agents
```

### 步骤2: 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 步骤3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤4: 配置API Key

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的 OpenAI API Key：

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**获取API Key**：
1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册/登录账号
3. 在 API Keys 页面创建新密钥
4. 复制密钥到 `.env` 文件

---

## 3. 第一个示例

### 运行基础示例

```bash
python examples/basic_usage.py
```

这个示例会：
1. 初始化知识库
2. 加载示例文档
3. 创建故障诊断智能体
4. 运行几个示例查询

**预期输出**：

```
============================================================
风电故障诊断智能体 - 基础示例
============================================================

📚 初始化知识库...
✅ 知识库加载完成

🤖 创建故障诊断智能体...
✅ 智能体创建完成

============================================================
开始诊断示例
============================================================

【示例 1】
故障描述: 发电机后轴承温度达到85度，振动值略有上升，这是什么问题？

诊断结果:
------------------------------------------------------------
[AI生成的诊断内容]
------------------------------------------------------------
...
```

### 代码解析

```python
# 1. 导入模块
from agents.fault_diagnosis import create_fault_diagnosis_agent
from core.knowledge_base import create_knowledge_base

# 2. 创建知识库
kb = create_knowledge_base()
kb.add_from_directory("knowledge")  # 加载知识文档

# 3. 创建智能体
agent = create_fault_diagnosis_agent()

# 4. 使用智能体
result = agent.process("故障描述...")
print(result["diagnosis"])
```

---

## 4. 使用知识库

### 添加自己的文档

将您的文档放在 `knowledge/` 目录下：

```
knowledge/
├── documents/
│   ├── your_document1.pdf
│   ├── your_document2.txt
│   └── your_document3.docx
├── regulations/
│   └── your_regulation.pdf
└── reports/
    └── your_report_template.txt
```

支持的文件格式：
- PDF (`.pdf`)
- Word文档 (`.docx`, `.doc`)
- 文本文件 (`.txt`)

### 加载文档

```python
from core.knowledge_base import create_knowledge_base

kb = create_knowledge_base()

# 方式1: 加载整个目录
kb.add_from_directory("knowledge")

# 方式2: 加载单个文件
documents = kb.load_document("path/to/your/document.pdf")
kb.add_documents(documents)
```

### 搜索知识库

```python
# 搜索相关内容
results = kb.search("齿轮箱维护", k=3)

for doc in results:
    print(doc.page_content)
    print(doc.metadata)
```

---

## 5. Web演示界面

### 启动Gradio界面

```bash
python examples/gradio_demo.py
```

启动后，打开浏览器访问：
```
http://localhost:7860
```

### 界面功能

1. **故障诊断标签页**
   - 输入故障描述
   - 点击"开始诊断"
   - 查看诊断结果和建议

2. **规程问答标签页**
   - 输入问题
   - 点击"获取答案"
   - 查看基于知识库的回答

3. **报告生成标签页**
   - 输入报告要求
   - 选择报告类型
   - 点击"生成报告"
   - 获取结构化报告

### 自定义端口

```python
# 在 gradio_demo.py 中修改
demo.launch(
    server_port=8080,  # 改为其他端口
    share=True  # 生成公共链接（可选）
)
```

---

## 6. 自定义智能体

### 创建新的智能体

```python
from agents.base_agent import BaseAgent
from typing import Dict, Any

class CustomAgent(BaseAgent):
    """自定义智能体"""
    
    def get_system_prompt(self) -> str:
        """定义智能体的角色和任务"""
        return """你是一位风电行业的XXX专家。
你的任务是...
"""
    
    def process(self, query: str, **kwargs) -> Dict[str, Any]:
        """处理用户查询"""
        # 1. 检索相关知识
        context = self.retrieve_context(query)
        
        # 2. 构建提示
        prompt = f"""
基于以下信息：
{context}

用户问题：{query}

请提供专业的回答...
"""
        
        # 3. 生成回答
        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt()
        )
        
        return {
            "query": query,
            "response": response,
            "context": context
        }

# 工厂函数
def create_custom_agent(config=None):
    return CustomAgent(config)
```

### 使用自定义智能体

```python
from your_module import create_custom_agent

agent = create_custom_agent()
result = agent.process("您的问题")
print(result["response"])
```

---

## 7. 常见问题

### Q1: 安装依赖时出错

**问题**: `pip install` 失败

**解决方案**:
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: API调用失败

**问题**: `OpenAI API error: Invalid API key`

**解决方案**:
1. 检查 `.env` 文件中的API key是否正确
2. 确认API key有足够的额度
3. 检查网络连接是否正常

### Q3: 知识库加载慢

**问题**: 加载大量文档很慢

**解决方案**:
```python
# 首次加载后，向量已持久化
# 第二次直接使用，无需重新加载
kb = create_knowledge_base()
# 向量数据保存在 chroma_db/ 目录
```

### Q4: 生成的回答不准确

**解决方案**:
1. 确保知识库中有相关文档
2. 调整检索参数：
```python
from core.config import AgentConfig, set_config

config = AgentConfig()
config.top_k = 5  # 增加检索结果数量
config.chunk_size = 1500  # 调整文本块大小
set_config(config)
```

### Q5: 想使用其他LLM

**解决方案**:
```python
from core.config import LLMConfig, AgentConfig, set_config

# 使用GPT-4
llm_config = LLMConfig(
    provider="openai",
    model="gpt-4",
    temperature=0.7
)

config = AgentConfig(llm=llm_config)
set_config(config)
```

### Q6: 如何在生产环境部署

**建议**:
1. 使用环境变量管理配置
2. 配置日志记录
3. 添加错误处理和重试机制
4. 使用专业的Web服务器（如Gunicorn）
5. 配置反向代理（如Nginx）
6. 实现访问控制和认证

---

## 下一步

- 📖 阅读[完整文档](README.md)
- 🔧 查看[更多示例](examples/)
- 🤝 参与[项目贡献](CONTRIBUTING.md)
- 💬 加入社区讨论

---

## 获取帮助

如果遇到问题：

1. 查看[常见问题](#7-常见问题)
2. 搜索[已有Issues](https://github.com/saivian1/--AI-Agents/issues)
3. 提交[新Issue](https://github.com/saivian1/--AI-Agents/issues/new)

---

**祝您使用愉快！🎉**
