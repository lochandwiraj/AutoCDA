import json
import os
import requests

# Load prompt template
with open('prompts/intent_extraction_prompt.txt', 'r') as f:
    PROMPT_TEMPLATE = f.read()

def extract_intent(user_input):
    """Test intent extraction with Claude via OpenRouter"""
    full_prompt = PROMPT_TEMPLATE + "\n\n" + user_input
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "user", "content": full_prompt}
            ],
            "max_tokens": 1000
        }
    )
    
    if response.status_code != 200:
        return None, f"API Error: {response.status_code} - {response.text}"
    
    response_data = response.json()
    response_text = response_data['choices'][0]['message']['content']
    
    # Try to parse JSON
    try:
        circuit_json = json.loads(response_text)
        return circuit_json, None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}\nRaw response:\n{response_text}"

def test_all_circuits():
    """Test all 3 circuit types"""
    test_cases = [
        {
            "name": "RC Low-Pass Filter",
            "input": "Design a low-pass RC filter with 1kHz cutoff frequency",
            "expected_type": "low_pass_filter"
        },
        {
            "name": "Voltage Divider",
            "input": "Design a voltage divider to convert 9V to 5V",
            "expected_type": "voltage_divider"
        },
        {
            "name": "RC High-Pass Filter",
            "input": "Design a high-pass RC filter with cutoff at 1kHz",
            "expected_type": "high_pass_filter"
        }
    ]
    
    print("=" * 70)
    print("Testing Intent Extraction Prompt")
    print("=" * 70)
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 70)
        print(f"Input: {test['input']}")
        print()
        
        circuit_json, error = extract_intent(test['input'])
        
        if error:
            print(f"❌ FAILED: {error}")
            results.append(False)
        else:
            print("✓ JSON parsed successfully")
            print(f"Circuit Type: {circuit_json.get('circuit_type')}")
            print(f"Components: {len(circuit_json.get('components', []))}")
            print(f"\nFull JSON:")
            print(json.dumps(circuit_json, indent=2))
            
            # Validate expected type
            if circuit_json.get('circuit_type') == test['expected_type']:
                print(f"\n✓ Correct circuit type identified")
                results.append(True)
            else:
                print(f"\n❌ Wrong circuit type. Expected: {test['expected_type']}")
                results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"SUMMARY: {sum(results)}/{len(results)} tests passed")
    print("=" * 70)
    
    return all(results)

if __name__ == '__main__':
    # Make sure API key is set
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: Set OPENROUTER_API_KEY environment variable")
        print("On Windows: set OPENROUTER_API_KEY=your-key-here")
        exit(1)
    
    success = test_all_circuits()
    exit(0 if success else 1)
