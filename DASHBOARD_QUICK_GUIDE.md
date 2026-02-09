# 📊 Manager Dashboard - Quick Start Guide

## 🎯 Quick Access

**Local**: Open `manager_dashboard.html` in your browser  
**Online**: https://kingnstarpancard-code.github.io/axis_automation/manager_dashboard.html

---

## 📱 Dashboard Overview

### **Two Main Tabs**

#### 1️⃣ **Job Executions** (Default)
View automatic job run history and statistics

**What You'll See:**
- 📊 **Statistics Cards** at the top:
  - Total Executions
  - Successful Runs (green)
  - Failed Runs (red)
  - Total Checks Completed
  - Success Rate %
  - Last Execution Time

- 📋 **Execution History Table**:
  - Execution ID
  - Date & Time
  - Status (Success/Failed badge)
  - Number of checks
  - Success/Failure counts
  - Test defects
  - Duration
  - View button for details

#### 2️⃣ **Verification Report**
View system health check verification records

---

## ✅ How It Works

### **Automatic Logging**

When you run the automation script:
```bash
python axis3_enhanced.py
```

The system automatically:
1. Captures execution start time
2. Runs all 7 banking system checks
3. Logs execution details to `job_executions.json`
4. Displays on dashboard immediately

**No manual intervention needed!**

---

## 🖱️ Dashboard Features

### **Refresh Data**
Click the **🔄 Refresh Data** button to manually reload job history.

*Note*: Dashboard auto-refreshes every 30 seconds automatically.

### **View Execution Details**
Click the **📋 View** link in the table to see:
- Full execution ID
- Timestamp
- Status
- All check counts
- Output files
- Exact duration

### **Tab Navigation**
- Click "📊 Job Executions" to see running history
- Click "✓ Verification Report" to see system checks

---

## 📊 Statistics Explained

| Metric | Description |
|--------|-------------|
| **Total Executions** | How many times the job has run |
| **Successful Runs** | Number of successful executions |
| **Failed Runs** | Number of failed executions |
| **Total Checks Completed** | Total of all checks across all runs |
| **Success Rate** | Percentage of successful runs |
| **Last Execution** | When the job last ran |

---

## 🎨 Color Coding

- 🟢 **Green**: Successful execution or check
- 🔴 **Red**: Failed execution or check
- 🔵 **Blue**: Primary color for navigation
- ⚪ **Gray**: Supporting information

---

## 📝 Example Data

When a job runs successfully, you'll see:
```
Execution ID:     a1b2c3d4...
Timestamp:        Feb 9, 2026 6:30 PM
Status:           ✅ SUCCESS
Total Checks:     7
Successful:       6
Failed:           1
Test Defects:     2
Duration:         45.32 seconds
```

---

## ⚙️ System Files

Behind the scenes, these files work together:

| File | Purpose |
|------|---------|
| `manager_dashboard.html` | The dashboard interface |
| `job_executions.json` | Stores execution history |
| `axis3_enhanced.py` | Automation script |
| `job_execution_logger.py` | Logging system |

---

## 🚨 Troubleshooting

### **Dashboard shows "No execution data available yet"**
- ✅ Run the automation script: `python axis3_enhanced.py`
- ✅ Wait 30 seconds for auto-refresh
- ✅ Click "🔄 Refresh Data" manually

### **Job Executions tab is empty**
- ✅ Check that `job_executions.json` exists
- ✅ Run the automation script to generate data
- ✅ Check browser console for errors (F12)

### **Data looks old**
- ✅ Click "🔄 Refresh Data" button
- ✅ Try refreshing the page (Ctrl+R)
- ✅ Check that automation script is running

---

## 📈 Performance

- **Load Time**: < 1 second
- **Auto-Refresh**: Every 30 seconds
- **Data Retention**: Last 100 executions
- **File Size**: ~7KB average (optimized)

---

## 🎯 Common Tasks

### **I want to see all executions**
1. Go to "Job Executions" tab
2. Table shows newest first
3. Scroll down to see older runs

### **I want to know if a job succeeded**
1. Look for green ✅ SUCCESS badge
2. Check "Successful" count
3. View details for more info

### **I want to see how long a job took**
1. Check "Duration (s)" column
2. Click "📋 View" for exact time
3. Or check "Last Execution" timestamp

### **I want to export data**
1. Open browser DevTools (F12)
2. Go to Application → Local Storage
3. Find `reportData` key
4. Copy the JSON data

---

## 🔐 Data Security

- Data stored locally in JSON file
- No data sent to external servers
- All processing happens locally
- Compatible with GitHub Pages (public)

---

## 📱 Mobile Access

Dashboard is **fully responsive**:
- ✅ Works on phones (320px+)
- ✅ Works on tablets (768px+)
- ✅ Works on desktops (1024px+)

---

## 🎨 Theme

- **Professional Axis Bank Design**
- **Modern, Clean Interface**
- **Color-coded status indicators**
- **Smooth animations**
- **Responsive layout**

---

## 📞 Support

For issues or questions:
1. Check this quick guide
2. Review the full documentation
3. Check automation script logs
4. Verify `job_executions.json` exists

---

## 💡 Tips

✨ **Pro Tips:**
- Dashboard works best in Chrome or Edge
- Auto-refresh means you don't need to refresh manually
- Click card values to see more details
- Use "View" button to see full execution info
- Run jobs regularly to maintain history

---

**Last Updated**: February 9, 2026  
**Status**: ✅ FULLY FUNCTIONAL
