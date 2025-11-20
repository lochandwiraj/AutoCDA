import asyncio
from temporalio.client import Client
from workflows import CircuitGenerationWorkflow

async def test_workflow():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        CircuitGenerationWorkflow.run,
        "Design a simple RC low-pass filter with 1kHz cutoff",
        id="test-workflow-1",
        task_queue="autocda-task-queue",
    )

    print("✅ Workflow completed!")
    print("Result:", result)

if __name__ == '__main__':
    asyncio.run(test_workflow())
