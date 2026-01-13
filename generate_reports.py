"""
Report Generation Script
Generates comprehensive reports from alert data
"""

import json
import os
from datetime import datetime
from pathlib import Path
from database import AlertDatabase
from utils import Logger, AlertReporter, Formatter


def main():
    """Generate comprehensive reports"""
    
    logger = Logger()
    logger.info("=" * 60)
    logger.info("📊 Generating Comprehensive Reports")
    logger.info("=" * 60)
    
    # Create reports directory
    Path("reports").mkdir(exist_ok=True)
    
    # Load data
    db = AlertDatabase()
    
    # Load processed results
    if not os.path.exists("alert_engine_results.json"):
        logger.warning("alert_engine_results.json not found")
        return
    
    with open("alert_engine_results.json", "r") as f:
        engine_results = json.load(f)
    
    # Load tickets
    tickets = []
    if os.path.exists("ticket_summary.json"):
        with open("ticket_summary.json", "r") as f:
            ticket_summary = json.load(f)
            tickets = ticket_summary.get('tickets', [])
    
    logger.info(f"\n📥 Loaded data:")
    logger.info(f"  ├─ Raw alerts: {engine_results['summary']['total_alerts']}")
    logger.info(f"  ├─ Actionable: {engine_results['summary']['actionable']}")
    logger.info(f"  ├─ Tickets: {len(tickets)}")
    logger.info(f"  └─ Time range: Last 24 hours")
    
    # Generate summary report
    logger.info(f"\n▶️  Generating reports...")
    
    # 1. Executive Summary
    summary_report = AlertReporter.generate_summary_report(
        engine_results.get('alerts', []),
        tickets
    )
    
    with open("reports/executive_summary.json", "w") as f:
        json.dump(summary_report, f, default=str, indent=2)
    logger.info(f"  ├─ Executive summary: ✓")
    
    # 2. Detailed Alert Report
    detailed_report = {
        "timestamp": datetime.now().isoformat(),
        "summary": engine_results['summary'],
        "actionable_alerts": engine_results.get('actionable_alerts', []),
        "suppressed_alerts": engine_results.get('suppressed_alerts', []),
        "correlated_groups": engine_results.get('correlated_groups', [])
    }
    
    with open("reports/detailed_alert_report.json", "w") as f:
        json.dump(detailed_report, f, default=str, indent=2)
    logger.info(f"  ├─ Detailed alert report: ✓")
    
    # 3. Ticket Report
    ticket_report = {
        "timestamp": datetime.now().isoformat(),
        "total_tickets": len(tickets),
        "by_priority": {
            "critical": len([t for t in tickets if t.get('score', 0) > 85]),
            "high": len([t for t in tickets if 70 < t.get('score', 0) <= 85]),
            "medium": len([t for t in tickets if t.get('score', 0) <= 70])
        },
        "by_type": {
            "test_defects": len([t for t in tickets if t.get('is_simulated')]),
            "production": len([t for t in tickets if not t.get('is_simulated')])
        },
        "tickets": tickets
    }
    
    with open("reports/ticket_report.json", "w") as f:
        json.dump(ticket_report, f, default=str, indent=2)
    logger.info(f"  ├─ Ticket report: ✓")
    
    # 4. Database Statistics
    stats = db.get_alert_statistics(hours=24)
    
    stats_report = {
        "timestamp": datetime.now().isoformat(),
        "statistics": stats,
        "execution_history": db.get_execution_history(limit=20)
    }
    
    with open("reports/statistics.json", "w") as f:
        json.dump(stats_report, f, default=str, indent=2)
    logger.info(f"  ├─ Statistics: ✓")
    
    # 5. HTML Dashboard
    html_content = _generate_html_dashboard(summary_report, ticket_report, stats)
    
    with open("reports/dashboard.html", "w") as f:
        f.write(html_content)
    logger.info(f"  ├─ HTML dashboard: ✓")
    
    # 6. CSV Export
    try:
        db.export_to_csv("reports/alerts_export.csv", hours=24)
        logger.info(f"  └─ CSV export: ✓")
    except:
        logger.info(f"  └─ CSV export: ✗")
    
    logger.info(f"\n✅ Reports generated in: ./reports/")
    logger.info(f"  ├─ executive_summary.json")
    logger.info(f"  ├─ detailed_alert_report.json")
    logger.info(f"  ├─ ticket_report.json")
    logger.info(f"  ├─ statistics.json")
    logger.info(f"  ├─ dashboard.html")
    logger.info(f"  └─ alerts_export.csv")
    
    logger.info(f"\n📊 Report Statistics:")
    logger.info(f"  ├─ Total Alerts: {engine_results['summary']['total_alerts']}")
    logger.info(f"  ├─ Actionable: {engine_results['summary']['actionable']}")
    logger.info(f"  ├─ Suppressed: {engine_results['summary']['suppressed']}")
    logger.info(f"  ├─ Tickets: {ticket_report['total_tickets']}")
    logger.info(f"  ├─ Critical Issues: {ticket_report['by_priority']['critical']}")
    logger.info(f"  └─ Test Defects: {ticket_report['by_type']['test_defects']}")
    
    logger.info(f"\n✅ Report generation completed at {datetime.now().isoformat()}")
    logger.info("=" * 60)


def _generate_html_dashboard(summary, tickets, stats):
    """Generate HTML dashboard"""
    
    critical_count = tickets['by_priority']['critical']
    high_count = tickets['by_priority']['high']
    medium_count = tickets['by_priority']['medium']
    test_count = tickets['by_type']['test_defects']
    
    # Determine status color
    if critical_count > 0:
        status_color = "#dc143c"
        status_text = "⚠️ Critical Issues"
    elif high_count > 0:
        status_color = "#ff8c00"
        status_text = "⚠️ High Priority"
    elif medium_count > 0:
        status_color = "#ffd700"
        status_text = "⚠️ Medium Priority"
    else:
        status_color = "#36a64f"
        status_text = "✅ All Clear"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Alert Engine Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            header {{
                background: white;
                padding: 30px;
                border-radius: 8px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            h1 {{
                color: #333;
                margin-bottom: 10px;
            }}
            
            .timestamp {{
                color: #666;
                font-size: 14px;
            }}
            
            .status-banner {{
                background: {status_color};
                color: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
            }}
            
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            .card h3 {{
                color: #666;
                font-size: 14px;
                text-transform: uppercase;
                margin-bottom: 10px;
            }}
            
            .card .value {{
                font-size: 32px;
                font-weight: bold;
                color: #333;
            }}
            
            .card.critical .value {{
                color: #dc143c;
            }}
            
            .card.high .value {{
                color: #ff8c00;
            }}
            
            .card.medium .value {{
                color: #ffd700;
            }}
            
            .card.success .value {{
                color: #36a64f;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            th {{
                background: #f0f0f0;
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #333;
                border-bottom: 2px solid #ddd;
            }}
            
            td {{
                padding: 15px;
                border-bottom: 1px solid #eee;
            }}
            
            tr:hover {{
                background: #f9f9f9;
            }}
            
            .badge {{
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
            }}
            
            .badge.critical {{
                background: #dc143c;
                color: white;
            }}
            
            .badge.high {{
                background: #ff8c00;
                color: white;
            }}
            
            .badge.medium {{
                background: #ffd700;
                color: #333;
            }}
            
            .badge.test {{
                background: #6c5ce7;
                color: white;
            }}
            
            footer {{
                text-align: center;
                color: white;
                margin-top: 40px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🤖 Alert Engine Dashboard</h1>
                <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </header>
            
            <div class="status-banner">
                {status_text}
            </div>
            
            <div class="grid">
                <div class="card success">
                    <h3>Total Alerts</h3>
                    <div class="value">{summary['total_alerts_processed']}</div>
                </div>
                
                <div class="card critical">
                    <h3>Critical</h3>
                    <div class="value">{critical_count}</div>
                </div>
                
                <div class="card high">
                    <h3>High Priority</h3>
                    <div class="value">{high_count}</div>
                </div>
                
                <div class="card medium">
                    <h3>Medium Priority</h3>
                    <div class="value">{medium_count}</div>
                </div>
                
                <div class="card">
                    <h3>Tickets Created</h3>
                    <div class="value">{summary['total_tickets_created']}</div>
                </div>
                
                <div class="card">
                    <h3>Test Defects</h3>
                    <div class="value">{test_count}</div>
                </div>
            </div>
            
            <h2 style="color: white; margin-bottom: 20px;">📋 Priority Breakdown</h2>
            <table>
                <thead>
                    <tr>
                        <th>Priority</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="badge critical">Critical</span></td>
                        <td>{critical_count}</td>
                        <td>{(critical_count / summary['total_tickets_created'] * 100) if summary['total_tickets_created'] > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td><span class="badge high">High</span></td>
                        <td>{high_count}</td>
                        <td>{(high_count / summary['total_tickets_created'] * 100) if summary['total_tickets_created'] > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td><span class="badge medium">Medium</span></td>
                        <td>{medium_count}</td>
                        <td>{(medium_count / summary['total_tickets_created'] * 100) if summary['total_tickets_created'] > 0 else 0:.1f}%</td>
                    </tr>
                    <tr>
                        <td><span class="badge test">Test Defects</span></td>
                        <td>{test_count}</td>
                        <td>{(test_count / summary['total_alerts_processed'] * 100) if summary['total_alerts_processed'] > 0 else 0:.1f}%</td>
                    </tr>
                </tbody>
            </table>
            
            <footer>
                <p>🤖 Alert Engine v1.0 | 24x7 Automated Monitoring System</p>
                <p>Reports generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    main()
