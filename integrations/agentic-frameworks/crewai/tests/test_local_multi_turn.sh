#!/bin/bash

# Multi-turn conversation test
# Usage: 
#   1. Start app.py: python app.py
#   2. Run this script: bash tests/test_local_multi_turn.sh

set -e

# Service configuration
BASE_URL="http://localhost:8080"
ENDPOINT="${BASE_URL}/invocations"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "========================================================================"
echo -e "${GREEN}🚀 AutoGen Agent 多轮对话测试${NC}"
echo "========================================================================"
echo ""

# Check service
if ! curl -s -f "${BASE_URL}/ping" > /dev/null 2>&1; then
    echo "❌ Service not running! Start with: python app.py"
    exit 1
fi

# Round 1
echo "========================================================================"
echo -e "${BLUE}第 1 轮${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 北京的天气怎么样？${NC}"
echo ""

RESPONSE1=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "北京的天气怎么样？", "streaming": false}')

echo -e "${GREEN}📥 响应:${NC}"
echo "${RESPONSE1}" | jq -r '.result // .error // .'
echo ""
sleep 1

# Round 2: Test memory
echo "========================================================================"
echo -e "${BLUE}第 2 轮：测试记忆${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 我刚才问了哪个城市的天气？${NC}"
echo ""

RESPONSE2=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "我刚才问了哪个城市的天气？", "streaming": false}')

echo -e "${GREEN}📥 响应:${NC}"
echo "${RESPONSE2}" | jq -r '.result // .error // .'
echo ""

# Check memory
if echo "${RESPONSE2}" | grep -qi "北京"; then
    echo -e "${GREEN}✅ 成功！Agent 记住了之前的对话内容！${NC}"
else
    echo -e "${YELLOW}⚠️  警告：Agent 可能没有记住之前的对话${NC}"
fi

echo ""
echo "========================================================================"
echo -e "${GREEN}✅ 多轮对话测试完成${NC}"
echo "========================================================================"
echo ""

