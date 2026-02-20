import os
from dotenv import load_dotenv  ### NEW: Import dotenv

# ### NEW: Load environment variables from .env file
load_dotenv()

# Core configuration
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost:7233")
TASK_QUEUE = "strands-temporal-agent-queue"

# AWS Bedrock configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-20250514-v1:0")

# Docker configuration
DOCKER_HOST = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")

# ### NEW: Safer integer conversion to prevent crashes
try:
    DOCKER_TIMEOUT = int(os.getenv("DOCKER_TIMEOUT", "30"))
except ValueError:
    print("Warning: Invalid DOCKER_TIMEOUT format. Using default 30s.")
    DOCKER_TIMEOUT = 30

# Docker Monitor Task Queue
DOCKER_MONITOR_TASK_QUEUE = "docker-monitor-queue"

# Operation timeouts (seconds)
STATUS_CHECK_TIMEOUT = 10
HEALTH_CHECK_TIMEOUT = 15
LOG_RETRIEVAL_TIMEOUT = 10
RESTART_TIMEOUT = 30
AI_ORCHESTRATOR_TIMEOUT = 15

# Resource thresholds for health checks
CPU_THRESHOLD_PERCENT = 90.0
MEMORY_THRESHOLD_PERCENT = 90.0
RESTART_COUNT_THRESHOLD = 5

# Timeouts (legacy - for existing agents)
WEATHER_TIMEOUT = 15
