#!/usr/bin/env python3
"""Debug script to check alerts and notifications"""

import os
import json
from database import AlertDatabase
from alert_engine import AlertEngine
from ticket_generator import GitHubTicketGenerator
from slack_notifier import SlackNotifier
from email_notifier import EmailNotifier

print("=" * 60)
print("DEBUG: Alert System Status")
print("=" * 60)

# 1. Check raw alerts
print("\n1. Checking raw alerts...")
db = AlertDatabase()
recent = db.get_recent_alerts(hours=24, limit=5)
print(f"   Total alerts: {len(recent)}")
if recent:
    for alert in recent[:3]:
        print(f"   - {alert.get('activity_name')}: {alert.get('status')} (Score: {alert.get('actionability_score', 'N/A')})")
else:
    print("   ⚠️ No alerts found!")

# 2. Process alerts
print("\n2. Processing alerts...")
try:
    engine = AlertEngine()
    processed = engine.process_alerts(recent)
    print(f"   ✓ Processed: {len(processed['actionable'])} actionable alerts")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 3. Test GitHub tickets
print("\n3. Testing GitHub ticket creation...")
github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    print(f"   ✓ GITHUB_TOKEN set")
else:
    print(f"   ✗ GITHUB_TOKEN not set")

# 4. Test Slack
print("\n4. Testing Slack webhook...")
slack_url = os.getenv('SLACK_WEBHOOK_URL')
if slack_url:
    print(f"   ✓ SLACK_WEBHOOK_URL set: {slack_url[:20]}...")
else:
    print(f"   ✗ SLACK_WEBHOOK_URL not set")

# 5. Test Email
print("\n5. Testing Email configuration...")
email_user = os.getenv('EMAIL_USER')
email_pass = os.getenv('EMAIL_PASSWORD')
if email_user and email_pass:
    print(f"   ✓ Email configured: {email_user}")
else:
    print(f"   ✗ Email not configured")
    if not email_user:
        print(f"      - EMAIL_USER not set")
    if not email_pass:
        print(f"      - EMAIL_PASSWORD not set")

print("\n" + "=" * 60)
