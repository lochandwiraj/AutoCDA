"""
Prepare GitHub repository for public release
"""

import os
import shutil
from pathlib import Path

def clean_repo():
    """Remove sensitive and unnecessary files"""
    
    patterns_to_remove = [
        '*.pyc',
        '__pycache__',
        '.DS_Store',
        '*.log',
        '.env',
        '.env.production',
        '.vscode',
        '.idea'
    ]
    
    print("🧹 Cleaning repository...")
    
    for pattern in patterns_to_remove:
        if '*' in pattern:
            # Glob pattern
            for path in Path('.').rglob(pattern):
                try:
                    if path.is_file():
                        path.unlink()
                        print(f"  Removed: {path}")
                    elif path.is_dir():
                        shutil.rmtree(path)
                        print(f"  Removed dir: {path}")
                except Exception as e:
                    print(f"  Could not remove {path}: {e}")
        else:
            # Specific file/folder
            path = Path(pattern)
            if path.exists():
                try:
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                    print(f"  Removed: {path}")
                except Exception as e:
                    print(f"  Could not remove {path}: {e}")

def create_env_template():
    """Create .env.template"""
    
    template_content = """# OpenRouter API
OPENROUTER_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# File Storage
OUTPUT_DIR=./output
MAX_FILE_AGE_HOURS=24

# Rate Limiting
RATE_LIMIT_ENABLED=False
MAX_REQUESTS_PER_HOUR=100

# Application
BASE_URL=http://localhost:5000
"""
    
    with open('.env.template', 'w') as f:
        f.write(template_content)
    
    print("✅ Created .env.template")

def create_gitignore():
    """Create/update .gitignore"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# Environment
.env
.env.production
.env.local

# Output
output/
output_standalone/
output_api/
output_test/
*.net
*.kicad_*

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary
tmp/
temp/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Updated .gitignore")

def verify_structure():
    """Verify repository structure"""
    
    required_files = [
        'backend/api.py',
        'wsgi.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'README.md'
    ]
    
    required_dirs = [
        'backend',
        'frontend'
    ]
    
    print("\n🔍 Verifying repository structure...")
    
    all_good = True
    
    for file in required_files:
        if not Path(file).exists():
            print(f"  ❌ Missing: {file}")
            all_good = False
        else:
            print(f"  ✅ Found: {file}")
    
    for dir in required_dirs:
        if not Path(dir).exists():
            print(f"  ❌ Missing directory: {dir}")
            all_good = False
        else:
            print(f"  ✅ Found directory: {dir}")
    
    return all_good

if __name__ == '__main__':
    print("🚀 Preparing AutoCDA Repository")
    print("=" * 50)
    
    clean_repo()
    create_env_template()
    create_gitignore()
    
    if verify_structure():
        print("\n✅ Repository is ready for public release!")
        print("\nNext steps:")
        print("1. Review all files for sensitive data")
        print("2. Test fresh clone: git clone <repo> && cd autocda && pip install -r requirements.txt")
        print("3. Push to GitHub: git add . && git commit -m 'Production ready' && git push")
    else:
        print("\n⚠️  Some files are missing. Please review.")
