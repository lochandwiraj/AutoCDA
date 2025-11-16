# temporal_workflows/activities.py
from temporalio import activity
import time
from app.services.llm_service import openrouter_generate

@activity.defn
async def extract_intent_activity(user_input: str) -> dict:
    activity.logger.info("Extracting intent (stub)")
    # stub: return small structured intent
    return {"raw": user_input, "intent": "generate_rc_lowpass"}

@activity.defn
async def generate_dsl_activity(intent: dict) -> dict:
    activity.logger.info("Generating DSL (stub)")
    # stub sample DSL
    return {"dsl": {"type": "rc_lowpass", "fc": "1kHz"}}

@activity.defn
async def validate_circuit_activity(dsl: dict) -> dict:
    activity.logger.info("Validating circuit (stub)")
    return {"valid": True, "errors": [], "warnings": []}

@activity.defn
async def generate_skidl_activity(dsl: dict) -> str:
    activity.logger.info("Generating SKiDL (stub)")
    skidl = "# SKiDL placeholder for " + str(dsl)
    return skidl

@activity.defn
async def create_schematic_activity(skidl_code: str) -> str:
    activity.logger.info("Creating schematic (stub)")
    return "/output/schematic.kicad_sch"

@activity.defn
async def run_simulation_activity(skidl_code: str) -> dict:
    activity.logger.info("Running simulation (stub)")
    time.sleep(1)
    return {"results": "ok", "success": True}
