import requests
import json

print("Testing AutoCDA API...")
print("=" * 60)

# Test the generate endpoint
response = requests.post(
    "http://localhost:5000/generate",
    json={"description": "Design a low-pass RC filter with 1kHz cutoff frequency"},
    timeout=30
)

print(f"Status Code: {response.status_code}")
print(f"\nResponse:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 200:
    print("\n✅ API is working!")
else:
    print("\n❌ API returned an error")
