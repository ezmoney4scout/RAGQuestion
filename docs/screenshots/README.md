# 📸 界面截图目录

本目录用于存放项目的界面截图，供 README 与文档展示使用。

## 📋 需要的截图清单

请将以下截图放入本目录（可先用占位图）：

| 文件名 | 内容 | 建议尺寸 |
| :--- | :--- | :--- |
| `home.png` | 应用主界面（首次打开） | 1920×1080 |
| `upload.png` | PDF 文档上传界面 | 1920×1080 |
| `processing.png` | 文档向量化进度展示 | 1920×1080 |
| `chat.png` | 多轮智能问答对话 | 1920×1080 |
| `citation.png` | 引用来源展示效果 | 1920×1080 |
| `sidebar.png` | 侧边栏参数设置 | 1920×1080 |
| `demo.gif` | 完整使用流程动图 | ≤ 10 MB |

## 🎨 截图建议

- 📐 **统一尺寸**：保持所有截图宽高比一致，推荐 16:9
- 🌓 **主题**：建议同时提供浅色 / 深色主题版本，文件名加 `-light` / `-dark` 后缀
- 🖼️ **格式选择**：
  - 静态图：优先 **PNG**（无损、支持透明）
  - 动图：**GIF** 或 **WebP**（控制在 10MB 以内）
- 🔍 **清晰度**：使用 2x 分辨率截图（Retina）
- 🔐 **脱敏处理**：
  - 打码 API Key、个人邮箱、token 等敏感信息
  - 使用示例文档（如公开论文）而非真实业务文档
- ✂️ **裁剪**：去除浏览器地址栏、任务栏等无关元素

## 📝 在 README 中引用

```markdown
![主界面](docs/screenshots/home.png)

<p align="center">
  <img src="docs/screenshots/chat.png" alt="智能问答" width="800"/>
</p>
```

## 🛠️ 推荐截图工具

| 平台 | 工具 |
| :--- | :--- |
| macOS | `Cmd+Shift+4`、[CleanShot X](https://cleanshot.com/)、[Shottr](https://shottr.cc/) |
| Windows | `Win+Shift+S`、[ShareX](https://getsharex.com/)、[Snagit](https://www.techsmith.com/snagit.html) |
| Linux | [Flameshot](https://flameshot.org/)、[Shutter](https://shutter-project.org/) |
| 跨平台 | [Kap](https://getkap.co/)（录屏 GIF）、[LICEcap](https://www.cockos.com/licecap/) |

## 📦 图片优化

提交前建议压缩图片以减小仓库体积：

```bash
# PNG 压缩（无损）
pngquant --quality=80-95 --ext .png --force *.png

# GIF 压缩
gifsicle -O3 --lossy=80 input.gif -o output.gif
```
