import requests
import time
import sys
from pathlib import Path

BASE_URL = "http://localhost:5000"  # Change to your production URL

TEST_CASES = [
    "Design a low-pass RC filter with 1kHz cutoff",
    "Create a voltage divider that converts 9V to 5V",
    "Design a high-pass RC filter with 500Hz cutoff"
]

def test_endpoint():
    """Test all circuit generations"""
    print("🧪 Testing AutoCDA Production Deployment...")
    
    for i, test_input in enumerate(TEST_CASES, 1):
        print(f"\n📝 Test {i}: {test_input}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/generate",
                json={"description": test_input},
                timeout=30
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS ({elapsed:.2f}s)")
                print(f"   - Explanation length: {len(data.get('explanation', ''))}")
                print(f"   - Download URL: {data.get('download_url', 'N/A')}")
            else:
                print(f"❌ FAILED: Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return False
    
    print("\n✅ All tests passed!")
    return True

def check_health():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    if not check_health():
        print("❌ Server is not responding. Start the application first.")
        sys.exit(1)
    
    success = test_endpoint()
    sys.exit(0 if success else 1)
