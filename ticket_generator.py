"""
GitHub Ticket Generator
Creates GitHub Issues for actionable alerts
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class GitHubTicketGenerator:
    """Generate GitHub Issues from actionable alerts"""
    
    def __init__(self, github_token: str = None):
        """
        Initialize GitHub ticket generator
        
        Args:
            github_token: GitHub API token (from environment if not provided)
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.repo_owner = os.getenv('GITHUB_REPO_OWNER', 'user')
        self.repo_name = os.getenv('GITHUB_REPO_NAME', 'sahil_automation_project')
        
        if not self.github_token:
            print("⚠️ Warning: GITHUB_TOKEN not set. Tickets will be created in dry-run mode")
        
        self.created_tickets = []
        self.dry_run = not self.github_token
    
    def create_ticket(self, processed_alert: Dict) -> Optional[Dict]:
        """
        Create GitHub issue for actionable alert
        
        Args:
            processed_alert: Dict from alert engine with alert, score, etc
        
        Returns:
            Dict with ticket info or None if not created
        """
        
        alert = processed_alert["alert"]
        score = processed_alert["score"]
        
        if not processed_alert["should_create_ticket"]:
            return None
        
        # Build ticket details
        title = self._build_title(alert, score)
        body = self._build_body(alert, processed_alert)
        labels = self._get_labels(score, alert)
        
        ticket_data = {
            "title": title,
            "body": body,
            "labels": labels,
            "created_at": datetime.now().isoformat(),
            "alert_id": alert["alert_id"],
            "activity": alert["activity_name"],
            "score": score,
            "is_simulated": alert.get("is_simulated", False),
            "dry_run": self.dry_run
        }
        
        if self.dry_run:
            print(f"\n📋 [DRY-RUN] Would create GitHub Issue:")
            print(f"   Title: {title}")
            print(f"   Labels: {labels}")
            ticket_data["issue_number"] = f"dry-run-{len(self.created_tickets)}"
        else:
            # Actually create the issue
            issue_number = self._post_issue(title, body, labels)
            ticket_data["issue_number"] = issue_number
            print(f"✓ GitHub Issue Created: #{issue_number}")
        
        self.created_tickets.append(ticket_data)
        return ticket_data
    
    def create_tickets_batch(self, processed_alerts: List[Dict]) -> List[Dict]:
        """
        Create multiple tickets
        
        Args:
            processed_alerts: List of processed alerts from engine
        
        Returns:
            List of created ticket dicts
        """
        
        tickets = []
        for alert in processed_alerts:
            ticket = self.create_ticket(alert)
            if ticket:
                tickets.append(ticket)
        
        print(f"\n✓ Created {len(tickets)} GitHub Issues")
        return tickets
    
    def _build_title(self, alert: Dict, score: int) -> str:
        """Build GitHub issue title"""
        
        # Priority indicator
        if score > 85:
            priority = "🔴 CRITICAL"
        elif score > 70:
            priority = "🟠 HIGH"
        else:
            priority = "🟡 MEDIUM"
        
        # Status
        status = alert["status"].upper()
        
        # Activity name
        activity = alert["activity_name"]
        
        return f"{priority} | {activity} - {status}"
    
    def _build_body(self, alert: Dict, processed_alert: Dict) -> str:
        """Build GitHub issue body/description"""
        
        assessment = processed_alert["assessment"]
        score = processed_alert["score"]
        
        severity_indicator = "🔴" if score > 80 else "🟠" if score > 70 else "🟡"
        
        body = f"""## {severity_indicator} Alert Details

### Activity Information
- **Activity Name:** {alert['activity_name']}
- **Check ID:** {alert['check_id']}
- **Timestamp:** {alert['timestamp']}
- **Execution ID:** {alert.get('execution_id', 'N/A')}

### Status & Response
- **Status:** `{alert['status']}`
- **Response Code:** {alert['response_code'] or 'N/A'}
- **Response Time:** {alert['response_time']:.2f}s
- **URL:** {alert['url']}

### Severity & Scoring
- **Actionability Score:** {score}/100
- **Severity Score:** {assessment['severity_score']:.1f}/10
- **Previous Status:** {alert['previous_status']}

### Analysis
- **Is False Positive:** {'✓ Yes' if assessment['is_false_positive'] else '✗ No'}
- **Is Threshold Exceeded:** {'✓ Yes' if assessment['threshold_exceeded'] else '✗ No'}
- **Has Historical Context:** {'✓ Yes' if assessment['has_historical_context'] else '✗ No'}

### Alert Details
```
{alert['error_message'] if alert['error_message'] else 'No error message'}
```

### Frequency Analysis
- **Alerts in 5 min:** {assessment['frequency_check'].get('count_5_min', 'N/A')}
- **Is Storm:** {'✓ Yes' if assessment['frequency_check'].get('is_storm', False) else '✗ No'}
- **Frequency Exceeded:** {'✓ Yes' if assessment['frequency_check'].get('exceeded', False) else '✗ No'}

### Test Information
- **Is Simulated Defect:** {'✓ Yes' if alert.get('is_simulated') else '✗ No'}
- **Retry Count:** {alert.get('retry_count', 0)}

### Next Steps
1. Investigate the reported activity
2. Check historical data for patterns
3. Determine if this is recurring or isolated
4. Take corrective action if needed
5. Update ticket status

---
*Auto-generated by Alert Engine*
*Do not manually edit this ticket*
"""
        
        return body
    
    def _get_labels(self, score: int, alert: Dict) -> List[str]:
        """Determine GitHub issue labels"""
        
        labels = ["auto-generated"]
        
        # Priority labels
        if score > 85:
            labels.append("critical")
        elif score > 70:
            labels.append("high")
        else:
            labels.append("medium")
        
        # Type label
        if alert.get("is_simulated"):
            labels.append("test-defect")
        else:
            labels.append("production-incident")
        
        # Activity-specific labels
        activity_name = alert["activity_name"].lower().replace(" ", "-")
        labels.append(f"activity-{activity_name}")
        
        # Status label
        if alert["status"] == "failure":
            labels.append("failure")
        elif alert["status"] == "error":
            labels.append("error")
        
        return labels
    
    def _post_issue(self, title: str, body: str, labels: List[str]) -> Optional[str]:
        """
        Post issue to GitHub API
        
        Args:
            title: Issue title
            body: Issue body
            labels: List of labels
        
        Returns:
            Issue number or None if failed
        """
        
        try:
            import requests
        except ImportError:
            print("⚠️ requests library not installed. Install with: pip install requests")
            return None
        
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues"
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "title": title,
            "body": body,
            "labels": labels
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 201:
                issue = response.json()
                return str(issue.get("number"))
            else:
                print(f"✗ GitHub API Error: {response.status_code}")
                print(f"  Response: {response.text}")
                return None
        
        except Exception as e:
            print(f"✗ Error posting to GitHub: {e}")
            return None
    
    def close_ticket(self, issue_number: int, resolution: str = "Resolved"):
        """Close a GitHub issue"""
        
        if self.dry_run:
            print(f"📋 [DRY-RUN] Would close issue #{issue_number}")
            return
        
        try:
            import requests
        except ImportError:
            return
        
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "state": "closed",
            "body": f"{resolution}\n\nAuto-resolved by Alert Engine"
        }
        
        try:
            response = requests.patch(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"✓ Closed issue #{issue_number}")
        except Exception as e:
            print(f"✗ Error closing issue: {e}")
    
    def get_created_tickets_summary(self) -> Dict:
        """Get summary of created tickets"""
        
        if not self.created_tickets:
            return {"message": "No tickets created"}
        
        return {
            "total_created": len(self.created_tickets),
            "critical": sum(1 for t in self.created_tickets if t["score"] > 85),
            "high": sum(1 for t in self.created_tickets if 70 < t["score"] <= 85),
            "medium": sum(1 for t in self.created_tickets if t["score"] <= 70),
            "test_defects": sum(1 for t in self.created_tickets if t["is_simulated"]),
            "production": sum(1 for t in self.created_tickets if not t["is_simulated"]),
            "tickets": self.created_tickets
        }
    
    def save_tickets_to_file(self, filepath: str = "created_tickets.json"):
        """Save created tickets to JSON file"""
        
        with open(filepath, 'w') as f:
            json.dump(self.get_created_tickets_summary(), f, indent=2)
        
        print(f"✓ Tickets saved to {filepath}")


class TicketTracker:
    """Track ticket lifecycle"""
    
    def __init__(self, storage_file: str = "ticket_tracker.json"):
        self.storage_file = storage_file
        self.tickets = self._load_tickets()
    
    def track_ticket(self, ticket_data: Dict):
        """Track a created ticket"""
        
        if not hasattr(self, 'tickets'):
            self.tickets = {}
        
        issue_number = ticket_data.get("issue_number")
        if issue_number:
            self.tickets[str(issue_number)] = {
                "data": ticket_data,
                "created_at": datetime.now().isoformat(),
                "status": "open",
                "resolved_at": None
            }
            self._save_tickets()
    
    def resolve_ticket(self, issue_number: int):
        """Mark ticket as resolved"""
        
        ticket_key = str(issue_number)
        if ticket_key in self.tickets:
            self.tickets[ticket_key]["status"] = "resolved"
            self.tickets[ticket_key]["resolved_at"] = datetime.now().isoformat()
            self._save_tickets()
    
    def get_open_tickets(self) -> List[Dict]:
        """Get all open tickets"""
        
        return [
            ticket for ticket in self.tickets.values()
            if ticket["status"] == "open"
        ]
    
    def _load_tickets(self) -> Dict:
        """Load tickets from storage"""
        
        if Path(self.storage_file).exists():
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_tickets(self):
        """Save tickets to storage"""
        
        with open(self.storage_file, 'w') as f:
            json.dump(self.tickets, f, indent=2)
