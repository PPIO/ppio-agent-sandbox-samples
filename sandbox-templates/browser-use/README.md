# Browser-Use Remote Chromium Connection Solution

A complete solution that enables `browser-use` to connect to a remote Chromium instance running in a PPIO sandbox via Chrome DevTools Protocol (CDP) from your local machine.

## Core Challenges

When running in a cloud sandbox environment, `browser-use` faces two main challenges when connecting to remote Chromium:

1. **Host Header Security Restriction** - Chromium rejects CDP connection requests from non-localhost domains
2. **WebSocket URL Rewriting** - Need to rewrite internal addresses (`127.0.0.1:9222`) to externally accessible addresses

## Solution Architecture

### Overall Flow

```
Local browser-use → PPIO Sandbox External Domain:9223 → Go Reverse Proxy → Chromium:9222
```

### Core Components

1. **Manually Downloaded Chromium** - Latest version, avoiding package manager limitations
2. **Enhanced Go Reverse Proxy** - Intelligent Host header handling and WebSocket URL rewriting
3. **PPIO Sandbox** - Provides containerized runtime environment

## Workflow

### 1. Container Startup Phase
- Download latest Chromium binary from Google official source
- Start Chromium, binding to internal address `127.0.0.1:9222`
- Start Go reverse proxy, listening on external address `0.0.0.0:9223`

### 2. Connection Establishment Phase
- `browser-use` initiates connection request to PPIO Sandbox external domain
- Reverse proxy intercepts request, rewrites Host header to `127.0.0.1:9222`
- Chromium receives "local request", passes security verification

### 3. CDP Protocol Interaction Phase

`browser-use` follows the standard Chrome DevTools Protocol connection flow:

**Step 1: Retrieve WebSocket Connection Information**
```
browser-use → GET https://9223-sandbox-host/json/version/
            ↓ (reverse proxy rewrites Host header)
            → GET http://127.0.0.1:9222/json/version/
```

**Chrome Original Response:**
```json
{
  "Browser": "Chrome/138.0.7204.168",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/abc123"
}
```

**Reverse Proxy Dynamic Rewrite Response:**
```json
{
  "Browser": "Chrome/138.0.7204.168", 
  "webSocketDebuggerUrl": "wss://9223-sandbox-host/devtools/browser/abc123"
}
```

**Step 2: Establish WebSocket Connection**
```
browser-use → WSS wss://9223-sandbox-host/devtools/browser/abc123
            ↓ (reverse proxy handles WebSocket upgrade + Host rewrite)
            → WS ws://127.0.0.1:9222/devtools/browser/abc123
```

**Key Rewrite Points:**
- `ws://` → `wss://` (PPIO Sandbox HTTPS environment requires secure WebSocket)
- `127.0.0.1:9222` → `9223-sandbox-host` (rewrite to externally accessible address)
- Host header: `sandbox-host` → `127.0.0.1:9222` (bypass Chromium security restriction)

**Why Rewriting is Needed:**
- Chromium's security mechanism only allows localhost addresses to access CDP
- PPIO Sandbox serves externally via HTTPS, requiring WSS protocol
- `browser-use` needs the correct external WebSocket URL to connect

### 4. Real-time Communication Phase
- After WebSocket connection is established, all CDP commands are transparently proxied
- `browser-use` sends operation commands (click, input, screenshot, etc.)
- Chromium returns page state and response data
- Reverse proxy ensures bidirectional communication stability

## Key Features

### 🛡️ Security Bypass
- Intelligent Host header rewriting, bypassing Chromium security restrictions
- Support for multiple URL format recognition and conversion

### 🔌 Protocol Compatibility
- Full support for HTTP and WebSocket protocols
- Automatic handling of `/json/version` and `/json` endpoints

### 📊 Production Ready
- Built-in health check (`/health`) and performance monitoring (`/metrics`)
- Configurable timeout, log level, and other parameters

### 🎯 High Performance
- Only intercept and process necessary endpoints
- Other traffic is transparently proxied with minimal overhead

## Deployment

### One-Click Build (Recommended)
```bash
# Run the one-click build script
./build.sh
```

The build script will automatically:
1. Check Go and PPIO Sandbox CLI dependencies
2. Compile Go reverse proxy to Linux x86 binary
3. Build PPIO Sandbox Template

### Manual Build
For manual build, execute step by step:

```bash
# 1. Compile reverse proxy
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o reverse-proxy reverse-proxy.go

# 2. Build template
ppio-sandbox-cli template build -c "/app/.browser-use/start-up.sh"
```

### Local Connection
```python
from ppio_sandbox.core import Sandbox
from browser_use import Agent

# Create sandbox
sandbox = Sandbox(template="your-template-id")

# Get Chrome connection address (port 9223)
host = sandbox.get_host(9223)
cdp_url = f"https://{host}"

# Connect browser-use
agent = Agent(
    task="your task",
    llm=llm,
    use_vision=True
)

# Use remote Chrome
result = agent.run(cdp_url=cdp_url)
```

## Network Architecture

```
┌─────────────────┐    HTTPS     ┌──────────────────────┐
│   browser-use   │─────────────→│ PPIO Sandbox External │
│     (Local)     │              │    Domain:9223        │
└─────────────────┘              └──────────────────────┘
                                          │
                                          │ HTTP
                                          ▼
                                ┌──────────────────┐
                                │   Go Reverse     │
                                │     Proxy        │
                                │ (Host Rewrite)   │
                                └──────────────────┘
                                          │
                                          │ HTTP  
                                          ▼
                                ┌──────────────────┐
                                │     Chromium     │
                                │  127.0.0.1:9222  │
                                └──────────────────┘
```
