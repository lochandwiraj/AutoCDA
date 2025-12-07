"""Test React-Backend Integration"""
import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_generate():
    """Test generate endpoint"""
    print("\nTesting /generate endpoint...")
    payload = {
        "description": "Design a low-pass RC filter with 1kHz cutoff frequency"
    }
    
    try:
        print(f"  Sending: {payload}")
        response = requests.post(
            f"{API_URL}/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"  Status: {response.status_code}")
        
        data = response.json()
        print(f"  Success: {data.get('success')}")
        
        if data.get('success'):
            print(f"  Explanation length: {len(data.get('explanation', ''))}")
            print(f"  Download URL: {data.get('download_url')}")
            print(f"  Filename: {data.get('filename')}")
            return True
        else:
            print(f"  Error: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    print("=" * 60)
    print("AutoCDA Integration Test")
    print("=" * 60)
    
    health_ok = test_health()
    generate_ok = test_generate()
    
    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"Health Check: {'✓ PASS' if health_ok else '✗ FAIL'}")
    print(f"Generate Circuit: {'✓ PASS' if generate_ok else '✗ FAIL'}")
    
    if health_ok and generate_ok:
        print("\n✅ Integration working! React frontend should work now.")
    else:
        print("\n⚠️  Some tests failed. Check backend logs.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
