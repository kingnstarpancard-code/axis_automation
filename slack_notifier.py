"""
Slack Alert Notifier
Sends real-time notifications to Slack
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class SlackNotifier:
    """Send alerts to Slack in real-time"""
    
    def __init__(self, webhook_url: str = None):
        """
        Initialize Slack notifier
        
        Args:
            webhook_url: Slack webhook URL (from environment if not provided)
        """
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        self.dry_run = not self.webhook_url
        
        if self.dry_run:
            print("⚠️ Warning: SLACK_WEBHOOK_URL not set. Notifications in dry-run mode")
        
        self.sent_notifications = []
    
    def send_alert(self, processed_alert: Dict, channel: str = None) -> bool:
        """
        Send alert to Slack
        
        Args:
            processed_alert: Processed alert from engine
            channel: Slack channel override
        
        Returns:
            True if sent successfully
        """
        
        alert = processed_alert["alert"]
        score = processed_alert["score"]
        
        # Build message
        message = self._build_message(alert, score)
        
        if self.dry_run:
            self._log_dry_run("Alert", message)
            return False
        
        # Send to Slack
        return self._post_to_slack(message)
    
    def send_batch(self, processed_alerts: List[Dict]) -> Dict:
        """
        Send multiple alerts to Slack
        
        Args:
            processed_alerts: List of processed alerts
        
        Returns:
            Dict with results
        """
        
        results = {
            "total": len(processed_alerts),
            "sent": 0,
            "failed": 0,
            "messages": []
        }
        
        for alert in processed_alerts:
            if self.send_alert(alert):
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        print(f"\n✓ Slack: {results['sent']}/{results['total']} notifications sent")
        return results
    
    def send_daily_summary(self, summary_data: Dict) -> bool:
        """
        Send daily health check summary to Slack
        
        Args:
            summary_data: Summary dict with stats
        
        Returns:
            True if sent successfully
        """
        
        message = self._build_summary_message(summary_data)
        
        if self.dry_run:
            self._log_dry_run("Daily Summary", message)
            return False
        
        return self._post_to_slack(message)
    
    def send_test_message(self) -> bool:
        """Send test message to verify webhook connection"""
        
        message = {
            "text": "🤖 Alert Engine - Test Message",
            "attachments": [
                {
                    "color": "#36a64f",
                    "title": "Webhook Connection Test",
                    "text": "If you see this message, Slack webhook is configured correctly!",
                    "footer": "Alert Engine",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        print("📨 Sending test message to Slack...")
        return self._post_to_slack(message)
    
    def _build_message(self, alert: Dict, score: int) -> Dict:
        """Build Slack message payload"""
        
        # Determine color and icon
        if score > 85:
            color = "#dc143c"  # Crimson
            emoji = "🔴"
            priority = "CRITICAL"
        elif score > 70:
            color = "#ff8c00"  # Dark orange
            emoji = "🟠"
            priority = "HIGH"
        else:
            color = "#ffd700"  # Gold
            emoji = "🟡"
            priority = "MEDIUM"
        
        # Build fields
        fields = [
            {
                "title": "Activity",
                "value": alert['activity_name'],
                "short": True
            },
            {
                "title": "Status",
                "value": alert['status'].upper(),
                "short": True
            },
            {
                "title": "Response Code",
                "value": str(alert['response_code'] or 'N/A'),
                "short": True
            },
            {
                "title": "Response Time",
                "value": f"{alert['response_time']:.2f}s",
                "short": True
            },
            {
                "title": "Score",
                "value": f"{score}/100",
                "short": True
            },
            {
                "title": "Type",
                "value": "Test Defect ✓" if alert.get('is_simulated') else "Production Incident",
                "short": True
            },
            {
                "title": "Error Details",
                "value": alert['error_message'] or "No error message",
                "short": False
            }
        ]
        
        message = {
            "text": f"{emoji} {priority} Alert: {alert['activity_name']}",
            "attachments": [
                {
                    "color": color,
                    "title": f"{emoji} {alert['activity_name']} - {alert['status'].upper()}",
                    "title_link": alert['url'],
                    "fields": fields,
                    "footer": "Alert Engine | Automated Monitoring",
                    "ts": int(datetime.fromisoformat(alert['timestamp']).timestamp())
                }
            ]
        }
        
        return message
    
    def _build_summary_message(self, summary_data: Dict) -> Dict:
        """Build daily summary message"""
        
        total = summary_data.get('total_alerts', 0)
        actionable = summary_data.get('actionable_alerts', 0)
        suppressed = summary_data.get('suppressed_alerts', 0)
        
        # Color based on severity
        if actionable > 5:
            color = "#dc143c"
            status = "⚠️ Multiple Issues"
        elif actionable > 0:
            color = "#ff8c00"
            status = "⚠️ Issues Found"
        else:
            color = "#36a64f"
            status = "✅ All Clear"
        
        fields = [
            {
                "title": "Total Alerts",
                "value": str(total),
                "short": True
            },
            {
                "title": "Actionable",
                "value": str(actionable),
                "short": True
            },
            {
                "title": "Suppressed",
                "value": str(suppressed),
                "short": True
            },
            {
                "title": "Deduplicated",
                "value": str(summary_data.get('deduplicated_alerts', 0)),
                "short": True
            },
            {
                "title": "Tickets Created",
                "value": str(summary_data.get('tickets_created', 0)),
                "short": True
            },
            {
                "title": "Test Defects",
                "value": str(summary_data.get('test_defects', 0)),
                "short": True
            }
        ]
        
        message = {
            "text": f"📊 Daily Health Check Summary - {status}",
            "attachments": [
                {
                    "color": color,
                    "title": "Daily Health Check Report",
                    "text": f"Summary for {datetime.now().strftime('%Y-%m-%d')}",
                    "fields": fields,
                    "footer": "Alert Engine | Daily Digest",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        return message
    
    def _post_to_slack(self, message: Dict) -> bool:
        """
        Post message to Slack webhook
        
        Args:
            message: Message payload dict
        
        Returns:
            True if successful
        """
        
        try:
            import requests
        except ImportError:
            print("⚠️ requests library not installed. Install with: pip install requests")
            return False
        
        try:
            response = requests.post(
                self.webhook_url,
                json=message,
                timeout=10
            )
            
            if response.status_code == 200:
                self.sent_notifications.append({
                    "timestamp": datetime.now().isoformat(),
                    "message": message,
                    "status": "sent"
                })
                return True
            else:
                print(f"✗ Slack API Error: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ Error sending to Slack: {e}")
            return False
    
    def _log_dry_run(self, msg_type: str, message: Dict):
        """Log dry-run message"""
        
        print(f"\n📋 [DRY-RUN] Would send Slack {msg_type}:")
        print(f"   Payload: {json.dumps(message, indent=2)[:200]}...")
    
    def get_notification_summary(self) -> Dict:
        """Get summary of sent notifications"""
        
        return {
            "total_sent": len(self.sent_notifications),
            "notifications": self.sent_notifications
        }


class SlackChannelRouter:
    """Route alerts to appropriate Slack channels"""
    
    CHANNEL_ROUTING = {
        "critical": "#critical-alerts",
        "high": "#high-priority-alerts",
        "medium": "#monitoring-alerts",
        "test": "#test-alerts",
        "production": "#production-alerts"
    }
    
    @staticmethod
    def get_channel(score: int, is_simulated: bool) -> str:
        """Determine target channel based on alert severity"""
        
        if is_simulated:
            return SlackChannelRouter.CHANNEL_ROUTING["test"]
        
        if score > 85:
            return SlackChannelRouter.CHANNEL_ROUTING["critical"]
        elif score > 70:
            return SlackChannelRouter.CHANNEL_ROUTING["high"]
        else:
            return SlackChannelRouter.CHANNEL_ROUTING["medium"]
    
    @staticmethod
    def send_to_channel(webhook_url: str, channel: str, message: Dict) -> bool:
        """Send message to specific channel"""
        
        try:
            import requests
        except ImportError:
            return False
        
        # Add channel to message
        message["channel"] = channel
        
        try:
            response = requests.post(webhook_url, json=message, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"✗ Error sending to {channel}: {e}")
            return False
