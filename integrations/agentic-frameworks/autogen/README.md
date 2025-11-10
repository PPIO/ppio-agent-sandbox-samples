# Microsoft AutoGen Agent 示例项目

这个示例展示如何使用 Microsoft AutoGen 构建多 Agent 对话系统，并集成到 PPIO Agent Runtime 中。

## 功能特性

- ✅ 使用 AutoGen 构建对话式 Agent
- ✅ 支持工具调用和反思（reflect_on_tool_use）
- ✅ 支持流式输出
- ✅ 完整集成 PPIO Agent Runtime

## 可用工具

### 1. get_weather
获取指定城市的天气信息

### 2. search_information
搜索相关信息（可接入真实搜索 API）

### 3. calculate
计算数学表达式

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
OPENAI_API_KEY=your-openai-api-key
MODEL_NAME=gpt-4o-mini
```

### 3. 本地测试

```bash
python app.py
```

测试示例：

```bash
# 查询天气
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "深圳今天天气怎么样？"}'

# 搜索信息
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "搜索一下量子计算的最新进展"}'

# 计算
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "帮我算一下 (123 + 456) * 789"}'
```

### 4. 部署到 PPIO

```bash
npx ppio-sandbox-cli agent configure
npx ppio-sandbox-cli agent launch
npx ppio-sandbox-cli agent invoke "北京的天气如何？"
```

## AutoGen 特性

### 工具反思（Reflect on Tool Use）

AutoGen 支持 Agent 在使用工具后进行反思，提高响应质量：

```python
agent = AssistantAgent(
    name="助手",
    model_client=model_client,
    tools=[your_tools],
    reflect_on_tool_use=True,  # 启用工具使用反思
)
```

### 流式输出

支持流式输出，提供更好的用户体验：

```python
result = await Console(agent.run_stream(task=prompt))
```

## 自定义配置

### 添加新工具

```python
async def your_tool(param: str) -> str:
    """工具描述"""
    return "工具结果"

# 添加到工具列表
tools = [get_weather, search_information, calculate, your_tool]
```

### 自定义系统消息

```python
agent = AssistantAgent(
    name="助手",
    system_message="你的自定义系统消息",
    tools=[your_tools]
)
```

## 相关资源

- [Microsoft AutoGen 文档](https://microsoft.github.io/autogen/)
- [PPIO Agent Runtime 文档](https://docs.ppio.cloud/sandbox/agent-runtime-introduction)

