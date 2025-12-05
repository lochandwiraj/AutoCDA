import subprocess
from pathlib import Path

def check_git_status():
    """Check if there are uncommitted changes"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("⚠️  Uncommitted changes detected:")
            print(result.stdout)
            return False
        else:
            print("✅ All changes committed")
            return True
        
    except Exception as e:
        print(f"❌ Could not check git status: {e}")
        return False

def check_required_files():
    """Verify all required files exist"""
    required_files = [
        "README.md",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
        ".env.example"
    ]
    
    print("\n📁 Checking required files:")
    all_exist = True
    
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} MISSING")
            all_exist = False
    
    return all_exist

def check_repo_visibility():
    """Check if repo is public (if pushed to remote)"""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            url = result.stdout.strip()
            print(f"\n🌐 Remote URL: {url}")
            print("   ⚠️  Manually verify repository is PUBLIC on GitHub")
            return True
        else:
            print("\n⚠️  No remote repository configured")
            print("   Run: git remote add origin <your-repo-url>")
            return False
        
    except Exception as e:
        print(f"❌ Could not check remote: {e}")
        return False

def check_readme_quality():
    """Basic README quality checks"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("\n❌ README.md not found")
        return False
    
    content = readme_path.read_text()
    
    print("\n📖 README Quality Checks:")
    
    checks = {
        "Has title/heading": content.startswith('#'),
        "Has demo link": 'demo' in content.lower() or 'live' in content.lower(),
        "Has installation instructions": 'install' in content.lower(),
        "Has usage examples": 'usage' in content.lower() or 'example' in content.lower(),
        "Has screenshots/images": '![' in content,
        "Length > 500 chars": len(content) > 500
    }
    
    all_passed = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {check}")
        if not passed:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("=== GitHub Repository Final Check ===\n")
    
    git_clean = check_git_status()
    files_exist = check_required_files()
    has_remote = check_repo_visibility()
    readme_ok = check_readme_quality()
    
    print("\n" + "="*50)
    
    if git_clean and files_exist and has_remote and readme_ok:
        print("✅ Repository is submission-ready!")
    else:
        print("⚠️  Fix the issues above before submitting")
