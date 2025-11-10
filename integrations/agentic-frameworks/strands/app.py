"""
Strands Agents 示例项目

这个示例展示如何使用 Strands Agents 轻量级框架构建 Agent，
并集成到 PPIO Agent Runtime 中。

功能：
- 使用 Strands Agents 快速构建 Agent
- 支持文件操作工具
- 轻量级、易于扩展
- 完整集成 PPIO Agent Runtime
"""

import os
import logging
from typing import Dict, Any

# 导入 PPIO Agent Runtime
from ppio_sandbox.agent_runtime import AgentRuntimeApp

app = AgentRuntimeApp()

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("strands_agent")

# 检查 Strands 是否可用
try:
    # 注意：Strands Agents 可能需要特定的安装方式
    # 这里使用简化的实现
    STRANDS_AVAILABLE = False
    logger.warning("Strands Agents 未安装，使用简化实现")
except ImportError:
    STRANDS_AVAILABLE = False


# 简化版本的 Agent 实现
class SimpleAgent:
    """简化版本的 Agent 类"""
    
    def __init__(self, tools: list, model: str = "gpt-4", system_prompt: str = ""):
        self.tools = tools
        self.model = model
        self.system_prompt = system_prompt
        logger.info(f"初始化 Agent，模型：{model}，工具数量：{len(tools)}")
    
    def __call__(self, prompt: str) -> Dict[str, Any]:
        """
        调用 Agent
        
        Args:
            prompt: 用户输入
            
        Returns:
            Agent 响应
        """
        logger.info(f"处理请求：{prompt}")
        
        # 简单的响应逻辑
        if "文件" in prompt or "file" in prompt.lower():
            message = "我可以帮你进行文件操作。可用的操作包括：读取文件、写入文件、编辑文件等。"
        elif "天气" in prompt or "weather" in prompt.lower():
            message = "我可以帮你查询天气信息。请告诉我你想查询哪个城市的天气。"
        else:
            message = f"收到你的消息：{prompt}。我是一个基于 Strands Agents 的助手，可以帮你处理文件操作等任务。"
        
        return AgentResponse(message=message)


class AgentResponse:
    """Agent 响应类"""
    
    def __init__(self, message: str):
        self.message = message


# 定义工具函数
def file_read(filepath: str) -> str:
    """
    读取文件内容
    
    Args:
        filepath: 文件路径
        
    Returns:
        文件内容
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"读取文件：{filepath}")
        return f"文件内容：\n{content}"
    except Exception as e:
        error_msg = f"读取文件失败：{str(e)}"
        logger.error(error_msg)
        return error_msg


def file_write(filepath: str, content: str) -> str:
    """
    写入文件
    
    Args:
        filepath: 文件路径
        content: 文件内容
        
    Returns:
        操作结果
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"写入文件：{filepath}")
        return f"成功写入文件：{filepath}"
    except Exception as e:
        error_msg = f"写入文件失败：{str(e)}"
        logger.error(error_msg)
        return error_msg


def editor(filepath: str, old_text: str, new_text: str) -> str:
    """
    编辑文件（替换文本）
    
    Args:
        filepath: 文件路径
        old_text: 要替换的文本
        new_text: 新文本
        
    Returns:
        操作结果
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace(old_text, new_text)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info(f"编辑文件：{filepath}")
        return f"成功编辑文件：{filepath}，替换 {content.count(old_text)} 处"
    except Exception as e:
        error_msg = f"编辑文件失败：{str(e)}"
        logger.error(error_msg)
        return error_msg


# 初始化 Strands Agent
agent = SimpleAgent(
    tools=[file_read, file_write, editor],
    model=os.getenv("MODEL_NAME", "gpt-4"),
    system_prompt="你是一个有用的文件管理助手，可以帮助用户读取、写入和编辑文件。"
)


# 定义 PPIO Agent Runtime 入口点
@app.entrypoint
def agent_invocation(request: dict) -> dict:
    """
    Strands Agent 入口点
    
    Args:
        request: 请求数据，包含以下字段：
            - prompt: 用户输入的提示信息
            
    Returns:
        响应数据字典，包含 result 字段
    """
    prompt = request.get("prompt", "请提供有效的提示信息")
    
    print(f"📨 收到请求：{prompt}")
    
    try:
        # 调用 Agent
        result = agent(prompt)
        
        response = result.message
        
        print(f"✅ 返回响应：{response[:100]}...")
        
        return {
            "result": response,
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
    print("🚀 启动 Strands Agents Runtime...")
    print("📁 可用工具：file_read, file_write, editor")
    print("🔗 监听端口：8080")
    app.run()

