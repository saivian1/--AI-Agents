from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wind-power-ai-agents",
    version="0.1.0",
    author="Wind Power AI Community",
    description="开源风电行业AI智能体工具包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saivian1/--AI-Agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-openai>=0.0.2",
        "langchain-chroma>=0.0.1",
        "langchain-core>=0.1.0",
        "langchain-text-splitters>=0.0.1",
        "chromadb>=0.4.22",
        "gradio>=4.0.0",
        "openai>=1.0.0",
        "pypdf>=3.17.0",
        "python-docx>=1.1.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
    ],
)
