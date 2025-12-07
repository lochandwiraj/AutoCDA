"""Test React frontend setup"""
import os
import subprocess
import time
import requests

def test_backend():
    """Test if backend is accessible"""
    print("Testing backend API...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend API is running")
            return True
        else:
            print("✗ Backend returned status:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running. Start it with: python backend/api.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_react_files():
    """Test if React files exist"""
    print("\nChecking React files...")
    required_files = [
        "client/package.json",
        "client/src/App.jsx",
        "client/src/App.css",
        "client/src/main.jsx",
        "client/vite.config.js"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist

def test_node_modules():
    """Test if node_modules is installed"""
    print("\nChecking Node.js dependencies...")
    if os.path.exists("client/node_modules"):
        print("✓ node_modules installed")
        return True
    else:
        print("✗ node_modules not found. Run: cd client && npm install")
        return False

def main():
    print("=" * 60)
    print("AutoCDA React Setup Test")
    print("=" * 60)
    print()
    
    backend_ok = test_backend()
    files_ok = test_react_files()
    deps_ok = test_node_modules()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"Backend API: {'✓ OK' if backend_ok else '✗ Not Running'}")
    print(f"React Files: {'✓ OK' if files_ok else '✗ Missing Files'}")
    print(f"Dependencies: {'✓ OK' if deps_ok else '✗ Not Installed'}")
    
    if backend_ok and files_ok and deps_ok:
        print("\n✅ All checks passed! Ready to run:")
        print("   Windows: start-react.bat")
        print("   Linux/Mac: ./start-react.sh")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
