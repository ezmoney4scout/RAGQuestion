"""
app.py —— RAG 知识库问答系统主程序

运行方式：
    streamlit run app.py

包含以下模块：
    1. 页面与会话初始化
    2. 侧边栏：API / 模型 / 参数配置
    3. 主区域：文档上传 + 多轮对话问答
    4. 功能按钮：清空对话、重置知识库
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st

import config
import utils
import chains

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================================================
# 1. 页面初始化
# ======================================================================
st.set_page_config(**config.PAGE_CONFIG)


def init_session_state() -> None:
    """
    初始化 Streamlit session_state 中使用的所有字段。
    幂等：多次调用不会覆盖已有值。
    """
    defaults: Dict[str, Any] = {
        "messages": [],           # 对话历史：[{role, content, citations_md}]
        "vector_store": None,     # 当前向量库
        "qa_chain": None,         # 当前问答链
        "uploaded_files": [],     # 已处理的文件名列表
        "processed": False,       # 是否已完成向量化
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ======================================================================
# 2. 侧边栏配置
# ======================================================================
def render_sidebar() -> None:
    """
    渲染左侧配置栏：
        - 模型选择（OpenAI / Ollama）
        - API 密钥输入
        - RAG 参数调节（Top-K、温度）
        - 功能按钮（清空、重置）
    """
    with st.sidebar:
        st.title("⚙️ 设置")

        # ---- 模型提供方 ----
        st.subheader("🧠 模型配置")
        provider = st.radio(
            "选择 LLM 提供方",
            options=["OpenAI", "Ollama（本地）"],
            index=1 if config.USE_OLLAMA else 0,
            horizontal=True,
        )
        config.USE_OLLAMA = provider.startswith("Ollama")

        if not config.USE_OLLAMA:
            api_key = st.text_input(
                "OpenAI API Key",
                value=config.OPENAI_API_KEY,
                type="password",
                placeholder="sk-...",
                help="可在 .env 中预先配置，或在此临时覆盖",
            )
            if api_key:
                config.OPENAI_API_KEY = api_key
                os.environ["OPENAI_API_KEY"] = api_key

            config.OPENAI_MODEL = st.selectbox(
                "OpenAI 模型",
                options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o-mini"],
                index=0,
            )
        else:
            config.OLLAMA_BASE_URL = st.text_input(
                "Ollama Base URL",
                value=config.OLLAMA_BASE_URL,
            )
            config.OLLAMA_MODEL = st.text_input(
                "Ollama 模型名",
                value=config.OLLAMA_MODEL,
                help="例如：llama2 / qwen / mistral",
            )

        st.divider()

        # ---- RAG 参数 ----
        st.subheader("🔧 RAG 参数")
        config.CHUNK_SIZE = st.slider(
            "分块大小", min_value=200, max_value=2000,
            value=config.CHUNK_SIZE, step=100,
        )
        config.CHUNK_OVERLAP = st.slider(
            "分块重叠", min_value=0, max_value=500,
            value=config.CHUNK_OVERLAP, step=50,
        )
        config.TOP_K = st.slider(
            "检索 Top-K", min_value=1, max_value=10,
            value=config.TOP_K,
        )
        config.TEMPERATURE = st.slider(
            "生成温度", min_value=0.0, max_value=1.0,
            value=config.TEMPERATURE, step=0.1,
        )

        st.divider()

        # ---- 功能按钮 ----
        st.subheader("🛠️ 操作")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 清空对话", use_container_width=True):
                clear_chat()
                st.rerun()
        with col2:
            if st.button("♻️ 重置知识库", use_container_width=True):
                reset_knowledge_base()
                st.rerun()

        st.divider()
        st.caption("📖 RAG 知识库问答系统 v1.0")


# ======================================================================
# 3. 核心业务函数
# ======================================================================
def handle_upload(uploaded_files: List[Any]) -> None:
    """
    处理用户上传的 PDF 文件：
        1. 保存到本地缓存目录
        2. 解析、分块、向量化
        3. 更新 session_state

    Args:
        uploaded_files: Streamlit file_uploader 返回的文件对象列表。
    """
    if not uploaded_files:
        st.warning("请先选择至少一个 PDF 文件")
        return

    progress = st.progress(0.0, text="🚀 正在处理文档...")
    total = len(uploaded_files)
    all_chunks = []

    try:
        for idx, uploaded_file in enumerate(uploaded_files, start=1):
            progress.progress(
                idx / (total + 1),
                text=f"📄 解析中 ({idx}/{total}): {uploaded_file.name}",
            )

            # 1) 保存到本地
            file_path = Path(config.DATA_DIR) / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 2) 解析 + 分块
            docs = utils.parse_pdf(file_path)
            chunks = utils.split_documents(docs)
            all_chunks.extend(chunks)

        # 3) 一次性向量化（效率更高）
        progress.progress(0.95, text="🧬 正在向量化并写入向量库...")
        utils.reset_vector_store()  # 避免新旧文档混淆
        vector_store = utils.build_vector_store(all_chunks)

        # 4) 构建问答链
        qa_chain = chains.build_qa_chain(vector_store)

        st.session_state.vector_store = vector_store
        st.session_state.qa_chain = qa_chain
        st.session_state.uploaded_files = [f.name for f in uploaded_files]
        st.session_state.processed = True

        progress.progress(1.0, text="✅ 处理完成！")
        st.success(
            f"已成功处理 {total} 个文档，共生成 {len(all_chunks)} 个向量块"
        )

    except Exception as e:
        logger.exception("文档处理失败")
        st.error(f"❌ 处理失败：{e}")
    finally:
        progress.empty()


def clear_chat() -> None:
    """清空当前对话历史，但保留已上传的知识库。"""
    st.session_state.messages = []
    # 重新构建链以清空 ConversationBufferMemory
    if st.session_state.vector_store is not None:
        st.session_state.qa_chain = chains.build_qa_chain(
            st.session_state.vector_store
        )
    st.toast("✅ 对话已清空", icon="🧹")


def reset_knowledge_base() -> None:
    """彻底重置：删除向量库、清空对话、释放资源。"""
    utils.reset_vector_store()
    st.session_state.messages = []
    st.session_state.vector_store = None
    st.session_state.qa_chain = None
    st.session_state.uploaded_files = []
    st.session_state.processed = False
    st.toast("✅ 知识库已重置", icon="♻️")


# ======================================================================
# 4. 主区域
# ======================================================================
def render_main() -> None:
    """渲染主区域：标题 / 上传区 / 对话区。"""
    st.title(config.APP_TITLE)
    st.caption(config.APP_DESCRIPTION)

    # ---- 文档上传区 ----
    with st.expander("📄 文档上传", expanded=not st.session_state.processed):
        uploaded_files = st.file_uploader(
            "选择 PDF 文件（可多选）",
            type=["pdf"],
            accept_multiple_files=True,
        )
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(
                "🚀 开始处理",
                type="primary",
                use_container_width=True,
                disabled=not uploaded_files,
            ):
                handle_upload(uploaded_files)
                st.rerun()
        with col2:
            if st.session_state.uploaded_files:
                st.info(
                    "📚 当前知识库：" + "、".join(st.session_state.uploaded_files)
                )

    st.divider()

    # ---- 对话区 ----
    st.subheader("💬 智能问答")

    if not st.session_state.processed:
        st.info("👆 请先上传并处理 PDF 文档，然后即可开始提问")
        return

    # 渲染历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citations_md"):
                st.markdown(msg["citations_md"])

    # 输入框
    question = st.chat_input("请输入你的问题...")
    if question:
        # 1) 显示用户消息
        st.session_state.messages.append(
            {"role": "user", "content": question, "citations_md": ""}
        )
        with st.chat_message("user"):
            st.markdown(question)

        # 2) 调用 RAG 链
        with st.chat_message("assistant"):
            with st.spinner("🤔 正在思考..."):
                try:
                    result = chains.ask(st.session_state.qa_chain, question)
                    answer = result["answer"] or "（模型未返回任何内容）"
                    citations_md = result["citations_md"]

                    st.markdown(answer)
                    if citations_md:
                        st.markdown(citations_md)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "citations_md": citations_md,
                        }
                    )
                except Exception as e:
                    logger.exception("问答失败")
                    err_msg = f"❌ 出错了：{e}"
                    st.error(err_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": err_msg, "citations_md": ""}
                    )


# ======================================================================
# 5. 程序入口
# ======================================================================
def main() -> None:
    """应用主入口函数。"""
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()
