from temporalio import activity
from simulation_engine.pipeline import SimulationPipeline
from dataclasses import dataclass
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class SimulationRequest:
    circuit_name: str
    netlist_components: str
    analysis_type: str = 'ac'
    design_id: str = None


@dataclass
class SimulationResult:
    success: bool
    circuit_name: str
    metrics: Optional[Dict] = None
    report_html: Optional[str] = None
    error: Optional[str] = None
    design_id: Optional[str] = None


@activity.defn
async def run_simulation_activity(request: SimulationRequest) -> SimulationResult:
    logger.info(f"Starting simulation for: {request.circuit_name}")
    
    try:
        pipeline = SimulationPipeline()
        
        result = pipeline.run_complete_analysis(
            circuit_name=request.circuit_name,
            netlist_components=request.netlist_components,
            analysis_type=request.analysis_type
        )
        
        return SimulationResult(
            success=result['success'],
            circuit_name=request.circuit_name,
            metrics=result.get('metrics'),
            report_html=result.get('report_html'),
            error=result.get('error'),
            design_id=request.design_id
        )
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        return SimulationResult(
            success=False,
            circuit_name=request.circuit_name,
            error=str(e),
            design_id=request.design_id
        )


@activity.defn
async def validate_netlist_activity(netlist: str) -> Dict:
    logger.info("Validating netlist...")
    
    validation = {
        'valid': True,
        'warnings': [],
        'errors': []
    }
    
    if not netlist.strip():
        validation['valid'] = False
        validation['errors'].append("Empty netlist")
        return validation
    
    lines = netlist.strip().split('\n')
    
    has_components = any(line.strip() and not line.startswith('*') for line in lines)
    if not has_components:
        validation['valid'] = False
        validation['errors'].append("No components found")
    
    if 'input' not in netlist.lower():
        validation['warnings'].append("No 'input' node found")
    
    if 'output' not in netlist.lower():
        validation['warnings'].append("No 'output' node found")
    
    if '0' not in netlist and 'GND' not in netlist.upper():
        validation['warnings'].append("No ground node found")
    
    logger.info(f"Validation complete: {'OK' if validation['valid'] else 'FAIL'}")
    return validation
