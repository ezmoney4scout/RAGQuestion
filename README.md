<div align="center">

# rag-knowledge-base

**基于检索增强生成（RAG）技术的智能知识库问答系统**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://github.com/langchain-ai/langchain)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*让你的文档"开口说话"，用自然语言轻松检索海量知识* ✨

</div>

---

## 📖 项目简介

**RAG知识库问答系统** 是一个基于检索增强生成（Retrieval-Augmented Generation）技术的智能问答平台。它能够读取你上传的 PDF 文档，自动进行智能分块与向量化，并基于大语言模型实现精准的语义检索与自然语言问答。

无论你是需要快速查阅技术文档的工程师、整理研究资料的学者，还是希望从海量资料中提取关键信息的知识工作者，本系统都能成为你的得力助手。

---

## ✨ 核心功能

| 功能 | 说明 |
| :---: | :--- |
| 📄 **PDF 文档上传与解析** | 支持拖拽上传 PDF 文件，自动提取全文内容 |
| 🧩 **智能分块与向量化存储** | 采用递归分块策略，生成高质量 Embedding 存入 Chroma |
| 🔍 **自然语言问答** | 用日常口语提问，获得精准答案 |
| 📚 **引用来源展示** | 每个答案附带原文出处与页码，确保可追溯、可验证 |
| 💬 **多轮对话支持** | 保留上下文记忆，实现连续追问与深度探讨 |

---

## 🛠️ 技术栈

- **🦜 LangChain** —— 构建 RAG 管道与链式逻辑
- **🎨 Chroma** —— 轻量高效的向量数据库
- **🧠 OpenAI GPT-3.5 / GPT-4** 或 **🦙 Ollama 本地模型** —— 双模式大语言模型支持，兼顾云端与私有化部署
- **🚀 Streamlit** —— 快速构建交互式 Web 前端
- **📊 Sentence-Transformers** —— 高质量文本向量化

---

## 🎬 使用效果

### 📄 文档上传界面

```
┌─────────────────────────────────────────────┐
│  📂 拖拽或点击上传 PDF 文档                 │
│  ─────────────────────────────────────────  │
│  ✅ machine_learning.pdf  (2.3 MB)          │
│  ✅ deep_learning_book.pdf  (15.7 MB)       │
│                                              │
│  [🔄 开始向量化处理]                        │
└─────────────────────────────────────────────┘
```

### 🔍 智能问答界面

```
┌─────────────────────────────────────────────┐
│  💬 对话历史                                 │
│  ─────────────────────────────────────────  │
│  👤 用户：什么是 Transformer 架构？         │
│                                              │
│  🤖 助手：Transformer 是一种基于自注意力    │
│     机制（Self-Attention）的深度学习架构... │
│                                              │
│     📚 引用来源：                           │
│        • deep_learning_book.pdf (第 127 页) │
│        • machine_learning.pdf (第 45 页)    │
└─────────────────────────────────────────────┘
```

### 💡 问答示例

> **👤 问：** 这份文档的核心观点是什么？
>
> **🤖 答：** 根据文档内容，核心观点可以归纳为三点：(1) 注意力机制是序列建模的关键突破；(2) 自注意力可以完全取代循环与卷积结构；(3) 并行化训练显著提升了大规模模型的效率。
>
> **📚 来源：** `deep_learning_book.pdf` — 第 3 章 · 第 87-92 页

> **👤 问：** 能详细解释一下第二点吗？
>
> **🤖 答：** 当然可以。自注意力机制通过计算序列中每个位置与其他所有位置的相关性权重，能够直接建模长距离依赖关系，无需像 RNN 那样按时间步递归...
>
> **📚 来源：** `deep_learning_book.pdf` — 第 3.2 节 · 第 89 页

---

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/yourusername/rag-knowledge-base.git
cd rag-knowledge-base
```

### 2️⃣ 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 4️⃣ 配置环境变量

复制环境变量模板并填写你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 使用 OpenAI（云端）
OPENAI_API_KEY=sk-your-api-key-here
MODEL_NAME=gpt-3.5-turbo

# 或使用 Ollama（本地部署）
USE_OLLAMA=true
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

### 5️⃣ 运行应用

```bash
streamlit run app.py
```

浏览器将自动打开 `http://localhost:8501`，开启你的知识库问答之旅！🎉

---

## 📁 目录结构

```
rag-knowledge-base/
│
├── app.py              # 🚀 Streamlit 主程序（UI 入口）
├── config.py           # ⚙️  全局配置与提示词模板
├── utils.py            # 🛠️  文档解析 / 分块 / 向量存储
├── chains.py           # 🔗 RAG 问答链 / LLM 工厂 / 引用提取
│
├── requirements.txt    # 📦 Python 依赖列表
├── .env.example        # 🔐 环境变量模板
├── .gitignore          # 🚫 Git 忽略规则
│
├── CONTRIBUTING.md     # 🤝 贡献指南
├── LICENSE             # 📄 MIT 开源协议
└── README.md           # 📖 项目说明文档
```

---

## ⚙️ 配置说明

| 环境变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | OpenAI API 密钥 | — |
| `MODEL_NAME` | 使用的 LLM 模型 | `gpt-3.5-turbo` |
| `USE_OLLAMA` | 是否使用本地 Ollama 模型 | `false` |
| `OLLAMA_MODEL` | Ollama 模型名称 | `llama2` |
| `CHUNK_SIZE` | 文档分块大小 | `1000` |
| `CHUNK_OVERLAP` | 分块重叠字符数 | `200` |
| `TOP_K` | 检索返回的文档片段数 | `4` |

---

## ❓ 常见问题 FAQ

<details>
<summary><strong>Q1：填了 OpenAI API Key 还是提示报错？</strong></summary>

请依次检查：

1. Key 是否以 `sk-` 开头且未过期
2. OpenAI 账户是否仍有可用额度
3. 本地网络是否能正常访问 `api.openai.com`（国内可能需要代理）
4. `.env` 文件是否位于**项目根目录**，且文件名正确（不是 `.env.txt`）
5. 如仍报错，可尝试切换到 Ollama 本地模式

</details>

<details>
<summary><strong>Q2：支持哪些文档格式？只能上传 PDF 吗？</strong></summary>

当前版本只内置支持 **PDF**。如需扩展到 Word / Markdown / TXT / HTML，可修改 `utils.py` 中的 `parse_pdf()`，LangChain 已经提供了丰富的 Loader 可以直接替换：

- `UnstructuredWordDocumentLoader` —— Word 文档
- `TextLoader` —— TXT / Markdown
- `UnstructuredHTMLLoader` —— HTML 网页
- `CSVLoader` —— CSV 表格

</details>

<details>
<summary><strong>Q3：能处理多大的 PDF 文档？</strong></summary>

理论上没有硬性限制，但需注意：

- **内存**：大文档会占用较多内存用于向量化
- **Token 成本**：使用 OpenAI 时，文档越大 Embedding 调用费用越高
- **处理时长**：上百页文档通常需要数十秒

建议单个文档控制在 **200 页以内**以获得最佳体验，超大文档可先按章节拆分后再上传。

</details>

<details>
<summary><strong>Q4：Ollama 本地模式如何配置？</strong></summary>

1. 安装 Ollama：访问 [ollama.com](https://ollama.com) 下载并安装
2. 启动服务：`ollama serve`
3. 下载模型：

   ```bash
   ollama pull llama2            # 对话模型，也可换 qwen / mistral
   ollama pull nomic-embed-text  # Embedding 模型
   ```

4. 在 `.env` 中设置 `USE_OLLAMA=true`
5. 重启应用即可

**优点**：完全本地运行、零 API 费用、数据隐私有保障
**缺点**：推理速度依赖本地硬件，回答质量通常略低于 GPT-4

</details>

<details>
<summary><strong>Q5：向量库存在哪？换一批文档要怎么操作？</strong></summary>

向量库默认持久化在项目根目录下的 `vector_store/`。切换文档时：

- **追加新文档**：直接上传即可，新内容会加入当前知识库
- **完全替换**：点击侧边栏 **♻️ 重置知识库**，再上传新文档
- **手动清理**：直接删除 `vector_store/` 目录

</details>

<details>
<summary><strong>Q6：为什么回答不够准确？如何优化？</strong></summary>

可尝试以下调优方向：

| 问题表现 | 优化建议 |
| :--- | :--- |
| 回答笼统、缺细节 | 增大 `TOP_K`（检索更多片段） |
| 回答偏题 | 减小 `CHUNK_SIZE`（提升检索精度） |
| 上下文被截断 | 增大 `CHUNK_OVERLAP` |
| 回答胡编乱造 | 降低 `TEMPERATURE`（接近 0） |
| 专业术语理解差 | 换用更强的模型（如 GPT-4、GPT-4o） |
| 检索不准 | 更换更好的 Embedding 模型 |

</details>

<details>
<summary><strong>Q7：支持中文吗？效果怎么样？</strong></summary>

完全支持中文。系统在以下环节针对中文做了优化：

- 分块分隔符包含中文标点（`。！？`）
- 系统提示词使用中文书写
- 默认使用支持多语言的 Embedding 模型

**推荐中文场景下的模型组合：**

- **OpenAI**：`gpt-4o-mini`（性价比高）或 `gpt-4`（效果最佳）
- **Ollama**：`qwen`（阿里通义千问，对中文极其友好）

</details>

<details>
<summary><strong>Q8：如何部署到服务器/生产环境？</strong></summary>

Streamlit 支持多种部署方式：

1. **Streamlit Community Cloud**（免费）：连接 GitHub 仓库一键部署
2. **Docker**：

   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
   ```

3. **自建服务器**：使用 `systemd` 或 `supervisor` 守护进程
4. **反向代理**：前置 Nginx 处理 HTTPS 与域名绑定

> ⚠️ **生产环境警告**：请务必通过 Streamlit Secrets 或环境变量管理 API Key，**绝不要**硬编码到代码中，也不要把 `.env` 提交到 git。

</details>

<details>
<summary><strong>Q9：引用来源显示"第 0 页"或不准确怎么办？</strong></summary>

这通常是因为：

1. PDF 为**扫描版**（图片格式），`pdfplumber` 无法提取文字 → 需要 OCR 预处理
2. PDF 内嵌特殊字体，提取失败 → 尝试用 `pypdf` 或 `PyMuPDF` 替代
3. 分块跨页，元数据丢失 → 增大 `CHUNK_SIZE` 以减少跨页

</details>

<details>
<summary><strong>Q10：能离线使用吗？</strong></summary>

可以！使用 **Ollama 本地模式** + 本地 Embedding 模型（如 `nomic-embed-text` 或 `sentence-transformers`），整个系统可以完全离线运行，适合涉密文档或无网络环境。

</details>

---

## 🤝 贡献指南

我们非常欢迎任何形式的贡献 —— 无论是报告 Bug、提出新功能、完善文档还是提交代码。

**快速开始：**

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

详细的开发流程、代码规范、Commit 规范与 PR 要求请参见 **[CONTRIBUTING.md](CONTRIBUTING.md)**。

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源协议发布。

---

## 🙏 致谢

感谢以下优秀的开源项目：

- [LangChain](https://github.com/langchain-ai/langchain) —— 强大的 LLM 应用开发框架
- [Chroma](https://github.com/chroma-core/chroma) —— 开源向量数据库
- [Streamlit](https://github.com/streamlit/streamlit) —— 快速构建数据应用
- [Ollama](https://github.com/ollama/ollama) —— 本地大模型运行工具

---

<div align="center">

**⭐ 如果这个项目对你有帮助，欢迎点个 Star 支持一下！⭐**

Made with ❤️ by Scott Lu

</div>
