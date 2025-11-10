# OpenAI Agents SDK 示例项目

这个示例展示如何使用 OpenAI 的 Function Calling 功能构建简单高效的 Agent，并集成到 PPIO Agent Runtime 中。

## 功能特性

- ✅ 使用 OpenAI Function Calling
- ✅ 支持多个工具函数（时间、计算、天气）
- ✅ 完整集成 PPIO Agent Runtime
- ✅ 异步执行支持

## 可用工具

### 1. get_current_time
获取当前时间（UTC）

### 2. calculate
计算数学表达式
- 示例：`calculate("2 + 3 * 4")`

### 3. get_weather
获取城市天气信息
- 支持城市：北京、上海、深圳、广州

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
# 查询时间
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "现在几点了？"}'

# 计算
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "帮我算一下 123 * 456"}'

# 查询天气
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "北京今天天气怎么样？"}'
```

### 4. 部署到 PPIO

```bash
npx ppio-sandbox-cli agent configure
npx ppio-sandbox-cli agent launch
npx ppio-sandbox-cli agent invoke "上海的天气如何？"
```

## 添加自定义工具

### 1. 定义工具函数

```python
def your_tool(param: str) -> str:
    """工具描述"""
    return "工具返回结果"
```

### 2. 添加工具定义

```python
TOOLS.append({
    "type": "function",
    "function": {
        "name": "your_tool",
        "description": "工具描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param": {
                    "type": "string",
                    "description": "参数描述"
                }
            },
            "required": ["param"]
        }
    }
})
```

### 3. 注册到函数映射

```python
TOOL_FUNCTIONS["your_tool"] = your_tool
```

## 相关资源

- [OpenAI Function Calling 文档](https://platform.openai.com/docs/guides/function-calling)
- [PPIO Agent Runtime 文档](https://docs.ppio.cloud/sandbox/agent-runtime-introduction)

