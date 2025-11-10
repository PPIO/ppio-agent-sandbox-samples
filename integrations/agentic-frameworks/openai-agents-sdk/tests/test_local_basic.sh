#!/bin/bash

# Basic functionality test - Non-streaming
# Usage: 
#   1. Start app.py: python app.py
#   2. Run this script: bash tests/test_local_basic.sh

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
echo -e "${GREEN}🚀 AutoGen Agent 功能测试${NC}"
echo "========================================================================"
echo ""

# Check service
if ! curl -s -f "${BASE_URL}/ping" > /dev/null 2>&1; then
    echo "❌ Service not running! Start with: python app.py"
    exit 1
fi

# Test 1: Weather Tool
echo "========================================================================"
echo -e "${BLUE}Test 1: 天气查询工具 (get_weather)${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 请查询北京的天气${NC}"
RESPONSE=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "请查询北京的天气", "streaming": false}')
echo -e "${GREEN}📥 Response:${NC}"
echo "${RESPONSE}" | jq -r '.result'
echo ""

# Test 2: Search Tool
echo "========================================================================"
echo -e "${BLUE}Test 2: 信息搜索工具 (search_information)${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 搜索人工智能相关信息${NC}"
RESPONSE=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "搜索人工智能相关信息", "streaming": false}')
echo -e "${GREEN}📥 Response:${NC}"
echo "${RESPONSE}" | jq -r '.result'
echo ""

# Test 3: Calculate Tool
echo "========================================================================"
echo -e "${BLUE}Test 3: 计算工具 (calculate)${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 计算 123 + 456${NC}"
RESPONSE=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "计算 123 + 456", "streaming": false}')
echo -e "${GREEN}📥 Response:${NC}"
echo "${RESPONSE}" | jq -r '.result'
echo ""

echo "========================================================================"
echo -e "${GREEN}✅ 所有测试完成${NC}"
echo "========================================================================"
echo ""

