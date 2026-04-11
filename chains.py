"""
chains.py —— RAG 问答链模块

提供以下功能：
    1. LLM 模型工厂（OpenAI / Ollama）
    2. 构建带上下文记忆的检索问答链（ConversationalRetrievalChain）
    3. 提取并格式化引用来源
    4. 对外统一的问答入口：ask(...)
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel

import config

logger = logging.getLogger(__name__)


# ======================================================================
# 1. LLM 工厂
# ======================================================================
def get_llm() -> BaseChatModel:
    """
    创建并返回 LLM 实例。

    根据 config.USE_OLLAMA 自动切换：
        - True  -> ChatOllama（本地模型）
        - False -> ChatOpenAI（OpenAI 官方 API）

    Returns:
        BaseChatModel: LangChain 兼容的聊天模型实例。

    Raises:
        RuntimeError: 依赖未安装或 API Key 缺失。
    """
    try:
        if config.USE_OLLAMA:
            from langchain_ollama import ChatOllama
            logger.info("使用 Ollama LLM: %s", config.OLLAMA_MODEL)
            return ChatOllama(
                model=config.OLLAMA_MODEL,
                base_url=config.OLLAMA_BASE_URL,
                temperature=config.TEMPERATURE,
            )

        if not config.OPENAI_API_KEY:
            raise RuntimeError("未检测到 OPENAI_API_KEY，请在 .env 中配置")

        from langchain_openai import ChatOpenAI
        logger.info("使用 OpenAI LLM: %s", config.OPENAI_MODEL)
        return ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            openai_api_key=config.OPENAI_API_KEY,
        )

    except ImportError as e:
        raise RuntimeError(f"LLM 依赖未正确安装：{e}") from e


# ======================================================================
# 2. Prompt 构造
# ======================================================================
def build_qa_prompt() -> PromptTemplate:
    """
    构造基于 config.QA_PROMPT_TEMPLATE 的 PromptTemplate。

    Returns:
        PromptTemplate: 可在 ConversationalRetrievalChain 中使用的模板。
    """
    template = config.QA_PROMPT_TEMPLATE.replace(
        "{system_prompt}", config.SYSTEM_PROMPT
    )
    return PromptTemplate(
        template=template,
        input_variables=["context", "chat_history", "question"],
    )


# ======================================================================
# 3. 构建 RAG 链
# ======================================================================
def build_qa_chain(
    vector_store: Chroma,
    top_k: int | None = None,
) -> ConversationalRetrievalChain:
    """
    构建带对话记忆的 RAG 检索问答链。

    Args:
        vector_store: 已加载或构建好的 Chroma 向量库。
        top_k: 检索返回的文档数量，默认读取 config.TOP_K。

    Returns:
        ConversationalRetrievalChain: 已配置好的问答链。

    Raises:
        ValueError: vector_store 为 None。
    """
    if vector_store is None:
        raise ValueError("vector_store 不能为空，请先上传并向量化文档")

    top_k = top_k or config.TOP_K
    llm = get_llm()

    # 检索器：基于相似度检索 Top-K 文档块
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )

    # 对话记忆：保留多轮上下文
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )

    qa_prompt = build_qa_prompt()

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,     # 返回引用文档，便于展示来源
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        verbose=False,
    )
    logger.info("RAG 问答链构建完成（Top-K=%d）", top_k)
    return chain


# ======================================================================
# 4. 引用提取与格式化
# ======================================================================
def extract_citations(source_documents: List[Document]) -> List[Dict[str, Any]]:
    """
    从检索结果中提取并去重引用来源。

    Args:
        source_documents: 检索链返回的 source_documents。

    Returns:
        List[Dict]: 每一项包含 source/page/snippet 三个字段。
    """
    citations: List[Dict[str, Any]] = []
    seen: set[Tuple[str, int]] = set()

    for doc in source_documents or []:
        source = doc.metadata.get("source", "未知来源")
        page = int(doc.metadata.get("page", 0))
        key = (source, page)
        if key in seen:
            continue
        seen.add(key)

        # 截取内容摘要，避免前端展示过长
        snippet = doc.page_content.strip().replace("\n", " ")
        if len(snippet) > 120:
            snippet = snippet[:120] + "…"

        citations.append(
            {
                "source": source,
                "page": page,
                "snippet": snippet,
            }
        )
    return citations


def format_citations(citations: List[Dict[str, Any]]) -> str:
    """
    将引用列表渲染为 Markdown 字符串，便于直接展示。

    Args:
        citations: extract_citations 的返回值。

    Returns:
        str: Markdown 格式的引用文本。
    """
    if not citations:
        return ""

    lines = ["\n\n**📚 引用来源：**"]
    for idx, c in enumerate(citations, start=1):
        lines.append(
            f"{idx}. `{c['source']}` · 第 {c['page']} 页  \n   > {c['snippet']}"
        )
    return "\n".join(lines)


# ======================================================================
# 5. 对外统一问答入口
# ======================================================================
def ask(
    chain: ConversationalRetrievalChain,
    question: str,
) -> Dict[str, Any]:
    """
    向 RAG 问答链发起一次提问。

    Args:
        chain: 已构建的问答链实例。
        question: 用户输入的问题。

    Returns:
        Dict[str, Any]: 包含以下字段：
            - answer (str): 模型生成的回答
            - citations (List[Dict]): 去重后的引用列表
            - citations_md (str): 引用的 Markdown 字符串
            - raw_sources (List[Document]): 原始检索结果

    Raises:
        ValueError: 问题为空。
        RuntimeError: 调用过程中出现异常。
    """
    if not question or not question.strip():
        raise ValueError("问题不能为空")

    try:
        result = chain.invoke({"question": question.strip()})
    except Exception as e:
        logger.exception("RAG 链调用失败")
        raise RuntimeError(f"问答失败：{e}") from e

    answer: str = result.get("answer", "").strip()
    source_docs: List[Document] = result.get("source_documents", []) or []
    citations = extract_citations(source_docs)

    return {
        "answer": answer,
        "citations": citations,
        "citations_md": format_citations(citations),
        "raw_sources": source_docs,
    }
