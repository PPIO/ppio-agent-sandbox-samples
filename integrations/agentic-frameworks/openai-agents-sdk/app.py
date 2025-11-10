"""
OpenAI Agents SDK 示例项目

这个示例展示如何使用 OpenAI Agents SDK 构建简单高效的 Agent，
并集成到 PPIO Agent Runtime 中。

功能：
- 使用 OpenAI 官方 Agent 框架
- 支持函数调用
- 完整集成 PPIO Agent Runtime
"""

import asyncio
import logging
import os
from typing import Dict, Any

# 加载环境变量
from dotenv import load_dotenv

# 导入 PPIO Agent Runtime
from ppio_sandbox.agent_runtime import AgentRuntimeApp

# 加载 .env 文件
load_dotenv()

app = AgentRuntimeApp()

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("openai_agents")

# 注意：由于 OpenAI Agents SDK 还在早期开发阶段，这里使用简化版本
# 实际使用时，请根据 OpenAI 官方文档进行调整

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI SDK 未安装，将使用模拟模式")


# 定义工具函数
def get_current_time(timezone: str = "UTC") -> str:
    """
    获取当前时间
    
    Args:
        timezone: 时区（暂不实现，返回 UTC 时间）
        
    Returns:
        当前时间字符串
    """
    from datetime import datetime
    now = datetime.utcnow()
    return f"当前时间（UTC）：{now.strftime('%Y-%m-%d %H:%M:%S')}"


def calculate(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式，如 "2 + 3 * 4"
        
    Returns:
        计算结果
    """
    try:
        # 安全地计算表达式
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


def get_weather(city: str) -> str:
    """
    获取城市天气（模拟）
    
    Args:
        city: 城市名称
        
    Returns:
        天气信息
    """
    weather_data = {
        "北京": "晴天，15°C，空气质量良好",
        "上海": "多云，20°C，湿度 60%",
        "深圳": "小雨，25°C，建议带伞",
        "广州": "晴天，28°C，炎热",
    }
    return weather_data.get(city, f"{city}：晴天，23°C")


# 工具定义（OpenAI Function Calling 格式）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区，如 'UTC', 'Asia/Shanghai'"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如 '北京', '上海'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 工具函数映射
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "get_weather": get_weather,
}


async def run_agent(query: str) -> str:
    """
    运行 OpenAI Agent
    
    Args:
        query: 用户查询
        
    Returns:
        Agent 响应
    """
    if not OPENAI_AVAILABLE:
        # 模拟模式
        return f"（模拟响应）收到查询：{query}。OpenAI SDK 未安装，请安装后使用完整功能。"
    
    try:
        logger.info(f"运行 Agent，查询：{query}")
        
        # 初始化 OpenAI 客户端
        client = AsyncOpenAI(
          base_url=os.getenv("OPENAI_API_BASE"),
          api_key=os.getenv("PPIO_API_KEY"),
        )
        
        # 第一次调用：发送用户消息和工具定义
        messages = [
            {"role": "system", "content": "你是一个有用的 AI 助手，可以获取时间、计算数学表达式和查询天气。"},
            {"role": "user", "content": query}
        ]
        
        response = await client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "deepseek/deepseek-v3.1-terminus"),
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # 检查是否需要调用工具
        if response_message.tool_calls:
            # 将助手的响应添加到消息历史
            messages.append(response_message)
            
            # 处理每个工具调用
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = eval(tool_call.function.arguments)
                
                logger.info(f"调用工具：{function_name}，参数：{function_args}")
                
                # 执行工具函数
                function_response = TOOL_FUNCTIONS[function_name](**function_args)
                
                # 将工具响应添加到消息历史
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })
            
            # 第二次调用：获取最终响应
            final_response = await client.chat.completions.create(
                model=os.getenv("MODEL_NAME", "deepseek/deepseek-v3.1-terminus"),
                messages=messages
            )
            
            result = final_response.choices[0].message.content
        else:
            result = response_message.content
        
        logger.info("Agent 执行完成")
        return result
        
    except Exception as e:
        logger.error(f"Agent 执行错误：{e}", exc_info=True)
        raise


# 定义 PPIO Agent Runtime 入口点（支持异步）
@app.entrypoint
async def agent_invocation(request: dict) -> dict:
    """
    OpenAI Agents SDK 入口点
    
    Args:
        request: 请求数据，包含以下字段：
            - prompt: 用户输入的查询
            
    Returns:
        响应数据字典，包含 result 字段
    """
    prompt = request.get("prompt", "你好！")
    
    print(f"📨 收到请求：{prompt}")
    
    try:
        result = await run_agent(prompt)
        
        print(f"✅ 返回响应：{result[:100]}...")
        
        return {
            "result": result,
            "status": "success"
        }
        
    except Exception as e:
        error_msg = f"处理请求时出错：{str(e)}"
        print(f"❌ 错误：{error_msg}")
        return {
            "result": error_msg,
            "status": "error"
        }


if __name__ == "__main__":
    print("🚀 启动 OpenAI Agents SDK Runtime...")
    print("🛠️  可用工具：get_current_time, calculate, get_weather")
    print("🔗 监听端口：8080")
    app.run()

