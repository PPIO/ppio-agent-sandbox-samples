# Strands Agents 示例项目

这个示例展示如何使用 Strands Agents 轻量级框架构建 Agent，并集成到 PPIO Agent Runtime 中。

## 功能特性

- ✅ 轻量级 Agent 框架
- ✅ 支持文件操作工具
- ✅ 易于扩展和定制
- ✅ 完整集成 PPIO Agent Runtime

## 可用工具

### 1. file_read
读取文件内容
- 参数：`filepath` - 文件路径

### 2. file_write
写入文件
- 参数：`filepath` - 文件路径，`content` - 文件内容

### 3. editor
编辑文件（替换文本）
- 参数：`filepath` - 文件路径，`old_text` - 要替换的文本，`new_text` - 新文本

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
MODEL_NAME=gpt-4
# 如果使用 OpenAI
OPENAI_API_KEY=your-openai-api-key
```

### 3. 本地测试

```bash
python app.py
```

测试示例：

```bash
# 基本对话
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好！你能帮我做什么？"}'

# 文件操作
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "帮我创建一个文件"}'
```

### 4. 部署到 PPIO

```bash
npx ppio-sandbox-cli agent configure
npx ppio-sandbox-cli agent launch
npx ppio-sandbox-cli agent invoke "你好，请介绍一下你的功能"
```

## 扩展 Agent

### 添加新工具

```python
def your_tool(param: str) -> str:
    """工具描述"""
    # 工具逻辑
    return "工具结果"

# 添加到 Agent
agent = SimpleAgent(
    tools=[file_read, file_write, editor, your_tool],
    model="gpt-4"
)
```

### 自定义系统提示

```python
agent = SimpleAgent(
    tools=[your_tools],
    system_prompt="你的自定义系统提示"
)
```

## 为什么选择 Strands Agents？

1. **轻量级**：最小依赖，快速启动
2. **简单易用**：API 简洁，易于理解
3. **灵活**：容易定制和扩展
4. **高效**：适合快速原型开发

## 注意事项

- 本示例使用简化的 Agent 实现
- 生产环境建议使用完整的 Strands Agents 库
- 文件操作工具仅作为示例，实际使用时需要添加安全检查

## 相关资源

- [PPIO Agent Runtime 文档](https://docs.ppio.cloud/sandbox/agent-runtime-introduction)
- [快速开始指南](https://docs.ppio.cloud/sandbox/agent-runtime-quick-start)

