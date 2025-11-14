<div align="center">
  <h1>PPIO Agent Sandbox Samples</h1>
  
  <p>
    <a href="https://ppio.com/docs/sandbox/overview">📚 Documentation</a> •
    <a href="#-about-ppio-agent-sandbox">Introduction</a> •
    <a href="#-project-structure">Project Structure</a>
  </p>
  
  <p>
    <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a>
  </p>
</div>

---

Welcome to the **PPIO Agent Sandbox Samples** repository!

This repository provides usage examples for the PPIO Agent Sandbox product, helping you quickly understand and integrate PPIO Agent Sandbox capabilities into your applications.

> [!IMPORTANT]
> The examples provided in this repository are for experimental and educational purposes only. They demonstrate concepts and techniques but are not suitable for direct production use.

## 📖 About PPIO Agent Sandbox

**Agent Sandbox** is a next-generation runtime infrastructure designed specifically for AI Agent scenarios, providing a secure and isolated cloud sandbox environment to execute AI-generated code. This sandbox environment prevents AI Agents from accessing or tampering with resources outside the system, ensuring their behavior does not harm the system.

### Product Features

* **Security Isolation**. Sandboxes have system-level isolation capabilities to ensure the security of data and execution environment within the sandbox.
* **Fast Startup**. Startup time is less than 200ms with support for large-scale concurrent creation, suitable for AI application scenarios with high concurrency requirements.
* **Multi-language Execution Environment**. Supports running code in multiple programming languages such as Python, JavaScript, C++, meeting diverse AI task requirements.
* **Fast Pause and Resume**. Can pause the sandbox at any time and resume it when needed later, with file system and process state also being restored.
* **Background Execution**. Supports background task execution, suitable for scenarios that need to wait for results.
* **Easy Integration**. Seamlessly integrates with mainstream AI Agent frameworks and tools, supporting closed-loop code generation and execution.

### Use Cases

* AI data analysis, processing, and visualization
* Code execution environment for Code Agents
* Cloud virtual desktop environment for Computer Use Agents

> For more information, please visit the [Official Documentation](https://ppio.com/docs/sandbox/overview)

## 📁 Project Structure

### 🚀 [`agent-runtime/`](./agent-runtime/)
**PPIO Agent Runtime Sample Projects**

PPIO Agent Runtime is a framework-agnostic and model-agnostic lightweight AI Agent runtime framework that allows you to safely and quickly deploy and run AI Agents.

This directory contains integration examples for multiple mainstream AI Agent frameworks:

- **[LangGraph](./agent-runtime/integrations/agentic-frameworks/langgraph/)**
- **[AutoGen](./agent-runtime/integrations/agentic-frameworks/autogen/)**
- **[Google ADK](./agent-runtime/integrations/agentic-frameworks/google-adk/)**
- **[OpenAI Agents SDK](./agent-runtime/integrations/agentic-frameworks/openai-agents-sdk/)**

## 📚 Related Resources

- [PPIO Agent Sandbox Documentation](https://ppio.com/docs/sandbox/overview)
- [PPIO Agent Runtime Documentation](https://ppio.com/docs/sandbox/agent-runtime-introduction)

## 🤝 Contributing

We welcome contributions! If you want to contribute code or improve examples:

- Add new framework examples or use cases
- Improve existing examples
- Report issues
- Suggest improvements

Please submit an Issue or Pull Request.

## 📄 License

Please refer to the LICENSE files in each sample project.

---

<div align="center">
  Made with ❤️ by PPIO Team
</div>

