import asyncio
import os
import json
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
  """测试三个核心工具：天气查询、信息搜索、计算"""
  
  # 定义三个测试用例
  test_cases = [
    {"name": "天气查询工具 (get_weather)", "prompt": "请查询北京的天气"},
    {"name": "信息搜索工具 (search_information)", "prompt": "搜索人工智能相关信息"},
    {"name": "计算工具 (calculate)", "prompt": "计算 123 + 456"}
  ]
  
  print("\n" + "="*80)
  print("🚀 AutoGen Agent 功能测试")
  print("="*80 + "\n")
  
  for i, test in enumerate(test_cases, 1):
    try:
      print("="*80)
      print(f"Test {i}: {test['name']}")
      print("="*80)
      print(f"📤 {test['prompt']}")
      
      payload = json.dumps({"prompt": test['prompt'], "streaming": False}).encode()
      
      response = await client.invoke_agent_runtime(
        agentId=os.getenv("PPIO_AGENT_ID"),
        payload=payload,
        timeout=300,
        envVars={"OPENAI_API_KEY": os.getenv("PPIO_API_KEY")},
      )
      
      print(f"📥 响应:")
      if isinstance(response, dict):
        result = response.get('result', response)
        print(result)
      else:
        print(response)
      print("")
      
    except Exception as e:
      print(f"❌ 测试失败: {str(e)}")
      import traceback
      traceback.print_exc()
      print("")
  
  print("="*80)
  print("✅ 所有测试完成")
  print("="*80 + "\n")

if __name__ == "__main__":
  asyncio.run(main())