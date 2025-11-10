import asyncio
import os
import json
import uuid
from ppio_sandbox.agent_runtime import AgentRuntimeClient as PPIOAgentRuntimeClient
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("PPIO_API_KEY"))
print(os.getenv("PPIO_DOMAIN"))
print(os.getenv("PPIO_AGENT_ID"))

client = PPIOAgentRuntimeClient(
  api_key=os.getenv("PPIO_API_KEY")
)

async def main():
  """测试多轮对话"""
  # Create unique runtimeSessionId
  runtime_session_id = str(uuid.uuid4())
  
  print("\n" + "="*80)
  print("🚀 AutoGen Agent 多轮对话测试")
  print("="*80)
  print(f"🔑 会话 ID: {runtime_session_id}")
  print("="*80 + "\n")
  
  # 定义两轮对话
  conversation_rounds = [
    {"round": "第 1 轮", "prompt": "北京的天气怎么样？"},
    {"round": "第 2 轮：测试记忆", "prompt": "我刚才问了哪个城市的天气？"}
  ]
  
  try:
    responses = []
    
    for turn in conversation_rounds:
      print("="*80)
      print(f"{turn['round']}")
      print("="*80)
      print(f"📤 {turn['prompt']}")
      
      payload = json.dumps({"prompt": turn['prompt'], "streaming": False}).encode()
      
      response = await client.invoke_agent_runtime(
        agentId=os.getenv("PPIO_AGENT_ID"),
        payload=payload,
        timeout=300,
        envVars={"OPENAI_API_KEY": os.getenv("PPIO_API_KEY")},
        runtimeSessionId=runtime_session_id  # 使用相同的 sessionId
      )
      
      print(f"📥 响应:")
      if isinstance(response, dict):
        result = response.get('result', response)
        print(result)
        responses.append(result)
      else:
        print(response)
        responses.append(str(response))
      print("")
      
      # 在轮次之间暂停
      await asyncio.sleep(1)
    
    # 检查记忆能力
    if len(responses) >= 2 and "北京" in str(responses[1]):
      print("="*80)
      print("✅ 成功！Agent 记住了之前的对话内容！")
      print("="*80 + "\n")
    else:
      print("="*80)
      print("⚠️  警告：Agent 可能没有记住之前的对话")
      print("="*80 + "\n")
    
    print("="*80)
    print("✅ 多轮对话测试完成")
    print("="*80 + "\n")
    
  except Exception as e:
    print("\n" + "="*80)
    print("❌ 测试失败")
    print("="*80)
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {str(e)}")
    import traceback
    print("\n完整错误:")
    traceback.print_exc()
    print("="*80 + "\n")

if __name__ == "__main__":
  asyncio.run(main())

