import json
from pathlib import Path
from datetime import datetime
from enum import Enum

class Priority(Enum):
    P0 = "P0_CRITICAL"
    P1 = "P1_NICE_TO_HAVE"

class IssueTracker:
    def __init__(self):
        self.issues_file = Path("logs/issues.json")
        self.issues = self._load_issues()

    def _load_issues(self):
        if self.issues_file.exists():
            with open(self.issues_file, 'r') as f:
                return json.load(f)
        return []

    def _save_issues(self):
        self.issues_file.parent.mkdir(exist_ok=True)
        with open(self.issues_file, 'w') as f:
            json.dump(self.issues, f, indent=2)

    def add_issue(self, title, description, priority, source="user_testing"):
        issue = {
            "id": len(self.issues) + 1,
            "title": title,
            "description": description,
            "priority": priority.value,
            "source": source,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "resolved_at": None
        }
        self.issues.append(issue)
        self._save_issues()
        return issue

    def resolve_issue(self, issue_id, resolution_notes=""):
        for issue in self.issues:
            if issue["id"] == issue_id:
                issue["status"] = "resolved"
                issue["resolved_at"] = datetime.now().isoformat()
                issue["resolution_notes"] = resolution_notes
                self._save_issues()
                return issue
        return None

    def get_open_p0_issues(self):
        return [i for i in self.issues if i["status"] == "open" and i["priority"] == Priority.P0.value]

    def get_open_p1_issues(self):
        return [i for i in self.issues if i["status"] == "open" and i["priority"] == Priority.P1.value]

    def get_all_open_issues(self):
        return [i for i in self.issues if i["status"] == "open"]
