# 📝 Changelog

本文档记录项目的所有重要变更。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### 计划中

- 支持 Word / Markdown / TXT / HTML 文档
- 支持扫描版 PDF 的 OCR 预处理
- 导出对话历史为 Markdown / PDF
- 多知识库隔离与切换
- 用户认证与权限管理
- 流式输出（Streaming）响应

---

## [1.0.0] - 2026-04-11

### ✨ 新增

- 🎉 首个正式版本发布
- 📄 **PDF 文档解析**：基于 `pdfplumber` 按页提取文本，保留页码元数据
- 🧩 **智能分块**：`RecursiveCharacterTextSplitter` + 中文友好分隔符策略
- 🗄️ **向量存储**：基于 `Chroma` 的持久化向量库，支持构建/加载/重置
- 🔍 **语义检索**：基于相似度的 Top-K 检索
- 💬 **多轮对话**：`ConversationBufferMemory` 支持上下文记忆
- 📚 **引用展示**：自动提取并展示来源文件与页码
- 🔄 **双模型模式**：
  - OpenAI：`gpt-3.5-turbo` / `gpt-4` / `gpt-4o-mini`
  - Ollama：本地 `llama2` / `qwen` / `mistral` 等
- 🎨 **Streamlit UI**：
  - 侧边栏实时调节分块大小、Top-K、温度等参数
  - 主区域拖拽上传、进度条、聊天气泡
  - 清空对话 / 重置知识库按钮
- 🐳 **Docker 支持**：多阶段构建的 Dockerfile + docker-compose
- ⚙️ **完整配置**：`.env.example` + `.streamlit/config.toml`
- 📖 **中文文档**：README + CONTRIBUTING + FAQ 全中文

### 🛠️ 技术栈

- `langchain` 0.1.x
- `langchain-openai` / `langchain-ollama`
- `chromadb` 0.4.x
- `pdfplumber` 0.10.x
- `streamlit` 1.30+

---

[Unreleased]: https://github.com/your-username/rag-knowledge-base/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/your-username/rag-knowledge-base/releases/tag/v1.0.0
