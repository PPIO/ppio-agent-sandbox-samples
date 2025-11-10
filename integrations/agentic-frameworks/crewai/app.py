"""
CrewAI Agent 示例项目

这个示例展示如何使用 CrewAI 构建多 Agent 协作系统，
并集成到 PPIO Agent Runtime 中。

功能：
- 多个 AI Agent 协同工作
- 研究员 + 分析师协作模式
- 完整集成 PPIO Agent Runtime
"""

from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv
load_dotenv()
import os

llm = LLM(
  model=os.getenv("MODEL_NAME", "deepseek/deepseek-v3.1-terminus"),
  api_key=os.getenv("PPIO_API_KEY"),
  base_url="https://api.ppinfra.com/v3/openai",
  temperature=0.7,
)

# 导入 PPIO Agent Runtime
from ppio_sandbox.agent_runtime import AgentRuntimeApp

app = AgentRuntimeApp()

# 定义工具
@tool("搜索工具")
def search_tool(query: str) -> str:
    """
    搜索相关信息
    
    Args:
        query: 搜索查询字符串
        
    Returns:
        搜索结果
    """
    # 模拟搜索结果
    return f"""
    关于 '{query}' 的搜索结果：
    
    1. {query} 是一个重要的主题，在当前技术领域中得到广泛应用。
    2. 最新研究表明，{query} 的发展前景广阔。
    3. 业界专家认为，{query} 将在未来 3-5 年内迎来重大突破。
    
    数据来源：模拟搜索引擎（示例数据）
    """


@tool("数据分析工具")
def analyze_tool(data: str) -> str:
    """
    分析数据并提供洞察
    
    Args:
        data: 需要分析的数据
        
    Returns:
        分析结果
    """
    return f"""
    数据分析结果：
    
    📊 关键发现：
    - 趋势分析：数据显示持续增长态势
    - 相关性：发现多个关键因素之间的强相关性
    - 预测：基于当前数据，未来发展趋势乐观
    
    💡 建议：
    - 建议关注相关领域的最新发展
    - 可以考虑进一步深入研究
    """


# 定义研究员 Agent
def create_researcher():
    """创建研究员 Agent"""
    return Agent(
        llm=llm,
        role="高级研究专员",
        goal="查找关于主题的全面准确信息",
        backstory="""你是一位经验丰富的研究专员，拥有 10 年的行业研究经验。
        你擅长从各种渠道找到相关信息，并能快速识别关键要点。
        你的研究报告总是全面、准确、有深度。""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
    )


# 定义分析师 Agent
def create_analyst():
    """创建分析师 Agent"""
    return Agent(
        llm=llm,
        role="资深数据分析师",
        goal="分析研究结果并提供有价值的洞察",
        backstory="""你是一位资深数据分析师，拥有统计学和商业分析背景。
        你擅长从数据中提取有价值的见解，并能提供切实可行的建议。
        你的分析报告总是逻辑清晰、见解深刻。""",
        verbose=True,
        allow_delegation=False,
        tools=[analyze_tool],
    )


# 定义撰写员 Agent
def create_writer():
    """创建撰写员 Agent"""
    return Agent(
        llm=llm,
        role="专业内容撰写员",
        goal="撰写清晰、专业的最终报告",
        backstory="""你是一位专业的内容撰写员，擅长将复杂的信息转化为易懂的文字。
        你的写作风格清晰、简洁、有条理，深受读者喜爱。""",
        verbose=True,
        allow_delegation=False,
    )


# 创建 Crew
def create_crew():
    """创建并配置 CrewAI Crew"""
    # 创建 Agents
    researcher = create_researcher()
    analyst = create_analyst()
    writer = create_writer()
    
    # 创建研究任务
    research_task = Task(
        description="""
        研究主题：{topic}
        
        请进行全面的研究，包括：
        1. 主题的基本概念和定义
        2. 当前的发展状态
        3. 主要的应用场景
        4. 未来的发展趋势
        
        使用搜索工具获取相关信息。
        """,
        agent=researcher,
        expected_output="包含关键信息和数据的详细研究报告"
    )
    
    # 创建分析任务
    analysis_task = Task(
        description="""
        基于研究员提供的研究报告，进行深入分析：
        
        1. 分析关键趋势和模式
        2. 识别机会和挑战
        3. 提供数据支持的洞察
        4. 给出可行的建议
        
        使用数据分析工具处理数据。
        """,
        agent=analyst,
        expected_output="包含数据分析、洞察和建议的分析报告"
    )
    
    # 创建撰写任务
    writing_task = Task(
        description="""
        基于研究报告和分析报告，撰写最终的综合报告：
        
        1. 整合研究和分析结果
        2. 使用清晰的结构组织内容
        3. 突出关键发现和建议
        4. 确保报告专业、易读
        
        报告应包含：
        - 执行摘要
        - 详细分析
        - 结论和建议
        """,
        agent=writer,
        expected_output="结构清晰、内容全面的最终报告"
    )
    
    # 创建 Crew
    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=True
    )


# 初始化 Crew
crew = create_crew()


# 定义 PPIO Agent Runtime 入口点
@app.entrypoint
def agent_invocation(request: dict) -> dict:
    """
    CrewAI Agent 入口点
    
    Args:
        request: 请求数据，包含以下字段：
            - prompt: 用户输入的研究主题
            
    Returns:
        响应数据字典，包含 result 字段
    """
    prompt = request.get("prompt", "人工智能的未来发展")
    
    print(f"📨 收到研究请求: {prompt}")
    print("👥 启动多 Agent 协作...")
    
    try:
        # 运行 Crew
        result = crew.kickoff(inputs={"topic": prompt})
        
        print("✅ 多 Agent 协作完成！")
        
        return {
            "result": result.raw,
            "status": "success"
        }
        
    except Exception as e:
        error_msg = f"处理请求时出错: {str(e)}"
        print(f"❌ 错误: {error_msg}")
        return {
            "result": error_msg,
            "status": "error"
        }


if __name__ == "__main__":
    print("🚀 启动 CrewAI Agent Runtime...")
    print("👥 Agent 团队: 研究员 → 分析师 → 撰写员")
    print("🔗 监听端口: 8080")
    app.run()

