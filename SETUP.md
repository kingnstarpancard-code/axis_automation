# 🤖 Alert Engine - Complete Setup Guide

## System Overview

This is a **24x7 Automated Monitoring System** with:
- ✅ Selenium-based health checks (7 activities)
- ✅ Intelligent Alert Engine with filtering & correlation
- ✅ Automatic defect injection for testing
- ✅ GitHub Issues ticket creation
- ✅ Slack real-time notifications
- ✅ Daily email digests
- ✅ JSON-based data persistence

---

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install selenium requests openpyxl pyyaml sendgrid webdriver-manager
```

### 2. Set GitHub Secrets

Go to your GitHub repository:
- **Settings** → **Secrets and variables** → **Actions**
- Add these secrets:

```
GITHUB_TOKEN = (automatically available)
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SENDGRID_API_KEY = sg.xxxxxxx...
FROM_EMAIL = alerts@yourcompany.com
RECIPIENT_EMAIL = admin@yourcompany.com
```

### 3. Enable GitHub Actions

- Go to **Settings** → **Actions** → **General**
- Select: "Allow all actions and reusable workflows"
- Save

### 4. Trigger First Run

```bash
# Local test run
python axis3_enhanced.py

# Or push to GitHub and Actions will run automatically
```

---

## Setup Details

### Configuration A: Local Development

```bash
# 1. Clone and setup
git clone <your-repo>
cd sahil_automation_project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test locally
python axis3_enhanced.py
python process_alerts.py
python create_tickets.py
```

### Configuration B: GitHub Actions (24x7)

The system automatically runs every 30 minutes via `.github/workflows/health-check.yml`

Workflow steps:
1. Run Selenium health checks
2. Process alerts through engine
3. Create GitHub Issues
4. Send Slack notifications
5. Generate reports
6. Save artifacts
7. Send email digest (daily)

---

## Components Breakdown

### 1. **Defect Injector** (`defect_injector.py`)

Intentionally injects simulated failures for testing:

```python
from defect_injector import DefectInjector

injector = DefectInjector(enabled=True)
defect = injector.get_defect(check_id=1, activity_name="Account Verification")
# Returns: {"type": "TIMEOUT", "severity": 75, ...} or None
```

**Defect Types:**
- TIMEOUT (15%)
- SLOW_RESPONSE (20%)
- CONNECTION_ERROR (12%)
- DUPLICATE_ALERT (10%)
- FALSE_POSITIVE (8%)
- ALERT_STORM (5%)

### 2. **Alert Engine** (`alert_engine.py`)

Processes raw alerts into actionable tickets:

```python
from alert_engine import AlertEngine

engine = AlertEngine()
results = engine.process_alerts(raw_alerts)

# Results:
# ├─ actionable_alerts (Score >60)
# ├─ suppressed_alerts
# ├─ deduplicated_alerts
# ├─ correlated_groups
# └─ summary
```

**Scoring:** 0-100
- **Critical:** >85
- **High:** 70-85
- **Medium:** 60-70
- **Low:** <60

### 3. **Ticket Generator** (`ticket_generator.py`)

Creates GitHub Issues from alerts:

```python
from ticket_generator import GitHubTicketGenerator

generator = GitHubTicketGenerator()
ticket = generator.create_ticket(processed_alert)
# Creates issue with title, body, labels automatically
```

### 4. **Slack Notifier** (`slack_notifier.py`)

Sends real-time notifications:

```python
from slack_notifier import SlackNotifier

notifier = SlackNotifier()
notifier.send_alert(processed_alert)
notifier.send_daily_summary(summary_data)
```

### 5. **Email Notifier** (`email_notifier.py`)

Sends daily digests via SendGrid:

```python
from email_notifier import EmailNotifier

notifier = EmailNotifier()
notifier.send_daily_digest(summary_data, recipients)
```

### 6. **Database** (`database.py`)

JSON-based persistence:

```python
from database import AlertDatabase

db = AlertDatabase()
db.add_alert(alert)
db.add_ticket(ticket)
recent = db.get_recent_alerts(hours=24)
stats = db.get_alert_statistics()
```

---

## Configuration Files

### `alert_rules.yaml`

Define rules for each activity:

```yaml
rules:
  - id: "activity_1"
    activity_name: "Account Verification"
    conditions:
      - name: "response_time_threshold"
        operator: ">"
        value: 5000
    false_positives:
      - reason: "Maintenance"
        days: [6]  # Sunday
        hours: [22, 23]
```

### `defect_injection.yaml` (Optional)

Control defect injection:

```yaml
defect_injection:
  enabled: true
  percentage: 25
  exclude_hours: [9, 10, 11]  # Don't inject during business hours
```

---

## Slack Setup (10 minutes)

### Step 1: Create Slack Workspace
Already have one? Skip to Step 2.

### Step 2: Create Channel
```
1. In Slack: Click "+" next to "Channels"
2. Create: #monitoring-alerts, #critical-alerts, #test-alerts
```

### Step 3: Create Webhook

```
1. Go to: https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "Alert Engine Bot"
4. Select your workspace
5. Enable "Incoming Webhooks"
6. Click "Add New Webhook to Workspace"
7. Select channel: #monitoring-alerts
8. Copy the Webhook URL
```

### Step 4: Add to GitHub Secrets
```
SLACK_WEBHOOK_URL = https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX
```

### Step 5: Test
```bash
python -c "from slack_notifier import SlackNotifier; SlackNotifier().send_test_message()"
```

---

## SendGrid Setup (5 minutes)

### Step 1: Sign Up
- Go to: https://sendgrid.com
- Click "Start Free"
- Create account

### Step 2: Get API Key
```
1. Dashboard → "Settings" → "API Keys"
2. Click "Create API Key"
3. Name: "Alert Engine"
4. Copy the key
```

### Step 3: Add to GitHub Secrets
```
SENDGRID_API_KEY = sg.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL = alerts@yourcompany.com
RECIPIENT_EMAIL = admin@yourcompany.com
```

### Step 4: Test
```bash
python -c "from email_notifier import EmailNotifier; EmailNotifier().send_test_email('your@email.com')"
```

---

## Running the System

### Local Execution

```bash
# 1. Run health checks
python axis3_enhanced.py

# 2. Process alerts
python process_alerts.py

# 3. Create tickets
python create_tickets.py

# 4. Send Slack notifications
python send_slack_notifications.py

# 5. Send email
python send_daily_email.py
```

### Automated (GitHub Actions)

```
Runs automatically every 30 minutes
Or manually: Actions → Workflows → Health Check → "Run workflow"
```

---

## Monitoring & Dashboards

### View Results

**GitHub Issues:**
```
https://github.com/your-username/sahil_automation_project/issues
```

**Slack Channels:**
- #monitoring-alerts (regular alerts)
- #critical-alerts (high severity)
- #test-alerts (simulated defects)

**Local Reports:**
```bash
# Excel report
link_check_report.xlsx

# JSON reports
raw_alerts.json
alert_engine_results.json
actionable_alerts.json
ticket_summary.json

# Logs
alert_engine.log
```

---

## Understanding Alert Scores

Factors that increase score:
- ✅ Failure status: +30 points
- ✅ Not a false positive: +25 points
- ✅ Frequency check passed: +20 points
- ✅ High severity: +15 points
- ✅ Threshold exceeded: +10 points
- ✅ Critical service: +15 points

Factors that decrease score:
- ❌ Simulated defect: -10 points
- ❌ Alert storm: -50 points

**Thresholds:**
- Score >60 = Create ticket
- Score >70 = High priority
- Score >85 = Critical priority

---

## Troubleshooting

### "GITHUB_TOKEN not set"
**Solution:** GitHub Actions automatically provides this. For local testing:
```bash
export GITHUB_TOKEN=ghp_xxxxx
```

### "SLACK_WEBHOOK_URL not set"
**Solution:** Runs in dry-run mode. Won't send actual notifications. To enable:
```bash
export SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

### "SENDGRID_API_KEY not set"
**Solution:** Email won't send. To enable:
```bash
export SENDGRID_API_KEY=sg_xxxxx
```

### "ChromeDriver not found"
**Solution:**
```bash
pip install webdriver-manager
```

### "Port 5502 not responding"
**Solution:** Make sure local server is running:
```bash
# In another terminal
python -m http.server 5502
```

---

## Production Checklist

- [ ] GitHub Secrets configured
- [ ] Slack workspace and webhook created
- [ ] SendGrid account and API key set up
- [ ] Email recipients configured
- [ ] Alert rules reviewed in `alert_rules.yaml`
- [ ] Defect injection percentage appropriate (0% for production)
- [ ] GitHub Actions enabled
- [ ] Workflow schedule verified (every 30 minutes)
- [ ] Test run completed successfully
- [ ] Monitoring dashboard accessible

---

## Disabling Defect Injection (Production)

### Option 1: Environment Variable
```bash
export DEFECTS_ENABLED=false
```

### Option 2: GitHub Actions
Edit `.github/workflows/health-check.yml`:
```yaml
- name: Run health checks
  run: python axis3_enhanced.py
  env:
    DEFECTS_ENABLED: false
```

### Option 3: Code
Edit `axis3_enhanced.py`:
```python
defect_injector = DefectInjector(enabled=False)
```

---

## Support & Debugging

### Enable Debug Logging
```python
from utils import Logger
logger = Logger()
logger.debug("Debug message")
```

### Export Data
```python
from database import AlertDatabase
db = AlertDatabase()
db.export_to_csv("alerts_export.csv", hours=24)
```

### Check System Status
```bash
python -c "
from database import AlertDatabase
db = AlertDatabase()
print(db.get_alert_statistics(hours=24))
"
```

---

## Next Steps

1. **Complete Setup:** Follow GitHub Secrets section
2. **Test Locally:** Run `python axis3_enhanced.py`
3. **Enable Actions:** Push to GitHub
4. **Monitor:** Check dashboard after first run
5. **Customize:** Edit `alert_rules.yaml` for your needs

---

## Support

For issues:
- Check logs in `alert_engine.log`
- Run individual components in debug mode
- Contact admin team
- Review GitHub Issues for solutions

---

**System Created:** January 13, 2026
**Version:** 1.0.0
**Status:** ✅ Production Ready
