# 🎯 Quick Reference Guide

## Command Cheat Sheet

### Run Full Pipeline Locally
```bash
python axis3_enhanced.py           # Health checks + defects
python process_alerts.py           # Process through engine
python create_tickets.py           # Create GitHub issues
python send_slack_notifications.py # Send to Slack
python send_daily_email.py         # Send email digest
python generate_reports.py         # Generate reports
```

### Test Individual Components
```bash
# Test Slack connection
python -c "from slack_notifier import SlackNotifier; SlackNotifier().send_test_message()"

# Test Email connection
python -c "from email_notifier import EmailNotifier; EmailNotifier().send_test_email('your@email.com')"

# Check database
python -c "from database import AlertDatabase; db = AlertDatabase(); print(db.get_alert_statistics())"

# Export data
python -c "from database import AlertDatabase; db = AlertDatabase(); db.export_to_csv('report.csv')"
```

### Disable Defects
```bash
export DEFECTS_ENABLED=false
python axis3_enhanced.py
```

---

## File Reference

| File | Purpose | When to Edit |
|------|---------|--------------|
| `alert_rules.yaml` | Alert rules per activity | Adding/modifying activities |
| `defect_injector.py` | Defect injection logic | Changing defect types |
| `alert_engine.py` | Alert processing | Adjusting scoring |
| `.github/workflows/health-check.yml` | GitHub Actions | Changing execution frequency |
| `axis3_enhanced.py` | Selenium tests | Adding new activities |

---

## GitHub Secrets Required

```
GITHUB_TOKEN              (auto-provided by Actions)
SLACK_WEBHOOK_URL         https://hooks.slack.com/services/...
SENDGRID_API_KEY          sg.xxxxxx...
FROM_EMAIL                alerts@company.com
RECIPIENT_EMAIL           admin@company.com
```

---

## Alert Score Quick Reference

```
85+  🔴 CRITICAL    → Create ticket, notify team
70-85 🟠 HIGH       → Create ticket, Slack alert
60-70 🟡 MEDIUM     → Create ticket, quiet
<60   ✅ SUPPRESSED → No ticket, logged only
```

---

## Defect Types & Injection Rates

```
TIMEOUT           15% (Connection timeout)
SLOW_RESPONSE     20% (Response time >5s)
CONNECTION_ERROR  12% (Connection refused)
DUPLICATE_ALERT   10% (Send alert 3x)
FALSE_POSITIVE     8% (Expected failure)
ALERT_STORM        5% (50+ alerts/5min)
```

---

## Key Classes & Methods

```python
# Defect Injection
from defect_injector import DefectInjector
injector = DefectInjector(enabled=True)
defect = injector.get_defect(check_id, activity_name)

# Alert Engine
from alert_engine import AlertEngine
engine = AlertEngine()
results = engine.process_alerts(raw_alerts)

# Ticket Generation
from ticket_generator import GitHubTicketGenerator
generator = GitHubTicketGenerator()
ticket = generator.create_ticket(processed_alert)

# Slack Notifications
from slack_notifier import SlackNotifier
notifier = SlackNotifier()
notifier.send_alert(alert)

# Email
from email_notifier import EmailNotifier
emailer = EmailNotifier()
emailer.send_daily_digest(data, recipients)

# Database
from database import AlertDatabase
db = AlertDatabase()
db.add_alert(alert)
stats = db.get_alert_statistics()
```

---

## Debugging

### Check Logs
```bash
tail -f alert_engine.log
grep "ERROR" alert_engine.log
```

### Dry-Run Mode
```python
# Slack (no webhook = dry-run)
# GitHub (no token = dry-run)
# Email (no key = dry-run)
```

### Inspect Raw Data
```bash
cat raw_alerts.json | python -m json.tool
cat alert_engine_results.json | python -m json.tool
```

---

## Production Checklist

- [ ] Defects disabled: `DEFECTS_ENABLED=false`
- [ ] All GitHub Secrets configured
- [ ] Slack webhook tested
- [ ] SendGrid API key tested
- [ ] Alert rules reviewed
- [ ] Email recipients set
- [ ] GitHub Actions enabled
- [ ] First run successful
- [ ] Dashboard accessible
- [ ] Team trained

---

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| No Slack messages | Check SLACK_WEBHOOK_URL in Secrets |
| No emails | Check SENDGRID_API_KEY in Secrets |
| No GitHub issues | Check GITHUB_TOKEN exists |
| Chrome error | `pip install webdriver-manager` |
| Port 5502 error | `python -m http.server 5502` |
| Import error | `pip install -r requirements.txt` |

---

## Common Tasks

### Change Defect Injection Rate
Edit `alert_rules.yaml`:
```yaml
defect_injection:
  percentage: 10  # Change 25 to 10
```

### Add New Activity
1. Add to `alert_rules.yaml`
2. Add activity mapping in `axis3_enhanced.py`
3. Update Selenium script

### Change Execution Frequency
Edit `.github/workflows/health-check.yml`:
```yaml
cron: '0 * * * *'  # Every hour instead of 30 min
```

### Disable Slack Notifications
In GitHub Secrets, leave `SLACK_WEBHOOK_URL` empty

### Disable Email Notifications
In GitHub Secrets, leave `SENDGRID_API_KEY` empty

---

## File Outputs Reference

```
raw_alerts.json              ← Raw alerts from Selenium
alert_engine_results.json    ← Processed results
actionable_alerts.json       ← Alerts that created tickets
ticket_summary.json          ← Created GitHub issues
link_check_report.xlsx       ← Excel report
alert_engine.log             ← Execution logs

reports/
├── dashboard.html           ← Visual dashboard
├── executive_summary.json
├── detailed_alert_report.json
├── statistics.json
└── alerts_export.csv
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Health checks | 7 activities |
| Frequency | Every 30 minutes |
| Alert processing | <5 seconds |
| Ticket creation | <2 seconds per ticket |
| Email sending | <3 seconds |
| Slack messages | <1 second |
| Data retention | 30 days (configurable) |

---

## API Integration Endpoints

```
GitHub: api.github.com/repos/{owner}/{repo}/issues
Slack: hooks.slack.com/services/{token}
SendGrid: api.sendgrid.com/v3/mail/send
```

---

## Environment Variables

```bash
GITHUB_TOKEN              # GitHub authentication
SLACK_WEBHOOK_URL         # Slack notifications
SENDGRID_API_KEY          # Email sending
FROM_EMAIL                # Sender email
RECIPIENT_EMAIL           # Recipient email
EXECUTION_ID              # Unique run identifier
DEFECTS_ENABLED           # Enable/disable defect injection
```

---

## Useful Links

- Slack Webhook: https://api.slack.com/apps
- SendGrid: https://app.sendgrid.com
- GitHub Actions: github.com/{repo}/settings/actions
- GitHub Issues: github.com/{repo}/issues

---

**Last Updated:** January 13, 2026
**Version:** 1.0.0
**Status:** ✅ Ready to Use
