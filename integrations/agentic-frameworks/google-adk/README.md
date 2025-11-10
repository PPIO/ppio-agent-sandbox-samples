# Google ADK Agent 示例项目

这个示例展示如何使用 Google Agent Development Kit (ADK) 和 Gemini 模型构建 Agent，并集成到 PPIO Agent Runtime 中。

## 功能特性

- ✅ 使用 Google Gemini 模型
- ✅ 支持会话管理（带降级方案）
- ✅ 支持 Google Search 工具
- ✅ 完整集成 PPIO Agent Runtime
- ✅ 自动降级到直接 API 调用

## 支持的模型

- `gemini-2.0-flash-exp` - 最新的 Gemini Flash 模型（推荐）
- `gemini-1.5-pro` - Gemini Pro 模型
- `gemini-1.5-flash` - Gemini Flash 模型

## 快速开始

### 1. 获取 Google API Key

访问 [Google AI Studio](https://makersuite.google.com/app/apikey) 获取 API Key。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
GOOGLE_API_KEY=your-google-api-key
GEMINI_MODEL=gemini-2.0-flash-exp
```

### 4. 本地测试

```bash
python app.py
```

测试示例：

```bash
# 基本对话
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好！请介绍一下 Google Gemini"}'

# 查询天气
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "北京今天天气怎么样？"}'

# 搜索信息
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "搜索一下量子计算的应用"}'
```

### 5. 部署到 PPIO

```bash
npx ppio-sandbox-cli agent configure
npx ppio-sandbox-cli agent launch
npx ppio-sandbox-cli agent invoke "介绍一下 Google Gemini 模型"
```

## 会话管理

Google ADK 支持会话管理，可以保持多轮对话的上下文：

```python
# 在请求中传递 session_id
{
    "prompt": "继续上次的话题",
    "user_id": "user123",
    "session_id": "session-456"
}
```

## 自定义配置

### 更改模型

在 `.env` 中设置：

```bash
GEMINI_MODEL=gemini-1.5-pro  # 使用 Pro 模型
```

### 自定义系统指令

在代码中修改：

```python
model = GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction="你的自定义系统指令"
)
```

## 注意事项

1. **API 配额**：Google AI Studio 提供免费配额，请注意使用限制
2. **模型选择**：Flash 模型速度更快，Pro 模型能力更强
3. **会话管理**：建议为每个用户对话使用唯一的 session_id

## 相关资源

- [Google AI Studio](https://makersuite.google.com/)
- [Google Generative AI 文档](https://ai.google.dev/docs)
- [PPIO Agent Runtime 文档](https://docs.ppio.cloud/sandbox/agent-runtime-introduction)

