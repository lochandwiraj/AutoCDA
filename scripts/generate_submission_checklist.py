from datetime import datetime
from pathlib import Path
import json

def generate_submission_checklist():
    """Generate pre-submission checklist"""
    
    checklist = {
        "timestamp": datetime.now().isoformat(),
        "critical_checks": [
            {
                "item": "GitHub repository is public",
                "verified": False,
                "url": "TODO: Add your GitHub repo URL"
            },
            {
                "item": "README.md is complete and formatted",
                "verified": False,
                "file": "README.md"
            },
            {
                "item": "Demo video is uploaded and accessible",
                "verified": False,
                "url": "TODO: Add video URL (YouTube/Vimeo)"
            },
            {
                "item": "Live demo is deployed and accessible",
                "verified": False,
                "url": "TODO: Add production URL"
            },
            {
                "item": "requirements.txt includes all dependencies",
                "verified": False,
                "file": "requirements.txt"
            },
            {
                "item": "Environment variables are documented",
                "verified": False,
                "file": ".env.example"
            },
            {
                "item": "All links in README are clickable and working",
                "verified": False,
                "command": "python scripts/verify_links.py"
            },
            {
                "item": "Presentation slides are finalized",
                "verified": False,
                "file": "TODO: Add slides filename"
            },
            {
                "item": "License file exists",
                "verified": False,
                "file": "LICENSE"
            }
        ],
        "submission_fields": {
            "project_name": "AutoCDA - AI Circuit Design Assistant",
            "tagline": "Convert natural language to electronic schematics instantly",
            "description": "TODO: 200-word description for submission form",
            "tech_stack": [
                "Python",
                "Flask",
                "OpenRouter API",
                "SKiDL",
                "KiCad",
                "Streamlit"
            ],
            "category": "TODO: Primary category",
            "demo_url": "TODO: Live demo URL",
            "video_url": "TODO: Demo video URL",
            "repo_url": "TODO: GitHub repository URL",
            "slides_url": "TODO: Presentation slides URL"
        }
    }
    
    output_path = Path("submission_checklist.json")
    output_path.write_text(json.dumps(checklist, indent=2))
    
    print("✅ Submission checklist generated: submission_checklist.json")
    print("\n📋 Critical Checks:")
    for i, check in enumerate(checklist["critical_checks"], 1):
        print(f"   {i}. [ ] {check['item']}")
    
    return checklist

if __name__ == "__main__":
    generate_submission_checklist()
