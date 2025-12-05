import json
from datetime import datetime
from pathlib import Path

class UserTestingLogger:
    def __init__(self):
        self.log_dir = Path("logs/user_testing")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.events = []

    def log_event(self, event_type, data):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        self.events.append(event)
        self._save()

    def log_input(self, user_input):
        self.log_event("user_input", {"text": user_input})

    def log_confusion(self, element, notes):
        self.log_event("confusion", {"element": element, "notes": notes})

    def log_error_encountered(self, error_msg):
        self.log_event("error", {"message": error_msg})

    def log_success(self, circuit_type):
        self.log_event("success", {"circuit_type": circuit_type})

    def log_feedback(self, rating, comments):
        self.log_event("feedback", {"rating": rating, "comments": comments})

    def _save(self):
        log_file = self.log_dir / f"session_{self.session_id}.json"
        with open(log_file, 'w') as f:
            json.dump({
                "session_id": self.session_id,
                "events": self.events
            }, f, indent=2)

    def get_summary(self):
        total_inputs = sum(1 for e in self.events if e["type"] == "user_input")
        confusions = sum(1 for e in self.events if e["type"] == "confusion")
        errors = sum(1 for e in self.events if e["type"] == "error")
        successes = sum(1 for e in self.events if e["type"] == "success")
        
        return {
            "total_attempts": total_inputs,
            "confusion_points": confusions,
            "errors": errors,
            "successes": successes,
            "success_rate": successes / total_inputs if total_inputs > 0 else 0
        }
