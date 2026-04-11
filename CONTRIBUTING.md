# 🤝 贡献指南

首先，感谢你愿意为 **RAG 知识库问答系统** 做出贡献！❤️

本项目欢迎任何形式的参与 —— 无论你是第一次提交 PR 的新手，还是经验丰富的开发者，我们都期待与你合作。

---

## 📋 目录

- [你可以如何贡献](#-你可以如何贡献)
- [报告 Bug](#-报告-bug)
- [提出新功能](#-提出新功能)
- [提交代码](#-提交代码)
- [代码规范](#-代码规范)
- [Commit 规范](#-commit-规范)
- [Pull Request 要求](#-pull-request-要求)
- [行为准则](#-行为准则)

---

## 🎯 你可以如何贡献

- 🐛 **报告 Bug**：发现问题时提交 Issue
- 💡 **提出新功能**：分享你的想法
- 📝 **完善文档**：修正错别字、补充示例、翻译
- 🔧 **提交代码**：修复 Bug 或实现新功能
- 🧪 **编写测试**：提升项目稳定性
- 🌍 **本地化**：将界面与文档翻译为其他语言
- ⭐ **推广项目**：给项目点 Star、在社交媒体分享

---

## 🐛 报告 Bug

提交 Bug 前，请先：

1. 在 [Issues](../../issues) 中搜索，确认该问题尚未被报告
2. 确认使用的是最新版本
3. 能够稳定复现问题

### Bug 报告模板

```markdown
**描述**
简明扼要地描述 Bug。

**复现步骤**
1. 进入 '...'
2. 点击 '....'
3. 看到错误 '....'

**期望行为**
描述你期望发生什么。

**实际行为**
描述实际发生了什么（附截图/日志）。

**环境信息**
- 操作系统: [例如 macOS 14.2]
- Python 版本: [例如 3.11.5]
- 关键依赖版本: [streamlit==1.30.0, langchain==0.1.16]
- LLM 模式: [OpenAI / Ollama]

**补充信息**
其他有助于定位问题的信息。
```

---

## 💡 提出新功能

在 [Issues](../../issues) 创建 **Feature Request**，请包含：

- **问题场景**：你希望解决什么问题？
- **建议方案**：你理想中的实现方式
- **替代方案**：你考虑过的其他方案
- **参考资料**：相关文档、论文、其他项目的类似实现

---

## 🔧 提交代码

### 开发流程

1. **Fork 本仓库**，并 clone 到本地：

   ```bash
   git clone https://github.com/your-username/rag-knowledge-base.git
   cd rag-knowledge-base
   ```

2. **创建新分支**：

   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **配置开发环境**：

   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux / macOS
   venv\Scripts\activate          # Windows

   pip install -r requirements.txt
   cp .env.example .env           # 然后填入你的 API Key
   ```

4. **进行你的修改**，确保应用可以正常运行：

   ```bash
   streamlit run app.py
   ```

5. **提交修改**：

   ```bash
   git add .
   git commit -m "feat: 添加 XXX 功能"
   ```

6. **Push 到你的 Fork**：

   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**，等待 Review

---

## 📏 代码规范

### Python 风格

- **命名约定**
  - 变量 / 函数：`snake_case`
  - 类：`PascalCase`
  - 常量：`UPPER_SNAKE_CASE`
  - 私有成员：`_leading_underscore`

- **注释**：关键逻辑必须有**中文注释**，说明「为什么这么做」而非「做了什么」

- **Docstring**：所有公共函数/类必须有 docstring，推荐 Google 风格：

  ```python
  def parse_pdf(file_path: str) -> List[Document]:
      """
      解析 PDF 文件并返回 Document 列表。

      Args:
          file_path: PDF 文件的绝对路径。

      Returns:
          按页切分的 Document 列表，metadata 包含 source 与 page。

      Raises:
          FileNotFoundError: 文件不存在时抛出。
          ValueError: PDF 内容为空时抛出。
      """
  ```

- **类型标注**：尽量为函数签名添加 Type Hints

- **错误处理**：所有外部调用（文件 IO、API 请求、数据库操作）必须有 `try/except`，并记录日志

- **日志**：统一使用 `logging` 模块，**禁止**使用 `print`

- **行长度**：建议不超过 100 字符

### 推荐工具

```bash
# 代码格式化
pip install black
black .

# 静态检查
pip install ruff
ruff check .

# 类型检查
pip install mypy
mypy .
```

---

## 📝 Commit 规范

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 规范：

```
<类型>(<可选作用域>): <简短描述>

<可选正文>

<可选脚注>
```

### 类型（type）

| 类型 | 说明 | 示例 |
| :--- | :--- | :--- |
| `feat` | 新功能 | `feat: 支持 Word 文档上传` |
| `fix` | Bug 修复 | `fix: 修复中文分块异常` |
| `docs` | 文档变更 | `docs: 完善 FAQ 章节` |
| `style` | 代码格式（不影响功能） | `style: 统一缩进为 4 空格` |
| `refactor` | 重构（非新功能非 Bug） | `refactor: 提取向量库工厂函数` |
| `perf` | 性能优化 | `perf: 批量向量化提速 3x` |
| `test` | 测试相关 | `test: 为 parse_pdf 添加单元测试` |
| `chore` | 构建/工具链变更 | `chore: 升级 langchain 至 0.1.20` |
| `ci` | CI/CD 配置 | `ci: 添加 GitHub Actions 自动测试` |

### 示例

```
feat(chains): 支持多轮对话上下文记忆

使用 ConversationBufferMemory 保留历史消息，
让模型能够理解"它"、"这个"等指代关系。

Closes #42
```

---

## ✅ Pull Request 要求

### 提交前检查清单

- [ ] 代码可以正常运行，无报错
- [ ] 新增功能有对应的 docstring 与注释
- [ ] 修改未破坏现有功能
- [ ] 遵循代码规范（建议用 `black` 格式化）
- [ ] Commit 信息符合规范
- [ ] 如涉及 UI 变更，提供截图
- [ ] 如涉及新依赖，已更新 `requirements.txt`
- [ ] 如涉及配置项变更，已更新 `.env.example` 与 `README.md`

### PR 描述模板

```markdown
## 变更内容
简要描述本次 PR 做了什么。

## 变更原因
说明为什么需要这个变更。

## 关联 Issue
Closes #123

## 测试情况
- [ ] 本地运行通过
- [ ] 已测试 OpenAI 模式
- [ ] 已测试 Ollama 模式
- [ ] 已更新/添加测试

## 截图（如适用）
附上界面截图或对比图。

## 备注
其他需要 Reviewer 关注的内容。
```

### Review 流程

1. 至少 1 名 Maintainer Review 通过
2. 所有讨论已解决
3. CI 检查通过
4. 合并到 `main` 分支（使用 Squash Merge）

---

## 🤝 行为准则

为营造开放、友善的社区环境，请遵守以下准则：

- 🤗 **尊重他人**：尊重每一位贡献者，不论其经验水平、性别、国籍、信仰
- 💬 **友善沟通**：使用礼貌的语言，避免攻击性言论
- 🎯 **就事论事**：讨论代码与方案，不对人进行评判
- 🙌 **乐于助人**：对新手保持耐心，欢迎提问
- 📚 **建设性反馈**：批评要具体，建议要可操作
- ❌ **零容忍**：骚扰、歧视、人身攻击等行为将被永久禁止参与

---

## 📬 联系方式

- 💬 **讨论与提问**：[GitHub Issues](../../issues)
- 🐛 **Bug 报告**：[GitHub Issues](../../issues/new?labels=bug)
- 💡 **功能建议**：[GitHub Issues](../../issues/new?labels=enhancement)
- 📧 **紧急联系**：maintainer@example.com

---

<div align="center">

**再次感谢你的贡献！每一个 PR、每一个 Issue、每一颗 Star 都是对项目的支持 ❤️**

</div>
