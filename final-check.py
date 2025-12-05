#!/usr/bin/env python3
"""
AutoCDA Final System Check - Day 19
Run this to verify everything is ready
"""

import os
import sys
from pathlib import Path

def check_demo_video():
    """Check if demo video exists"""
    video_path = Path("./backup/demo-video.mp4")
    if video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"✓ Demo video exists ({size_mb:.1f}MB)")
        return True
    else:
        print("⚠ Demo video NOT FOUND (optional)")
        return True  # Not critical

def check_presentation():
    """Check if presentation files exist"""
    script_path = Path("./presentation-script.txt")
    if script_path.exists():
        print("✓ Presentation script exists")
        return True
    else:
        print("✗ Presentation script NOT FOUND")
        return False

def check_contingency():
    """Check contingency files"""
    files = [
        "event-checklist.txt",
        "contingency-plan.txt",
        "qa-responses.txt"
    ]
    all_exist = True
    for file in files:
        if Path(file).exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} NOT FOUND")
            all_exist = False
    return all_exist

def check_offline_mode():
    """Check if offline mode is ready"""
    offline_path = Path("backend/offline_circuits.py")
    if offline_path.exists():
        print("✓ Offline circuits module exists")
        return True
    else:
        print("✗ Offline circuits NOT FOUND")
        return False

def check_localhost():
    """Check if localhost dependencies work"""
    try:
        import flask
        import pydantic
        print("✓ Core Python dependencies installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def check_bonus_docs():
    """Check bonus documentation"""
    bonus_files = [
        "bonus_qualification_report.json",
        "bonus_submission_summaries.json"
    ]
    count = sum(1 for f in bonus_files if Path(f).exists())
    if count >= 1:
        print(f"✓ {count} bonus documentation files exist")
        return True
    else:
        print("⚠ No bonus documentation (optional)")
        return True  # Not critical

def main():
    print("=" * 50)
    print("AutoCDA Final System Check - Day 19")
    print("=" * 50)
    print()
    
    checks = []
    
    print("Checking presentation materials...")
    checks.append(check_presentation())
    checks.append(check_contingency())
    print()
    
    print("Checking backup materials...")
    checks.append(check_demo_video())
    checks.append(check_offline_mode())
    print()
    
    print("Checking local environment...")
    checks.append(check_localhost())
    print()
    
    print("Checking bonus materials...")
    checks.append(check_bonus_docs())
    print()
    
    print("=" * 50)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✓ ALL CHECKS PASSED ({passed}/{total})")
        print("You are READY for the event!")
    elif passed >= total - 2:
        print(f"⚠ MOSTLY READY ({passed}/{total})")
        print("Fix remaining issues but you're in good shape")
    else:
        print(f"✗ NEEDS ATTENTION ({passed}/{total})")
        print("Address failed checks before event")
    
    print("=" * 50)
    
    return 0 if passed >= total - 1 else 1

if __name__ == "__main__":
    sys.exit(main())
