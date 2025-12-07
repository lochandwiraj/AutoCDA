"""Quick integration test"""
import requests

print("Testing backend connection...")
try:
    # Test health
    health = requests.get("http://localhost:5000/health", timeout=5)
    print(f"✓ Health check: {health.status_code}")
    
    # Test generate with longer timeout
    print("\nTesting circuit generation (this may take 10-15 seconds)...")
    response = requests.post(
        "http://localhost:5000/generate",
        json={"description": "Design a voltage divider from 9V to 5V"},
        timeout=60  # Longer timeout for AI processing
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print("✓ Circuit generated successfully!")
        print(f"  Explanation preview: {data['explanation'][:100]}...")
        print(f"  Download: {data.get('download_url')}")
    else:
        print(f"✗ Error: {data.get('error')}")
        
except requests.exceptions.Timeout:
    print("✗ Request timed out - backend may be slow or API key issue")
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect - is backend running?")
except Exception as e:
    print(f"✗ Error: {e}")
