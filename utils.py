"""
utils.py —— 工具函数模块

提供以下功能：
    1. PDF 文档解析（pdfplumber）
    2. 文本分块（RecursiveCharacterTextSplitter）
    3. 向量存储的构建与加载（Chroma）
    4. Embedding 模型的统一创建入口
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import List, Optional

import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

import config

# 日志（basicConfig 仅在 app.py 入口调用，这里只获取 logger）
logger = logging.getLogger(__name__)


# ======================================================================
# 1. Embedding 模型工厂
# ======================================================================
def get_embeddings():
    """
    创建并返回 Embedding 模型实例。

    根据 config.USE_OLLAMA 自动切换：
        - True  -> OllamaEmbeddings（本地部署）
        - False -> OpenAIEmbeddings（云端 API）

    Returns:
        Embeddings: LangChain 兼容的 Embedding 实例。

    Raises:
        RuntimeError: 当所需依赖未安装或密钥缺失时抛出。
    """
    try:
        if config.USE_OLLAMA:
            from langchain_ollama import OllamaEmbeddings
            logger.info("使用 Ollama Embedding: %s", config.OLLAMA_EMBEDDING_MODEL)
            return OllamaEmbeddings(
                model=config.OLLAMA_EMBEDDING_MODEL,
                base_url=config.OLLAMA_BASE_URL,
            )

        # 默认使用 OpenAI
        if not config.OPENAI_API_KEY:
            raise RuntimeError("未检测到 OPENAI_API_KEY，请在 .env 中配置")

        from langchain_openai import OpenAIEmbeddings
        logger.info("使用 OpenAI Embedding: %s", config.OPENAI_EMBEDDING_MODEL)
        return OpenAIEmbeddings(
            model=config.OPENAI_EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )

    except ImportError as e:
        raise RuntimeError(f"Embedding 依赖未正确安装：{e}") from e


# ======================================================================
# 2. PDF 解析
# ======================================================================
def parse_pdf(file_path: str | Path) -> List[Document]:
    """
    使用 pdfplumber 解析 PDF，按页返回 LangChain Document 列表。

    Args:
        file_path: PDF 文件路径（绝对或相对路径均可）。

    Returns:
        List[Document]: 每一页对应一个 Document，metadata 中包含
        source 文件名与 page 页码（从 1 开始）。

    Raises:
        FileNotFoundError: 文件不存在。
        ValueError: 文件无法被 pdfplumber 打开或内容为空。
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    documents: List[Document] = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                text = (page.extract_text() or "").strip()
                if not text:
                    continue  # 跳过空白页
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file_path.name,
                            "page": page_idx,
                        },
                    )
                )
    except Exception as e:
        raise ValueError(f"PDF 解析失败：{file_path.name} - {e}") from e

    if not documents:
        raise ValueError(f"PDF 中未提取到任何文本：{file_path.name}")

    logger.info("已解析 %s，共 %d 页", file_path.name, len(documents))
    return documents


# ======================================================================
# 3. 文本分块
# ======================================================================
def split_documents(
    documents: List[Document],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
) -> List[Document]:
    """
    将长文档切分为语义块，便于向量化与检索。

    Args:
        documents: 原始文档列表。
        chunk_size: 每个块的最大字符数，默认读取 config.CHUNK_SIZE。
        chunk_overlap: 相邻块之间的重叠字符数，默认读取 config.CHUNK_OVERLAP。

    Returns:
        List[Document]: 切分后的文档块列表，保留原有 metadata。
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    logger.info("分块完成：%d 页 -> %d 块", len(documents), len(chunks))
    return chunks


# ======================================================================
# 4. 向量存储
# ======================================================================
def build_vector_store(
    chunks: List[Document],
    persist_directory: Optional[str | Path] = None,
) -> Chroma:
    """
    将文档块向量化并持久化到 Chroma。

    Args:
        chunks: 经过分块的文档列表。
        persist_directory: 持久化目录，默认使用 config.VECTOR_DIR。

    Returns:
        Chroma: 已构建并持久化的向量数据库实例。

    Raises:
        ValueError: 传入的 chunks 为空。
    """
    if not chunks:
        raise ValueError("待向量化的文档块为空")

    persist_directory = str(persist_directory or config.VECTOR_DIR)
    embeddings = get_embeddings()

    logger.info("开始构建向量库（共 %d 块）...", len(chunks))
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    # chromadb 0.4.x+ 设置 persist_directory 后会自动持久化，无需手动调用
    logger.info("向量库已持久化到 %s", persist_directory)
    return vector_store


def load_vector_store(
    persist_directory: Optional[str | Path] = None,
) -> Optional[Chroma]:
    """
    从磁盘加载已有的 Chroma 向量库。

    Args:
        persist_directory: 向量库目录，默认读取 config.VECTOR_DIR。

    Returns:
        Chroma 实例；若目录不存在或为空，返回 None。
    """
    persist_directory = Path(persist_directory or config.VECTOR_DIR)
    if not persist_directory.exists() or not any(persist_directory.iterdir()):
        logger.warning("向量库目录不存在或为空：%s", persist_directory)
        return None

    try:
        embeddings = get_embeddings()
        vector_store = Chroma(
            persist_directory=str(persist_directory),
            embedding_function=embeddings,
        )
        logger.info("向量库加载成功：%s", persist_directory)
        return vector_store
    except Exception as e:
        logger.error("加载向量库失败：%s", e)
        return None


def reset_vector_store(persist_directory: Optional[str | Path] = None) -> None:
    """
    清空并删除向量库目录。用于「重置」功能。

    Args:
        persist_directory: 要删除的目录，默认读取 config.VECTOR_DIR。
    """
    persist_directory = Path(persist_directory or config.VECTOR_DIR)
    if persist_directory.exists():
        shutil.rmtree(persist_directory)
        logger.info("已删除向量库目录：%s", persist_directory)
    persist_directory.mkdir(parents=True, exist_ok=True)


# ======================================================================
# 5. 一站式入口：文件 -> 向量库
# ======================================================================
def ingest_pdf(file_path: str | Path) -> Chroma:
    """
    便捷函数：解析 PDF → 分块 → 向量化 → 持久化，一步完成。

    Args:
        file_path: 待处理的 PDF 文件路径。

    Returns:
        Chroma: 已写入新文档的向量库实例。
    """
    docs = parse_pdf(file_path)
    chunks = split_documents(docs)
    return build_vector_store(chunks)
