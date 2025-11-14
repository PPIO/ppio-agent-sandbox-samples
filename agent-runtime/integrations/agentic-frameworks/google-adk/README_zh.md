# PPIO Agent Runtime - Google ADK 示例

**使用 Google Agent Development Kit 构建 AI Agent，并在几分钟内部署到 PPIO Agent Runtime。**

这个示例展示如何将一个由 Google Gemini 驱动、集成原生 Google 搜索的 AI Agent 快速部署到 PPIO Agent Runtime。

[English](README.md) | 简体中文

## 📋 目录

- [示例内容](#-示例内容)
- [快速开始](#-快速开始)
  - [准备工作](#准备工作)
  - [本地运行](#本地运行)
  - [部署到 PPIO Agent Runtime](#部署到-ppio-agent-runtime)
- [项目结构](#-项目结构)
- [Agent 能力](#-agent-能力)
- [测试](#-测试)
- [API 参考](#-api-参考)
- [常见问题](#-常见问题)
- [资源链接](#-资源链接)

## ✨ 示例内容

这个 Agent 示例包含了以下能力：

- ✅ **Google Gemini 模型** - 由 Google 最新的 Gemini 模型驱动
- ✅ **原生 Google 搜索** - 内置 Google 搜索工具集成
- ✅ **会话管理** - 内存会话服务用于保持上下文
- ✅ **简单高效** - 最小化配置，强大功能

## 🚀 快速开始

### 准备工作

开始之前，请安装以下环境：

- **Python 3.9+** 和 **Node.js 20+**
- **Google AI API 密钥** - [从 Google AI Studio 获取](https://aistudio.google.com/app/apikey)
- **PPIO API 密钥** - [在控制台获取](https://ppio.com/settings/key-management)

### 本地运行

**1. 克隆代码仓库**

```bash
git clone git@github.com:PPIO/agent-runtime-example.git
cd agent-runtime-example/integrations/agentic-frameworks/google-adk
```

**2. 创建 Python 虚拟环境**

```bash
python -m venv .venv

# macOS/Linux：
source .venv/bin/activate

# Windows：
.venv\Scripts\activate
```

**3. 安装 Python 依赖**

```bash
pip install -r requirements.txt
```

**4. 在 `.env` 中添加 API 密钥**

复制示例文件并添加密钥：

```bash
cp .env.example .env
```

编辑 `.env` 填入以下必需的值：

| 变量 | 说明 | 必需 | 获取位置 |
|------|------|------|----------|
| `GOOGLE_API_KEY` | Google AI API 密钥 | ✅ 是 | [Google AI Studio → API 密钥](https://aistudio.google.com/app/apikey) |
| `GEMINI_MODEL` | Gemini 模型名称 | 否 | 默认：`gemini-2.5-flash` |
| `PPIO_API_KEY` | PPIO API 密钥（用于部署） | 仅部署时 | [PPIO 控制台 → 密钥管理](https://ppio.com/settings/key-management) |
| `PPIO_AGENT_ID` | 部署后的 Agent ID | 仅 CLI 测试时 | 部署后从 `.ppio-agent.yaml` 获取 |

**5. 在本地启动 Agent**

```bash
python app.py
```

Agent 运行在 `http://localhost:8080`。测试一下：

```bash
bash tests/test_local_basic.sh
```

你应该看到由 Google Gemini 驱动的带有搜索功能的响应。

### 部署到 PPIO Agent Runtime

**1. 本地安装 PPIO sandbox CLI (beta)**

```bash
npm install ppio-sandbox-cli@beta

npx ppio-sandbox-cli --version
```

**2. 配置 Agent**

运行交互式配置（仅首次部署）：

```bash
npx ppio-sandbox-cli agent configure
```

CLI 会创建三个文件：
- `.ppio-agent.yaml` - Agent 元信息和配置
- `ppio.Dockerfile` - 沙箱模板 Dockerfile
- `.dockerignore` - 排除文件列表

**3. 部署到 PPIO 云端**

```bash
npx ppio-sandbox-cli agent launch
```

部署成功后，`.ppio-agent.yaml` 包含你的 Agent ID：

```yaml
status:
  phase: deployed
  agent_id: agent-xxxx  # ⭐ 调用 Agent 需要这个 ID
  last_deployed: '2025-10-23T10:35:00Z'
```

**4. 使用 CLI 测试**

调用已部署的 Agent（将 Google API 密钥作为环境变量传递）：

```bash
npx ppio-sandbox-cli agent invoke "告诉我关于 Google Gemini 的信息" --env GOOGLE_API_KEY="<your-google-api-key>"
```

CLI 会自动从 `.ppio-agent.yaml` 读取 `agent_id`。

**5. 在你的应用中使用 SDK 调用 Agent**

将 `.ppio-agent.yaml` 中的 Agent ID 保存到 `.env` 文件中：

```bash
PPIO_AGENT_ID=agent-xxxx  # 从 .ppio-agent.yaml 的 status.agent_id 复制
```

测试 SDK 调用：

```bash
python tests/test_sandbox_basic.py
```

## 📁 项目结构

```
google-adk/
├── app.py                       # Agent 程序
├── tests/                       # 所有测试文件
│   ├── test_local_basic.sh      # 本地基础测试
│   └── test_sandbox_basic.py    # 远程基础测试
├── .env.example                 # 环境变量模板
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
├── README_zh.md
└── LICENSE
```

## 🏗️ Agent 能力

这个示例 Agent 展示了 Google ADK 的核心功能：

### 🤖 Google Gemini 模型

Agent 使用 Google 的 Gemini 模型（默认：`gemini-2.0-flash`），提供：
- 快速高效的响应
- 高级推理能力
- 大型上下文窗口
- 多模态理解（适用时）

你可以通过在 `.env` 文件中设置 `GEMINI_MODEL` 来更改模型。

### 🔍 原生 Google 搜索集成

Agent 通过 `google_search` 工具内置了 Google 搜索能力。当用户提出需要最新信息的问题时，Agent 会自动：
1. 在 Google 上搜索相关信息
2. 处理搜索结果
3. 综合生成全面的回答

**示例：**
```
用户："Google Gemini 2.5 的最新功能有哪些？"
Agent：[搜索 Google 并提供最新信息]
```

### 💾 会话管理

Agent 使用内存会话服务在同一沙箱实例内维护对话上下文。会话通过请求上下文中的 `session_id` 进行标识。

## 🧪 测试

### 本地测试（开发环境）

本地测试针对运行在 `localhost:8080` 的 `app.py`。

**启动 Agent：**

```bash
python app.py
```

**在另一个终端运行测试：**

```bash
bash tests/test_local_basic.sh
```

> **Windows 用户：** 使用 Git Bash 或 WSL 运行 bash 脚本。

### 生产测试（PPIO 沙箱）

生产测试使用 SDK 调用已部署的 Agent。

**前置条件：**
- 已用 `agent launch` 命令部署 Agent
- 已在 `.env` 文件中添加 `PPIO_AGENT_ID`
- 环境中可用 `GOOGLE_API_KEY`

**运行测试：**

```bash
python tests/test_sandbox_basic.py
```

如果 Agent 配置正确，测试应该通过。

## 🔌 API 参考

### 健康检查端点

检查 Agent 是否正常运行：

```bash
GET /ping
```

**响应：**
```json
{
  "status": "healthy",
  "service": "Google ADK Agent",
  "features": ["google_search"]
}
```

### Agent 调用端点

向 Agent 发送请求：

```bash
POST /invocations
```

**请求体参数：**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `prompt` | 字符串 | ✅ 是 | - | 用户消息或问题 |
| `user_id` | 字符串 | 否 | `"user1234"` | 用户标识符 |

**请求示例：**
```json
{
  "prompt": "AI 领域的最新进展有哪些？",
  "user_id": "user123"
}
```

**响应：**
```json
{
  "result": "根据最新信息，AI 领域的最新进展包括..."
}
```

## 🔧 常见问题

### 出现"Session not found"或"app name"错误

**原因：** 会话服务配置问题。

**解决方法：** Agent 会自动回退到直接调用 Gemini API。这是正常行为，Agent 仍然可以正常工作。

### Google 搜索没有返回结果

**原因：** Google Search API 配额限制或连接问题。

**解决方法：** 
1. 检查 Google AI API 密钥是否有效
2. 验证是否有足够的 API 配额
3. 检查网络连接

### 本地运行时出现导入错误

**原因：** 依赖未安装或 Python 环境不正确。

**解决方法：** 
1. 激活虚拟环境
2. 安装依赖：`pip install -r requirements.txt`
3. 验证安装：`pip list | grep google-adk`

### Agent 响应很慢

**原因：** Google 搜索查询可能需要时间，具体取决于网络条件。

**解决方法：** 这是 Agent 需要搜索时的预期行为。对于简单查询，Agent 会直接响应而不搜索，速度会更快。

## 📚 资源链接

- [PPIO Agent Runtime 文档](https://ppio.com/docs/sandbox/agent-runtime-introduction)
- [PPIO Agent 沙箱文档](https://ppio.com/docs/sandbox/overview)
- [Google Agent Development Kit](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview)
- [Google AI Studio](https://aistudio.google.com/)

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

**需要帮助？** 提交 issue 或访问 [ppio.com](https://ppio.com) 联系支持。

