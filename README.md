# 🤖 SwarmAI Assistant

SwarmAI is a professional-grade **Multi-Agent Orchestration** system built with **LangGraph** and **Groq (Llama-3)**. It leverages the **Model Context Protocol (MCP)** to decouple agentic reasoning from tool execution.

## 🏗️ System Architecture

```mermaid
graph TD
    User([User Input]) --> UI[Streamlit Frontend]
    UI --> LG{LangGraph Orchestrator}
    
    subgraph Agents [Specialized AI Agents]
        Supervisor[Supervisor Planner]
        Research[Researcher Agent]
        Email[Email Agent]
        Calendar[Calendar Agent]
    end
    
    LG --> Supervisor
    Supervisor -->|Plan| LG
    LG --> Research
    LG --> Email
    LG --> Calendar
    
    subgraph MCP [Model Context Protocol Layer]
        Client[MCP Client]
        Registry[Tool Registry]
    end
    
    Research --> Registry
    Email --> Registry
    Calendar --> Registry
    Registry --> Client
    
    subgraph Servers [MCP Tool Servers]
        SearchSrv[Search Server]
        GmailSrv[Gmail Server]
        CalSrv[Calendar Server]
    end
    
    Client -->|JSON-RPC| SearchSrv
    Client -->|JSON-RPC| GmailSrv
    Client -->|JSON-RPC| CalSrv
```

## 🌟 Key Features
- **Real MCP Integration**: Tools run as independent subprocesses, communicating via standardized JSON-RPC over stdio.
- **Dynamic Skill Discovery**: Agents discover their capabilities at runtime from the tool registry.
- **Stateful Orchestration**: Complex multi-step tasks are managed via LangGraph's cyclic state machine.
- **Explainable UI**: Real-time "Agent Activity" panel shows the internal reasoning and planning process.

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   uv sync
   ```
2. **Setup Credentials**:
   - Add your `TAVILY_API_KEY` and `GROQ_API_KEY` to a `.env` file.
   - Place your Google `credentials.json` in the root directory.
3. **Run the App**:
   ```bash
   uv run streamlit run interface/app.py
   ```

---
*Built for scale. Architected for speed.*
