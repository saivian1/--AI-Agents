# API参考文档

本文档提供各模块和智能体的API参考。

## 目录

- [Core模块](#core模块)
  - [Config配置](#config配置)
  - [LLM Client](#llm-client)
  - [Knowledge Base](#knowledge-base)
- [Agents智能体](#agents智能体)
  - [Base Agent](#base-agent)
  - [Fault Diagnosis Agent](#fault-diagnosis-agent)
  - [Regulation Q&A Agent](#regulation-qa-agent)
  - [Report Generator Agent](#report-generator-agent)

---

## Core模块

### Config配置

#### LLMConfig

```python
from core.config import LLMConfig

config = LLMConfig(
    provider="openai",          # LLM提供商
    model="gpt-3.5-turbo",     # 模型名称
    api_key="sk-...",          # API密钥（可选，从环境变量读取）
    temperature=0.7,            # 生成温度 0.0-2.0
    max_tokens=2000            # 最大token数
)
```

#### VectorDBConfig

```python
from core.config import VectorDBConfig

config = VectorDBConfig(
    db_type="chromadb",                    # 向量数据库类型
    persist_directory="./chroma_db",       # 持久化目录
    collection_name="wind_power_docs"      # 集合名称
)
```

#### AgentConfig

```python
from core.config import AgentConfig, get_config, set_config

# 创建配置
config = AgentConfig(
    llm=LLMConfig(...),              # LLM配置
    vector_db=VectorDBConfig(...),   # 向量DB配置
    chunk_size=1000,                 # 文本分块大小
    chunk_overlap=200,               # 分块重叠
    top_k=3                          # 检索结果数量
)

# 设置全局配置
set_config(config)

# 获取全局配置
config = get_config()
```

查看完整的API参考，请参考代码中的文档字符串。

---

## 使用示例

### 完整工作流

```python
# 1. 配置
from core.config import AgentConfig, LLMConfig, set_config

config = AgentConfig(
    llm=LLMConfig(model="gpt-4", temperature=0.7)
)
set_config(config)

# 2. 准备知识库
from core.knowledge_base import create_knowledge_base

kb = create_knowledge_base()
kb.add_from_directory("knowledge/")

# 3. 创建智能体
from agents.fault_diagnosis import create_fault_diagnosis_agent

agent = create_fault_diagnosis_agent()

# 4. 使用智能体
result = agent.process("发电机轴承温度过高")
print(result["diagnosis"])
```

---

## 更多资源

- 📖 [完整文档](../README.md)
- 🎓 [教程](../TUTORIAL.md)
- 🤝 [贡献指南](../CONTRIBUTING.md)
- 💬 [GitHub Issues](https://github.com/saivian1/--AI-Agents/issues)
