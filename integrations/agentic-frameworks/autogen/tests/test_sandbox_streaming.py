import asyncio
import os
import json
import time
import sys
from ppio_sandbox.agent_runtime import AgentRuntimeClient as PPIOAgentRuntimeClient
from dotenv import load_dotenv
load_dotenv()

# Force disable stdout buffering to ensure real-time output
sys.stdout.reconfigure(line_buffering=True)

# Debug mode: Display detailed information and timestamps for each chunk
DEBUG_MODE = False

print(os.getenv("PPIO_API_KEY"))
print(os.getenv("PPIO_DOMAIN"))
print(os.getenv("PPIO_AGENT_ID"))

client = PPIOAgentRuntimeClient(
  api_key=os.getenv("PPIO_API_KEY")
)

async def main():
  """测试流式输出"""
  try:
    print("\n" + "="*80)
    print("🚀 AutoGen Agent 流式输出测试")
    print("="*80)
    
    # 流式测试用例
    request_dict = {"prompt": "请查询深圳的天气并计算 25 + 15", "streaming": True}
    payload = json.dumps(request_dict).encode()
    print(f"📤 {request_dict['prompt']}")
    print(f"🎯 Agent ID: {os.getenv('PPIO_AGENT_ID')}")
    
    print("\n⏱️  调用 Agent...")
    invoke_start_time = time.time()
    
    response = await client.invoke_agent_runtime(
      agentId=os.getenv("PPIO_AGENT_ID"),
      payload=payload,
      timeout=300,
      envVars={"OPENAI_API_KEY": os.getenv("PPIO_API_KEY")},
    )
    
    first_response_time = time.time() - invoke_start_time
    print(f"✅ 响应对象接收完成, 耗时: {first_response_time:.3f}s")
    
    print("\n" + "="*80)
    print("📡 流式响应:")
    print("="*80 + "\n")
    
    # Handle streaming response
    if hasattr(response, '__aiter__'):
      print("-" * 80)
      chunk_count = 0
      content_count = 0
      
      start_time = time.time()
      last_chunk_time = start_time
      
      print(f"⏱️  Starting to iterate response stream, current timestamp: {time.time():.3f}")
      iteration_start = time.time()
      
      async for chunk in response:
        chunk_count += 1
        current_time = time.time()
        time_since_start = current_time - start_time
        time_since_last = current_time - last_chunk_time
        last_chunk_time = current_time
        
        # Special log for first chunk arrival
        if chunk_count == 1:
          time_to_first_chunk = current_time - iteration_start
          if DEBUG_MODE:
            sys.stdout.write(f"\n🎉 首个数据块到达! 耗时: {time_to_first_chunk:.3f}s\n")
            sys.stdout.write(f"   调用总耗时: {current_time - invoke_start_time:.3f}s\n\n")
            sys.stdout.flush()
        
        if DEBUG_MODE:
          # Use sys.stdout.write and immediate flush to ensure real-time output
          debug_msg = f"\n[Chunk #{chunk_count}] +{time_since_last:.3f}s | Type: {type(chunk).__name__}\n"
          sys.stdout.write(debug_msg)
          sys.stdout.flush()
        
        # Helper function to parse chunk
        def parse_and_print(data):
          nonlocal content_count
          if isinstance(data, dict):
            if data.get('type') == 'content':
              content = data.get('chunk', '')
              if content:
                content_count += 1
                # Use sys.stdout.write instead of print to ensure real-time output
                sys.stdout.write(content)
                sys.stdout.flush()
                
                if DEBUG_MODE:
                  sys.stdout.write(f" [{len(content)} chars]")
                  sys.stdout.flush()
            elif data.get('type') == 'end':
              sys.stdout.write(f"\n{'-' * 80}\n")
              sys.stdout.write(f"✅ 流式输出完成\n")
              if DEBUG_MODE:
                sys.stdout.write(f"   总数据块: {chunk_count}\n")
                sys.stdout.write(f"   内容块: {content_count}\n")
                sys.stdout.write(f"   总耗时: {time_since_start:.2f}s\n")
              sys.stdout.flush()
            elif data.get('type') == 'error':
              sys.stdout.write(f"\n❌ Error: {data.get('error')}\n")
              sys.stdout.flush()
          else:
            sys.stdout.write(str(data))
            sys.stdout.flush()
        
        # Handle different chunk formats
        if isinstance(chunk, str):
          # String format: might be JSON string
          try:
            data = json.loads(chunk)
            parse_and_print(data)
          except json.JSONDecodeError:
            # Not JSON, output directly
            sys.stdout.write(chunk)
            sys.stdout.flush()
        
        elif isinstance(chunk, dict):
          # Dict format: might be data directly, or contain nested 'chunk' key
          if 'chunk' in chunk and isinstance(chunk['chunk'], str):
            # SDK wrapper format: {'chunk': '...', ...}
            try:
              inner_data = json.loads(chunk['chunk'])
              parse_and_print(inner_data)
            except (json.JSONDecodeError, TypeError):
              # Not JSON, output directly
              sys.stdout.write(chunk['chunk'])
              sys.stdout.flush()
          else:
            # Direct data format
            parse_and_print(chunk)
        
        else:
          # Other types, output directly
          sys.stdout.write(str(chunk))
          sys.stdout.flush()
      
      if chunk_count == 0:
        print("⚠️ 未接收到数据")
        
    elif isinstance(response, dict):
      # 如果是普通响应（非流式）
      print("\n💬 Agent 响应 (非流式):")
      print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
      # 其他类型
      print("\n💬 Agent 响应 (未知格式):")
      print(response)
    
    print("\n" + "="*80)
    print("✅ 流式测试完成")
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