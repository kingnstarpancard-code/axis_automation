# 📥 ARTIFACT DOWNLOADS - QUICK REFERENCE

## ✨ What's New

Your Manager Dashboard now has **one-click downloads** for job execution artifacts!

---

## 🎁 Download Options

In the **Manager Dashboard**, for each job execution, you can now download:

### 1. **📊 Excel Report** (Green Button)
```
File: link_check_report.xlsx
Contains: Detailed verification results
Size: ~50-200 KB
Use For: Analysis, sharing, compliance
```

### 2. **🖼️ Screenshots** (Orange Button)
```
Files: screenshot_1.png through screenshot_7.png
Contains: Visual verification images
Size: ~500 KB per set
Use For: Documentation, presentations, visual review
```

### 3. **⚠️ Alerts Data** (Red Button)
```
File: raw_alerts.json
Contains: Alert events and error logs
Size: ~10-50 KB
Use For: Debugging, analysis, root cause investigation
```

---

## 🚀 How to Use

**Step 1**: Open your Manager Dashboard
- Local: `manager_dashboard.html`
- Online: https://kingnstarpancard-code.github.io/axis_automation/manager_dashboard.html

**Step 2**: Go to "Job Executions" tab

**Step 3**: Find the job you want to download

**Step 4**: Click the download buttons in the "Downloads" column:
- 📊 for Excel
- 🖼️ for Screenshots  
- ⚠️ for Alerts

**Step 5**: Files download to your Downloads folder

---

## 📋 Visual Layout

```
Job Executions Table (NEW DOWNLOADS COLUMN):

┌─────────┬──────────┬────────┬────┬─────┬──────┬────┬──────┬──────────────┬───────┐
│ Exec ID │ Time     │ Status │ Total │ OK │ Fail │... │ Dur  │  DOWNLOADS   │Details│
├─────────┼──────────┼────────┼────┼─────┼──────┼────┼──────┼──────────────┼───────┤
│ abc123..│ 6:30 PM  │ ✅     │ 7  │ 6   │ 1    │... │45.32 │📊🖼️⚠️        │📋View │
│ def456..│ 5:45 PM  │ ✅     │ 7  │ 6   │ 1    │... │42.89 │📊🖼️⚠️        │📋View │
│ ghi789..│ 4:20 PM  │ ❌     │ 7  │ 4   │ 3    │... │51.10 │📊🖼️⚠️        │📋View │
└─────────┴──────────┴────────┴────┴─────┴──────┴────┴──────┴──────────────┴───────┘
                                                          ↑
                                                    NEW COLUMN!
```

---

## 💡 What Each File Contains

### **📊 Excel Report**
- System verification results
- Check-by-check breakdown
- Response codes and status
- Timestamps and durations
- Summary statistics
- Professional formatting

### **🖼️ Screenshots**
1. Customer Authentication Verification
2. Transaction Processing Review
3. Account Management Check
4. Fund Transfer Service Audit
5. Balance Inquiry Verification
6. Security Compliance Verification
7. System Availability Monitoring

### **⚠️ Alerts JSON**
- All alert events from the execution
- Error details and messages
- Alert severity levels
- Event IDs and timestamps
- System logs
- Raw data for analysis

---

## ✅ Benefits

✓ **One-click access** to all artifacts  
✓ **No navigation needed** - download from dashboard  
✓ **Automatic naming** with execution ID  
✓ **Multiple formats** for different use cases  
✓ **Works online & offline**  
✓ **Professional organization**  
✓ **Compliance-ready** archiving  

---

## 🎯 Common Tasks

### **Want to share results with team?**
1. Download 📊 Excel report
2. Share via email
3. They can open in Excel or Google Sheets

### **Need visual proof?**
1. Click 🖼️ Screenshots
2. View all verification images
3. Download for documentation

### **Investigating an issue?**
1. Click ⚠️ Alerts
2. Download JSON file
3. Analyze error details

### **Compliance audit?**
1. Download all three (Excel, Screenshots, Alerts)
2. Archive with execution ID
3. Keep for 7 years

---

## 📁 File Locations

**When running locally**, files are saved at:
```
project_root/
├── link_check_report.xlsx
├── raw_alerts.json
└── screenshots/
    ├── screenshot_1.png
    ├── screenshot_2.png
    └── ... (7 total)
```

---

## 🔗 Links

**Manager Dashboard**:
https://kingnstarpancard-code.github.io/axis_automation/manager_dashboard.html

**Full Documentation**:
- `ARTIFACTS_DOWNLOAD_GUIDE.md` - Complete guide
- `ARTIFACT_DOWNLOADS_SUMMARY.md` - Implementation details

---

## 🎉 Ready to Use!

The feature is **live and ready**. Just:

1. Run your automation: `python axis3_enhanced.py`
2. Open the dashboard
3. Click download buttons
4. Access your artifacts!

**That's it!** 🚀
