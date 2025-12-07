#!/usr/bin/env python3
"""
Vercel Deployment Readiness Check
Tests that all required files and configurations are in place
"""

import os
import json
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_json_valid(filepath):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print(f"✅ Valid JSON: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Invalid JSON: {filepath} - {e}")
        return False

def check_env_file(filepath):
    """Check if env file has required variables"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        has_api_url = 'VITE_API_URL' in content
        status = "✅" if has_api_url else "❌"
        print(f"{status} {filepath} contains VITE_API_URL")
        return has_api_url
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 VERCEL DEPLOYMENT READINESS CHECK")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Check critical files
    print("📁 Checking Critical Files...")
    all_checks.append(check_file_exists("vercel.json", "Vercel config"))
    all_checks.append(check_file_exists("requirements.txt", "Python dependencies"))
    all_checks.append(check_file_exists("client/package.json", "Node dependencies"))
    all_checks.append(check_file_exists("backend/api.py", "Backend API"))
    all_checks.append(check_file_exists("client/src/App.jsx", "Frontend App"))
    print()
    
    # Check JSON validity
    print("📋 Checking JSON Files...")
    all_checks.append(check_json_valid("vercel.json"))
    all_checks.append(check_json_valid("client/package.json"))
    print()
    
    # Check environment files
    print("🔐 Checking Environment Files...")
    all_checks.append(check_file_exists("client/.env.production", "Production env"))
    all_checks.append(check_file_exists("client/.env.development", "Development env"))
    if os.path.exists("client/.env.production"):
        all_checks.append(check_env_file("client/.env.production"))
    if os.path.exists("client/.env.development"):
        all_checks.append(check_env_file("client/.env.development"))
    print()
    
    # Check App.jsx uses dynamic API URL
    print("🔗 Checking API Configuration...")
    try:
        with open("client/src/App.jsx", 'r', encoding='utf-8') as f:
            content = f.read()
        uses_env = 'import.meta.env.VITE_API_URL' in content
        status = "✅" if uses_env else "❌"
        print(f"{status} App.jsx uses dynamic API URL")
        all_checks.append(uses_env)
    except Exception as e:
        print(f"❌ Error checking App.jsx: {e}")
        all_checks.append(False)
    print()
    
    # Check documentation
    print("📚 Checking Documentation...")
    all_checks.append(check_file_exists("README.md", "README"))
    all_checks.append(check_file_exists("DEPLOYMENT.md", "Deployment guide"))
    all_checks.append(check_file_exists("VERCEL_CHECKLIST.md", "Deployment checklist"))
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print()
        print("🎉 Your project is ready for Vercel deployment!")
        print()
        print("Next steps:")
        print("1. Push to Git: git add . && git commit -m 'Ready for Vercel' && git push")
        print("2. Go to: https://vercel.com/new")
        print("3. Import your repository")
        print("4. Add environment variable: OPENROUTER_API_KEY")
        print("5. Click Deploy!")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed}/{total})")
        print()
        print("Please fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
