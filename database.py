"""
Database Module
Manages alert history and data persistence using JSON
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path


class AlertDatabase:
    """JSON-based database for alert storage"""
    
    def __init__(self, db_file: str = "alert_database.json"):
        self.db_file = db_file
        self.data = self._load_database()
    
    def add_alert(self, alert: Dict):
        """Add alert to database"""
        
        if "alerts" not in self.data:
            self.data["alerts"] = []
        
        self.data["alerts"].append({
            **alert,
            "stored_at": datetime.now().isoformat()
        })
        
        self._save_database()
    
    def add_ticket(self, ticket: Dict):
        """Add ticket to database"""
        
        if "tickets" not in self.data:
            self.data["tickets"] = []
        
        self.data["tickets"].append({
            **ticket,
            "stored_at": datetime.now().isoformat()
        })
        
        self._save_database()
    
    def get_alerts_for_activity(self, activity_name: str, 
                                hours: int = 24) -> List[Dict]:
        """Get recent alerts for specific activity"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        alerts = [
            alert for alert in self.data.get("alerts", [])
            if alert.get("activity_name") == activity_name
            and datetime.fromisoformat(alert.get("timestamp", "")) > cutoff_time
        ]
        
        return alerts
    
    def get_recent_alerts(self, hours: int = 24, 
                         limit: int = 100) -> List[Dict]:
        """Get recent alerts"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        alerts = [
            alert for alert in self.data.get("alerts", [])
            if datetime.fromisoformat(alert.get("timestamp", "")) > cutoff_time
        ]
        
        return sorted(alerts, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
    
    def get_open_tickets(self) -> List[Dict]:
        """Get all open tickets"""
        
        return [
            ticket for ticket in self.data.get("tickets", [])
            if ticket.get("status") in ["open", "in-progress"]
        ]
    
    def update_ticket_status(self, ticket_id: str, status: str):
        """Update ticket status"""
        
        for ticket in self.data.get("tickets", []):
            if ticket.get("id") == ticket_id or ticket.get("issue_number") == ticket_id:
                ticket["status"] = status
                ticket["updated_at"] = datetime.now().isoformat()
                self._save_database()
                return True
        
        return False
    
    def get_alert_statistics(self, hours: int = 24) -> Dict:
        """Get alert statistics"""
        
        alerts = self.get_recent_alerts(hours)
        
        if not alerts:
            return {"message": "No alerts in time period"}
        
        return {
            "total": len(alerts),
            "by_status": {
                "success": len([a for a in alerts if a.get("status") == "success"]),
                "failure": len([a for a in alerts if a.get("status") == "failure"]),
                "error": len([a for a in alerts if a.get("status") == "error"])
            },
            "by_activity": self._group_by_activity(alerts),
            "high_score_alerts": len([a for a in alerts if a.get("score", 0) > 70]),
            "simulated_defects": len([a for a in alerts if a.get("is_simulated")])
        }
    
    def cleanup_old_records(self, days: int = 30):
        """Remove old records from database"""
        
        cutoff_time = datetime.now() - timedelta(days=days)
        
        initial_count = len(self.data.get("alerts", []))
        
        self.data["alerts"] = [
            alert for alert in self.data.get("alerts", [])
            if datetime.fromisoformat(alert.get("stored_at", "")) > cutoff_time
        ]
        
        removed = initial_count - len(self.data.get("alerts", []))
        self._save_database()
        
        return f"Removed {removed} old alert records"
    
    def _group_by_activity(self, alerts: List[Dict]) -> Dict:
        """Group alerts by activity"""
        
        grouped = {}
        for alert in alerts:
            activity = alert.get("activity_name", "Unknown")
            grouped[activity] = grouped.get(activity, 0) + 1
        
        return grouped
    
    def _load_database(self) -> Dict:
        """Load database from file"""
        
        if Path(self.db_file).exists():
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading database: {e}")
        
        return {
            "alerts": [],
            "tickets": [],
            "created_at": datetime.now().isoformat()
        }
    
    def _save_database(self):
        """Save database to file"""
        
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def export_to_csv(self, filepath: str = "alerts_export.csv", 
                      hours: int = 24):
        """Export alerts to CSV"""
        
        import csv
        
        alerts = self.get_recent_alerts(hours)
        
        if not alerts:
            print("No alerts to export")
            return
        
        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=alerts[0].keys())
                writer.writeheader()
                writer.writerows(alerts)
            
            print(f"✓ Exported {len(alerts)} alerts to {filepath}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
    
    def get_execution_history(self, limit: int = 50) -> List[Dict]:
        """Get execution history"""
        
        executions = {}
        
        for alert in self.data.get("alerts", []):
            exec_id = alert.get("execution_id", "unknown")
            if exec_id not in executions:
                executions[exec_id] = {
                    "execution_id": exec_id,
                    "timestamp": alert.get("timestamp"),
                    "alert_count": 0,
                    "activities": set()
                }
            
            executions[exec_id]["alert_count"] += 1
            executions[exec_id]["activities"].add(alert.get("activity_name"))
        
        # Convert to list and sort
        result = []
        for exec_id, data in sorted(executions.items(), reverse=True):
            data["activities"] = list(data["activities"])
            result.append(data)
        
        return result[:limit]
