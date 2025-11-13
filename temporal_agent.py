import os
import logging
from datetime import datetime, timedelta
from temporalio import activity, workflow
from temporalio.common import RetryPolicy
from config import OLLAMA_HOST, OLLAMA_MODEL

logger = logging.getLogger(__name__)


@activity.defn
async def get_time_activity() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@activity.defn
async def get_weather_activity(city: str) -> str:
    import requests
    
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t", timeout=10)
        if response.status_code == 200:
            return f"{city}: {response.text.strip()}"
        return f"Weather unavailable for {city}"
    except requests.RequestException:
        # Let Temporal handle retries
        raise


@activity.defn
async def list_files_activity() -> str:
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    return f"Files: {', '.join(files[:5])}"


@activity.defn
async def get_fact_activity(topic: str) -> str:
    from strands import Agent
    from strands.models.ollama import OllamaModel
    
    agent = Agent(
        model=OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL),
        system_prompt="Provide interesting, accurate facts about the requested topic. Be concise."
    )
    
    result = agent(f"Tell me an interesting fact about {topic}")
    return str(result.content if hasattr(result, 'content') else result)


@activity.defn
async def ai_orchestrator_activity(task: str) -> str:
    from strands import Agent
    from strands.models.ollama import OllamaModel
    
    # TODO: optimize this 
    agent = Agent(
        model=OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL),
        system_prompt="""Analyze the user request and return a comma-separated list of activities.

Available: time, weather:city, files, fact:topic

Examples:
"what time is it" -> "time"
"weather in tokyo" -> "time,weather:tokyo"
"show files and weather in london" -> "time,files,weather:london"

Always include 'time' first. Extract cities/topics accurately."""
    )
    
    try:
        result = agent(task)
        plan = str(result.content if hasattr(result, 'content') else result).strip()
        return plan
    except Exception as e:
        logger.warning(f"AI orchestrator failed: {e}")
        return "time"  # Safe fallback


@workflow.defn
class TemporalAgentWorkflow:
    
    @workflow.run
    async def run(self, task: str) -> str:
        workflow.logger.info(f"Processing: {task}")
        results = []
        
        # Get execution plan from AI
        plan = await workflow.execute_activity(
            ai_orchestrator_activity,
            task,
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=2)
        )
        
        # Execute planned activities
        for activity_spec in plan.split(','):
            activity_spec = activity_spec.strip()
            
            if ':' in activity_spec:
                activity_name, param = activity_spec.split(':', 1)
            else:
                activity_name, param = activity_spec, None
            
            # Execute based on activity type
            if activity_name == 'time':
                result = await workflow.execute_activity(
                    get_time_activity,
                    start_to_close_timeout=timedelta(seconds=5)
                )
                results.append(f"Time: {result}")
            
            elif activity_name == 'weather' and param:
                result = await workflow.execute_activity(
                    get_weather_activity,
                    param,
                    start_to_close_timeout=timedelta(seconds=15),
                    retry_policy=RetryPolicy(maximum_attempts=3)
                )
                results.append(f"Weather: {result}")
            
            elif activity_name == 'files':
                result = await workflow.execute_activity(
                    list_files_activity,
                    start_to_close_timeout=timedelta(seconds=5)
                )
                results.append(f"Files: {result}")
            
            elif activity_name == 'fact' and param:
                result = await workflow.execute_activity(
                    get_fact_activity,
                    param,
                    start_to_close_timeout=timedelta(seconds=20)
                )
                results.append(f"Fact: {result}")
        
        return " | ".join(results)
