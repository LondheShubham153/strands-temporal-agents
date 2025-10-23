import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporal_ollama_agent import (
    OllamaAgentWorkflow,
    read_file_activity,
    list_files_activity, 
    get_time_activity,
    ollama_chat_activity
)

TASK_QUEUE = "ollama-agent-queue"
TEMPORAL_HOST = "localhost:7233"


async def create_worker():
    client = await Client.connect(TEMPORAL_HOST)
    
    return Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[OllamaAgentWorkflow],
        activities=[
            read_file_activity,
            list_files_activity,
            get_time_activity,
            ollama_chat_activity
        ]
    )


async def main():
    worker = await create_worker()
    print(f"Worker started on {TASK_QUEUE}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
