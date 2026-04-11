"""
config.py —— 项目全局配置

包含以下内容：
    1. 默认运行参数（分块大小、检索数量等）
    2. 模型配置（OpenAI / Ollama）
    3. 提示词模板（PromptTemplate）
    4. 路径与环境变量定义
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ======================================================================
# 1. 加载 .env 环境变量
# ======================================================================
load_dotenv()


# ======================================================================
# 2. 路径配置
# ======================================================================
BASE_DIR: Path = Path(__file__).resolve().parent       # 项目根目录
DATA_DIR: Path = BASE_DIR / "data"                     # 上传文件缓存目录
VECTOR_DIR: Path = BASE_DIR / "vector_store"           # 向量库持久化目录

# 确保必要目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)


# ======================================================================
# 3. 模型配置
# ======================================================================
# 是否使用本地 Ollama 模型（否则使用 OpenAI）
USE_OLLAMA: bool = os.getenv("USE_OLLAMA", "false").lower() == "true"

# ---- OpenAI 配置 ----
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
OPENAI_EMBEDDING_MODEL: str = os.getenv(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)

# ---- Ollama 配置 ----
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_EMBEDDING_MODEL: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")


# ======================================================================
# 4. RAG 运行参数
# ======================================================================
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))          # 分块长度（字符）
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))     # 分块重叠
TOP_K: int = int(os.getenv("TOP_K", "4"))                       # 检索返回数量
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))     # 生成温度
MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))          # 最大输出 token


# ======================================================================
# 5. 提示词模板
# ======================================================================
# 系统提示：约束模型行为
SYSTEM_PROMPT: str = """你是一个严谨、专业的知识库助手。
请严格依据下方提供的【上下文】回答用户的问题。
要求：
1. 回答必须基于上下文，不得编造、臆测或引入未出现的信息；
2. 如果上下文无法回答问题，请直接回答："根据已有资料，我无法回答该问题"；
3. 回答应条理清晰、简洁准确；
4. 如涉及专业术语，请给出简要解释；
5. 使用与用户相同的语言作答（默认中文）。
"""

# RAG 问答模板：传入上下文与问题
QA_PROMPT_TEMPLATE: str = """{system_prompt}

【上下文】
{context}

【历史对话】
{chat_history}

【用户问题】
{question}

请根据上下文给出你的回答："""

# 引用格式模板
CITATION_TEMPLATE: str = "📚 来源：{source} (第 {page} 页)"


# ======================================================================
# 6. Streamlit 页面配置
# ======================================================================
PAGE_CONFIG: dict = {
    "page_title": "RAG 知识库问答系统",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# 应用元信息
APP_TITLE: str = "📚 RAG 知识库问答系统"
APP_DESCRIPTION: str = "上传 PDF 文档，基于检索增强生成技术进行智能问答"
