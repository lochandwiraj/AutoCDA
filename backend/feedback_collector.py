from pathlib import Path
import json
from datetime import datetime

class FeedbackCollector:
    def __init__(self):
        self.feedback_dir = Path("logs/feedback")
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

    def collect_feedback(self, user_id, feedback_data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        feedback_file = self.feedback_dir / f"feedback_{user_id}_{timestamp}.json"
        
        feedback = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "ease_of_use": feedback_data.get("ease_of_use", 0),
            "explanation_clarity": feedback_data.get("explanation_clarity", 0),
            "result_quality": feedback_data.get("result_quality", 0),
            "confusion_points": feedback_data.get("confusion_points", []),
            "suggestions": feedback_data.get("suggestions", ""),
            "would_use_again": feedback_data.get("would_use_again", False),
            "comments": feedback_data.get("comments", "")
        }
        
        with open(feedback_file, 'w') as f:
            json.dump(feedback, f, indent=2)
        
        return feedback_file

    def get_all_feedback(self):
        feedback_files = list(self.feedback_dir.glob("feedback_*.json"))
        all_feedback = []
        
        for file in feedback_files:
            with open(file, 'r') as f:
                all_feedback.append(json.load(f))
        
        return all_feedback

    def get_feedback_summary(self):
        all_feedback = self.get_all_feedback()
        
        if not all_feedback:
            return {"message": "No feedback collected yet"}
        
        total = len(all_feedback)
        avg_ease = sum(f.get("ease_of_use", 0) for f in all_feedback) / total
        avg_clarity = sum(f.get("explanation_clarity", 0) for f in all_feedback) / total
        avg_quality = sum(f.get("result_quality", 0) for f in all_feedback) / total
        would_use = sum(1 for f in all_feedback if f.get("would_use_again", False))
        
        all_confusions = []
        for f in all_feedback:
            all_confusions.extend(f.get("confusion_points", []))
        
        confusion_counts = {}
        for c in all_confusions:
            confusion_counts[c] = confusion_counts.get(c, 0) + 1
        
        return {
            "total_responses": total,
            "average_ease_of_use": round(avg_ease, 2),
            "average_explanation_clarity": round(avg_clarity, 2),
            "average_result_quality": round(avg_quality, 2),
            "would_use_again_percent": round((would_use / total) * 100, 1),
            "top_confusion_points": sorted(confusion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
