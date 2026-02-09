"""
Daily Email Digest Script
Sends daily summary emails
"""

import json
import os
from datetime import datetime
from email_notifier import EmailNotifier
from database import AlertDatabase
from utils import Logger


def main():
    """Send daily email digest"""
    
    logger = Logger()
    logger.info("=" * 60)
    logger.info("📧 Sending Daily Email Digest")
    logger.info("=" * 60)
    
    # Initialize components
    notifier = EmailNotifier()
    db = AlertDatabase()
    
    logger.info(f"\n🔧 Configuration:")
    logger.info(f"  ├─ From Email: {notifier.email_user}")
    logger.info(f"  ├─ Gmail SMTP: {'✓ Set' if not notifier.dry_run else '✗ Not set (dry-run)'}")
    logger.info(f"  └─ Dry Run: {'✓ Yes' if notifier.dry_run else '✗ No'}")
    
    # Get recipient email
    recipient = os.getenv('RECIPIENT_EMAIL', 'admin@amxis-bank.local')
    
    # Get 24-hour statistics
    logger.info(f"\n📊 Gathering statistics for last 24 hours...")
    stats = db.get_alert_statistics(hours=24)
    recent_alerts = db.get_recent_alerts(hours=24, limit=100)
    
    # Build summary data
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "total_alerts": stats.get('total', 0),
        "actionable_alerts": len([a for a in recent_alerts if a.get('status') == 'failure']),
        "suppressed_alerts": len([a for a in recent_alerts if a.get('status') == 'success']),
        "test_defects": stats.get('simulated_defects', 0),
        "by_status": stats.get('by_status', {}),
        "by_activity": stats.get('by_activity', {}),
        "high_score_alerts": stats.get('high_score_alerts', 0)
    }
    
    logger.info(f"  ├─ Total Alerts: {summary_data['total_alerts']}")
    logger.info(f"  ├─ Actionable: {summary_data['actionable_alerts']}")
    logger.info(f"  ├─ Test Defects: {summary_data['test_defects']}")
    logger.info(f"  └─ Activities: {len(summary_data['by_activity'])}")
    
    # Send test email first
    logger.info(f"\n🧪 Testing email configuration...")
    if not notifier.dry_run:
        if notifier.send_test_email(recipient):
            logger.info(f"  ✓ Test email sent successfully")
        else:
            logger.warning(f"  ✗ Test email failed")
    else:
        logger.info(f"  ℹ️  Dry-run mode - test email not sent")
    
    # Send daily digest
    logger.info(f"\n▶️  Sending daily digest to {recipient}...")
    result = notifier.send_daily_digest(summary_data, [recipient])
    
    logger.info(f"  ├─ Sent: {result.get('sent', 0)}")
    logger.info(f"  ├─ Failed: {result.get('failed', 0)}")
    logger.info(f"  └─ Total: {result.get('total_recipients', 0)}")
    
    # Get email summary
    email_summary = notifier.get_email_summary()
    logger.info(f"\n✅ Email Summary:")
    logger.info(f"  ├─ Total Sent: {email_summary['total_sent']}")
    logger.info(f"  └─ Total Attempted: {email_summary['total_attempted']}")
    
    logger.info(f"\n✅ Email digest completed at {datetime.now().isoformat()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
