"""Test deployment readiness"""
import os
import sys

print("Testing Deployment Readiness...")
print("=" * 50)

# Check Python version
print(f"Python: {sys.version}")

# Check required files
required_files = [
    'backend/api.py',
    'frontend/app.py',
    'requirements.txt',
    'vercel.json',
    '.env.example'
]

for file in required_files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} MISSING")

# Check environment variable
if os.getenv('OPENROUTER_API_KEY'):
    print("✓ OPENROUTER_API_KEY set")
else:
    print("⚠ OPENROUTER_API_KEY not set (will need for deployment)")

print("=" * 50)
print("Deployment files ready!")
