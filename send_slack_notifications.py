"""
Slack Notification Script
Sends alerts and summaries to Slack
"""

import json
import os
from datetime import datetime
from slack_notifier import SlackNotifier, SlackChannelRouter
from utils import Logger


def main():
    """Send notifications to Slack"""
    
    logger = Logger()
    logger.info("=" * 60)
    logger.info("📨 Sending Slack Notifications")
    logger.info("=" * 60)
    
    # Load actionable alerts
    if not os.path.exists("actionable_alerts.json"):
        logger.warning("actionable_alerts.json not found")
        return
    
    with open("actionable_alerts.json", "r") as f:
        actionable_alerts = json.load(f)
    
    # Initialize notifier
    notifier = SlackNotifier()
    
    logger.info(f"\n🔧 Configuration:")
    logger.info(f"  ├─ Webhook URL: {'✓ Set' if not notifier.dry_run else '✗ Not set (dry-run)'}")
    logger.info(f"  └─ Dry Run: {'✓ Yes' if notifier.dry_run else '✗ No'}")
    
    # Test webhook connection
    if not notifier.dry_run:
        logger.info(f"\n🧪 Testing Slack webhook...")
        if notifier.send_test_message():
            logger.info(f"  ✓ Webhook connection successful")
        else:
            logger.warning(f"  ✗ Webhook connection failed")
    
    # Send individual alerts
    if actionable_alerts:
        logger.info(f"\n▶️  Sending {len(actionable_alerts)} alert notifications...")
        logger.info("=" * 60)
        
        for i, alert in enumerate(actionable_alerts, 1):
            notifier.send_alert(alert)
            activity = alert['alert']['activity_name']
            score = alert['score']
            channel = SlackChannelRouter.get_channel(score, alert['alert'].get('is_simulated', False))
            logger.info(f"  {i}. {activity} → {channel} (Score: {score})")
        
        logger.info("=" * 60)
    
    # Create summary for all runs
    logger.info(f"\n📊 Preparing summary...")
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "total_alerts": len(actionable_alerts),
        "actionable_alerts": len(actionable_alerts),
        "suppressed_alerts": 0,  # Would get from alert engine results
        "deduplicated_alerts": 0,
        "tickets_created": len(actionable_alerts),
        "test_defects": sum(1 for a in actionable_alerts if a['alert'].get('is_simulated')),
        "activities": list(set(a['alert']['activity_name'] for a in actionable_alerts))
    }
    
    # Send summary
    logger.info(f"\n▶️  Sending summary notification...")
    if notifier.send_daily_summary(summary_data):
        logger.info(f"  ✓ Summary sent to Slack")
    else:
        logger.info(f"  ℹ️  Summary notification sent (dry-run)")
    
    # Get notification stats
    notification_summary = notifier.get_notification_summary()
    logger.info(f"\n✅ Slack Notifications:")
    logger.info(f"  ├─ Total Sent: {notification_summary['total_sent']}")
    logger.info(f"  └─ Notifications: {notification_summary.get('notifications', [])[:3]}")
    
    logger.info(f"\n✅ Slack notifications completed at {datetime.now().isoformat()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
