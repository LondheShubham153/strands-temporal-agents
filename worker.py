import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from config import TEMPORAL_HOST, TASK_QUEUE
from temporal_agent import (
    TemporalAgentWorkflow,
    ai_orchestrator_activity,
    get_time_activity,
    get_weather_activity,
    list_files_activity,
    get_fact_activity
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await Client.connect(TEMPORAL_HOST)
    
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[TemporalAgentWorkflow],
        activities=[
            ai_orchestrator_activity,
            get_time_activity,
            get_weather_activity,
            list_files_activity,
            get_fact_activity
        ]
    )
    
    logger.info(f"Worker started on queue: {TASK_QUEUE}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
