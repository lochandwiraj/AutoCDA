import subprocess
from datetime import datetime
from pathlib import Path
import json

def create_code_freeze():
    """Lock codebase - no more changes after this"""
    
    print("🔒 INITIATING CODE FREEZE")
    print("="*60)
    
    # Check for uncommitted changes
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("⚠️  You have uncommitted changes:")
        print(result.stdout)
        
        response = input("\nCommit all changes? (yes/no): ")
        if response.lower() == 'yes':
            subprocess.run(["git", "add", "."])
            subprocess.run([
                "git", "commit", "-m",
                f"CODE FREEZE - Pre-event final version - {datetime.now().isoformat()}"
            ])
            print("✅ Changes committed")
        else:
            print("❌ Code freeze aborted")
            return False
    
    # Create freeze tag
    freeze_tag = f"pre-event-freeze-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    subprocess.run([
        "git", "tag", "-a", freeze_tag,
        "-m", "Code freeze before hackathon event"
    ])
    
    print(f"\n✅ Code freeze tag created: {freeze_tag}")
    
    # Push to remote
    response = input("\nPush to remote repository? (yes/no): ")
    if response.lower() == 'yes':
        subprocess.run(["git", "push"])
        subprocess.run(["git", "push", "--tags"])
        print("✅ Pushed to remote")
    
    # Create freeze manifest
    freeze_manifest = {
        "frozen_at": datetime.now().isoformat(),
        "tag": freeze_tag,
        "message": "NO CODE CHANGES AFTER THIS POINT",
        "allowed_actions": [
            "Testing existing features",
            "Reviewing documentation",
            "Practicing presentation",
            "Charging devices",
            "Resting"
        ],
        "forbidden_actions": [
            "Adding new features",
            "Refactoring code",
            "Changing UI design",
            "Modifying dependencies",
            "Editing configuration"
        ]
    }
    
    manifest_path = Path("CODE_FREEZE_MANIFEST.json")
    manifest_path.write_text(json.dumps(freeze_manifest, indent=2))
    
    print(f"\n✅ Freeze manifest created: {manifest_path}")
    print("\n" + "="*60)
    print("🔒 CODE IS NOW FROZEN")
    print("="*60)
    print("\n✅ ALLOWED:")
    for action in freeze_manifest["allowed_actions"]:
        print(f"   ✓ {action}")
    
    print("\n❌ FORBIDDEN:")
    for action in freeze_manifest["forbidden_actions"]:
        print(f"   ✗ {action}")
    
    print("\n💤 Go rest. You're ready for the event.")
    
    return True

if __name__ == "__main__":
    create_code_freeze()
