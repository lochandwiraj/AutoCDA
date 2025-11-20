from temporalio import workflow
from datetime import timedelta
from dataclasses import dataclass
from typing import Optional
import logging

with workflow.unsafe.imports_passed_through():
    from temporal_workflows.simulation_activities import (
        run_simulation_activity,
        validate_netlist_activity,
        SimulationRequest,
        SimulationResult
    )

logger = logging.getLogger(__name__)


@dataclass
class CircuitDesignRequest:
    user_description: str
    design_id: str
    user_id: Optional[str] = None


@dataclass
class CircuitDesignResult:
    success: bool
    design_id: str
    dsl: Optional[str] = None
    skidl_code: Optional[str] = None
    netlist: Optional[str] = None
    simulation_result: Optional[SimulationResult] = None
    error: Optional[str] = None


@workflow.defn
class CircuitDesignWorkflow:

    @workflow.run
    async def run(self, request: CircuitDesignRequest) -> CircuitDesignResult:
        
        logger.info(f"Starting design workflow for: {request.design_id}")
        
        result = CircuitDesignResult(
            success=False,
            design_id=request.design_id
        )
        
        try:
            logger.info("Step 1: Parsing text (mock)")
            logger.info("Step 2: Generating DSL (mock)")
            logger.info("Step 3: Generating SKiDL code (mock)")
            
            logger.info("Step 4: Validating netlist...")
            mock_netlist = """
R1 input output 1k
C1 output 0 159nF
"""
            
            validation = await workflow.execute_activity(
                validate_netlist_activity,
                mock_netlist,
                start_to_close_timeout=timedelta(seconds=10)
            )
            
            if not validation['valid']:
                result.error = f"Netlist validation failed: {validation['errors']}"
                return result
            
            logger.info("Step 5: Running simulation...")
            
            sim_request = SimulationRequest(
                circuit_name="Test Filter",
                netlist_components=mock_netlist,
                analysis_type='ac',
                design_id=request.design_id
            )
            
            simulation_result = await workflow.execute_activity(
                run_simulation_activity,
                sim_request,
                start_to_close_timeout=timedelta(seconds=60)
            )
            
            result.simulation_result = simulation_result
            result.success = simulation_result.success
            if not simulation_result.success:
                result.error = simulation_result.error
            
            logger.info("Workflow complete")
        
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            result.error = str(e)
        
        return result
