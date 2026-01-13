"""
Utility Helpers
Common utilities for alert engine system
"""

import json
import logging
import sys
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class Logger:
    """Centralized logging"""
    
    def __init__(self, log_file: str = "alert_engine.log"):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging"""
        
        # Set UTF-8 encoding for console output on Windows
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('AlertEngine')
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def debug(self, message: str):
        self.logger.debug(message)


class ConfigLoader:
    """Load and parse configuration files"""
    
    @staticmethod
    def load_yaml(filepath: str) -> Dict:
        """Load YAML configuration"""
        
        try:
            import yaml
            with open(filepath, 'r') as f:
                return yaml.safe_load(f)
        except ImportError:
            print("⚠️ PyYAML not installed. Install with: pip install pyyaml")
            return {}
        except Exception as e:
            print(f"Error loading YAML: {e}")
            return {}
    
    @staticmethod
    def load_json(filepath: str) -> Dict:
        """Load JSON configuration"""
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {}
    
    @staticmethod
    def save_config(config: Dict, filepath: str):
        """Save configuration to file"""
        
        try:
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✓ Configuration saved to {filepath}")
        except Exception as e:
            print(f"Error saving configuration: {e}")


class Formatter:
    """Format data for display and export"""
    
    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        """Format ISO timestamp for display"""
        
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human-readable format"""
        
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def format_alert_summary(alerts: List[Dict]) -> str:
        """Format alert list as readable summary"""
        
        if not alerts:
            return "No alerts"
        
        summary = f"Total: {len(alerts)} alerts\n"
        
        for alert in alerts[:5]:  # Show first 5
            summary += f"  - {alert.get('activity_name')}: {alert.get('status')}\n"
        
        if len(alerts) > 5:
            summary += f"  ... and {len(alerts) - 5} more\n"
        
        return summary
    
    @staticmethod
    def format_json(data: Dict, pretty: bool = True) -> str:
        """Format data as JSON"""
        
        if pretty:
            return json.dumps(data, indent=2)
        else:
            return json.dumps(data)


class Validator:
    """Validate input data"""
    
    @staticmethod
    def validate_alert(alert: Dict) -> tuple[bool, str]:
        """Validate alert structure"""
        
        required_fields = ["alert_id", "timestamp", "activity_name", "status"]
        
        for field in required_fields:
            if field not in alert:
                return False, f"Missing required field: {field}"
        
        if alert["status"] not in ["success", "failure", "error"]:
            return False, f"Invalid status: {alert['status']}"
        
        return True, "Valid"
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_webhook_url(url: str) -> bool:
        """Validate webhook URL"""
        
        return url.startswith("https://") and "webhook" in url.lower()


class DataProcessor:
    """Process and transform data"""
    
    @staticmethod
    def merge_alerts(alerts: List[Dict]) -> Dict:
        """Merge multiple alerts into single report"""
        
        if not alerts:
            return {}
        
        merged = {
            "total": len(alerts),
            "timestamp": datetime.now().isoformat(),
            "activities": set(),
            "statuses": {},
            "response_codes": {},
            "avg_response_time": 0,
            "errors": []
        }
        
        total_response_time = 0
        count_with_time = 0
        
        for alert in alerts:
            merged["activities"].add(alert.get("activity_name", "Unknown"))
            
            status = alert.get("status", "unknown")
            merged["statuses"][status] = merged["statuses"].get(status, 0) + 1
            
            code = alert.get("response_code")
            if code:
                merged["response_codes"][str(code)] = merged["response_codes"].get(str(code), 0) + 1
            
            if alert.get("response_time"):
                total_response_time += alert["response_time"]
                count_with_time += 1
            
            if alert.get("error_message"):
                merged["errors"].append(alert["error_message"])
        
        merged["activities"] = list(merged["activities"])
        merged["avg_response_time"] = (
            total_response_time / count_with_time if count_with_time > 0 else 0
        )
        
        return merged
    
    @staticmethod
    def extract_insights(alerts: List[Dict]) -> Dict:
        """Extract insights from alerts"""
        
        if not alerts:
            return {}
        
        insights = {
            "most_common_error": None,
            "most_affected_activity": None,
            "failure_rate": 0,
            "pattern": "normal"
        }
        
        # Most common error
        errors = [a.get("error_message") for a in alerts if a.get("error_message")]
        if errors:
            insights["most_common_error"] = max(set(errors), key=errors.count)
        
        # Most affected activity
        activities = [a.get("activity_name") for a in alerts]
        if activities:
            insights["most_affected_activity"] = max(set(activities), key=activities.count)
        
        # Failure rate
        failures = len([a for a in alerts if a.get("status") == "failure"])
        insights["failure_rate"] = (failures / len(alerts)) * 100 if alerts else 0
        
        # Pattern detection
        if insights["failure_rate"] > 70:
            insights["pattern"] = "critical_outage"
        elif insights["failure_rate"] > 30:
            insights["pattern"] = "widespread_issues"
        elif insights["failure_rate"] > 10:
            insights["pattern"] = "intermittent_issues"
        
        return insights


class TimeHelper:
    """Time-related utilities"""
    
    @staticmethod
    def get_execution_window() -> tuple[str, str]:
        """Get start and end time of current execution window"""
        
        now = datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
        
        return start.isoformat(), end.isoformat()
    
    @staticmethod
    def is_maintenance_window() -> bool:
        """Check if currently in maintenance window"""
        
        now = datetime.now()
        # Sunday 22:00-23:59
        return now.weekday() == 6 and 22 <= now.hour < 24
    
    @staticmethod
    def get_time_until_maintenance() -> str:
        """Get time until next maintenance window"""
        
        now = datetime.now()
        
        # If it's Sunday, calculate for next Sunday
        days_until_sunday = (6 - now.weekday()) % 7
        if days_until_sunday == 0 and now.hour >= 22:
            days_until_sunday = 7
        
        next_maintenance = now.replace(hour=22, minute=0, second=0, microsecond=0)
        if days_until_sunday > 0:
            from datetime import timedelta
            next_maintenance += timedelta(days=days_until_sunday)
        
        time_diff = next_maintenance - now
        
        hours = int(time_diff.total_seconds() / 3600)
        minutes = int((time_diff.total_seconds() % 3600) / 60)
        
        return f"{hours}h {minutes}m"


class AlertReporter:
    """Generate reports from alert data"""
    
    @staticmethod
    def generate_summary_report(alerts: List[Dict], 
                               tickets: List[Dict]) -> Dict:
        """Generate summary report"""
        
        return {
            "report_generated": datetime.now().isoformat(),
            "total_alerts_processed": len(alerts),
            "total_tickets_created": len(tickets),
            "summary_by_status": {
                "success": len([a for a in alerts if a.get("status") == "success"]),
                "failure": len([a for a in alerts if a.get("status") == "failure"]),
                "error": len([a for a in alerts if a.get("status") == "error"])
            },
            "summary_by_priority": {
                "critical": len([t for t in tickets if t.get("score", 0) > 85]),
                "high": len([t for t in tickets if 70 < t.get("score", 0) <= 85]),
                "medium": len([t for t in tickets if t.get("score", 0) <= 70])
            },
            "top_activities": Formatter.format_alert_summary(alerts)
        }
    
    @staticmethod
    def generate_html_report(data: Dict) -> str:
        """Generate HTML report"""
        
        html = f"""
        <html>
        <head>
            <title>Alert Engine Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Alert Engine Report</h1>
            <p>Generated: {data.get('report_generated', 'N/A')}</p>
            
            <h2>Summary</h2>
            <ul>
                <li>Total Alerts: {data.get('total_alerts_processed', 0)}</li>
                <li>Tickets Created: {data.get('total_tickets_created', 0)}</li>
            </ul>
            
            <h2>Status Breakdown</h2>
            <table>
                <tr>
                    <th>Status</th>
                    <th>Count</th>
                </tr>
        """
        
        for status, count in data.get('summary_by_status', {}).items():
            html += f"<tr><td>{status}</td><td>{count}</td></tr>"
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html
