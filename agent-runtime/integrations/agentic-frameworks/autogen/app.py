"""
Microsoft AutoGen Agent 示例项目

这个示例展示如何使用 Microsoft AutoGen 构建多 Agent 对话系统，
并集成到 PPIO Agent Runtime 中。

功能：
- 使用 AutoGen 构建对话式 Agent
- 支持工具调用和反思
- 完整集成 PPIO Agent Runtime
"""

import logging
import os

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入 PPIO Agent Runtime
from ppio_sandbox.agent_runtime import AgentRuntimeApp, RequestContext

app = AgentRuntimeApp()

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("autogen_agent")

# 初始化全局对话历史 - 在沙箱生命周期内持久化
# 同一个沙箱实例的所有请求共享此历史
conversation_history = []

# 检查 AutoGen 是否可用
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_agentchat.messages import TextMessage
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.models import ModelFamily, ModelInfo
    from autogen_core import CancellationToken
    AUTOGEN_AVAILABLE = True
    logger.info("AutoGen 导入成功")
except ImportError as e:
    AUTOGEN_AVAILABLE = False
    logger.error(f"AutoGen 导入失败：{e}", exc_info=True)
    logger.warning("AutoGen 未安装或导入失败，将使用模拟模式")


# 定义工具函数
async def get_weather(city: str) -> str:
    """
    获取指定城市的天气
    
    Args:
        city: 城市名称
        
    Returns:
        天气信息字符串
    """
    weather_data = {
        "北京": "晴天，温度 15°C，空气质量良好",
        "上海": "多云，温度 20°C，湿度 60%",
        "深圳": "小雨，温度 25°C，建议带伞",
        "广州": "晴天，温度 28°C，炎热",
    }
    return weather_data.get(city, f"{city}：晴天，温度 23°C")


async def search_information(query: str) -> str:
    """
    搜索信息
    
    Args:
        query: 搜索查询
        
    Returns:
        搜索结果
    """
    return f"关于 '{query}' 的搜索结果：这是一个示例搜索结果。实际使用时可以接入真实搜索 API。"


async def calculate(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式
        
    Returns:
        计算结果
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


def _create_agent(streaming=False):
    """
    创建 AutoGen Agent（复用配置）
    
    Args:
        streaming: 是否启用流式输出（token 级别）
    """
    model_client = OpenAIChatCompletionClient(
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.ppinfra.com/v3/openai"),
        model=os.getenv("MODEL_NAME", "deepseek/deepseek-v3.1-terminus"),
        api_key=os.getenv("OPENAI_API_KEY"),
        model_info=ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family=ModelFamily.UNKNOWN,
            structured_output=True,
        ),
        # 启用 token 级别的流式输出
        stream_options={"include_usage": True} if streaming else None,
    )
    
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[get_weather, search_information, calculate],
        system_message="""你是一个有用的 AI 助手，可以：
        1. 查询天气信息
        2. 搜索相关信息
        3. 进行数学计算
        
        请根据用户的请求选择合适的工具。""",
        reflect_on_tool_use=True,
    )
    
    return agent


async def _handle_streaming():
    """
    处理流式请求 - 生成器函数
    
    实时流式返回 LLM 响应，并累积完整响应保存到对话历史
    """
    if not AUTOGEN_AVAILABLE:
        yield {"chunk": "（模拟响应）AutoGen 未安装", "type": "content"}
        yield {"chunk": "", "type": "end"}
        return
    
    try:
        agent = _create_agent(streaming=True)
        accumulated_content = ""
        
        # 将对话历史转换为 AutoGen 消息格式
        messages = []
        for msg in conversation_history:
            messages.append(TextMessage(content=msg["content"], source=msg["role"]))
        
        # 创建 CancellationToken
        cancellation_token = CancellationToken()
        
        # 运行 Agent 流式输出
        async for message in agent.on_messages_stream(messages, cancellation_token):
            # 提取消息内容
            content = None
            
            # 处理 Response 类型（包含 chat_message）
            if hasattr(message, 'chat_message') and hasattr(message.chat_message, 'content'):
                content = message.chat_message.content
            # 处理直接包含 content 的事件（如 ThoughtEvent）
            elif hasattr(message, 'content'):
                content = message.content
            
            # 输出有效内容
            if content and isinstance(content, str) and content.strip():
                accumulated_content += content
                yield {"chunk": content, "type": "content"}
        
        # 保存到对话历史
        if accumulated_content:
            conversation_history.append({"role": "assistant", "content": accumulated_content})
        
        yield {"chunk": "", "type": "end"}
        
    except Exception as e:
        logger.error(f"流式处理错误: {str(e)}", exc_info=True)
        yield {"error": str(e), "type": "error"}


async def _handle_non_streaming():
    """
    处理非流式请求 - 返回完整响应字典
    
    调用 Agent，提取响应，保存到对话历史
    """
    if not AUTOGEN_AVAILABLE:
        return {"result": "（模拟响应）AutoGen 未安装，请安装后使用完整功能。"}
    
    try:
        agent = _create_agent()
        
        # 将对话历史转换为 AutoGen 消息格式
        messages = []
        for msg in conversation_history:
            messages.append(TextMessage(content=msg["content"], source=msg["role"]))
        
        # 创建 CancellationToken
        cancellation_token = CancellationToken()

        # 运行 Agent
        response_message = await agent.on_messages(messages, cancellation_token)
        
        # 提取响应内容
        if response_message and hasattr(response_message, 'chat_message'):
            chat_msg = response_message.chat_message
            response = chat_msg.content if hasattr(chat_msg, 'content') else str(chat_msg)
        else:
            response = str(response_message) if response_message else "未生成响应"
        
        # 保存到对话历史
        conversation_history.append({"role": "assistant", "content": response})
        
        return {"result": response}
        
    except Exception as e:
        logger.error(f"Agent 执行错误: {str(e)}", exc_info=True)
        return {
            "error": f"Agent 执行失败: {str(e)}",
            "error_type": type(e).__name__
        }


# 定义 PPIO Agent Runtime 入口点（支持异步）
@app.entrypoint
async def agent_invocation(request: dict, context: RequestContext):
    """
    AutoGen Agent 入口点（支持流式和多轮对话）
    
    Args:
        request: 请求数据，包含以下字段：
            - prompt: 用户输入的查询
            - streaming: 是否使用流式输出（可选，默认 False）
        context: 请求上下文
            
    Returns:
        响应数据字典（非流式）或生成器（流式）
    """
    try:
        # 获取请求参数
        prompt = request.get("prompt", "你好！")
        streaming = request.get("streaming", False)
        
        # 添加新用户消息到全局历史
        conversation_history.append({"role": "user", "content": prompt})
        
        # 根据 streaming 参数选择处理函数
        if streaming:
            return _handle_streaming()
        else:
            return await _handle_non_streaming()
    
    except Exception as e:
        logger.error(f"Agent 错误: {str(e)}", exc_info=True)
        return {
            "error": f"Agent 错误: {str(e)}",
            "error_type": type(e).__name__
        }


@app.ping
def health_check() -> dict:
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "AutoGen Agent",
        "features": ["weather", "search", "calculate", "streaming", "multi-turn"]
    }


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 启动 Microsoft AutoGen Agent Runtime")
    print("="*80)
    print("🛠️  可用工具：get_weather, search_information, calculate")
    print("💬 支持功能：流式输出、多轮对话")
    print("🔗 监听端口：8080")
    print("="*80 + "\n")
    app.run(port=8080)

