# temporal_workflows/worker.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporal_workflows.workflows import CircuitGenerationWorkflow
import os

TASK_QUEUE = "autocda-task-queue"

async def main():
    # Try localhost, but when tools run in Docker use host.docker.internal
    address = os.getenv("TEMPORAL_HOST", "localhost:7233")
    # if user uses Docker Compose, Temporal is exposed at localhost:7233
    client = await Client.connect(address)
    worker = Worker(client, task_queue=TASK_QUEUE, workflows=[CircuitGenerationWorkflow], activities=[])

    print("🚀 AutoCDA Temporal Worker started!")
    print("📋 Task Queue:", TASK_QUEUE)
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
