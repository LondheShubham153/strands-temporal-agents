# Strands Temporal Agents

AI agents built with Strands framework and Temporal workflows for reliable, distributed execution.

## What This Does

This project combines two powerful frameworks:
- **Strands**: Simple AI agent framework for building conversational agents
- **Temporal**: Workflow orchestration platform for reliable, fault-tolerant execution

The result? AI agents that can handle file operations, time queries, and LLM conversations with built-in retry logic, error recovery, and execution visibility.

## Core Files

- `temporal_ollama_agent.py` - Main agent with Temporal workflows and activities
- `temporal_agent_worker.py` - Worker process that executes agent workflows
- `temporal_agent_client.py` - Client to interact with running agents
- `ollama_agent.py` - Direct Ollama integration (no Temporal)
- `my-agent.py` - Simple Strands agent example

## Quick Start

### Prerequisites
- Python 3.8+
- [Temporal CLI](https://docs.temporal.io/cli) installed
- [Ollama](https://ollama.ai) running locally with llama3.2 model

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start Temporal server (keep this running)
temporal server start-dev
```

### Running the Agent

**Terminal 1 - Start the Worker:**
```bash
python temporal_agent_worker.py
```

**Terminal 2 - Run Tasks:**
```bash
python temporal_agent_client.py
```

## How It Works

The agent can handle these types of tasks:
- **File Operations**: "Read file requirements.txt", "List files in current directory"
- **Time Queries**: "What time is it?"
- **General Questions**: "What is machine learning?" (uses Ollama LLM)

## Temporal UI Dashboard

When you run the agent, you can monitor everything through Temporal's web interface at `http://localhost:8233`

### Workflows Overview
![Temporal Workflows](images/temporal-workflows-overview.png)
*All your agent workflows in one place - see which tasks are running, completed, or failed*

### Workflow Execution Details
![Workflow Details](images/workflow-execution-details.png)
*Dive deep into any workflow to see the complete execution timeline and task routing*

### Activity Execution History
![Activity History](images/activity-execution-history.png)
*Track individual activities like file reads, API calls, and their retry attempts*

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client        │───▶│   Temporal       │───▶│   Worker        │
│                 │    │   Server         │    │                 │
│ Sends tasks     │    │                  │    │ Executes        │
│ Gets results    │    │ Orchestrates     │    │ Activities      │
└─────────────────┘    │ Workflows        │    └─────────────────┘
                       └──────────────────┘
                               │
                               ▼
                       ┌──────────────────┐
                       │   Activities     │
                       │                  │
                       │ • File I/O       │
                       │ • Time queries   │
                       │ • Ollama calls   │
                       └──────────────────┘
```

## Why Temporal?

**Without Temporal** (see `ollama_agent.py`):
- If Ollama is down, your task fails
- No retry logic
- No execution history
- Hard to debug issues

**With Temporal** (see `temporal_ollama_agent.py`):
- Automatic retries with backoff
- Complete execution visibility
- Fault tolerance
- Easy to scale across machines

## Examples

### Simple Strands Agent
```python
from strands import Agent

agent = Agent()
response = agent("Tell me about agentic AI")
print(response)
```

### Temporal-Powered Agent
The Temporal version handles the same queries but with enterprise-grade reliability:

```python
# This runs through Temporal workflows
client = AgentClient(temporal_client)
result = await client.execute_task("What is Python?", "task-1")
```

## Development

### Adding New Activities
1. Create activity function in `temporal_ollama_agent.py`
2. Register it in `temporal_agent_worker.py`
3. Add routing logic in `OllamaAgentWorkflow.run()`

### Testing Different Models
Change the model in `ollama_chat_activity()`:
```python
async def ollama_chat_activity(prompt: str, model: str = "llama3.2:latest"):
```

## Troubleshooting

**Worker not starting?**
- Check if Temporal server is running: `temporal server start-dev`
- Verify Ollama is running: `ollama list`

**Tasks failing?**
- Check Temporal UI at `http://localhost:8233` for detailed error logs
- Ensure the model exists: `ollama pull llama3.2:latest`

**Connection issues?**
- Default Temporal server runs on `localhost:7233`
- Web UI is available at `http://localhost:8233`

