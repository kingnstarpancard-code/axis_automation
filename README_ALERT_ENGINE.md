# 🤖 Alert Engine - 24x7 Automated Monitoring System

**A complete automated monitoring solution with intelligent alert processing, defect injection testing, and multi-channel notifications.**

---

## ✨ Features

### Core Capabilities
- ✅ **Selenium-based Health Checks** - Automates 7 activity checks every 30 minutes
- ✅ **Intelligent Alert Engine** - Processes 1000+ alerts with filtering, correlation, and scoring
- ✅ **Automatic Defect Injection** - Simulates 6 types of failures for system testing
- ✅ **GitHub Issues Integration** - Creates tickets automatically with smart prioritization
- ✅ **Slack Real-time Notifications** - Instant alerts to configured channels
- ✅ **Daily Email Digests** - SendGrid-based summary reports
- ✅ **JSON Data Persistence** - All data stored locally for analysis
- ✅ **24x7 Automation** - GitHub Actions runs every 30 minutes
- ✅ **Comprehensive Reporting** - JSON, CSV, HTML dashboards

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────┐
│    GitHub Actions (Every 30 min)   │
└────────────────┬────────────────────┘
                 │
        ┌────────▼─────────────┐
        │  Selenium Script     │
        │  (axis3_enhanced.py) │
        │  7 Activities        │
        │  +Defect Injection   │
        └────────┬─────────────┘
                 │ Raw Alerts (JSON)
                 ▼
        ┌────────────────────────┐
        │  Alert Engine          │
        │  ├─ Normalize          │
        │  ├─ Assess             │
        │  ├─ Correlate          │
        │  ├─ Filter             │
        │  └─ Score (0-100)      │
        └────────┬───────────────┘
                 │ Actionable Alerts (Score >60)
        ┌────────┴──────────────────────────┐
        │                                   │
    ┌───▼────┐  ┌─────────┐  ┌──────────┐  │
    │ GitHub │  │  Slack  │  │  Email   │  │
    │ Issues │  │  Notif  │  │ SendGrid │  │
    └────────┘  └─────────┘  └──────────┘  │
                                            │
                 ┌──────────────────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │  Dashboard & Reports   │
        │  ├─ HTML Dashboard     │
        │  ├─ CSV Export         │
        │  ├─ JSON Reports       │
        │  └─ Execution History  │
        └────────────────────────┘
```

---

## 📁 Project Structure

```
sahil_automation_project/
├── 📄 Core Components
│   ├── axis3_enhanced.py           # Enhanced Selenium with defect injection
│   ├── defect_injector.py          # Simulated failure injection
│   ├── alert_engine.py             # Alert processing engine
│   ├── database.py                 # JSON-based persistence
│   └── utils.py                    # Utilities & helpers
│
├── 🎯 Integration Modules
│   ├── ticket_generator.py         # GitHub Issues creation
│   ├── slack_notifier.py           # Slack notifications
│   ├── email_notifier.py           # SendGrid emails
│   └── process_alerts.py           # Alert processing script
│
├── ⚙️ Configuration
│   ├── alert_rules.yaml            # Alert rules for each activity
│   ├── requirements.txt            # Python dependencies
│   └── .github/workflows/
│       └── health-check.yml        # GitHub Actions workflow
│
├── 📊 Outputs
│   ├── raw_alerts.json             # Raw alert events
│   ├── alert_engine_results.json   # Processed results
│   ├── actionable_alerts.json      # Tickets to create
│   ├── ticket_summary.json         # Created tickets
│   ├── link_check_report.xlsx      # Excel report
│   └── reports/
│       ├── dashboard.html          # Visual dashboard
│       ├── executive_summary.json
│       ├── detailed_alert_report.json
│       └── statistics.json
│
└── 📚 Documentation
    ├── README.md                   # This file
    └── SETUP.md                    # Complete setup guide
```

---

## 🚀 Quick Start

### 1. Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### 2. Configure GitHub Secrets (5 min)

Add these to your GitHub repo (Settings → Secrets):
- `SLACK_WEBHOOK_URL` - For Slack notifications
- `SENDGRID_API_KEY` - For email sending
- `FROM_EMAIL` - Sender email address
- `RECIPIENT_EMAIL` - Recipient email

### 3. Local Test (2 min)

```bash
# Run the full pipeline locally
python axis3_enhanced.py      # Health checks
python process_alerts.py      # Process alerts
python create_tickets.py      # Create GitHub issues
python send_slack_notifications.py  # Slack notifs
python generate_reports.py    # Generate reports
```

### 4. Deploy to GitHub (1 min)

```bash
git add .
git commit -m "Add Alert Engine system"
git push
```

**System will auto-run every 30 minutes!**

---

## 🎯 Alert Scoring System

Alerts scored 0-100. Only >60 create tickets.

### Scoring Factors

| Factor | Points | Description |
|--------|--------|-------------|
| Failure detected | +30 | Alert status is failure/error |
| Not false positive | +25 | Known false positives suppressed |
| Frequency ok | +20 | Not an alert storm |
| Severity | +15 | Based on response code & error type |
| Threshold exceeded | +10 | Response time or status code threshold |
| Critical service | +15 | Account/Transaction/Loan servers |
| **Penalty:** Simulated defect | -10 | Test alerts score lower |
| **Penalty:** Alert storm | -50 | Too many alerts in window |

### Ticket Creation

```
Score > 85: 🔴 CRITICAL
Score 70-85: 🟠 HIGH
Score 60-70: 🟡 MEDIUM
Score < 60: ✅ SUPPRESSED (no ticket)
```

---

## 🧪 Defect Injection

System injects simulated failures for testing (disabled in production):

### Defect Types (25% total injection rate by default)

| Type | Percentage | Impact | Example |
|------|-----------|--------|---------|
| TIMEOUT | 15% | Connection timeout after 10s | Network latency test |
| SLOW_RESPONSE | 20% | Response time >5s | Performance test |
| CONNECTION_ERROR | 12% | Connection refused | Network failure test |
| DUPLICATE_ALERT | 10% | Same alert 3x | Correlation test |
| FALSE_POSITIVE | 8% | Expected failure | Known issue test |
| ALERT_STORM | 5% | 50+ alerts in 5min | System overload test |

**All defects marked as `is_simulated: true` in output**

---

## 📊 Understanding the Outputs

### 1. Raw Alerts (`raw_alerts.json`)
```json
{
  "alert_id": "uuid",
  "timestamp": "2026-01-13T10:30:45",
  "activity_name": "Account Verification",
  "status": "failure",
  "response_code": null,
  "error_message": "Timeout",
  "is_simulated": true,
  "response_time": 12.5
}
```

### 2. Processed Results (`alert_engine_results.json`)
```json
{
  "summary": {
    "total_alerts": 7,
    "actionable": 2,
    "suppressed": 3,
    "deduplicated": 2,
    "tickets_to_create": 2
  },
  "correlated_groups": [...]
}
```

### 3. GitHub Issues
Automatically created with:
- Title: `🔴 CRITICAL | Activity Name - FAILURE`
- Priority labels
- Full alert details
- Error messages
- Correlation info

### 4. Slack Messages
```
🚨 HIGH Alert: Account Verification - FAILURE
Activity: Account Verification
Status: FAILURE
Response Code: 500
Score: 75/100
Error: Internal Server Error
```

### 5. Email Digest
Daily summary with:
- Total alerts processed
- Priority breakdown
- Activity status table
- Test defect count
- Actionable items

---

## ⚙️ Configuration

### Alert Rules (`alert_rules.yaml`)

Define behavior per activity:

```yaml
rules:
  - id: "activity_1"
    activity_name: "Account Verification"
    conditions:
      - name: "response_time_threshold"
        operator: ">"
        value: 5000  # milliseconds
    false_positives:
      - reason: "Maintenance"
        days: [6]  # Sunday
        hours: [22, 23]
```

### Defect Injection (`defect_injection.yaml`)

Control defect injection:

```yaml
defect_injection:
  enabled: true           # Set to false in production
  percentage: 25
  exclude_hours: [9, 10, 11]  # No defects 9-11 AM
```

---

## 🔧 Production Setup

### Disable Defect Injection

**Option 1: Environment Variable**
```bash
export DEFECTS_ENABLED=false
```

**Option 2: GitHub Actions**
Edit `.github/workflows/health-check.yml`:
```yaml
env:
  DEFECTS_ENABLED: false
```

### Configure Notifications

**Slack:**
1. Create workspace and channels
2. Create incoming webhook
3. Add to GitHub Secrets

**Email:**
1. Sign up for SendGrid
2. Create API key
3. Add to GitHub Secrets

---

## 📈 Monitoring

### View Results

```
GitHub Issues: github.com/your-repo/issues
Slack Channels: #monitoring-alerts, #critical-alerts
Local Reports: ./reports/
Dashboard: ./reports/dashboard.html
```

### Check Logs

```bash
tail -f alert_engine.log
```

### Export Data

```python
from database import AlertDatabase
db = AlertDatabase()
db.export_to_csv("monthly_report.csv", hours=720)  # 30 days
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "GITHUB_TOKEN not set" | GitHub Actions provides it automatically |
| "No webhook URL" | Configure SLACK_WEBHOOK_URL in Secrets |
| "No SendGrid key" | Set SENDGRID_API_KEY in Secrets |
| "Port 5502 not responding" | Start local server: `python -m http.server 5502` |
| "ChromeDriver not found" | `pip install webdriver-manager` |

---

## 📋 Checklist for Production

- [ ] All GitHub Secrets configured
- [ ] Slack workspace & webhooks created
- [ ] SendGrid account & API key set up
- [ ] Defect injection disabled (`DEFECTS_ENABLED=false`)
- [ ] Alert rules reviewed
- [ ] Email recipients configured
- [ ] GitHub Actions enabled
- [ ] Test run completed successfully
- [ ] Monitoring dashboard accessible
- [ ] Team notified of monitoring system

---

## 🤝 Integration Examples

### Add to Existing Dashboard

```html
<iframe src="./reports/dashboard.html" width="100%" height="600"></iframe>
```

### Use Alert Data in Scripts

```python
from database import AlertDatabase

db = AlertDatabase()
recent_alerts = db.get_recent_alerts(hours=24)
stats = db.get_alert_statistics()

print(f"Total alerts: {stats['total']}")
print(f"Failure rate: {stats['by_status']['failure']}")
```

### Create Custom Reports

```python
from utils import AlertReporter, DataProcessor

insights = DataProcessor.extract_insights(alerts)
report = AlertReporter.generate_summary_report(alerts, tickets)
```

---

## 📞 Support

**Documentation:** See [SETUP.md](SETUP.md) for detailed setup

**Debug Mode:**
```python
from utils import Logger
logger = Logger()
logger.debug("Debug message")
```

**Export Logs:**
```bash
tail -n 1000 alert_engine.log > debug_logs.txt
```

---

## 📝 License

This project is part of the Sahil Automation Project.

---

## 🎉 What You Get

```
✅ Fully automated 24x7 monitoring
✅ Intelligent alert filtering & correlation
✅ Automatic ticket creation
✅ Real-time Slack notifications
✅ Daily email reports
✅ Defect injection for testing
✅ Comprehensive data persistence
✅ Beautiful dashboards & reports
✅ Production-ready code
✅ Complete documentation
```

---

## 🚀 Next Steps

1. ✅ **Setup complete** - All files created
2. 🔧 **Configure** - Add GitHub Secrets
3. 🧪 **Test locally** - Run scripts individually
4. 📤 **Deploy** - Push to GitHub
5. 📊 **Monitor** - Check dashboard daily

---

**Created:** January 13, 2026  
**Status:** ✅ Production Ready  
**Version:** 1.0.0

---

For questions or issues, refer to [SETUP.md](SETUP.md) or check the code comments in each module.
