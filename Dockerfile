# syntax=docker/dockerfile:1

# ======================================================================
# RAG 知识库问答系统 —— Dockerfile
# ======================================================================

FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（chromadb 编译 hnswlib 需要 cmake / g++）
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        cmake \
    && rm -rf /var/lib/apt/lists/*

# 优先复制依赖清单以利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目源码
COPY . .

# 创建运行时目录
RUN mkdir -p /app/data /app/vector_store

# ---- 环境变量 ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app.py"]
