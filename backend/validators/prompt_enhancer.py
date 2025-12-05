"""
Prompt enhancement for ambiguous or edge case inputs
"""

from typing import Dict


class PromptEnhancer:
    """Enhances prompts for ambiguous or edge case inputs"""
    
    @staticmethod
    def enhance_prompt_for_ambiguity(user_input: str, constraints: Dict[str, str]) -> str:
        """
        Creates enhanced prompt for Claude API when input is ambiguous
        """
        base_prompt = f"""You are designing an electronic circuit based on this description: "{user_input}"

"""
        
        if not constraints:
            base_prompt += """IMPORTANT: This description is ambiguous or lacks specific parameters. Please make reasonable engineering assumptions and clearly state them in your response. If critical information is missing, choose standard/common values and explain why.

"""
        
        base_prompt += """Generate a circuit design in the following JSON format:
{
  "components": [
    {"id": "R1", "type": "resistor", "value": "1k", "nets": ["IN", "OUT"]},
    {"id": "C1", "type": "capacitor", "value": "100n", "nets": ["OUT", "GND"]}
  ],
  "constraints": {
    "cutoff_frequency": "1kHz"
  },
  "assumptions": [
    "Assumed standard supply voltage of 5V",
    "Selected E12 series resistor values"
  ]
}

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no preamble."""
        
        return base_prompt
    
    @staticmethod
    def create_clarification_prompt(user_input: str, missing_info: str) -> str:
        """
        Creates a prompt that asks Claude to identify what's missing
        """
        return f"""The user requested: "{user_input}"

This description is missing critical information: {missing_info}

Please respond with:
1. A list of reasonable default assumptions you would make
2. A brief explanation of why these defaults are standard

Format as JSON:
{{
  "assumptions": ["assumption1", "assumption2"],
  "explanation": "brief explanation"
}}

Return ONLY JSON."""
