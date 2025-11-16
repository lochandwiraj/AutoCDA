import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import CircuitGenerationWorkflow
from activities import (
    extract_intent_activity,
    generate_dsl_activity,
    validate_circuit_activity,
    generate_skidl_activity,
    create_schematic_activity,
    run_simulation_activity,
)

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="autocda-task-queue",
        workflows=[CircuitGenerationWorkflow],
        activities=[
            extract_intent_activity,
            generate_dsl_activity,
            validate_circuit_activity,
            generate_skidl_activity,
            create_schematic_activity,
            run_simulation_activity,
        ],
    )

    print("🚀 AutoCDA Temporal Worker started!")
    print("📋 Task Queue: autocda-task-queue")
    print("🔄 Listening for workflows...")

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
