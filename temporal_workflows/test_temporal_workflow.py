import asyncio
from temporalio.client import Client
from temporal_workflows.circuit_design_workflow import (
    CircuitDesignWorkflow,
    CircuitDesignRequest
)


async def test_workflow():
    
    print("Connecting to Temporal...")
    client = await Client.connect("localhost:7233")
    
    print("Starting workflow...")
    request = CircuitDesignRequest(
        user_description="Design a 1kHz RC low-pass filter",
        design_id="test-001",
        user_id="user-123"
    )
    
    result = await client.execute_workflow(
        CircuitDesignWorkflow.run,
        request,
        id=f"circuit-design-{request.design_id}",
        task_queue="circuit-design-queue"
    )
    
    print("\n==============================")
    print("WORKFLOW RESULT")
    print("==============================")
    
    if result.success:
        print("SUCCESS!")
        print("\nSimulation Metrics:")
        for k, v in result.simulation_result.metrics.items():
            print(f"   {k}: {v}")
    else:
        print(f"FAILED: {result.error}")


if __name__ == "__main__":
    asyncio.run(test_workflow())
