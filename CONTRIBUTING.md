# 贡献指南

感谢您对风电AI智能体项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告Bug

如果您发现了bug，请通过 GitHub Issues 报告，并包含以下信息：

- 问题的详细描述
- 复现步骤
- 预期行为和实际行为
- 系统环境信息（Python版本、操作系统等）
- 相关的错误日志

### 提出新功能

如果您有好的想法或建议：

1. 先查看现有的 Issues 和 Pull Requests，避免重复
2. 创建新的 Issue，详细描述您的想法
3. 等待社区讨论和反馈

### 提交代码

1. **Fork 项目**
   ```bash
   # Fork 后克隆到本地
   git clone https://github.com/YOUR_USERNAME/--AI-Agents.git
   cd --AI-Agents
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行开发**
   - 编写代码
   - 添加测试
   - 更新文档

4. **代码规范**
   ```bash
   # 使用 black 格式化代码
   black .
   
   # 使用 flake8 检查代码风格
   flake8 .
   ```

5. **运行测试**
   ```bash
   pytest
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   # 或
   git commit -m "fix: fix your bug description"
   ```

7. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 访问您的 Fork 仓库
   - 点击 "New Pull Request"
   - 填写 PR 描述，说明您的更改
   - 提交 PR

## 代码规范

### Python 代码风格

- 遵循 PEP 8 规范
- 使用 4 个空格缩进
- 最大行长度 100 字符
- 使用有意义的变量和函数名

### 文档字符串

使用 Google 风格的文档字符串：

```python
def example_function(param1: str, param2: int) -> bool:
    """
    函数的简短描述
    
    Args:
        param1: 第一个参数的描述
        param2: 第二个参数的描述
        
    Returns:
        返回值的描述
        
    Raises:
        ValueError: 何时会抛出此异常
    """
    pass
```

### 提交信息规范

使用语义化的提交信息：

- `feat: 新功能`
- `fix: Bug修复`
- `docs: 文档更新`
- `style: 代码格式调整（不影响功能）`
- `refactor: 代码重构`
- `test: 测试相关`
- `chore: 构建或辅助工具的变动`

例如：
```
feat: add support for Claude LLM provider
fix: resolve knowledge base loading error
docs: update installation instructions
```

## 开发环境设置

### 安装开发依赖

```bash
pip install -r requirements.txt
pip install black flake8 pytest pytest-asyncio
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_agents.py

# 运行并显示覆盖率
pytest --cov=agents --cov=core
```

## 项目结构说明

- `agents/`: 智能体实现
- `core/`: 核心功能模块
- `examples/`: 示例和演示
- `knowledge/`: 示例知识库文档
- `tests/`: 测试文件

## 添加新智能体

创建新智能体的步骤：

1. 在 `agents/` 目录创建新文件
2. 继承 `BaseAgent` 类
3. 实现 `process()` 方法
4. 重写 `get_system_prompt()` 方法
5. 添加工厂函数
6. 编写测试
7. 更新文档

示例：

```python
from agents.base_agent import BaseAgent
from typing import Dict, Any

class MyNewAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return "Your system prompt here"
    
    def process(self, query: str, **kwargs) -> Dict[str, Any]:
        # Your implementation
        pass

def create_my_new_agent(config=None):
    return MyNewAgent(config)
```

## 数据安全要求

⚠️ **重要**：提交的所有文档和数据必须：

- 完全脱敏，不包含真实设备信息
- 使用虚构的数据和场景
- 添加明确的免责声明

## 问题和讨论

- 提问和讨论：使用 GitHub Issues
- 即时沟通：（如果有的话，添加聊天群组链接）

## 行为准则

参与本项目时，请：

- 尊重其他贡献者
- 保持友好和专业
- 接受建设性的批评
- 关注项目的最佳利益

## 许可证

贡献的代码将按照项目的 MIT 许可证进行许可。

---

再次感谢您的贡献！🙏
