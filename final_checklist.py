"""
Pre-deployment final checklist
"""

import os
from pathlib import Path
import subprocess

def check_item(name, condition, fix_msg=""):
    status = "✅" if condition else "❌"
    print(f"{status} {name}")
    if not condition and fix_msg:
        print(f"   Fix: {fix_msg}")
    return condition

def run_checklist():
    print("🔍 AutoCDA Pre-Deployment Checklist")
    print("=" * 50)
    
    checks = []
    
    # Environment
    print("\n📋 Environment Configuration:")
    checks.append(check_item(
        ".env.example exists",
        Path('.env.example').exists(),
        "Create .env.example file"
    ))
    checks.append(check_item(
        ".env.production exists",
        Path('.env.production').exists(),
        "Create .env.production with your API key"
    ))
    
    # Files
    print("\n📋 Required Files:")
    required = ['backend/api.py', 'wsgi.py', 'requirements.txt', 'Procfile', 'README.md', 'LICENSE']
    for file in required:
        checks.append(check_item(
            f"{file} exists",
            Path(file).exists()
        ))
    
    # Backend modules
    print("\n📋 Backend Modules:")
    backend_modules = [
        'intent_extractor',
        'dsl_generator',
        'circuit_validator',
        'explainer',
        'skidl_generator',
        'file_manager'
    ]
    for module in backend_modules:
        checks.append(check_item(
            f"backend/{module}.py exists",
            Path(f'backend/{module}.py').exists()
        ))
    
    # Dependencies
    print("\n📋 Dependencies:")
    try:
        import flask
        checks.append(check_item("Flask installed", True))
    except:
        checks.append(check_item("Flask installed", False, "pip install flask"))
    
    try:
        import pydantic
        checks.append(check_item("Pydantic installed", True))
    except:
        checks.append(check_item("Pydantic installed", False, "pip install pydantic"))
    
    try:
        import skidl
        checks.append(check_item("SKiDL installed", True))
    except:
        checks.append(check_item("SKiDL installed", False, "pip install skidl"))
    
    # Git
    print("\n📋 Git Repository:")
    checks.append(check_item(
        ".git exists",
        Path('.git').exists(),
        "Run: git init"
    ))
    checks.append(check_item(
        ".gitignore exists",
        Path('.gitignore').exists(),
        "Run: python prepare_repo.py"
    ))
    
    # Security
    print("\n📋 Security:")
    if Path('.git').exists():
        git_files = subprocess.getoutput('git ls-files')
        checks.append(check_item(
            "No .env in repo",
            '.env' not in git_files and '.env.production' not in git_files,
            "Run: git rm --cached .env .env.production"
        ))
    else:
        checks.append(check_item("No .env in repo", True))
    
    # Results
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100
    
    print(f"Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready for deployment.")
        return True
    else:
        print(f"\n⚠️  {total - passed} issue(s) need attention before deployment.")
        return False

if __name__ == '__main__':
    success = run_checklist()
    exit(0 if success else 1)
