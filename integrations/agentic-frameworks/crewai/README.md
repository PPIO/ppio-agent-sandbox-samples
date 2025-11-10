# CrewAI 多 Agent 协作示例项目

这个示例展示如何使用 CrewAI 构建多 Agent 协作系统，并集成到 PPIO Agent Runtime 中。

## 功能特性

- ✅ 多个 AI Agent 协同工作
- ✅ 研究员 → 分析师 → 撰写员工作流
- ✅ 完整集成 PPIO Agent Runtime
- ✅ 支持自定义工具

## Agent 团队

### 1. 研究员（Researcher）
- 负责搜集和整理信息
- 使用搜索工具查找相关资料
- 输出详细的研究报告

### 2. 分析师（Analyst）
- 分析研究员的报告
- 使用数据分析工具提取洞察
- 提供可行的建议

### 3. 撰写员（Writer）
- 整合研究和分析结果
- 撰写结构清晰的最终报告
- 确保内容专业易读

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
OPENAI_API_KEY=your-openai-api-key
```

### 3. 本地测试

```bash
python app.py
```

在另一个终端测试：

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "人工智能在医疗领域的应用"}'
```

### 4. 部署到 PPIO

```bash
# 配置 Agent
npx ppio-sandbox-cli agent configure

# 部署 Agent
npx ppio-sandbox-cli agent launch

# 测试调用
npx ppio-sandbox-cli agent invoke "区块链技术的最新发展趋势"
```

## 工作流程

```
用户输入
   ↓
研究员（搜索工具）→ 研究报告
   ↓
分析师（分析工具）→ 分析报告
   ↓
撰写员 → 最终报告
   ↓
返回给用户
```

## 自定义 Agent

### 添加新 Agent

```python
def create_your_agent():
    return Agent(
        role="角色名称",
        goal="Agent 目标",
        backstory="背景故事",
        tools=[your_tools],
        verbose=True
    )
```

### 添加新任务

```python
your_task = Task(
    description="任务描述：{topic}",
    agent=your_agent,
    expected_output="期望输出"
)
```

## 相关资源

- [CrewAI 文档](https://docs.crewai.com/)
- [PPIO Agent Runtime 文档](https://docs.ppio.cloud/sandbox/agent-runtime-introduction)

