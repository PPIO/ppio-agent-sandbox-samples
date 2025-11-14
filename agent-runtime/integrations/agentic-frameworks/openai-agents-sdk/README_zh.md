# PPIO Agent Runtime - OpenAI Agents SDK 示例

**使用 OpenAI Agents SDK 构建 AI Agent，并在几分钟内部署到 PPIO Agent Runtime。**

这个示例展示如何将一个使用 OpenAI Function Calling 和多工具集成的 AI Agent 快速部署到 PPIO Agent Runtime。

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

- ✅ **OpenAI Function Calling** - 标准的 OpenAI 工具集成模式
- ✅ **多工具集成** - 时间查询、计算和天气工具
- ✅ **简洁架构** - 易于理解和扩展
- ✅ **兼容 OpenAI API** - 适用于任何兼容 OpenAI 的端点

## 🚀 快速开始

### 准备工作

开始之前，请安装以下环境：

- **Python 3.9+** 和 **Node.js 20+**
- **PPIO API 密钥** - [在控制台获取](https://ppio.com/settings/key-management)

### 本地运行

**1. 克隆代码仓库**

```bash
git clone git@github.com:PPIO/agent-runtime-example.git
cd agent-runtime-example/integrations/agentic-frameworks/openai-agents-sdk
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
| `PPIO_API_KEY` | PPIO 平台 API 密钥 | ✅ 是 | [PPIO 控制台 → 密钥管理](https://ppio.com/settings/key-management) |
| `MODEL_NAME` | 使用的模型名称 | 否 | 默认：`deepseek/deepseek-v3.1-terminus` |
| `OPENAI_API_BASE` | 兼容 OpenAI 的 API 端点 | 否 | 默认：`https://api.ppinfra.com/v3/openai` |
| `OPENAI_TIMEOUT` | API 超时时间（秒） | 否 | 默认：`60` |
| `PPIO_AGENT_ID` | 部署后的 Agent ID | 仅 CLI 测试时 | 部署后从 `.ppio-agent.yaml` 获取 |

**5. 在本地启动 Agent**

```bash
python app.py
```

Agent 运行在 `http://localhost:8080`。测试一下：

```bash
bash tests/test_local_basic.sh
```

你应该看到 Agent 使用各种工具来回答问题。

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

调用已部署的 Agent：

```bash
npx ppio-sandbox-cli agent invoke "现在几点了？" --env PPIO_API_KEY="<your-api-key>"
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
openai-agents-sdk/
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

这个示例 Agent 展示了 OpenAI Function Calling 与三个实用工具的集成：

### 🛠️ 内置工具

Agent 可以访问三个工具：

1. **get_current_time** - 获取当前 UTC 时间
   ```json
   {
     "name": "get_current_time",
     "description": "获取当前时间",
     "parameters": {
       "timezone": "UTC"
     }
   }
   ```

2. **calculate** - 执行数学计算
   ```json
   {
     "name": "calculate",
     "description": "计算数学表达式",
     "parameters": {
       "expression": "2 + 3 * 4"
     }
   }
   ```

3. **get_weather** - 查询中国城市的天气信息（演示数据）
   ```json
   {
     "name": "get_weather",
     "description": "获取城市天气",
     "parameters": {
       "city": "北京"
     }
   }
   ```

### 🔄 函数调用流程

Agent 遵循 OpenAI 标准的函数调用模式：

1. **第一次 LLM 调用** - Agent 接收用户查询和工具定义
2. **工具选择** - Agent 决定使用哪些工具（如果需要）
3. **工具执行** - 使用适当的参数执行选定的工具
4. **第二次 LLM 调用** - Agent 将工具结果综合成最终响应

这种方法确保了准确的工具使用和自然语言响应。

### 🔌 可扩展性

添加新工具非常简单：

1. 定义你的 Python 函数
2. 将函数定义添加到 `TOOLS` 列表
3. 在 `TOOL_FUNCTIONS` 字典中映射函数

Agent 会自动将新工具集成到其能力中。

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

测试套件会验证所有三个工具：
- 天气查询工具
- 信息搜索工具
- 计算工具

> **Windows 用户：** 使用 Git Bash 或 WSL 运行 bash 脚本。

### 生产测试（PPIO 沙箱）

生产测试使用 SDK 调用已部署的 Agent。

**前置条件：**
- 已用 `agent launch` 命令部署 Agent
- 已在 `.env` 文件中添加 `PPIO_AGENT_ID`

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
  "service": "OpenAI Agents SDK Runtime"
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

**请求示例：**
```json
{
  "prompt": "现在几点了？"
}
```

**响应：**
```json
{
  "result": "当前时间（UTC）：2025-11-14 10:30:45",
  "status": "success"
}
```

**使用工具的示例：**

请求：
```json
{
  "prompt": "计算 123 + 456，并告诉我北京的天气"
}
```

响应：
```json
{
  "result": "计算结果是 579。北京目前晴天，温度 15°C，空气质量良好。",
  "status": "success"
}
```

## 🔧 常见问题

### 函数调用不工作

**原因：** 模型不支持函数调用或配置问题。

**解决方法：** 
1. 验证你的模型支持函数调用（大多数现代模型都支持）
2. 检查 `tools` 参数格式是否正确
3. 确保 API 调用中设置了 `tool_choice: "auto"`

### 工具没有在预期时被调用

**原因：** 模型可能无法识别何时使用工具。

**解决方法：** 
1. 改进工具描述，使其更具体
2. 调整系统消息以鼓励工具使用
3. 尝试使用能力更强的模型

### 本地运行时出现导入错误

**原因：** 依赖未安装或 Python 环境不正确。

**解决方法：** 
1. 激活虚拟环境
2. 安装依赖：`pip install -r requirements.txt`
3. 验证安装：`pip list | grep openai`

### API 连接错误

**原因：** API 端点或 API 密钥不正确。

**解决方法：**
1. 验证 `OPENAI_API_BASE` 是否正确
2. 检查 `PPIO_API_KEY` 是否有效
3. 测试 API 连接：`curl https://api.ppinfra.com/v3/openai/models`

## 📚 资源链接

- [PPIO Agent Runtime 文档](https://ppio.com/docs/sandbox/agent-runtime-introduction)
- [PPIO Agent 沙箱文档](https://ppio.com/docs/sandbox/overview)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

**需要帮助？** 提交 issue 或访问 [ppio.com](https://ppio.com) 联系支持。

