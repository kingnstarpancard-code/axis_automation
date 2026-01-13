"""
Defect Injector Module
Intentionally injects simulated failures for testing the alert engine
All defects are marked as "is_simulated: true"
"""

import random
import time
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class DefectInjector:
    """Injects random simulated defects for testing"""
    
    def __init__(self, enabled: bool = True, seed: int = None):
        """
        Initialize defect injector
        
        Args:
            enabled: Enable/disable defect injection
            seed: Random seed for reproducibility
        """
        self.enabled = enabled
        if seed:
            random.seed(seed)
        
        self.defect_config = {
            "TIMEOUT": {"percentage": 15, "priority": 75},
            "SLOW_RESPONSE": {"percentage": 20, "priority": 40},
            "DUPLICATE_ALERT": {"percentage": 10, "priority": 65},
            "FALSE_POSITIVE": {"percentage": 8, "priority": 30},
            "ALERT_STORM": {"percentage": 5, "priority": 85},
            "CONNECTION_ERROR": {"percentage": 12, "priority": 70}
        }
    
    def get_defect(self, check_id: int, activity_name: str, 
                   previous_status: str = "success") -> Optional[Dict]:
        """
        Determine if a defect should be injected for this check
        
        Args:
            check_id: Activity check ID
            activity_name: Name of activity being checked
            previous_status: Previous status ("success" or "failure")
        
        Returns:
            Dict with defect details if defect should be injected, None otherwise
        """
        
        if not self.enabled:
            return None
        
        rand = random.random() * 100
        cumulative = 0
        
        for defect_type, config in self.defect_config.items():
            cumulative += config["percentage"]
            
            if rand < cumulative:
                return self._create_defect(defect_type, check_id, activity_name, previous_status)
        
        return None
    
    def _create_defect(self, defect_type: str, check_id: int, 
                       activity_name: str, previous_status: str) -> Dict:
        """Create specific defect details"""
        
        if defect_type == "TIMEOUT":
            return {
                "type": "TIMEOUT",
                "message": "Connection timeout after 10s",
                "status_code": None,
                "response_time": None,
                "error": "requests.exceptions.ConnectTimeout",
                "is_simulated": True,
                "severity": 75
            }
        
        elif defect_type == "SLOW_RESPONSE":
            return {
                "type": "SLOW_RESPONSE",
                "message": "Response time exceeded threshold (>5s)",
                "status_code": 200,
                "response_time": random.uniform(5.5, 12.0),
                "error": None,
                "is_simulated": True,
                "severity": 40
            }
        
        elif defect_type == "CONNECTION_ERROR":
            return {
                "type": "CONNECTION_ERROR",
                "message": "Connection refused - server unreachable",
                "status_code": None,
                "response_time": None,
                "error": "requests.exceptions.ConnectionError",
                "is_simulated": True,
                "severity": 70
            }
        
        elif defect_type == "DUPLICATE_ALERT":
            return {
                "type": "DUPLICATE_ALERT",
                "message": f"Sending 3 duplicate alerts to test correlation",
                "duplicate_count": 3,
                "is_simulated": True,
                "severity": 65
            }
        
        elif defect_type == "FALSE_POSITIVE":
            # On maintenance window (Sunday 22:00-23:59)
            now = datetime.now()
            is_maintenance_window = now.weekday() == 6 and now.hour >= 22
            
            return {
                "type": "FALSE_POSITIVE",
                "message": "Expected failure during maintenance window",
                "actual_status_code": 200,
                "reported_status_code": 503,
                "is_maintenance_window": is_maintenance_window,
                "is_simulated": True,
                "severity": 30
            }
        
        elif defect_type == "ALERT_STORM":
            return {
                "type": "ALERT_STORM",
                "message": "Multiple alerts received in 5 minute window (50+)",
                "alert_count": random.randint(50, 100),
                "time_window_seconds": 300,
                "is_simulated": True,
                "severity": 85
            }
        
        return None
    
    def should_suppress_on_maintenance(self) -> bool:
        """Check if currently in maintenance window"""
        now = datetime.now()
        # Sunday 22:00-23:59
        return now.weekday() == 6 and now.hour >= 22
    
    def get_defect_stats(self) -> Dict:
        """Get statistics about defect distribution"""
        total_percentage = sum(config["percentage"] for config in self.defect_config.values())
        
        return {
            "enabled": self.enabled,
            "total_injection_percentage": min(total_percentage, 100),
            "defect_types": list(self.defect_config.keys()),
            "config": self.defect_config
        }


class DefectSimulator:
    """Simulate defects at the HTTP level"""
    
    @staticmethod
    def simulate_timeout() -> None:
        """Simulate network timeout"""
        time.sleep(random.uniform(10, 15))
        raise TimeoutError("Connection timeout after 10s")
    
    @staticmethod
    def simulate_slow_response(base_time: float = 0.5) -> float:
        """Add artificial delay to simulate slow response"""
        artificial_delay = random.uniform(5.5, 12.0)
        time.sleep(artificial_delay - base_time)
        return base_time + artificial_delay
    
    @staticmethod
    def simulate_connection_error() -> None:
        """Simulate connection refused"""
        raise ConnectionError("Connection refused - server unreachable")
    
    @staticmethod
    def get_mock_error_response(error_type: str) -> Dict:
        """Get mock error response for testing"""
        
        responses = {
            "503": {
                "status_code": 503,
                "reason": "Service Unavailable",
                "text": "Server is temporarily unavailable"
            },
            "504": {
                "status_code": 504,
                "reason": "Gateway Timeout",
                "text": "Server failed to respond in time"
            },
            "500": {
                "status_code": 500,
                "reason": "Internal Server Error",
                "text": "An unexpected error occurred"
            },
            "502": {
                "status_code": 502,
                "reason": "Bad Gateway",
                "text": "Invalid response from upstream server"
            }
        }
        
        return responses.get(error_type, responses["500"])


class DefectConfiguration:
    """Load and manage defect configuration"""
    
    @staticmethod
    def get_default_config() -> Dict:
        """Get default defect configuration"""
        return {
            "enabled": True,
            "defects": {
                "TIMEOUT": {
                    "percentage": 15,
                    "activity_ids": [1, 2, 3],  # Specific activities
                    "exclude_days": [],
                    "exclude_hours": []
                },
                "SLOW_RESPONSE": {
                    "percentage": 20,
                    "threshold_ms": 5000,
                    "activity_ids": [1, 2, 4, 5],
                    "exclude_days": [4, 5],  # Not on Fridays/Saturdays
                    "exclude_hours": []
                },
                "DUPLICATE_ALERT": {
                    "percentage": 10,
                    "count": 3,
                    "activity_ids": [3, 6],
                    "exclude_days": [],
                    "exclude_hours": []
                },
                "FALSE_POSITIVE": {
                    "percentage": 8,
                    "only_days": [6],  # Only on Sundays
                    "only_hours": [22, 23],  # 10 PM - midnight
                    "reason": "maintenance_window"
                },
                "ALERT_STORM": {
                    "percentage": 5,
                    "min_alerts": 50,
                    "max_alerts": 150,
                    "time_window": 300,
                    "activity_ids": [1, 2, 3, 4]
                },
                "CONNECTION_ERROR": {
                    "percentage": 12,
                    "activity_ids": [5, 6, 7],
                    "exclude_days": [],
                    "exclude_hours": []
                }
            },
            "scheduling": {
                "maintenance_window": {
                    "day": "Sunday",
                    "start_hour": 22,
                    "end_hour": 23,
                    "suppress_alerts": False
                }
            }
        }
    
    @staticmethod
    def load_from_file(filepath: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            import yaml
            with open(filepath, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            return DefectConfiguration.get_default_config()
