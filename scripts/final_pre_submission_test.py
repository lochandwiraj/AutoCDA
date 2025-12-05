import subprocess
import sys
from pathlib import Path

def run_all_checks():
    """Run all pre-submission checks"""
    
    checks = [
        ("GitHub Repo Check", "python scripts/github_repo_check.py"),
        ("Submission Checklist", "python scripts/generate_submission_checklist.py"),
        ("Submission Data", "python scripts/prepare_submission_data.py"),
    ]
    
    print("🚀 Running Final Pre-Submission Tests\n")
    print("="*60)
    
    all_passed = True
    
    for name, command in checks:
        print(f"\n▶️  Running: {name}")
        print("-"*60)
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(result.stdout)
            
            if result.returncode != 0:
                print(f"❌ {name} FAILED")
                print(result.stderr)
                all_passed = False
            else:
                print(f"✅ {name} PASSED")
            
        except subprocess.TimeoutExpired:
            print(f"❌ {name} TIMED OUT")
            all_passed = False
        except Exception as e:
            print(f"❌ {name} ERROR: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED - READY FOR SUBMISSION!")
        print("\n📋 Final Manual Checklist:")
        print("   [ ] Submission form filled completely")
        print("   [ ] All URLs copied correctly")
        print("   [ ] Demo video uploaded and public")
        print("   [ ] GitHub repository is public")
        print("   [ ] Slides uploaded and accessible")
        print("   [ ] Screenshot of submission confirmation taken")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - FIX ISSUES BEFORE SUBMITTING")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_checks())
