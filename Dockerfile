# syntax=docker/dockerfile:1

# ======================================================================
# RAG 知识库问答系统 —— Dockerfile
# 使用多阶段构建以减小最终镜像体积
# ======================================================================

# ==================== 构建阶段 ====================
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# 优先复制依赖清单以利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ==================== 运行阶段 ====================
FROM python:3.11-slim

# 创建非 root 用户以提升安全性
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# 从构建阶段复制已安装的 Python 依赖
COPY --from=builder /root/.local /home/app/.local

# 复制项目源码
COPY --chown=app:app . .

# 创建运行时目录并授权
RUN mkdir -p /app/data /app/vector_store \
    && chown -R app:app /app

USER app

# ---- 环境变量 ----
ENV PATH=/home/app/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501

# 健康检查：调用 Streamlit 内建的 /_stcore/health 端点
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app.py"]
