# 🔒 安全策略

## 支持的版本

我们为以下版本提供安全更新：

| 版本 | 是否支持 |
| :--- | :---: |
| 1.0.x | ✅ |
| < 1.0 | ❌ |

---

## 🚨 报告漏洞

如果你发现了安全漏洞，请**不要**通过公开的 Issue 报告。

请通过以下**任一**私密渠道联系我们：

- 📧 **邮箱**：security@example.com
- 🔐 **GitHub Security Advisory**（推荐）：[创建私密安全建议](../../security/advisories/new)

### 响应时间承诺

- ⏱️ **48 小时**内回复确认收到
- 📋 **7 天**内提供初步评估与修复计划
- 🛠️ 确认为真实漏洞后，我们会：
  1. 在私密分支修复
  2. 发布补丁版本
  3. 发布安全公告并致谢报告者（除非你希望匿名）

---

## 🛡️ 安全最佳实践

使用本项目时，请遵循以下安全建议：

### 🔐 API Key 管理

- ❌ **不要**将 API Key 硬编码到源代码中
- ❌ **不要**将 `.env` 文件提交到 git 仓库
- ✅ 生产环境请使用环境变量或专业密钥管理服务：
  - AWS Secrets Manager
  - HashiCorp Vault
  - Azure Key Vault
  - GCP Secret Manager
- ✅ 定期轮换 API Key
- ✅ 为不同环境（开发/测试/生产）使用独立的 Key
- ✅ 监控 API Key 的使用情况，发现异常立即吊销

### 📄 文档隐私

- 🔒 **涉密文档**强烈建议使用 **Ollama 本地模式**，避免数据外传
- ⚠️ 使用 OpenAI 模式前，请确认其 [数据使用政策](https://openai.com/policies/api-data-usage-policies)
- 📦 向量库 `vector_store/` 包含文档内容的 Embedding，请妥善保管
- 🗑️ 处理完敏感文档后及时调用「重置知识库」清理

### 🌐 网络安全

- ✅ 生产部署务必启用 **HTTPS**
- ✅ 使用反向代理（Nginx / Caddy / Traefik）前置保护
- ✅ 限制 Streamlit 服务的网络暴露范围（不要直接暴露 8501 到公网）
- ✅ 启用 Streamlit 的 XSRF 保护（默认已开启）
- ✅ 考虑前置 WAF（如 Cloudflare）防御常见攻击
- ✅ 实施访问控制（Basic Auth / OAuth / SSO）

### 📦 依赖安全

- ✅ 定期运行 `pip-audit` 检查依赖漏洞：
  ```bash
  pip install pip-audit
  pip-audit
  ```
- ✅ 关注 GitHub [Dependabot](../../security/dependabot) 告警
- ✅ 锁定依赖版本以防止供应链攻击
- ✅ 使用 `pip-compile` 生成可复现的依赖清单

### 🐳 容器安全

- ✅ 使用项目提供的 Dockerfile（已使用非 root 用户）
- ✅ 定期更新基础镜像
- ✅ 扫描镜像漏洞：`docker scout cves` 或 `trivy`
- ✅ 最小化暴露的端口与挂载卷

---

## 🏆 致谢

感谢所有负责任地报告安全漏洞的研究人员！你们的贡献让本项目与所有用户更加安全。

已报告漏洞的研究人员将被列入本页（除非希望匿名）。
