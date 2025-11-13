import asyncio
import logging
from datetime import datetime
from temporalio.client import Client
from config import TEMPORAL_HOST, TASK_QUEUE
from temporal_agent import TemporalAgentWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_workflow_id(task: str) -> str:
    import uuid
    return f"agent-workflow-{uuid.uuid4()}"


async def main():
    print("Temporal Agent Demo")
    print("Monitor at: http://localhost:8233")
    print("Type 'quit' to exit\n")
    
    try:
        client = await Client.connect(TEMPORAL_HOST)
    except Exception as e:
        print(f"Failed to connect to Temporal: {e}")
        return
    
    while True:
        try:
            task = input("Enter task: ").strip()
            
            if task.lower() in ['quit', 'q', 'exit']:
                break
            
            if not task:
                continue
            
            workflow_id = generate_workflow_id(task)
            print("Processing...")
            
            result = await client.execute_workflow(
                TemporalAgentWorkflow.run,
                task,
                id=workflow_id,
                task_queue=TASK_QUEUE
            )
            
            print(f"Result: {result}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
