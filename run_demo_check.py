#!/usr/bin/env python3
"""
Pre-event demo verification script
Run this before presentation
"""

import sys
from pathlib import Path

def verify_demo_readiness():
    """Verify all demo components are ready"""
    checks = {
        "Backend API script": Path("backend/api.py").exists(),
        "Frontend app": Path("frontend/app.py").exists(),
        "Demo script": Path("demo_script.py").exists(),
        "Q&A responses": Path("qa_responses.py").exists(),
        "Environment file": Path(".env").exists(),
        "Requirements": Path("requirements.txt").exists()
    }
    
    print("\n" + "=" * 60)
    print("DEMO READINESS CHECK")
    print("=" * 60)
    
    all_passed = True
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
        if not status:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("✓ ALL SYSTEMS READY FOR DEMO")
    else:
        print("✗ SOME CHECKS FAILED - REVIEW ABOVE")
    
    print("=" * 60 + "\n")
    
    return all_passed

def main():
    print("\n🚀 AutoCDA Demo Verification\n")
    
    if not verify_demo_readiness():
        print("\n❌ Demo readiness check failed!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("FINAL PRE-DEMO CHECKLIST")
    print("=" * 60)
    print("[ ] Backend running: python backend/api.py")
    print("[ ] Frontend running: streamlit run frontend/app.py")
    print("[ ] Browser open: http://localhost:8501")
    print("[ ] Test circuit generated successfully")
    print("[ ] KiCad installed and tested")
    print("[ ] Demo script reviewed")
    print("[ ] Q&A responses memorized")
    print("=" * 60)
    
    print("\n✅ DEMO SYSTEM READY - GOOD LUCK! 🎉\n")

if __name__ == "__main__":
    main()
