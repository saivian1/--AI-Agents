# 🌬️ 风电AI智能体工具包

<div align="center">

**一个专注于风力发电行业的开源AI智能体（Agent）工具包与案例库**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)](https://github.com/langchain-ai/langchain)

[快速开始](#快速开始) • [功能特性](#功能特性) • [架构设计](#架构设计) • [使用指南](#使用指南) • [贡献指南](#贡献指南)

</div>

---

## 🎯 项目简介

本项目是一个将**风力发电行业**与**大语言模型（LLM）**深度结合的开源工具包，基于RAG（检索增强生成）技术构建可复用的AI智能体，为风电行业提供智能化解决方案。

### 核心价值

- 🚀 **技术旗舰**：建立个人技术品牌，展示AI在垂直行业的应用能力
- 🧩 **行业积木**：提供可复用的组件，让开发者快速构建定制化应用
- 🤝 **社区驱动**：聚集行业力量，共同推动智能化转型
- 📚 **知识沉淀**：将行业经验和知识结构化、可复用

### 首批智能体

1. **🔧 故障诊断智能体**：基于症状描述，提供故障原因分析和解决方案
2. **📋 规程问答智能体**：回答运维规程、标准、操作流程相关问题
3. **📊 报告生成智能体**：自动生成故障、维护、性能等专业报告

---

## 🌟 功能特性

### 智能体能力

- ✅ **多源知识检索**：支持PDF、Word、TXT等多种文档格式
- ✅ **语义理解**：基于向量数据库的语义检索，准确匹配相关知识
- ✅ **上下文对话**：支持多轮对话，理解对话历史
- ✅ **结构化输出**：生成格式规范的专业报告
- ✅ **可扩展架构**：基类设计便于快速开发新智能体

### 技术栈

- 🤖 **LangChain**：大模型应用框架
- 🗄️ **ChromaDB**：向量数据库，用于知识检索
- 🎨 **Gradio**：快速构建Web演示界面
- 🔑 **OpenAI API**：大语言模型接口（可扩展其他提供商）
- 📄 **Document Loaders**：多格式文档加载器

---

## 📁 项目结构

```
.
├── agents/                 # 智能体实现
│   ├── __init__.py
│   ├── base_agent.py      # 智能体基类
│   ├── fault_diagnosis.py # 故障诊断智能体
│   ├── regulation_qa.py   # 规程问答智能体
│   └── report_generator.py # 报告生成智能体
│
├── core/                   # 核心模块
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── llm_client.py      # LLM客户端封装
│   └── knowledge_base.py  # 知识库管理
│
├── examples/              # 示例与演示
│   ├── basic_usage.py    # 基础使用示例
│   └── gradio_demo.py    # Gradio演示界面
│
├── knowledge/             # 知识库文档（示例）
│   ├── documents/         # 通用技术文档
│   ├── regulations/       # 规程标准文档
│   └── reports/           # 报告模板
│
├── tests/                 # 测试文件
│
├── .gitignore
├── requirements.txt       # 项目依赖
├── setup.py              # 安装配置
└── README.md             # 项目文档
```

---

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- OpenAI API Key（或其他支持的LLM提供商）

### 1. 克隆项目

```bash
git clone https://github.com/saivian1/--AI-Agents.git
cd --AI-Agents
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或使用开发模式安装：

```bash
pip install -e .
```

### 3. 配置环境变量

创建 `.env` 文件并配置：

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

或直接设置环境变量：

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### 4. 运行示例

#### 基础使用示例

```bash
python examples/basic_usage.py
```

#### Gradio Web演示

```bash
python examples/gradio_demo.py
```

然后在浏览器访问 `http://localhost:7860`

---

## 📖 使用指南

### 故障诊断示例

```python
from agents.fault_diagnosis import create_fault_diagnosis_agent

# 创建智能体
agent = create_fault_diagnosis_agent()

# 诊断故障
result = agent.process("发电机轴承温度过高，达到85度")

print(result["diagnosis"])
```

### 规程问答示例

```python
from agents.regulation_qa import create_regulation_qa_agent

# 创建智能体
agent = create_regulation_qa_agent()

# 提问
result = agent.process("日常巡检应该检查哪些项目？")

print(result["answer"])
```

### 报告生成示例

```python
from agents.report_generator import create_report_generator_agent

# 创建智能体
agent = create_report_generator_agent()

# 生成报告
result = agent.process(
    query="生成3号机组的月度维护报告",
    report_type="maintenance"
)

print(result["report"])
```

### 添加自定义知识库

```python
from core.knowledge_base import create_knowledge_base

# 创建知识库
kb = create_knowledge_base()

# 添加文档目录
kb.add_from_directory("path/to/your/documents")

# 或添加单个文档
kb.add_documents(kb.load_document("path/to/document.pdf"))
```

---

## 🏗️ 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────┐
│                   Gradio UI / API                   │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼─────┐          ┌─────▼────┐
    │  Agents  │          │   Core   │
    │          │          │          │
    │ • Fault  │◄────────►│ • Config │
    │ • QA     │          │ • LLM    │
    │ • Report │          │ • KB     │
    └──────────┘          └─────┬────┘
                                │
                    ┌───────────┴──────────┐
                    │                      │
              ┌─────▼─────┐         ┌─────▼─────┐
              │ ChromaDB  │         │  OpenAI   │
              │ (Vectors) │         │   (LLM)   │
              └───────────┘         └───────────┘
```

### 智能体工作流程

1. **接收查询**：用户输入问题或描述
2. **检索知识**：从向量数据库检索相关文档
3. **构建提示**：结合查询和检索结果构建LLM提示
4. **生成回答**：调用LLM生成专业回答
5. **返回结果**：返回结构化结果和引用来源

---

## 🔧 配置说明

### LLM配置

在 `core/config.py` 或通过代码配置：

```python
from core.config import LLMConfig, AgentConfig, set_config

llm_config = LLMConfig(
    provider="openai",
    model="gpt-4",  # 或 "gpt-3.5-turbo"
    temperature=0.7,
    max_tokens=2000
)

config = AgentConfig(llm=llm_config)
set_config(config)
```

### 知识库配置

```python
from core.config import VectorDBConfig, AgentConfig, set_config

vector_config = VectorDBConfig(
    persist_directory="./my_chroma_db",
    collection_name="my_collection"
)

config = AgentConfig(vector_db=vector_config)
set_config(config)
```

---

## 🤝 贡献指南

欢迎贡献！无论是新功能、Bug修复还是文档改进。

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码规范
- 添加适当的注释和文档字符串
- 编写单元测试
- 更新相关文档

---

## ⚠️ 重要声明

### 数据安全与隐私

- ✅ 所有示例文档均为**虚构内容**，不包含真实设备信息
- ✅ 请勿上传包含敏感信息的真实文档
- ✅ 在生产环境使用前，请确保所有数据已完全脱敏

### 免责声明

本项目提供的所有信息、诊断建议和生成内容**仅供参考和学习使用**：

- ⚠️ 不作为实际操作的依据
- ⚠️ 实际操作请严格遵循设备制造商的官方文档
- ⚠️ 涉及安全的作业必须由具备资质的专业人员执行
- ⚠️ 使用本系统产生的任何后果由使用者自行承担

---

## 📋 路线图

- [x] 核心架构与基础组件
- [x] 三个基础智能体实现
- [x] Gradio演示界面
- [x] 基础文档与示例
- [ ] 更多智能体类型（设备选型、预测性维护等）
- [ ] 支持更多LLM提供商（Claude、文心一言等）
- [ ] 多模态支持（图像、音频分析）
- [ ] 移动端支持
- [ ] 企业版功能（权限管理、审计日志等）

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 优秀的LLM应用框架
- [ChromaDB](https://www.trychroma.com/) - 高效的向量数据库
- [Gradio](https://gradio.app/) - 简洁的ML应用界面
- OpenAI - 强大的语言模型

---

## 📞 联系方式

- 项目仓库：[https://github.com/saivian1/--AI-Agents](https://github.com/saivian1/--AI-Agents)
- 问题反馈：[Issues](https://github.com/saivian1/--AI-Agents/issues)
- 功能建议：[Pull Requests](https://github.com/saivian1/--AI-Agents/pulls)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个 Star！⭐**

*让我们一起推动风电行业的智能化转型！*

</div>
