# 📥 Artifact Downloads Guide - Manager Dashboard

## Overview

The Manager Dashboard now includes **one-click downloads** for all job execution artifacts:
- 📊 **Excel Reports** (link_check_report.xlsx)
- 🖼️ **Screenshots** (All verification screenshots)
- ⚠️ **Alert Data** (raw_alerts.json)

---

## 🎯 How to Download Artifacts

### **Step 1: Access the Manager Dashboard**

**Local**: Open `manager_dashboard.html` in your browser  
**Online**: https://kingnstarpancard-code.github.io/axis_automation/manager_dashboard.html

### **Step 2: Go to "Job Executions" Tab**

- Click the 📊 **Job Executions** tab (default)
- You'll see a list of past job runs

### **Step 3: Click Download Buttons**

In the **Downloads** column, you'll see buttons for each execution:

| Button | What It Is | File Type |
|--------|-----------|-----------|
| 📊 Excel | Job verification report | .xlsx (Excel) |
| 🖼️ Screenshots | All verification screenshots | .png files |
| ⚠️ Alerts | Alert events data | .json (JSON) |

---

## 💡 What Each Artifact Contains

### **📊 Excel Report (link_check_report.xlsx)**

Contains:
- System check results
- Response codes
- Verification status
- Check details
- Timestamps
- Summary statistics

**Use for**: 
- ✅ Detailed verification report
- ✅ Spreadsheet analysis
- ✅ Print/Email to stakeholders

---

### **🖼️ Screenshots**

Contains images of:
1. Customer Authentication Verification
2. Transaction Processing Review
3. Account Management Check
4. Fund Transfer Service Audit
5. Balance Inquiry Verification
6. Security Compliance Verification
7. System Availability Monitoring

**Use for**:
- ✅ Visual verification
- ✅ Documentation
- ✅ Presentations
- ✅ Compliance records

---

### **⚠️ Alerts JSON (raw_alerts.json)**

Contains:
- Raw alert events
- Error details
- System messages
- Alert severity levels
- Timestamps
- Event IDs

**Use for**:
- ✅ Detailed analysis
- ✅ System debugging
- ✅ Alert correlation
- ✅ Root cause analysis

---

## 📱 Using Downloads

### **For Local Execution**

When you run the automation script locally:

```bash
python axis3_enhanced.py
```

Generated files are created:
- `link_check_report.xlsx` - In project root
- `raw_alerts.json` - In project root  
- `screenshots/screenshot_1.png` through `screenshot_7.png` - In screenshots folder

**Download Process:**
1. Click the download button in dashboard
2. File downloads to your Downloads folder
3. Open with appropriate application

### **For GitHub Pages**

When accessing online dashboard:

1. **Excel & Alerts**: 
   - Shows file info dialog
   - Explains where files are located
   - Points you to local copy or repo

2. **Screenshots**:
   - Shows available screenshots
   - Provides direct links
   - Lists GitHub repo path

---

## 🔍 Understanding the Download Buttons

### **Green 📊 Excel Button**
```
- Status: Report file ready
- Click to: Download .xlsx file
- File size: ~50-200 KB
- Contains: Verification results
```

### **Orange 🖼️ Screenshots Button**
```
- Status: Screenshots available
- Click to: View screenshot info
- # of files: Matches total checks run
- Contains: PNG images of verifications
```

### **Red ⚠️ Alerts Button**
```
- Status: Alert data available
- Click to: Download JSON file
- File size: ~10-50 KB
- Contains: Raw alert events
```

---

## 📊 Example Workflow

### **Scenario: Want to Review Job #5**

1. **Open Dashboard**
   - https://kingnstarpancard-code.github.io/axis_automation/manager_dashboard.html

2. **Find Execution**
   - Scroll to row with execution you want
   - Look at timestamp to identify

3. **Download Report**
   - Click 📊 Excel button
   - Opens report in Excel
   - Review results

4. **Check Screenshots**
   - Click 🖼️ Screenshots button
   - See all verification images
   - Download for documentation

5. **Analyze Alerts** (if any)
   - Click ⚠️ Alerts button
   - Download JSON file
   - Open in text editor
   - Analyze alert events

---

## 🚀 Quick Tips

### **Tip 1: Organize Downloads**
- Create folder: `Job_Executions_Archive`
- Save downloads with execution ID: `exec_abc123_report.xlsx`
- Keep all artifacts together

### **Tip 2: Batch Download**
- If multiple jobs completed, download from oldest to newest
- Or download specific ones you need
- Keep organized by date

### **Tip 3: Share Reports**
- Download Excel report
- Email to stakeholders
- Great for compliance reviews
- Professional presentation

### **Tip 4: Troubleshooting**
- If file not found: Run automation first
- Check dashboard updates after each run
- Files persist across sessions
- Accessible on next visit

---

## 📋 Download Checklist

When reviewing a job execution:

- [ ] Download Excel report for detailed results
- [ ] Review screenshots for visual verification  
- [ ] Check alerts for any issues
- [ ] Archive files with execution ID
- [ ] Document any findings
- [ ] Share with team if needed

---

## 🔗 File Locations

### **Local (When Running Locally)**

```
project_root/
├── link_check_report.xlsx      ← Excel download
├── raw_alerts.json             ← Alerts download
└── screenshots/
    ├── screenshot_1.png        ← Screenshots
    ├── screenshot_2.png
    ├── screenshot_3.png
    ├── screenshot_4.png
    ├── screenshot_5.png
    ├── screenshot_6.png
    └── screenshot_7.png
```

### **GitHub Repository**

```
github.com/kingnstarpancard-code/axis_automation/
├── link_check_report.xlsx
├── raw_alerts.json
└── screenshots/
    └── (all .png files)
```

---

## ⚙️ Technical Details

### **How Downloads Work**

1. **Excel Files**: 
   - Fetched from project directory
   - Downloaded with execution ID prefix
   - Opens in Excel, Google Sheets, or compatible app

2. **Screenshots**:
   - Located in `screenshots/` folder
   - Named: `screenshot_1.png` through `screenshot_7.png`
   - Can view or download individually

3. **Alerts JSON**:
   - Raw data file in JSON format
   - Can view in browser
   - Download as text file
   - Parse with any JSON tool

### **Browser Compatibility**

✅ Works in:
- Google Chrome (latest)
- Microsoft Edge (latest)
- Mozilla Firefox (latest)
- Safari (latest)

---

## 🆘 Troubleshooting Downloads

### **"File not found" Error**

**Solution**:
1. Run the automation script first: `python axis3_enhanced.py`
2. Wait for script to complete
3. Return to dashboard
4. Try download again

### **Screenshot not available**

**Solution**:
1. Check if automation ran successfully
2. Look for 🟢 SUCCESS badge in dashboard
3. If failed (🔴), no screenshots generated
4. Run automation again

### **Can't open downloaded file**

**Solution**:
- Excel: Use Excel, Google Sheets, LibreOffice
- JSON: Use text editor, VS Code, or online viewer
- PNG: Use any image viewer

### **Downloads folder is empty**

**Solution**:
1. Check your Downloads folder location
2. Try right-click → "Open containing folder"
3. Files might be in Documents or Desktop
4. Search for filename with file type

---

## 💾 Best Practices

### **Archive Strategy**

Create this folder structure:
```
Audit_Archive/
├── 2026_02_09/
│   ├── exec_abc123_report.xlsx
│   ├── exec_abc123_alerts.json
│   └── screenshots_abc123/
│       ├── 1_auth.png
│       ├── 2_transaction.png
│       └── ... (others)
│
├── 2026_02_08/
│   └── (previous executions)
```

### **Naming Convention**

Use this format:
```
{EXECUTION_ID}_{FILE_TYPE}_{DATE}.{EXT}

Example:
a1b2c3d4_report_2026-02-09.xlsx
a1b2c3d4_alerts_2026-02-09.json
```

### **Regular Backups**

- Download reports weekly
- Store on external drive
- Keep 3-month rolling archive
- Version important reports

---

## 📈 Use Cases

### **Compliance Audit**
✅ Download Excel reports
✅ Download all screenshots
✅ Archive for 7 years
✅ Generate summary

### **Incident Investigation**
✅ Download alerts JSON
✅ Analyze event sequence
✅ Identify root cause
✅ Document findings

### **Team Review**
✅ Download report
✅ Share via email
✅ Discuss findings
✅ Plan next steps

### **System Monitoring**
✅ Track success rates
✅ Monitor trends
✅ Identify patterns
✅ Plan improvements

---

## 🔐 Security Notes

- All downloads are **local to your system**
- No data sent to external services
- Files are **read-only** after download
- Keep sensitive data **secure**
- Comply with your **data retention policy**

---

## 📞 Support

For download issues:
1. Check this guide
2. Try troubleshooting section
3. Verify files exist locally
4. Run automation again
5. Check file permissions

---

## ✨ Summary

The artifact download feature makes it easy to:
- 📊 Get detailed Excel reports
- 🖼️ View verification screenshots
- ⚠️ Analyze alert data
- 📁 Archive for compliance
- 🔍 Review historical executions
- 📤 Share with stakeholders

**All with one click from the dashboard!**

---

**Last Updated**: February 9, 2026  
**Feature Status**: ✅ FULLY FUNCTIONAL
