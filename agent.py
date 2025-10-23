import os
from datetime import datetime, timedelta
from temporalio import activity, workflow
from temporalio.common import RetryPolicy


@activity.defn
async def read_file_activity(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


@activity.defn
async def list_files_activity(directory: str = ".") -> str:
    files = os.listdir(directory)
    return "\n".join(files)


@activity.defn
async def get_time_activity() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@activity.defn
async def ollama_chat_activity(prompt: str, model: str = "llama3.2:latest") -> str:
    import ollama
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']


@workflow.defn
class OllamaAgentWorkflow:
    
    def _get_retry_policy(self) -> RetryPolicy:
        return RetryPolicy(
            maximum_attempts=3,
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10)
        )
    
    def _extract_filename(self, task: str) -> str:
        words = task.split()
        return words[-1] if len(words) > 1 else "requirements.txt"
    
    @workflow.run
    async def run(self, task: str) -> str:
        retry_policy = self._get_retry_policy()
        task_lower = task.lower()
        
        if "read file" in task_lower:
            filename = self._extract_filename(task)
            return await workflow.execute_activity(
                read_file_activity,
                filename,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy
            )
        
        if "list files" in task_lower:
            return await workflow.execute_activity(
                list_files_activity,
                ".",
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy
            )
        
        if "time" in task_lower:
            return await workflow.execute_activity(
                get_time_activity,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry_policy
            )
        
        return await workflow.execute_activity(
            ollama_chat_activity,
            task,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy
        )
