import asyncio
from temporalio.client import Client
from temporal_ollama_agent import OllamaAgentWorkflow

TASK_QUEUE = "ollama-agent-queue"
TEMPORAL_HOST = "localhost:7233"


class AgentClient:
    def __init__(self, client: Client):
        self.client = client
    
    async def execute_task(self, task: str, task_id: str) -> str:
        result = await self.client.execute_workflow(
            OllamaAgentWorkflow.run,
            task,
            id=f"agent-task-{task_id}",
            task_queue=TASK_QUEUE
        )
        return result
    
    async def run_demo_tasks(self):
        tasks = [
            ("What time is it?", "1"),
            ("List files in current directory", "2"), 
            ("Read file requirements.txt", "3"),
            ("What is machine learning?", "4")
        ]
        
        for task, task_id in tasks:
            try:
                result = await self.execute_task(task, task_id)
                print(f"Task: {task}")
                print(f"Result: {result}\n")
            except Exception as e:
                print(f"Task failed: {task} - {e}\n")


async def main():
    client = await Client.connect(TEMPORAL_HOST)
    agent_client = AgentClient(client)
    await agent_client.run_demo_tasks()


if __name__ == "__main__":
    asyncio.run(main())
