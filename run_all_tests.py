import subprocess
import sys

def run_test(test_name, test_path):
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, test_path], capture_output=False)
    
    return result.returncode == 0

def main():
    tests = [
        ("End-to-End Integration", "tests/test_end_to_end.py"),
        ("KiCad Output Verification", "tests/verify_kicad_output.py"),
    ]
    
    results = []
    
    for test_name, test_path in tests:
        passed = run_test(test_name, test_path)
        results.append((test_name, passed))
    
    print(f"\n{'='*60}")
    print("FINAL TEST RESULTS")
    print(f"{'='*60}")
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed_count = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed_count}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed_count < total:
        sys.exit(1)

if __name__ == "__main__":
    main()
