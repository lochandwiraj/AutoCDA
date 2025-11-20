import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from temporal_workflows.simulation_activities import (
    run_simulation_activity,
    validate_netlist_activity
)
from temporal_workflows.circuit_design_workflow import CircuitDesignWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await Client.connect("localhost:7233")
    
    logger.info("Starting Temporal worker...")
    
    worker = Worker(
        client,
        task_queue="circuit-design-queue",
        workflows=[CircuitDesignWorkflow],
        activities=[
            run_simulation_activity,
            validate_netlist_activity
        ]
    )
    
    logger.info("Worker is ready.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
