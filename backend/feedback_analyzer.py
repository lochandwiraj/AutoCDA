from backend.feedback_collector import FeedbackCollector
from backend.issue_tracker import IssueTracker, Priority

class FeedbackAnalyzer:
    def __init__(self):
        self.collector = FeedbackCollector()
        self.tracker = IssueTracker()

    def analyze_and_create_issues(self):
        summary = self.collector.get_feedback_summary()
        
        if "top_confusion_points" not in summary:
            return []
        
        created_issues = []
        
        # Create P0 issues for high-frequency confusions
        for confusion, count in summary["top_confusion_points"]:
            if count >= 2:  # If 2+ users confused
                issue = self.tracker.add_issue(
                    title=f"User confusion: {confusion}",
                    description=f"{count} users reported confusion with: {confusion}",
                    priority=Priority.P0,
                    source="feedback_analysis"
                )
                created_issues.append(issue)
        
        # Create P0 for low ease of use
        if summary.get("average_ease_of_use", 5) < 3:
            issue = self.tracker.add_issue(
                title="Low ease of use score",
                description=f"Average ease of use: {summary['average_ease_of_use']}/5",
                priority=Priority.P0,
                source="feedback_analysis"
            )
            created_issues.append(issue)
        
        # Create P0 for low explanation clarity
        if summary.get("average_explanation_clarity", 5) < 3:
            issue = self.tracker.add_issue(
                title="Explanations not clear enough",
                description=f"Average clarity score: {summary['average_explanation_clarity']}/5",
                priority=Priority.P0,
                source="feedback_analysis"
            )
            created_issues.append(issue)
        
        return created_issues
