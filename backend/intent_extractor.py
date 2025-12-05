import json
import os
import time
import requests
from typing import Dict, Optional


class IntentExtractor:
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def extract_circuit_intent(self, user_input: str) -> Optional[Dict]:
        """
        Extract circuit intent from user's natural language description.
        Returns JSON with components, values, and constraints.
        """
        prompt = self._build_extraction_prompt(user_input)
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url=self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 500
                    }
                )
                
                if response.status_code != 200:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    continue
                
                # Extract JSON from response
                response_data = response.json()
                response_text = response_data['choices'][0]['message']['content']
                circuit_json = self._parse_json_response(response_text)
                
                if circuit_json:
                    return circuit_json
                else:
                    print(f"Attempt {attempt + 1}: Failed to parse valid JSON")
                
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1}: Request Error - {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                print(f"Attempt {attempt + 1}: Unexpected error - {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return None
    
    def _build_extraction_prompt(self, user_input: str) -> str:
        return f"""You are a circuit design assistant. Extract circuit information from the user's description and return ONLY valid JSON with no additional text, no markdown backticks, no preamble.

User's circuit description: "{user_input}"

Return JSON with this exact structure:
{{
  "circuit_type": "rc_lowpass" | "rc_highpass" | "voltage_divider",
  "components": [
    {{
      "id": "R1",
      "type": "resistor",
      "value": "1k",
      "nets": ["IN", "N1"]
    }},
    {{
      "id": "C1",
      "type": "capacitor",
      "value": "159n",
      "nets": ["N1", "GND"]
    }}
  ],
  "constraints": {{
    "cutoff_freq": "1000" (for filters, in Hz),
    "input_voltage": "9" (for dividers, in V),
    "output_voltage": "5" (for dividers, in V)
  }}
}}

Rules:
- Only support these circuit types: rc_lowpass, rc_highpass, voltage_divider
- Component IDs must be unique (R1, R2, C1, etc.)
- Nets must include "IN" for input, "GND" for ground
- Values should be numeric with units (k, n, u, m)
- Return ONLY the JSON, nothing else"""
    
    def _parse_json_response(self, response_text: str) -> Optional[Dict]:
        """
        Parse JSON from Claude's response, handling various formats.
        """
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith("```"):
                # Remove opening backticks
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text.rsplit("\n", 1)[0] if "\n" in text else text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            circuit_json = json.loads(text)
            
            # Basic validation
            if not isinstance(circuit_json, dict):
                return None
            if "circuit_type" not in circuit_json:
                return None
            if "components" not in circuit_json:
                return None
            
            return circuit_json
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {str(e)}")
            print(f"Response text: {response_text[:200]}...")
            return None
        except Exception as e:
            print(f"Unexpected parsing error: {str(e)}")
            return None


# Test function
def test_intent_extractor():
    """Test the intent extractor with sample inputs."""
    extractor = IntentExtractor()
    
    test_cases = [
        "Design a low-pass RC filter with 1kHz cutoff",
        "I need a high-pass filter at 500Hz",
        "Create a voltage divider that converts 9V to 5V",
        "Make an RC low-pass filter for audio, cutoff should be 2kHz",
        "Voltage divider from 12V to 3.3V",
    ]
    
    print("Testing Intent Extractor...")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_input}")
        print("-" * 60)
        
        result = extractor.extract_circuit_intent(test_input)
        
        if result:
            print("✓ SUCCESS")
            print(json.dumps(result, indent=2))
        else:
            print("✗ FAILED - No valid result returned")
        
        print()


if __name__ == "__main__":
    # Check for API key
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY environment variable not set")
        print("Set it with: set OPENROUTER_API_KEY=your-key-here")
    else:
        test_intent_extractor()
