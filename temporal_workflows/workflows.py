from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import (
        extract_intent_activity,
        generate_dsl_activity,
        validate_circuit_activity,
        generate_skidl_activity,
        create_schematic_activity,
        run_simulation_activity,
    )

@workflow.defn
class CircuitGenerationWorkflow:
    """Main workflow for circuit generation pipeline"""

    @workflow.run
    async def run(self, user_input: str) -> dict:

        retry_policy = RetryPolicy(
            maximum_attempts=3,
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
        )

        workflow.logger.info(f"🎬 Starting circuit generation for: {user_input}")

        intent = await workflow.execute_activity(
            extract_intent_activity,
            user_input,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )

        dsl = await workflow.execute_activity(
            generate_dsl_activity,
            intent,
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=retry_policy,
        )

        validation_result = await workflow.execute_activity(
            validate_circuit_activity,
            dsl,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=retry_policy,
        )

        skidl_code = await workflow.execute_activity(
            generate_skidl_activity,
            dsl,
            start_to_close_timeout=timedelta(seconds=20),
            retry_policy=retry_policy,
        )

        schematic_path = await workflow.execute_activity(
            create_schematic_activity,
            skidl_code,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )

        simulation_results = await workflow.execute_activity(
            run_simulation_activity,
            skidl_code,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )

        return {
            "intent": intent,
            "dsl": dsl,
            "validation": validation_result,
            "skidl_code": skidl_code,
            "schematic_path": schematic_path,
            "simulation_results": simulation_results,
            "status": "success"
        }
