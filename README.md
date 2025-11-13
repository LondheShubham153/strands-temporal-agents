# Strands Temporal Agents

A comparison of two approaches to building AI agents: simple direct execution vs enterprise-grade distributed workflows.

## What's This About?

Two different ways to build the same AI agent to show the trade-offs between simplicity and reliability:

- **Simple version** (`agent.py`) - Runs directly, great for development
- **Temporal version** - Distributed with retries, monitoring, and fault tolerance

Both agents can read files, list directories, tell time, and chat using Ollama.

## Files

- `config.py` - Shared configuration
- `agent.py` - Simple Strands agent
- `temporal_agent.py` - Workflow definitions
- `worker.py` - Temporal worker
- `client.py` - Temporal client

## Setup

You'll need Python 3.8+, Temporal CLI, and Ollama running locally.

```bash
pip install -r requirements.txt
```

Optional environment variables:
```bash
export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_MODEL="llama3.2:latest"
```

## Running

**Simple version:**
```bash
python agent.py
```

**Temporal version:**
```bash
# Terminal 1
temporal server start-dev

# Terminal 2  
python worker.py

# Terminal 3
python client.py
```

**Run tests:**
```bash
pytest test_activities.py
```

## What Each Agent Can Do

- "What time is it?"
- "List files in current directory"
- "Read file requirements.txt"
- "What is machine learning?"

## Why Two Versions?

The simple version is perfect for prototyping and development. The Temporal version adds enterprise features:

- Automatic retries when things fail
- Complete execution history
- Distributed processing
- Web UI for monitoring at `http://localhost:8233`

## Architecture

```
Simple: User → Agent → Result

Temporal: Client → Temporal Server → Worker → Activities → Result
```

The Temporal version is more complex but handles failures gracefully and scales across multiple machines.

## Screenshots

![Temporal Workflows](images/temporal-workflows-overview.png)
*Workflow monitoring dashboard*

![Workflow Details](images/workflow-execution-details.png)
*Detailed execution traces*

![Activity History](images/activity-execution-history.png)
*Individual activity tracking*

## Troubleshooting

**Worker won't start?** Make sure Temporal server is running first.

**Tasks failing?** Check the Temporal UI at `http://localhost:8233` for error details.

**Ollama issues?** Verify it's running with `ollama list` and pull the model if needed.

## The Point

This shows how you can start simple and add enterprise features when you need them. The core agent logic stays the same - you're just changing how it runs.
