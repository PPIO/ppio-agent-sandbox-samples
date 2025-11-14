<div align="center">
  <h1>PPIO Agent Runtime 示例项目</h1>
  
  <h2>使用任何框架和模型，快速部署和运行 AI Agent</h2>
  
  <p>
    <a href="#-快速开始">快速开始</a>
    <a href="https://ppio.com/docs/sandbox/agent-runtime-introduction">文档</a>
    <a href="#-示例项目">示例项目</a>
  </p>
</div>

---

欢迎来到 PPIO Agent Runtime 示例项目仓库！

**PPIO Agent Runtime** 是一个框架无关、模型无关的轻量级 AI Agent 运行时框架，让你可以安全、快速地部署和运行 AI Agent。无论你使用 [LangGraph](https://www.langchain.com/langgraph)、[Microsoft AutoGen](https://www.microsoft.com/en-us/research/project/autogen/)、[Google ADK](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview)，还是 [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)，PPIO Agent Runtime 都能为你提供基础设施支持。通过消除构建和管理 Agent 基础设施的繁重工作，PPIO Agent Runtime 让你能够使用自己喜欢的框架和模型，只需几行代码和命令即可完成部署。

本仓库提供了示例和教程，帮助你快速理解和集成 PPIO Agent Runtime 能力到你的应用程序中。

> [!IMPORTANT]
> 本仓库中提供的示例仅用于实验和教育目的。它们演示了概念和技术，但不适合直接用于生产环境。

## 📁 仓库结构

### 🔌 [`integrations/agentic-frameworks/`](./integrations/agentic-frameworks/)
**AI Agent 框架集成**

展示如何将 PPIO Agent Runtime 与流行的 AI Agent 框架集成。每个框架示例都包含完整的实现和详细的说明文档。

**[LangGraph](./integrations/agentic-frameworks/langgraph/)**
**[AutoGen](./integrations/agentic-frameworks/autogen/)**
**[Google ADK](./integrations/agentic-frameworks/google-adk/)**
**[OpenAI Agents SDK](./integrations/agentic-frameworks/openai-agents-sdk/)**

每个示例包含：
- ✅ 完整的 Agent 实现代码
- ✅ 本地开发、测试、部署指南（位于 `README.md` 文件中）
- ✅ 完整的测试套件（本地和沙箱环境，位于 `tests` 目录下）

## 🚀 快速开始

### 前置要求

在开始之前，请确保你已经安装：

- **Python 3.9+** 和 **Node.js 20+**
- **PPIO API 密钥** - [在控制台获取](https://ppio.com/settings/key-management)

### 步骤 1：选择一个框架示例

选择你熟悉的 AI Agent 框架开始：

```bash
# 克隆仓库
git clone git@github.com:PPIO/ppio-agent-sandbox-samples.git
cd ppio-agent-sandbox-samples

# 进入你选择的框架目录
cd integrations/agentic-frameworks/langgraph  # 或 autogen、google-adk、openai-agents-sdk
```

### 步骤 2：安装依赖并配置

```bash
# 创建 Python 虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

### 步骤 3：本地测试

```bash
# 启动 Agent
python app.py

# 在另一个终端测试
bash tests/test_local_basic.sh
```

成功！你应该看到 Agent 返回的响应。

### 步骤 4：部署到 PPIO Agent Runtime

```bash
# 安装 PPIO CLI
npm install ppio-sandbox-cli@beta

# 配置和部署（自动创建所有必需的资源）
npx ppio-sandbox-cli agent configure
npx ppio-sandbox-cli agent launch

# 测试已部署的 Agent，不同项目需要传入的 --env 参数可能不同
npx ppio-sandbox-cli agent invoke "你好，Agent！" --env PPIO_API_KEY="<your-api-key>"
```

恭喜！你的 Agent 现在已经在 PPIO Agent Runtime 上运行了！

查看每个框架目录中的详细 README 文档以了解更多信息。

## 💡 功能特性

### 🔄 框架无关
使用任何 AI Agent 框架 - LangGraph、AutoGen、Google ADK、OpenAI Agents SDK 或其他框架。无需修改代码，直接部署。

### 🤖 模型无关
支持任何 LLM - OpenAI、Anthropic、Google Gemini、DeepSeek 或其他兼容模型。自由选择最适合你的模型。

### ⚡ 快速部署
使用 PPIO CLI 一键部署。自动创建所有必需的资源，从本地开发到生产环境只需几分钟。

### 🔒 安全可靠
企业级安全保障，沙箱隔离运行环境，确保 Agent 安全运行。

### 📊 完整测试
每个示例都包含完整的测试套件，涵盖基础功能、流式响应和多轮对话测试。

### 📖 详细文档
中英文双语文档，包含详细的使用说明、API 参考和故障排查指南。

## 🔗 相关资源

- [PPIO Agent Runtime 文档](https://ppio.com/docs/sandbox/agent-runtime-introduction)
- [PPIO Agent 沙箱文档](https://ppio.com/docs/sandbox/overview)

## 🤝 贡献

我们欢迎贡献！如果你想贡献代码或改进示例：

- 添加新的框架示例
- 改进现有示例
- 报告问题
- 提出改进建议

请提交 Issue 或 Pull Request。
---

