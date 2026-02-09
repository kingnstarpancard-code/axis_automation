"""
Job Execution Logger
Logs all successful job runs to a dashboard-accessible file
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class JobExecutionLogger:
    """Logs job executions for dashboard display"""
    
    def __init__(self, log_file: str = "job_executions.json"):
        self.log_file = log_file
        self.ensure_log_file_exists()
    
    def ensure_log_file_exists(self):
        """Create log file if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f, indent=2)
    
    def log_execution(self, execution_data: Dict[str, Any]) -> bool:
        """
        Log a job execution
        
        Args:
            execution_data: Dict with execution details
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read existing logs
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            # Ensure it's a list
            if not isinstance(logs, list):
                logs = []
            
            # Add timestamp if not present
            if 'timestamp' not in execution_data:
                execution_data['timestamp'] = datetime.now().isoformat()
            
            # Add execution ID if not present
            if 'execution_id' not in execution_data:
                import uuid
                execution_data['execution_id'] = str(uuid.uuid4())
            
            # Append new execution
            logs.append(execution_data)
            
            # Keep only last 100 executions (optimize file size)
            if len(logs) > 100:
                logs = logs[-100:]
            
            # Write back
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Error logging execution: {e}")
            return False
    
    def get_executions(self, limit: int = None) -> List[Dict]:
        """
        Get all logged executions
        
        Args:
            limit: Maximum number of executions to return (None = all)
            
        Returns:
            List of execution records
        """
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            if limit:
                return logs[-limit:]
            return logs
        
        except Exception as e:
            print(f"Error reading executions: {e}")
            return []
    
    def get_latest_execution(self) -> Dict[str, Any]:
        """Get the most recent execution"""
        executions = self.get_executions(limit=1)
        return executions[0] if executions else {}
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about job executions"""
        executions = self.get_executions()
        
        if not executions:
            return {
                'total_executions': 0,
                'successful': 0,
                'failed': 0,
                'success_rate': 0,
                'last_execution': None,
                'total_checks': 0,
                'average_checks_per_run': 0,
                'total_successful_checks': 0,
                'total_failed_checks': 0,
                'total_defects_simulated': 0,
                'average_duration_seconds': 0
            }
        
        successful = sum(1 for e in executions if e.get('status') == 'success')
        failed = sum(1 for e in executions if e.get('status') == 'failed')
        total_checks = sum(e.get('total_checks', 0) for e in executions)
        total_successful_checks = sum(e.get('success_count', 0) for e in executions)
        total_failed_checks = sum(e.get('failure_count', 0) for e in executions)
        total_defects = sum(e.get('simulated_defects', 0) for e in executions)
        total_duration = sum(e.get('duration_seconds', 0) for e in executions)
        
        return {
            'total_executions': len(executions),
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / len(executions) * 100) if executions else 0,
            'last_execution': executions[-1].get('timestamp'),
            'total_checks': total_checks,
            'average_checks_per_run': total_checks / len(executions) if executions else 0,
            'total_successful_checks': total_successful_checks,
            'total_failed_checks': total_failed_checks,
            'total_defects_simulated': total_defects,
            'average_duration_seconds': total_duration / len(executions) if executions else 0
        }


# For easy integration
job_logger = JobExecutionLogger()
