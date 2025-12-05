#!/usr/bin/env python3
"""
Test the new Day 16 API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(name, url, method="GET", data=None):
    """Test a single endpoint"""
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Success: {result.get('success', False)}")
            return True
        else:
            print(f"✗ Status: {response.status_code}")
            print(f"✗ Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Testing Day 16 API Endpoints")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  python backend/api.py")
    print("\nPress ENTER to continue...")
    input()
    
    results = []
    
    # Test competitive analysis
    results.append(test_endpoint(
        "Competitive Analysis",
        f"{BASE_URL}/api/competitive-analysis"
    ))
    
    # Test elevator pitch
    results.append(test_endpoint(
        "Elevator Pitch",
        f"{BASE_URL}/api/elevator-pitch"
    ))
    
    # Test demo script
    results.append(test_endpoint(
        "Demo Script",
        f"{BASE_URL}/api/demo-script"
    ))
    
    # Test Q&A database
    results.append(test_endpoint(
        "Q&A Database",
        f"{BASE_URL}/api/qa-database"
    ))
    
    # Test Q&A search
    results.append(test_endpoint(
        "Q&A Search",
        f"{BASE_URL}/api/qa-search",
        method="POST",
        data={"keyword": "simulation"}
    ))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print("=" * 60)

if __name__ == "__main__":
    main()
